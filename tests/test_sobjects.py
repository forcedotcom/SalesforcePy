import testutil
import responses


@responses.activate
def test_insert():
    testutil.add_response("login_response_200")
    testutil.add_response("insert_response_201")
    testutil.add_response("api_version_response_200")

    client = testutil.get_client()
    create_result = client.sobjects(
        object_type="Account").insert({"Name": "sfdc_py"})
    assert create_result[0] == testutil.mock_responses["insert_response_201"]["body"]
    assert create_result[1].status == 201


@responses.activate
def test_insert_blob():
    testutil.add_response("login_response_200")
    testutil.add_response("insert_blob_response_201")
    testutil.add_response("api_version_response_200")

    client = testutil.get_client()
    # Create a file tuple ordered like so: ( filename, body, content_type )
    _file = ("sfdc_py.txt", "Hello world", "text/plain")

    insert_result = client.sobjects(object_type="Attachment", binary_field="Body").insert({  # Specify the binary field
        "Name": "sfdc_py",
        "ParentId": "0010Y0000056ljcQAA",
        "Description": "An excellent package"
    }, binary=_file)    # Pass your file through using the binary kwarg
    assert insert_result[0] == testutil.mock_responses["insert_blob_response_201"]["body"]
    assert insert_result[1].status == 201


@responses.activate
def test_insert_blob_negative():
    testutil.add_response("login_response_200")
    testutil.add_response("insert_blob_response_no_body")
    testutil.add_response("api_version_response_200")

    client = testutil.get_client()
    # Create a file tuple ordered like so: ( filename, body, content_type )
    _file = ("sfdc_py.txt", "Hello world", "text/plain")

    insert_result = client.sobjects(object_type="Attachment", binary_field="Body").insert({  # Specify the binary field
        "Name": "sfdc_py",
        "ParentId": "0010Y0000056ljcQAA",
        "Description": "An excellent package"
    }, binary=_file)    # Pass your file through using the binary kwarg
    assert insert_result[0] is None


@responses.activate
def test_insert_blob_missing_body():
    testutil.add_response("login_response_200")
    testutil.add_response("api_version_response_200")
    testutil.add_response("insert_blob_response_400")
    client = testutil.get_client()
    # Create a file tuple ordered like so: ( filename, body, content_type )
    _file = ("sfdc_py.txt", "Hello world", "text/plain")

    insert_result = client.sobjects(object_type="Attachment").insert({  # Missing binary field "Body"
        "Name": "sfdc_py",
        "ParentId": "0010Y0000056ljcQAA",
        "Description": "An excellent package"
    }, binary=_file)    # Pass your file through using the binary kwarg
    assert insert_result[0] == testutil.mock_responses["insert_blob_response_400"]["body"]
    assert insert_result[1].status == 400


@responses.activate
def test_insert_with_proxy():
    testutil.add_response("login_response_200")
    testutil.add_response("insert_response_201")
    testutil.add_response("api_version_response_200")

    client = testutil.get_client_with_proxy()
    create_result = client.sobjects(
        object_type="Account").insert({"Name": "sfdc_py"})
    assert create_result[0] == testutil.mock_responses["insert_response_201"]["body"]
    assert create_result[1].status == 201
    assert create_result[1].proxies.get("https") is testutil.proxies.get("https")


@responses.activate
def test_update():
    testutil.add_response("login_response_200")
    testutil.add_response("api_version_response_200")
    testutil.add_response("update_response_204")
    client = testutil.get_client()
    update_result = client.sobjects(
        id="0010Y0000055YG7QAM", object_type="Account").update({"Name": "sfdc_py 2"})
    assert update_result[0] == testutil.mock_responses["update_response_204"]["body"]
    assert update_result[1].status == 204


@responses.activate
def test_update_with_proxy():
    testutil.add_response("login_response_200")
    testutil.add_response("api_version_response_200")
    testutil.add_response("update_response_204")

    client = testutil.get_client_with_proxy()
    update_result = client.sobjects(
        id="0010Y0000055YG7QAM", object_type="Account").update({"Name": "sfdc_py 2"})
    assert update_result[0] == testutil.mock_responses["update_response_204"]["body"]
    assert update_result[1].status == 204
    assert update_result[1].proxies.get("https") is testutil.proxies.get("https")


