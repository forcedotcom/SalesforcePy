import SalesforcePy as sfdc
import testutil
import responses


@responses.activate
def test_create_job():
    testutil.add_response("login_response_200")
    testutil.add_response("api_version_response_200")
    testutil.add_response("jobs_create_200")

    client = testutil.get_client()
    job = {'object': 'Account', 'operation': 'insert'}
    create_result = client.jobs.ingest.create(job_resource=job)
    assert create_result[0] == testutil.mock_responses["jobs_create_200"]["body"]
    assert create_result[1].status == 200
