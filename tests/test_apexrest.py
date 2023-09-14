import testutil
import responses

@responses.activate
def test_apexrest_get_request():
	testutil.add_response("login_response_200")
	testutil.add_response("apexrest_get_response_200")
	testutil.add_response("api_version_response_200")

	client = testutil.get_client()
	apexrest_result = client.apexrest(
		action='foo',
		http_method='GET',
		request_params={"foo": 0}
	)

	assert apexrest_result[0] == testutil.mock_responses["apexrest_get_response_200"]["body"]
	assert apexrest_result[1].status is 200



@responses.activate
def test_apexrest_post_request():
	testutil.add_response("login_response_200")
	testutil.add_response("apexrest_post_response_200")
	testutil.add_response("api_version_response_200")


	client = testutil.get_client()
	apexrest_result = client.apexrest(
		action='foo',
		http_method='POST',
		request_body={'foo': 0}
	)

	assert apexrest_result[0] == testutil.mock_responses["apexrest_post_response_200"]["body"]
	assert apexrest_result[1].status is 200

@responses.activate
def test_apexrest_patch_request():
    testutil.add_response("login_response_200")
    testutil.add_response("apexrest_patch_response_200")
    testutil.add_response("api_version_response_200")

    client = testutil.get_client()
    apexrest_result = client.apexrest(
        action='foo',
        http_method='PATCH',
        request_params={'foo': 0}
    )

    assert apexrest_result[0] == testutil.mock_responses["apexrest_patch_response_200"]["body"]
    assert apexrest_result[1].status == 200


@responses.activate
def test_apexrest_put_request():
    testutil.add_response("login_response_200")
    testutil.add_response("apexrest_put_response_200")
    testutil.add_response("api_version_response_200")

    client = testutil.get_client()
    apexrest_result = client.apexrest(
        action='foo',
        http_method='PUT',
        request_params={'foo': 0}
    )

    assert apexrest_result[0] == testutil.mock_responses["apexrest_put_response_200"]["body"]
    assert apexrest_result[1].status == 200
