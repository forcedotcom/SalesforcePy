import testutil
import responses


@responses.activate
def test_query():
    testutil.add_response("login_response_200")
    testutil.add_response("query_response_200")
    testutil.add_response("api_version_response_200")
    client = testutil.get_client()
    query_result = client.query("SELECT Id, Name FROM Account LIMIT 10")
    assert query_result[0] == testutil.mock_responses["query_response_200"]["body"]
    assert query_result[1].status == 200


@responses.activate
def test_query_with_proxy():
    testutil.add_response("login_response_200")
    testutil.add_response("query_response_200")
    testutil.add_response("api_version_response_200")
    client = testutil.get_client_with_proxy()
    query_result = client.query("SELECT Id, Name FROM Account LIMIT 10")
    assert query_result[0] == testutil.mock_responses["query_response_200"]["body"]
    assert query_result[1].status == 200
    assert query_result[1].proxies.get("https") is testutil.proxies.get("https")
