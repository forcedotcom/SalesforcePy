import testutil
import responses


@responses.activate
def test_exec_anon():
    testutil.add_response("login_response_200")
    testutil.add_response("exec_anon_response_200")
    testutil.add_response("api_version_response_200")
    client = testutil.get_client()
    ea_result = client.execute_anonymous("system.debug('Hello world.');")
    assert ea_result[0] == testutil.mock_responses["exec_anon_response_200"]["body"]
    assert ea_result[1].status == 200


@responses.activate
def test_exec_anon_with_proxy():
    testutil.add_response("login_response_200")
    testutil.add_response("exec_anon_response_200")
    testutil.add_response("api_version_response_200")
    client = testutil.get_client_with_proxy()
    ea_result = client.execute_anonymous("system.debug('Hello world.');")
    assert ea_result[0] == testutil.mock_responses["exec_anon_response_200"]["body"]
    assert ea_result[1].status == 200
    assert ea_result[1].proxies.get("https") is testutil.proxies.get("https")


@responses.activate
def test_exec_anon_negative():
    testutil.add_response("login_response_200")
    testutil.add_response("exec_anon_response_no_body")
    testutil.add_response("api_version_response_200")
    client = testutil.get_client()
    ea_result = client.execute_anonymous("system.debug('Hello world.');")
    assert ea_result[0] is None
