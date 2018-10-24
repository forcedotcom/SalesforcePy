import testutil
import responses


@responses.activate
def test_logout():
    testutil.add_response("login_response_200")
    testutil.add_response("logout_response_200")
    testutil.add_response("api_version_response_200")
    client = testutil.get_client()
    logout = client.logout()
    assert logout[0] is None
    assert logout[1].status == 200


@responses.activate
def test_logout_ise():
    testutil.add_response("login_response_200")
    testutil.add_response("logout_response_500")
    testutil.add_response("api_version_response_200")
    client = testutil.get_client()
    logout = client.logout()
    assert logout[0] is None
    assert logout[1].status == 500


@responses.activate
def test_logout_with_proxy():
    testutil.add_response("login_response_200")
    testutil.add_response("logout_response_200")
    testutil.add_response("api_version_response_200")
    client = testutil.get_client_with_proxy()
    logout = client.logout()
    assert logout[0] is None
    assert logout[1].status == 200
    assert logout[1].proxies.get("https") is testutil.proxies.get("https")