@responses.activate
def test_delete():
    testutil.add_response("login_response_200")
    testutil.add_response("api_version_response_200")
    testutil.add_response("delete_response_204")
    client = testutil.get_client()
    delete_result = client.sobjects(
        id="0010Y0000055YG7QAM",
        object_type="Account").delete()
    assert delete_result[0] == testutil.mock_responses["delete_response_204"]["body"]
    assert delete_result[1].status == 204


@responses.activate
def test_delete_with_proxy():
    testutil.add_response("login_response_200")
    testutil.add_response("api_version_response_200")
    testutil.add_response("delete_response_204")

    client = testutil.get_client_with_proxy()
    delete_result = client.sobjects(
        id="0010Y0000055YG7QAM",
        object_type="Account").delete()
    assert delete_result[0] == testutil.mock_responses["delete_response_204"]["body"]
    assert delete_result[1].status == 204
    assert delete_result[1].proxies.get("https") is testutil.proxies.get("https")


@responses.activate
def test_query_sobj_row():
    testutil.add_response("login_response_200")
    testutil.add_response("api_version_response_200")
    testutil.add_response("query_sobj_row_response")
    client = testutil.get_client()
    query_result = client.sobjects(
        object_type="Account",
        id="0010Y0000056ljcQAA").query()
    assert query_result[0] == testutil.mock_responses["query_sobj_row_response"]["body"]
    assert query_result[1].status == 200


@responses.activate
def test_query_sobj_row_with_proxy():
    testutil.add_response("login_response_200")
    testutil.add_response("api_version_response_200")
    testutil.add_response("query_sobj_row_response")
    client = testutil.get_client_with_proxy()
    query_result = client.sobjects(
        object_type="Account",
        id="0010Y0000056ljcQAA").query()
    assert query_result[0] == testutil.mock_responses["query_sobj_row_response"]["body"]
    assert query_result[1].status == 200
    assert query_result[1].proxies.get("https") is testutil.proxies.get("https")


@responses.activate
def test_query_sobj_row_negative():
    testutil.add_response("login_response_200")
    testutil.add_response("api_version_response_200")
    testutil.add_response("query_sobj_row_response_no_body")
    client = testutil.get_client()
    query_result = client.sobjects(
        object_type="Account",
        id="0010Y0000056ljcQAA").query()
    assert query_result[0] is None


@responses.activate
def test_query_sobj_row_with_blob():
    testutil.add_response("login_response_200")
    testutil.add_response("api_version_response_200")
    testutil.add_response("query_attachments_before_blob_200")
    testutil.add_response("query_attachments_blob_200")
    client = testutil.get_client()
    query_result = client.sobjects(
        object_type="Attachment",
        id="00P0Y000000hUviUAE",
        binary_field="Body").query()
    blob_body = '"%s"' % (
        testutil.mock_responses["query_attachments_blob_200"]["body"])

    assert query_result[0] == testutil.mock_responses["query_attachments_before_blob_200"]["body"]
    assert query_result[1].status == 200
    assert query_result[2].status == 200
    assert query_result[2].response.content.decode("utf-8") == blob_body


@responses.activate
def test_query_sobj_row_with_blob_with_proxy():
    testutil.add_response("login_response_200")
    testutil.add_response("api_version_response_200")
    testutil.add_response("query_attachments_before_blob_200")
    testutil.add_response("query_attachments_blob_200")
    client = testutil.get_client_with_proxy()
    query_result = client.sobjects(
        object_type="Attachment",
        id="00P0Y000000hUviUAE",
        binary_field="Body").query()
    blob_body = '"%s"' % (
        testutil.mock_responses["query_attachments_blob_200"]["body"])

    assert query_result[0] == testutil.mock_responses["query_attachments_before_blob_200"]["body"]
    assert query_result[1].status == 200
    assert query_result[1].proxies.get("https") is testutil.proxies.get("https")
    assert query_result[2].status == 200
    assert query_result[2].proxies.get("https") is testutil.proxies.get("https")
    assert query_result[2].response.content.decode("utf-8") == blob_body


