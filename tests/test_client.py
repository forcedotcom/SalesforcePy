import pytest
import responses

import SalesforcePy as sfdc
import testutil


@responses.activate
def test_context_manager():

    testutil.add_response("login_response_200")
    testutil.add_response("query_response_200")
    testutil.add_response("logout_response_200")

    client_args = {
        "username": testutil.username,
        "password": testutil.password,
        "client_id": testutil.client_id,
        "client_secret": testutil.client_secret,
        "version": "37.0"}

    with sfdc.client(**client_args) as client:
        client.query("SELECT Id, Name FROM Account LIMIT 10")

    """
        The above should have made 3 calls: login, query, logout
    """
    assert len(responses.calls) == 3


@responses.activate
def test_context_manager_negative():

    testutil.add_response("login_response_200")
    testutil.add_response("query_response_200")

    client_args = {
        "username": testutil.username,
        "password": testutil.password,
        "client_id": testutil.client_id,
        "client_secret": testutil.client_secret,
        "version": "37.0"}

    def logout():
        raise Exception("Monkey patchin'...")

    with sfdc.client(**client_args) as client:
        client.query("SELECT Id, Name FROM Account LIMIT 10")
        client.logout = logout

    """
        The above should have made 2 calls: login, query
    """
    assert len(responses.calls) == 2


@responses.activate
def test_timeout_kwarg():
    """
    Test that the timeout kwarg is used in the request
    """

    testutil.add_response("login_response_200")
    testutil.add_response("query_response_200")
    testutil.add_response("logout_response_200")

    client_args = {
        "username": testutil.username,
        "password": testutil.password,
        "client_id": testutil.client_id,
        "client_secret": testutil.client_secret,
        "version": "37.0",
        "timeout": "10"}

    with sfdc.client(**client_args) as client:
        qr = client.query("SELECT Id, Name FROM Account LIMIT 10")
        assert qr[1].timeout == 10.0, 'Timeout value in request is different to client kwarg value'


@responses.activate
def test_function_kwarg_overrides_client_kwarg():
    """
    Test that kwargs value defined at the function level are used in favour of the client kwargs if
    the latter are defined
    """
    testutil.add_response("login_response_200")
    testutil.add_response("query_response_200")
    testutil.add_response("logout_response_200")
    client_timeout = 15
    function_timeout = 30

    client_args = {
        "username": testutil.username,
        "password": testutil.password,
        "client_id": testutil.client_id,
        "client_secret": testutil.client_secret,
        "version": "37.0",
        "timeout": client_timeout
    }

    function_kwargs = {
        "timeout": function_timeout
    }

    with sfdc.client(**client_args) as client:
        # kwarg defined at function level
        qr = client.query("SELECT Id, Name FROM Account LIMIT 10", **function_kwargs)
        assert qr[1].timeout == float(function_timeout), 'Timeout value in function was not used'
        # kwarg defined at client level
        qr = client.query("SELECT Id, Name FROM Account LIMIT 10")
        assert qr[1].timeout == float(client_timeout), 'Timeout value in client was not used'


@responses.activate
def test_client_proxy_in_sobjects():
    """
    Test that the client level args are still maintained at the sobject level, specifically test for proxies
    """
    proxy = {"https": "someproxy.net:8080"}
    testutil.add_response("login_response_200")
    testutil.add_response("insert_response_201")
    testutil.add_response("logout_response_200")
    client_args = {
        "username": testutil.username,
        "password": testutil.password,
        "client_id": testutil.client_id,
        "client_secret": testutil.client_secret,
        "version": "37.0",
        "proxies": proxy
    }
    with sfdc.client(**client_args) as client:
        create_result = client.sobjects(
            object_type="Account").insert({"Name": "sfdc_py"})
        assert create_result[1].proxies['https'] is 'someproxy.net:8080'
        assert create_result[0] == testutil.mock_responses["insert_response_201"]["body"]


@responses.activate
def test_client_kwargs__in_sobjects_at_function_level():
    """
    Test that the keywords level args are still maintained at the sobject level
    """
    proxy = {"https": "someproxy.net:8080"}
    testutil.add_response("login_response_200")
    testutil.add_response("update_response_204_v42")
    testutil.add_response("logout_response_200")
    client_args = {
        "username": testutil.username,
        "password": testutil.password,
        "client_id": testutil.client_id,
        "client_secret": testutil.client_secret,
        "version": "37.0",
        "proxies": proxy
    }
    fn_level_kwarg = {'version': '42.0'}
    with sfdc.client(**client_args) as client:
        update_result = client.sobjects(
            id="0010Y0000055YG7QAM", object_type="Account").update({"Name": "sfdc_py 2"}, **fn_level_kwarg)
        assert update_result[0] == testutil.mock_responses["update_response_204_v42"]["body"]
        assert update_result[1].status == 204
        assert update_result[1].proxies['https'] is 'someproxy.net:8080'
