import SalesforcePy as sfdc
import testutil
import responses
import logging
import os
import pytest

tests_dir = os.path.dirname(os.path.realpath(__file__))


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
def test_login_via_device_flow():
    testutil.add_response("device_code_authorization_response_200")
    testutil.add_response("poll_device_code_authentication_response_200")
    testutil.add_response("api_version_response_200")

    request_count = 0

    def on_authorize(res, authz):
        nonlocal request_count
        assert res == testutil.mock_responses["device_code_authorization_response_200"]["body"]
        assert authz.status == 200

        request_count += 1

    def on_authenticate(res, authn):
        nonlocal request_count
        assert res == testutil.mock_responses["poll_device_code_authentication_response_200"]["body"]
        assert authn.status == 200

        request_count += 1

    client = sfdc.client(None, None, client_id=testutil.client_id)
    
    with client.login_via_device_flow(on_authorize=on_authorize, on_authenticate=on_authenticate) as c:
        assert c.session_id == "00DD00000008Uw2!ARkAQGppKf6n.VwG.EnFSvi731qWh.7vKfaJjL7h49yutIC84gAsxMrqcE81GjpTjQbDLkytl2ZwosNbIJwUS0X8ahiILj3e"
        assert request_count == 2


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


@responses.activate
def test_login_via_soap():
    login_method = "POST"
    login_url = "https://login.salesforce.com/services/Soap/c/37.0/"
    login_status = 200
    login_content_type = "text/xml; charset=utf-8"

    with open (os.path.join(tests_dir, "fixtures/soap_login_response_200.xml"), "r") as f:
        login_body = f.read()

    responses.add(login_method, login_url, body=login_body, status=login_status, content_type=login_content_type)
    testutil.add_response("api_version_response_200")

    client = sfdc.client(
        username=testutil.username,
        password=testutil.password,
        org_id=testutil.org_id
    )
    login = client.login_via_soap()

    assert '{http://schemas.xmlsoap.org/soap/envelope/}Body' in login[0]
    assert login[1].status == 200
    assert login[1].exceptions == []
    assert login[1].session_id == client.session_id
    assert client.instance_url == 'eu11.salesforce.com'


@responses.activate
def test_login_via_soap_negative():
    login_method = "POST"
    login_url = "https://login.salesforce.com/services/Soap/c/37.0/"
    login_status = 500
    login_content_type = "text/xml; charset=utf-8"

    with open (os.path.join(tests_dir, "fixtures/soap_login_response_500.xml"), "r") as f:
        login_body = f.read()

    responses.add(login_method, login_url, body=login_body, status=login_status, content_type=login_content_type)
    
    client = sfdc.client(
        username=testutil.username,
        password=testutil.password,
        org_id=testutil.org_id
    )
    login = client.login_via_soap()

    assert '{http://schemas.xmlsoap.org/soap/envelope/}Body' in login[0]
    assert login[1].status == 500
    assert len(login[1].exceptions) == 1
    