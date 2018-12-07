import os
import testutil
import responses

tests_dir = os.path.dirname(os.path.realpath(__file__))

ACCOUNTS_INSERT_BULK_CSV = os.path.join(tests_dir, "fixtures/accounts_insert_bulk.csv")
ACCOUNTS_INSERT_JOB = {"object": "Account", "operation": "insert", "lineEnding": "CRLF"}
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


@responses.activate
def test_get_job_info():
    testutil.add_response("login_response_200")
    testutil.add_response("api_version_response_200")
    testutil.add_response("jobs_create_200")
    testutil.add_response("jobs_get_job_info_200")

    client = testutil.get_client()
    job = ACCOUNTS_INSERT_JOB
    create_result = client.jobs.ingest.create(job_resource=job)
    job_id = create_result[0].get("id")
    get_result = client.jobs.ingest.get(job_id=job_id)

    assert get_result[0] == testutil.mock_responses.get("jobs_get_job_info_200").get("body")
    assert get_result[1].status == 200


@responses.activate
def test_get_all_jobs():
    testutil.add_response("login_response_200")
    testutil.add_response("api_version_response_200")
    testutil.add_response("jobs_create_200")
    testutil.add_response("jobs_get_all_200")

    client = testutil.get_client()
    job = ACCOUNTS_INSERT_JOB
    client.jobs.ingest.create(job_resource=job)
    get_result = client.jobs.ingest.get()

    assert get_result[0] == testutil.mock_responses.get("jobs_get_all_200").get("body")
    assert get_result[1].status == 200


@responses.activate
def test_get_successful_jobs():
    testutil.add_response("login_response_200")
    testutil.add_response("api_version_response_200")
    testutil.add_response("jobs_create_200")
    testutil.add_response("jobs_batches_201")
    testutil.add_response("jobs_update_close_200")
    testutil.add_response("jobs_get_successes_200")

    client = testutil.get_client()
    job = ACCOUNTS_INSERT_JOB
    create_result = client.jobs.ingest.create(job_resource=job)

    with open(ACCOUNTS_INSERT_BULK_CSV) as f:
        csv_file = f.read()
        job_id = create_result[0].get("id")
        client.jobs.ingest.batches(job_id=job_id, csv_file=csv_file)

    get_result = client.jobs.ingest.get(job_id=job_id, successes=True)

    assert get_result[0] == testutil.mock_responses.get("jobs_get_successes_200").get("body")
    assert get_result[1].status == 200


@responses.activate
def test_get_failed_jobs():
    testutil.add_response("login_response_200")
    testutil.add_response("api_version_response_200")
    testutil.add_response("jobs_create_200")
    testutil.add_response("jobs_batches_201")
    testutil.add_response("jobs_update_close_200")
    testutil.add_response("jobs_get_failures_200")

    client = testutil.get_client()
    job = ACCOUNTS_INSERT_JOB
    create_result = client.jobs.ingest.create(job_resource=job)

    with open(ACCOUNTS_INSERT_BULK_CSV) as f:
        csv_file = f.read()
        job_id = create_result[0].get("id")
        client.jobs.ingest.batches(job_id=job_id, csv_file=csv_file)

    get_result = client.jobs.ingest.get(job_id=job_id, failures=True)

    assert get_result[0] == testutil.mock_responses.get("jobs_get_failures_200").get("body")
    assert get_result[1].status == 200


@responses.activate
def test_get_unprocessed_jobs():
    testutil.add_response("login_response_200")
    testutil.add_response("api_version_response_200")
    testutil.add_response("jobs_create_200")
    testutil.add_response("jobs_batches_201")
    testutil.add_response("jobs_update_close_200")
    testutil.add_response("jobs_get_unprocessed_200")

    client = testutil.get_client()
    job = ACCOUNTS_INSERT_JOB
    create_result = client.jobs.ingest.create(job_resource=job)

    with open(ACCOUNTS_INSERT_BULK_CSV) as f:
        csv_file = f.read()
        job_id = create_result[0].get("id")
        client.jobs.ingest.batches(job_id=job_id, csv_file=csv_file)

    get_result = client.jobs.ingest.get(job_id=job_id, unprocessed=True)

    assert get_result[0] == testutil.mock_responses.get("jobs_get_unprocessed_200").get("body")
    assert get_result[1].status == 200


@responses.activate
def test_delete_job():
    testutil.add_response("login_response_200")
    testutil.add_response("api_version_response_200")
    testutil.add_response("jobs_create_200")
    testutil.add_response("jobs_delete_204")

    client = testutil.get_client()
    job = ACCOUNTS_INSERT_JOB
    create_result = client.jobs.ingest.create(job_resource=job)
    job_id = create_result[0].get("id")
    delete_result = client.jobs.ingest.delete(job_id=job_id)

    assert delete_result[0] == testutil.mock_responses.get("jobs_delete_204").get("body")
    assert delete_result[1].status == 204
