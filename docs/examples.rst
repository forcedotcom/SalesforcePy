Usage Examples
==============

Query
-----

Once the login call has been performed successfully, 
the client maintains the session, allowing you to make API calls. 
Here's how you can perform a query.

.. code-block:: python

    query_results = client.query('SELECT Id, Name FROM Account LIMIT 1')

In the example above ``query_results[0]`` is a dict with the response. For more information, See
`Execute a SOQL Query <https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/dome_query.htm>`_.

Query More
----------

While the client ``query()`` method helps with making requests for a 
small amount of data, it is not useful if the total size of records exceeds the standard batch size (2000).

In such scenarios, ``query_more()`` comes handy. 
As the example shows, you simply provide the query string in the same way you did previously 
with ``query()``:

.. code-block:: python

    query_results = client.query_more('SELECT Id, Name FROM Account')

In this example, ``query_results[0]`` is a list of dicts, each of which is a single query result (batch). 
The behaviour of ``query_more()`` is to consume ``nextRecordsUrl`` of each query result recursively 
until it runs out. For more information, see Retrieving the Remaining SOQL Query Results in
`Execute a SOQL Query <https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/dome_query.htm>`_.

Insert sObjects
---------------

Use the ``sobjects`` class from the client to perform DML statements and file i/o with 
Salesforce objects. Here's an example to demonstrate such insert operation.

.. code-block:: python

    create_result = client.sobjects(object_type='Account').insert({"Name" : "SalesforcePy"})

In this example, ``create_result[0]`` is a dict with the response. For more information, see 
`Create a Record <https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/dome_sobject_create.htm>`_.

Update sObjects
---------------

Update works similarly to insert, with the main difference being that ``id`` is
a required ``kwarg`` in sobjects so it is clear which record is to be updated.

.. code-block:: python

    update_result = client.sobjects(id='0010Y0000055YG7QAM',object_type='Account').update({"Name" : "SalesforcePy 2"})

In the example above ``update_result[0]`` will be None. 
This is because the HTTP method used under the hood is ``PATCH``, 
for which the expected success code is ``204``. 
The success code can be found in ``update_result[1].status``. 
For more information, see 
`Update a Record <https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/dome_update_fields.htm>`_.

Delete sObjects
---------------

.. code-block:: python

    delete_result = client.sobjects(id='0010Y0000055YG7QAM',object_type='Account').delete()

In the example above ``delete_result[0]`` will be None. 
This is because the HTTP method used under the hood is ``DELETE``, 
for which the expected success code is ``204``. 
The success code can be found in ``delete_result[1].status``. For more information, see
`Delete a Record <https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/dome_delete_record.htm>`_.

Query SObject Row
-----------------

If you know the ID of a record, you can easily retrieve the entire row using this method. 
This may be preferable to ``query()`` if you wish to get all fields 
without specifying them.

.. code-block:: python

    query_result = client.sobjects( object_type="Account", id="0010Y0000056ljcQAA" ).query()

Describe SObject
----------------

The describe method retrieves the individual metadata at all levels for the specified SObject.

.. code-block:: python

    describe_result = client.sobjects(object_type='Account').describe()

In the example above ``describe_result[0]`` will be a dict with the response. For more information, see
`sObject Describe <https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/resources_sobject_describe.htm. The If-Modified-Since header cannot be used with this method>`_.

Describe Global
---------------

The describe global method lists the available objects and their metadata for the organization’s data. 
In addition, it provides the organization encoding, as well as the maximum batch size permitted in queries.

.. code-block:: python

    describe_global_result = client.sobjects().describe_global()

In the example above ``describe_global_result[0]`` will be a dict with the response. For more information, see
`Describe Global <https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/resources_describeGlobal.htm>`_.
The ``If-Modified-Since`` header cannot be used with this method.

Insert File
-----------

There are some special objects in Salesforce such as ``Attachment``, ``Document``, and ``ContentVersion`` which 
allow storage of files as blobs. The following is an example of how to insert a file.

.. code-block:: python

    # Create a file tuple ordered like so: ( filename, body, content_type )
    file = ( "SalesforcePy.txt", "Hello world", "text/plain" )

    insert_result = client.sobjects(object_type = "Attachment", binary_field="Body").insert({
            "Name":"SalesforcePy",
            "ParentId":"0010Y0000056ljcQAA",
            "Description":"An excellent package"
        }, binary=file )    # Pass your file through using the binary kwarg
    
Search
------

SOSL search statements can be made as follows:

.. code-block:: python

    search_result = client.search('FIND {SalesforcePy} RETURNING Account(Id, Name) LIMIT 5')

Execute Anonymous
-----------------

Anonymous Apex can be executed in a Salesforce organisation like so:

.. code-block:: python

    ea_result = client.execute_anonymous('system.debug(\'Hello world.\');')
    Approval Process
    Approvals can be retrieved, submitted and approved/rejected

    ap_result = client.approvals(requestBody)

See documentation for sample request body.

Chatter
-------

Create a feed item (chatter post). It returns a ``201`` status code for a successful request. 
See the `Chatter REST API Developer Guide <https://developer.salesforce.com/docs/atlas.en-us.chatterapi.meta/chatterapi/intro_what_is_chatter_connect.htm>`_ for information on the expected body to create feed items.

.. code-block:: python

    # create chatter post
    client.chatter.feed_item(body)

    # create a comment on a chatter post
    client.chatter.feed_comment('feed-elementid', body)

Wave
----

Retrieve a data set
^^^^^^^^^^^^^^^^^^^

Retrieve a wave data set using the ``datataset()`` function.

.. code-block:: python

    client.wave.dataset("opportunities")

Perform a query
^^^^^^^^^^^^^^^