@responses.activate
def test_query_sobj_row_with_blob_negative():
    testutil.add_response("login_response_200")
    testutil.add_response("api_version_response_200")
    testutil.add_response("query_attachments_before_blob_200")
    testutil.add_response("query_attachments_blob_no_body")
    client = testutil.get_client()
    query_result = client.sobjects(
        object_type="Attachment",
        id="00P0Y000000hUviUAE",
        binary_field="Body").query()

    assert query_result[0] == testutil.mock_responses["query_attachments_before_blob_200"]["body"]
    assert query_result[1].status == 200
    assert query_result[2].status == 200
    assert query_result[2].response.content == b''


@responses.activate
def test_describe():
    testutil.add_response("login_response_200")
    testutil.add_response("api_version_response_200")
    testutil.add_response("describe_response_200")
    client = testutil.get_client()
    describe_result = client.sobjects(object_type="Idea").describe()
    assert describe_result[0] == testutil.mock_responses["describe_response_200"]["body"]
    assert describe_result[1].status == 200


@responses.activate
def test_describe_with_proxy():
    testutil.add_response("login_response_200")
    testutil.add_response("api_version_response_200")
    testutil.add_response("describe_response_200")
    client = testutil.get_client_with_proxy()
    describe_result = client.sobjects(object_type="Idea").describe()
    assert describe_result[0] == testutil.mock_responses["describe_response_200"]["body"]
    assert describe_result[1].status == 200
    assert describe_result[1].proxies.get("https") is testutil.proxies.get("https")


@responses.activate
def test_upsert_existing_record():
    testutil.add_response("login_response_200")
    testutil.add_response("api_version_response_200")
    testutil.add_response("upsert_existing_record_response_204")
    client = testutil.get_client()
    update_result = client.sobjects(
        id="999", object_type="Upsert_Object__c", external_id='External_Field__c').upsert({"Name": "Test Upsert Name"})
    assert update_result[0] == testutil.mock_responses["upsert_existing_record_response_204"]["body"]
    assert update_result[1].status == 204


@responses.activate
def test_upsert_existing_record_with_proxy():
    testutil.add_response("login_response_200")
    testutil.add_response("api_version_response_200")
    testutil.add_response("upsert_existing_record_response_204")
    client = testutil.get_client_with_proxy()
    update_result = client.sobjects(
        id="999", object_type="Upsert_Object__c", external_id='External_Field__c').upsert({"Name": "Test Upsert Name"})
    assert update_result[0] == testutil.mock_responses["upsert_existing_record_response_204"]["body"]
    assert update_result[1].status == 204
    assert update_result[1].proxies.get("https") is testutil.proxies.get("https")


@responses.activate
def test_upsert_non_existing_record():
    testutil.add_response("login_response_200")
    testutil.add_response("api_version_response_200")
    testutil.add_response("upsert_non_existing_record_response_201")
    client = testutil.get_client()
    update_result = client.sobjects(
        id="333", object_type="Upsert_Object__c", external_id='External_Field__c').upsert({"Name": "Test Upsert Name"})
    assert update_result[0] == testutil.mock_responses["upsert_non_existing_record_response_201"]["body"]
    assert update_result[1].status == 201


@responses.activate
def test_upsert_non_existing_record_with_proxy():
    testutil.add_response("login_response_200")
    testutil.add_response("api_version_response_200")
    testutil.add_response("upsert_non_existing_record_response_201")
    client = testutil.get_client_with_proxy()
    update_result = client.sobjects(
        id="333", object_type="Upsert_Object__c", external_id='External_Field__c').upsert({"Name": "Test Upsert Name"})
    assert update_result[0] == testutil.mock_responses["upsert_non_existing_record_response_201"]["body"]
    assert update_result[1].status == 201
    assert update_result[1].proxies.get("https") is testutil.proxies.get("https")


@responses.activate
def test_describe_global():
    testutil.add_response("login_response_200")
    testutil.add_response("api_version_response_200")
    testutil.add_response("describe_global_response_200")
    client = testutil.get_client()
    describe_result = client.sobjects().describe_global()
    assert describe_result[0] == testutil.mock_responses["describe_global_response_200"]["body"]
    assert describe_result[1].status == 200
