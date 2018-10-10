import testutil
import responses


@responses.activate
def test_search():
    testutil.add_response("login_response_200")
    testutil.add_response("search_response_200")
    testutil.add_response("api_version_response_200")
    client = testutil.get_client()
    search_result = client.search(
        "FIND {sfdc_py} RETURNING Account(Id, Name) LIMIT 5")
    assert search_result[0] == testutil.mock_responses["search_response_200"]["body"]
    assert search_result[1].status == 200


@responses.activate
def test_search_with_proxy():
    testutil.add_response("login_response_200")
    testutil.add_response("search_response_200")
    testutil.add_response("api_version_response_200")
    client = testutil.get_client_with_proxy()
    search_result = client.search(
        "FIND {sfdc_py} RETURNING Account(Id, Name) LIMIT 5")
    assert search_result[0] == testutil.mock_responses["search_response_200"]["body"]
    assert search_result[1].status == 200
    assert search_result[1].proxies.get("https") is testutil.proxies.get("https")