Perform a SOQL query using the wave ``query()`` function.

.. code-block:: python

    query = {
        "query": """q = load \"0Fb0N000000XuvBSAS/0Fc0N000001M5BMSA0\";\nq = filter q by 'Account.Industry' in
    [\"Apparel\", \"Banking\", \"Biotechnology\"];\nq = group q by 'Account.Industry';\nq = foreach q generate
    'Account.Industry' as 'Account.Industry', count() as 'count';\nq = order q by 'Account.Industry' asc;\nq = limit q
    2000;"""
    }

    client.wave.query(query)

Bulk API 2.0
------------

As a general rule, supported Bulk API 2.0 calls can be made from ``client.jobs.ingest``. 
The samples here cover specific calls.

Create a Job
^^^^^^^^^^^^

In this example, we create a job to insert accounts.

.. code-block:: python

    job_resource = {"object": "Account", "operation": "insert", "lineEnding": "CRLF"}
    client.jobs.ingest.create(job_resource=job_resource)

For more information on the response for this request, see 
`Create a Job <https://developer.salesforce.com/docs/atlas.en-us.api_bulk_v2.meta/api_bulk_v2/create_job.htm>`_.

Upload Job Data
^^^^^^^^^^^^^^^

In this example, we create a job, then upload a csv file using the job ID.

.. code-block:: python

    job_resource = {"object": "Account", "operation": "insert", "lineEnding": "CRLF"}
    create_result = client.jobs.ingest.create(job_resource=job_resource)

    with open("/path/to/accounts.csv") as f:
        csv_file = f.read()
        job_id = create_result[0].get("id")
        batches_result = client.jobs.ingest.batches(job_id=job_id, csv_file=csv_file)

For more information on the response for this request, see 
`Upload Job Data <https://developer.salesforce.com/docs/atlas.en-us.api_bulk_v2.meta/api_bulk_v2/upload_job_data.htm>`_.

Update a job state
^^^^^^^^^^^^^^^^^^

In this example, we create a job, upload a csv file using its job ID, then update it with a state of ``UploadComplete``.

.. code-block:: python

    job_resource = {"object": "Account", "operation": "insert", "lineEnding": "CRLF"}
    create_result = client.jobs.ingest.create(job_resource=job_resource)
    job_id = create_result[0].get("Id")

    with open("/path/to/accounts.csv") as f:
        csv_file = f.read()
        batches_result = client.jobs.ingest.batches(job_id=job_id, csv_file=csv_file)

    client.jobs.ingest.update(job_id=job_id, state="UploadComplete")

For more information on the response for this request, see 
`Close or Abort a Job
<https://developer.salesforce.com/docs/atlas.en-us.api_bulk_v2.meta/api_bulk_v2/close_job.htm>`_.

Delete a job
^^^^^^^^^^^^

In this example, we delete a job based on its ID. 
Assumed in this example that this value is stored in ``job_id``.

.. code-block:: python

    delete_result = client.jobs.ingest.delete(job_id=job_id)

For more information on the response for this request, see 
`Delete a Job
<https://developer.salesforce.com/docs/atlas.en-us.api_bulk_v2.meta/api_bulk_v2/delete_job.htm>`_.

Get all jobs
^^^^^^^^^^^^

In this example, we get a list of all jobs.

.. code-block:: python

    get_result = client.jobs.ingest.get()

For more information on the response for this request, see 
`Get All Jobs <https://developer.salesforce.com/docs/atlas.en-us.api_bulk_v2.meta/api_bulk_v2/get_all_jobs.htm>`_.

Get Job Info
^^^^^^^^^^^^

In this example, we get information for a specific job based on its ID. 
Assumed in this example that this value is stored in ``job_id``.

.. code-block:: python

    get_result = client.jobs.ingest.get(job_id=job_id)

For more information on the response for this request, see 
`Get Job Info <https://developer.salesforce.com/docs/atlas.en-us.api_bulk_v2.meta/api_bulk_v2/get_job_info.htm>`_.

Get Job Successes
^^^^^^^^^^^^^^^^^

In this example, we get a successes CSV for a given job based on its ID. 
Assumed in this example that this value is stored in ``job_id``.

.. code-block:: python

    get_result = client.jobs.ingest.get(job_id=job_id, successes=True)

For more information on the response for this request, see 
`Get Job Successful Record Results <https://developer.salesforce.com/docs/atlas.en-us.api_bulk_v2.meta/api_bulk_v2/get_job_successful_results.htm>`_.

Get Job Failures
^^^^^^^^^^^^^^^^

In this example, we get a failures CSV for a given job based on its ID. 
Assumed in this example that this value is stored in ``job_id``.

.. code-block:: python

    get_result = client.jobs.ingest.get(job_id=job_id, failures=True)

For more information on the response for this request, see 
`Get Job Failed Record Results <https://developer.salesforce.com/docs/atlas.en-us.api_bulk_v2.meta/api_bulk_v2/get_job_failed_results.htm>`_.

Get Job Unprocessed Rows
^^^^^^^^^^^^^^^^^^^^^^^^

In this example, we get an unprocessed rows CSV for a given job based on its ID. 
Assumed in this example that this value is stored in ``job_id``.

.. code-block:: python

    get_result = client.jobs.ingest.get(job_id=job_id, unprocessed=True)

For more information on the response for this request, see 
`Get Job Unprocessed Record Results <https://developer.salesforce.com/docs/atlas.en-us.api_bulk_v2.meta/api_bulk_v2/get_job_unprocessed_results.htm>`_.

Logout
------

Expires the session by revoking the access token.
It returns a ``200`` status code for a successful token revocation.

.. code-block:: python

    client.logout()
