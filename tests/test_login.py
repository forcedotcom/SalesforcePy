import SalesforcePy as sfdc
import testutil
import responses
import logging
import pytest


@responses.activate
def test_login_via_client():
    testutil.add_response("login_response_200")
    testutil.add_response("api_version_response_200")
    client = sfdc.client(
        username=testutil.username,
        password=testutil.password,
        client_id=testutil.client_id,
        client_secret=testutil.client_secret
    )
    client.debug()
    login = client.login()
    assert login[0] == testutil.mock_responses["login_response_200"]["body"]
    assert login[1].status == 200
    assert login[1].get_session_id() == testutil.mock_responses["login_response_200"]["body"]["access_token"]


@responses.activate
def test_login_via_client_with_proxies():
    testutil.add_response("login_response_200")
    testutil.add_response("api_version_response_200")
    client = sfdc.client(
        username=testutil.username,
        password=testutil.password,
        client_id=testutil.client_id,
        client_secret=testutil.client_secret,
        proxies={"http": "localhost:8888/example/"}
    )
    client.debug(level=logging.INFO)
    login = client.login()
    assert login[0] == testutil.mock_responses["login_response_200"]["body"]
    assert login[1].status == 200
    assert login[1].get_session_id() == testutil.mock_responses["login_response_200"]["body"]["access_token"]


@responses.activate
def test_login_negative():
    testutil.add_response("login_response_401")
    testutil.add_response("api_version_response_200")
    client = sfdc.client(
        username=testutil.username,
        password=testutil.password,
        client_id=testutil.client_id,
        client_secret=testutil.client_secret
    )
    _, lr = client.login()
    assert lr.exceptions[0].args[0] == "OAuth call failed. Received 401 status code"
    assert lr.exceptions[0].oauth_response[0].get("message") == "Session expired or invalid"
    assert lr.exceptions[0].oauth_response[0].get("errorCode") == "INVALID_SESSION_ID"


@responses.activate
def test_login_url_kwarg():
    testutil.add_response("sandbox_login_response_200")
    testutil.add_response("api_version_response_200")
    client = sfdc.client(
        username=testutil.username,
        password=testutil.password,
        client_id=testutil.client_id,
        client_secret=testutil.client_secret,
        login_url='test.salesforce.com'
    )
    client.debug()
    login = client.login()
    assert login[0] == testutil.mock_responses["sandbox_login_response_200"]["body"]
    assert login[1].status == 200
    assert login[1].get_session_id() == testutil.mock_responses["sandbox_login_response_200"]["body"]["access_token"]
