import SalesforcePy as sfdc
import os
import testutil
import responses

tests_dir = os.path.dirname(os.path.realpath(__file__))

ACCOUNTS_INSERT_BULK_CSV = os.path.join(tests_dir, "fixtures/accounts_insert_bulk.csv")

@responses.activate
def test_create_job():
    testutil.add_response("login_response_200")
    testutil.add_response("api_version_response_200")
    testutil.add_response("jobs_create_200")

    client = testutil.get_client()
    job = {"object": "Account", "operation": "insert"}
    create_result = client.jobs.ingest.create(job_resource=job)

    assert create_result[0] == testutil.mock_responses["jobs_create_200"]["body"]
    assert create_result[1].status == 200


@responses.activate
def test_batches():
    testutil.add_response("login_response_200")
    testutil.add_response("api_version_response_200")
    testutil.add_response("jobs_create_200")
    # TODO: Set up responder for batches

    client = testutil.get_client()
    job = {"object": "Account", "operation": "insert"}
    create_result = client.jobs.ingest.create(job_resource=job)

    with open(ACCOUNTS_INSERT_BULK_CSV) as f:
        csv_file = f.read()
        job_id = create_result.get('Id')
        # TODO: Uncomment the following once we have a responder for batches
        # batches_result = client.jobs.ingest.batches(job_id=job_id, csv_file=csv_file)
