import SalesforcePy as sfdc
import os
import testutil
import responses

tests_dir = os.path.dirname(os.path.realpath(__file__))

ACCOUNTS_INSERT_BULK_CSV = os.path.join(tests_dir, "fixtures/accounts_insert_bulk.csv")
ACCOUNTS_INSERT_JOB = {"object": "Account", "operation": "insert"}
UPLOAD_COMPLETED = "UploadComplete"


@responses.activate
def test_create_job():
    testutil.add_response("login_response_200")
    testutil.add_response("api_version_response_200")
    testutil.add_response("jobs_create_200")

    client = testutil.get_client()
    job = ACCOUNTS_INSERT_JOB
    create_result = client.jobs.ingest.create(job_resource=job)

    assert create_result[0] == testutil.mock_responses.get("jobs_create_200").get("body")
    assert create_result[1].status == 200


@responses.activate
def test_batches():
    testutil.add_response("login_response_200")
    testutil.add_response("api_version_response_200")
    testutil.add_response("jobs_create_200")
    testutil.add_response("jobs_batches_201")

    client = testutil.get_client()
    job = ACCOUNTS_INSERT_JOB
    create_result = client.jobs.ingest.create(job_resource=job)

    with open(ACCOUNTS_INSERT_BULK_CSV) as f:
        csv_file = f.read()
        job_id = create_result[0].get("id")
        batches_result = client.jobs.ingest.batches(job_id=job_id, csv_file=csv_file)

        assert batches_result[0] == testutil.mock_responses.get("jobs_batches_201").get("body")
        assert batches_result[1].status == 201


@responses.activate
def test_update_close_job():
    testutil.add_response("login_response_200")
    testutil.add_response("api_version_response_200")
    testutil.add_response("jobs_create_200")
    testutil.add_response("jobs_update_close_200")

    client = testutil.get_client()
    job = ACCOUNTS_INSERT_JOB
    create_result = client.jobs.ingest.create(job_resource=job)
    job_id = create_result[0].get("id")
    update_result = client.jobs.ingest.update(job_id=job_id, state=UPLOAD_COMPLETED)

    assert update_result[0] == testutil.mock_responses.get("jobs_update_close_200").get("body")
    assert update_result[1].status == 200
