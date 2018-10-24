import testutil
import responses
import SalesforcePy.sfdc as sfdc


@responses.activate
def test_undefined_api_version():
    testutil.add_response("login_response_200")
    testutil.add_response("api_version_response_200")
    client = sfdc.client(
        username=testutil.username,
        password=testutil.password,
        client_id=testutil.client_id,
        client_secret=testutil.client_secret
    )
    login_obj = client.login()
    # uses the most recent version based on the mock response

    assert login_obj[1].api_version == "37.0"


@responses.activate
def test_undefined_api_version_with_proxy():
    testutil.add_response("login_response_200")
    testutil.add_response("api_version_response_200")
    client = sfdc.client(
        username=testutil.username,
        password=testutil.password,
        client_id=testutil.client_id,
        client_secret=testutil.client_secret,
        proxies=testutil.proxies
    )
    login_obj = client.login()
    # uses the most recent version based on the mock response

    assert login_obj[1].api_version == "37.0"
    assert login_obj[1].proxies.get("https") is testutil.proxies.get("https")


@responses.activate
def test_defined_api_version():
    testutil.add_response("login_response_200")
    client = sfdc.client(
        username=testutil.username,
        password=testutil.password,
        client_id=testutil.client_id,
        client_secret=testutil.client_secret,
        version=testutil.version
    )
    login_obj = client.login()
    assert login_obj[1].api_version == "39.0"  # as specified in testutil


@responses.activate
def test_api_at_function_level():
    testutil.add_response("login_response_200")
    testutil.add_response("query_response_200_version_40",)
    client = sfdc.client(
        username=testutil.username,
        password=testutil.password,
        client_id=testutil.client_id,
        client_secret=testutil.client_secret,
        version='39.0'
    )
    login_obj = client.login()
    assert login_obj[1].api_version == "39.0"  # as specified in testutil

    func_level_options = {'version': '40.0'}
    query_result = client.query("SELECT Id, Name FROM Account LIMIT 10", **func_level_options)
    assert query_result[1].api_version == '40.0'
    assert '/v40.0/' in query_result[1].request_url


@responses.activate
def test_non_200_api_version():
    testutil.add_response("login_response_200")
    testutil.add_response("api_version_response_500")

    client = sfdc.client(
        username=testutil.username,
        password=testutil.password,
        client_id=testutil.client_id,
        client_secret=testutil.client_secret
    )
    login_obj = client.login()
    assert login_obj[1].api_version == "37.0"  # as specified in config.__default_api_version__
