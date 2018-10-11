import testutil
import responses


@responses.activate
def test_query_approvals():
    testutil.add_response("login_response_200")
    testutil.add_response("api_version_response_200")
    testutil.add_response("approvals_response_200")
    client = testutil.get_client()
    ar = client.approvals()
    sfdc_response = ar[0]
    assert ar[1].status == 200
    assert ar[1].http_method is "GET"
    assert "approvals" in sfdc_response


@responses.activate
def test_query_approvals_with_proxy():
    testutil.add_response("login_response_200")
    testutil.add_response("api_version_response_200")
    testutil.add_response("approvals_response_200")
    client = testutil.get_client_with_proxy()
    ar = client.approvals()
    sfdc_response = ar[0]
    assert ar[1].status == 200
    assert ar[1].http_method is "GET"
    assert ar[1].proxies.get("https") is testutil.proxies.get("https")
    assert "approvals" in sfdc_response


@responses.activate
def test_approval_request():
    testutil.add_response("login_response_200")
    testutil.add_response("api_version_response_200")
    testutil.add_response("approval_request_response_200")
    client = testutil.get_client()
    body = {
        "requests": [{
            "actionType": "Submit",
            "contextId": "00161000011ueBV",
            "nextApproverIds": ["00561000000j3h2"],
            "comments": "this is a test",
            "contextActorId": "005610000027SlY",
            "processDefinitionNameOrId": "test_account",
            "skipEntryCriteria": "true"}]
    }
    ar = client.approvals(body)
    req_response = ar[0]
    request_status = req_response[0].get("instanceStatus", None)

    assert ar[1].status == 200
    assert ar[1].http_method is "POST"
    assert request_status == "Pending"


@responses.activate
def test_approval_request_with_proxy():
    testutil.add_response("login_response_200")
    testutil.add_response("api_version_response_200")
    testutil.add_response("approval_request_response_200")
    client = testutil.get_client_with_proxy()
    body = {
        "requests": [{
            "actionType": "Submit",
            "contextId": "00161000011ueBV",
            "nextApproverIds": ["00561000000j3h2"],
            "comments": "this is a test",
            "contextActorId": "005610000027SlY",
            "processDefinitionNameOrId": "test_account",
            "skipEntryCriteria": "true"}]
    }
    ar = client.approvals(body)
    req_response = ar[0]
    request_status = req_response[0].get("instanceStatus", None)

    assert ar[1].status == 200
    assert ar[1].http_method is "POST"
    assert ar[1].proxies.get("https") is testutil.proxies.get("https")
    assert request_status == "Pending"
