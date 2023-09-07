import responses

import SalesforcePy as sfdc
import testutil


@responses.activate
def test_query_more_singlebatch():
    testutil.add_response("login_response_200")
    testutil.add_response("query_response_200")
    testutil.add_response("api_version_response_200")
    client = testutil.get_client()
    query_result = client.query_more("SELECT Id, Name FROM Account LIMIT 10")
    assert query_result[0][0] == testutil.mock_responses["query_response_200"]["body"]
    assert query_result[0][0].get("done")


@responses.activate
def test_query_more_singlebatch_kwargs():
    testutil.add_response("login_response_200")
    testutil.add_response("query_response_200_version_40")
    client = sfdc.client(
        username=testutil.username,
        password=testutil.password,
        client_id=testutil.client_id,
        client_secret=testutil.client_secret,
        login_url=testutil.login_url,
        version="40.0",
    )
    client.login()
    query_result = client.query_more("SELECT Id, Name FROM Account LIMIT 10")
    assert query_result[0][0] == testutil.mock_responses["query_response_200_version_40"]["body"]
    assert query_result[0][0].get("done")


@responses.activate
def test_query_more_multibatch():
    testutil.add_response("login_response_200")
    testutil.add_response("query_more_multibatch_0_200")
    testutil.add_response("query_more_multibatch_1_200")
    testutil.add_response("query_more_multibatch_2_200")
    testutil.add_response("api_version_response_200")
    client = testutil.get_client()
    query_result = client.query_more("SELECT Id FROM Lead")
    assert query_result[0][0] == testutil.mock_responses["query_more_multibatch_0_200"]["body"]
    assert query_result[0][1] == testutil.mock_responses["query_more_multibatch_1_200"]["body"]
    assert query_result[0][2] == testutil.mock_responses["query_more_multibatch_2_200"]["body"]


@responses.activate
def test_query_more_multibatch_negative():
    testutil.add_response("login_response_200")
    testutil.add_response("query_more_multibatch_0_200")
    testutil.add_response("query_more_multibatch_1_no_body")
    testutil.add_response("api_version_response_200")
    client = testutil.get_client()
    query_result = client.query_more("SELECT Id FROM Lead")
    assert query_result[0] is None
