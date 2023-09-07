import testutil
import responses

query = {
    "query": """q = load \"0Fb0N000000XuvBSAS/0Fc0N000001M5BMSA0\";\nq = filter q by 'Account.Industry' in
[\"Apparel\", \"Banking\", \"Biotechnology\"];\nq = group q by 'Account.Industry';\nq = foreach q generate
'Account.Industry' as 'Account.Industry', count() as 'count';\nq = order q by 'Account.Industry' asc;\nq = limit q
2000;"""
}


@responses.activate
def test_wave_query():
    testutil.add_response("login_response_200")
    testutil.add_response("wave_query_response_200")
    testutil.add_response("api_version_response_200")

    client = testutil.get_client()
    wave_result = client.wave.query(query)

    assert wave_result[0] == testutil.mock_responses["wave_query_response_200"]["body"]
    assert wave_result[1].status is 200


@responses.activate
def test_wave_query_with_proxy():
    testutil.add_response("login_response_200")
    testutil.add_response("wave_query_response_200")
    testutil.add_response("api_version_response_200")

    client = testutil.get_client_with_proxy()
    wave_result = client.wave.query(query)

    assert wave_result[0] == testutil.mock_responses["wave_query_response_200"]["body"]
    assert wave_result[1].status is 200
    assert wave_result[1].proxies.get("https") is testutil.proxies.get("https")


@responses.activate
def test_wave_query_no_response_body():
    testutil.add_response("login_response_200")
    testutil.add_response("api_version_response_200")
    testutil.add_response("wave_query_no_body")

    client = testutil.get_client()
    wave_result = client.wave.query(None)

    assert wave_result[0] is None
    assert wave_result[1].status == 500
    # assert wave_result[1].exceptions[0].args[0] == 'Request body is null' # TODO: Dig into this exception and see what makes sense to assert


@responses.activate
def test_wave_dataset():
    testutil.add_response("login_response_200")
    testutil.add_response("wave_dataset_response_200")
    testutil.add_response("api_version_response_200")

    client = testutil.get_client()
    wave_result = client.wave.dataset("opportunities")

    assert wave_result[0] == testutil.mock_responses["wave_dataset_response_200"]["body"]
    assert wave_result[1].status is 200
