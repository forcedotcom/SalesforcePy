# SalesforcePy

[![Build Status](https://travis-ci.com/caffalaughrey/SalesforcePy.svg?token=VEFNGJhbySaAEtyHVj3L&branch=master)](https://travis-ci.com/caffalaughrey/SalesforcePy)
[![Coverage Status](https://coveralls.io/repos/github/caffalaughrey/SalesforcePy/badge.svg?branch=master)](https://coveralls.io/github/caffalaughrey/SalesforcePy?branch=master)

An absurdly simple package for making Salesforce Rest API calls.

by Aaron Caffrey, Colin Cheevers, Jose Garcia, Tania Prince

Salesforce.com

## Table of Contents
- [Introduction](#introduction)
- [Contributors](#contributors)
- [Requirements](#requirements)
- [Install](#install)
- [Create a client and log in](#create-a-client-and-log-in)
- [Query](#query)
- [Query More](#query-more)
- [Insert SObject](#insert-sobjects)
- [Update SObject](#update-sobjects)
- [Delete SObject](#delete-sobjects)
- [Query SObject Row](#query-sobject-row)
- [Describe SObject](#describe-sobject)
- [Describe Global](#describe-global)
- [Insert File](#insert-file)
- [Search](#search)
- [Execute Anonymous](#execute-anonymous)
- [Approval Process](#approval-process)
- [Chatter](#chatter)
- [Wave](#wave)
- [Logout](#logout)
- [Contributing](#contributing)
- [FAQ](#faq)

## Introduction
The reason this package exists is to produce:

1. A Salesforce client that is reusable, minimalistic, and pythonic
2. Interfaces that are closely knit to the Salesforce Rest API service specification
3. Gradual support for the Salesforce API extended family (ie. Chatter, Analytics, Wave, Tooling, Bulk, Metadata, etc.)

## Contributors
Thanks goes to the people who have contributed code to this module, see the
[GitHub Contributors page][].

[GitHub Contributors page]: https://github.com/forcedotcom/SalesforcePy/graphs/contributors

## Requirements
   * Python 2 or 3

## Install
### From git
```bash
pip install git+ssh://git@github.com/forcedotcom/SalesforcePy.git
```

### From local source
1. Download and extract, or clone this repo
2. `cd` into the `/SalesforcePy` directory
3. Run the following:
```bash
pip install .
```

## Create a client and log in
Getting started is a three-step process:

1.  Import `SalesforcePy`
2.  Create a client
3.  Perform a login request

```python
import SalesforcePy as sfdc

# Create an instance of a Salesforce client, replacing the credentials below with valid ones.
client = sfdc.client(
    username="jsoap@universalcontainers.com",
    password="p@ssword1",
    client_id="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    client_secret="123456789123456789",
    login_url="test.salesforce.com",
    version = "38.0", #optional parameter, defaults to the latest version for your instance
    timeout = "30", # optional, defines a connect/read timeout value, if not specified requests can hang for minutes or more.

)

# Log in
login_results = client.login()
```

In the example above, `login_results[0]` will be a dict with the response from the Salesforce OAuth resource.  The only supported flow at present is username-password.  For more on the response, see: https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/intro_understanding_username_password_oauth_flow.htm.

You can also use the context manager which handles `login()` and `logout()` automatically.

```python
client_args = {'username' :'jsoap@universalcontainers.com',
    'password' :'p@ssword1',
    'client_id': 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
    'client_secret' : '123456789123456789'
    }

with sfdc.client(**client_args) as client:

    search_result = client.search('FIND {"test"} RETURNING Case(Id)')

```

## Query
Once the login call has been performed successfully, the client will maintain the session leaving you free to make API calls.  This example demonstrates how to perform a query.
```python
query_results = client.query('SELECT Id, Name FROM Account LIMIT 1')
```

In the example above `query_results[0]` will be a dict with the response as documented here: https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/dome_query.htm.

## Query More
While the client [`query()`](#query) method can be useful for making requests when you're expecting a small amount of data, a single query result *won't* give you all records if the total size of records exceeds the standard batch size (2000).

In such scenarios, you may wish to use `query_more()`.  As the example shows, you simply provide the query string in the same way you did previously with `query()`:
```python
query_results = client.query_more('SELECT Id, Name FROM Account')
```

In the example above `query_results[0]` will be a list of dicts, each of which is a query result (batch).  The behaviour of `query_more` is to consume `"nextRecordsUrl"` of each query result recursively until it runs out.  For more on this topic, check out https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/dome_query.htm under the heading **"Retrieving the Remaining SOQL Query Results"**.

## Insert SObjects
From the client, the `sobjects` class can be used to perform DML statements and file i/o with Salesforce objects.  This example shows how to insert.
```python
create_result = client.sobjects(object_type='Account').insert({"Name" : "SalesforcePy"})
```

In the example above `create_result[0]` will be a dict with the response as documented here: https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/dome_sobject_create.htm.

## Update SObjects
Update works similarly to insert, with the main difference being that `id` is a required kwarg in `sobjects` so it is clear which record is to be updated.
```python
update_result = client.sobjects(id='0010Y0000055YG7QAM',object_type='Account').update({"Name" : "SalesforcePy 2"})
```

In the example above `update_result[0]` will be `None`.  This is because the HTTP method used under the hood is `PATCH`, for which the expected success code is `204`.  The success code can be found in `update_result[1].status`.  For more, read: https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/dome_update_fields.htm.

## Delete SObjects
```python
delete_result = client.sobjects(id='0010Y0000055YG7QAM',object_type='Account').delete()
```

In the example above `delete_result[0]` will be `None`.  This is because the HTTP method used under the hood is `DELETE`, for which the expected success code is `204`.  The success code can be found in `delete_result[1].status`.  For more, read: https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/dome_delete_record.htm.

## Query SObject Row
If you know the ID of a record, you can easily retrieve the entire row using this method.  This may be preferable to the `query` call documented further up if you wish to get all fields without specifying them.
```python
query_result = client.sobjects( object_type="Account", id="0010Y0000056ljcQAA" ).query()
```

## Describe SObject
The describe method retrieves the individual metadata at all levels for the specified SObject
```python
describe_result = client.sobjects(object_type='Account').describe()
```

In the example above `describe_result[0]` will be a dict with the response as documented here: https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/resources_sobject_describe.htm. The If-Modified-Since header cannot be used with this method.

## Describe Global
The describe global method lists the available objects and their metadata for the organization’s data. In addition, it provides the organization encoding, as well as the maximum batch size permitted in queries.
```
describe_global_result = client.sobjects().describe_global()
```

In the example above `describe_global_result[0]` will be a dict with the response as documented here: https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/resources_describeGlobal.htm. The If-Modified-Since header cannot be used with this method.

## Insert File
There are some special objects in Salesforce such as `Attachment`, `Document`, and `ContentVersion` which allow storage of files as blobs.  The following is an example of how to insert a file.
```python
# Create a file tuple ordered like so: ( filename, body, content_type )
file = ( "SalesforcePy.txt", "Hello world", "text/plain" )

insert_result = client.sobjects(object_type = "Attachment", binary_field="Body").insert({
        "Name":"SalesforcePy",
        "ParentId":"0010Y0000056ljcQAA",
        "Description":"An excellent package"
    }, binary=file )    # Pass your file through using the binary kwarg
```

## Search
SOSL search statements can be made like so:
```python
search_result = client.search('FIND {SalesforcePy} RETURNING Account(Id, Name) LIMIT 5')
```

## Execute Anonymous
Anonymous Apex can be executed in a Salesforce organisation like so:
```python
ea_result = client.execute_anonymous('system.debug(\'Hello world.\');')
```

## Approval Process
Approvals can be retrieved, submitted and approved/rejected
```python
ap_result = client.approvals(requestBody)
```
See documentation for sample request body

## Chatter
Create a feed item (chatter post). It returns a 201 status code for a successful request. See Chatter REST api
 documentation for information on the expected body to create feed items.

```python
# create chatter post
client.chatter.feed_item(body)

# create a comment on a chatter post
client.chatter.feed_comment('feed-elementid', body)
```

## Wave
### Retrieve a data set
Retrieve a wave data set using the `datataset()` function.

```python
client.wave.dataset("opportunities")
```

### Perform a query
Perform a SAQL query using the wave `query()` function.

```python
query = {
    "query": """q = load \"0Fb0N000000XuvBSAS/0Fc0N000001M5BMSA0\";\nq = filter q by 'Account.Industry' in
[\"Apparel\", \"Banking\", \"Biotechnology\"];\nq = group q by 'Account.Industry';\nq = foreach q generate
'Account.Industry' as 'Account.Industry', count() as 'count';\nq = order q by 'Account.Industry' asc;\nq = limit q
2000;"""
}

client.wave.query(query)
```

## Logout
Expires the session by revoking the access token. It returns a 200 status code for a successful token revocation.
```python
client.logout()
```

## Contributing
### What's the git workflow?
   1. Fork this repo
   2. `git clone -b <yourbranch> <yourfork>`
   3. From within the project root directory run `pip install .`
   4. Develop
   5. Cover your code in `/tests`
   6. Create a pull request to the `forcedotcom:developer` branch

### How to format code
We recommend following the Style Guide for Python the best you can: https://www.python.org/dev/peps/pep-0008/.

`autopep8` is a great tool for automatic formatting, we encourage its use: https://pypi.python.org/pypi/autopep8.

## FAQ
### I need to inspect my organisation schema.  What's an easy way to do this?
1. Log in to Workbench: https://workbench.developerforce.com/login.php
2. Go to Info > Standard and Custom Objects
3. In the Object dropdown, choose the object you wish to inspect (eg. Case) then click Select
4. Expand Fields.  You should find what you're looking for here.

### I need to test a query.  What's an easy way to do this?
1. Log in to Workbench: https://workbench.developerforce.com/login.php
2. Go to Queries > SOQL Query
3. Enter your query or optionally use the form to help you build the query, then click Query

### Is it possible to debug requests being made by `SalesforcePy`?
Yes.  Here's an example of how to do it, and what to expect.

```python
import logging
import SalesforcePy as sfdc

username = "jsoap@universalcontainers.com"
password = "p@ssword1"
client_id = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
client_secret = "123456789123456789"

client = sfdc.client(
    username=username,
    password=password,
    client_id=client_id,
    client_secret=client_secret
)
client.debug(level=logging.INFO)    # Tell the client to debug at an info level
client.login()  # Outputs "POST https://login.salesforce.com/services/oauth2/token" to logs
```

### I need a proxy to talk to Salesforce orgs.  Can I specify this in the code?
Yes.  Here's an example of how to do it.

```python
import SalesforcePy as sfdc

username = "jsoap@universalcontainers.com"
password = "p@ssword1"
client_id = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
client_secret = "123456789123456789"

client = sfdc.client(
    username=username,
    password=password,
    client_id=client_id,
    client_secret=client_secret,
    proxies={"https": "localhost:8888/example/"}    # `proxies` kwarg takes a dict as required by the `requests` module.
)
```

## Advanced Usage
### Using keyword arguments
Some of the parameters that are optionally defined at the client level can be defined at the function level
as well. Function level arguments supersede the client arguments.

For example, you may want to define an overall timeout value of `"30"` for all requests but specify a higher
value for query calls.
```python
client = sfdc.client(
    username=username,
    password=password,
    client_id=client_id,
    client_secret=client_secret,
    timeout="30"
)
query_kwarg= {"timeout" : "60"}
client.query("Select Id FROM Account",**query_kwarg)
```

The following parameters support function level overriding:
- `proxies`
- `timeout`
- `version`
