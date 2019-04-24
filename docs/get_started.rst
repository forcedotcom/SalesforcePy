Get Started with SalesforcePy
=============================

Install
-------

From Git
^^^^^^^^

Install directly from Git using PyPi.

::

    pip install git+ssh://git@github.com/forcedotcom/SalesforcePy.git

From Local Source
^^^^^^^^^^^^^^^^^
1. Download and extract, or clone this repo.
2. cd into the ``/SalesforcePy`` directory.
3. Run ``pip install .``.

Create a Client and Log In
--------------------------

Getting started with SalesforcePy is a three-step process:

1. Import SalesforcePy
2. Create a client
3. Perform a login request

.. code-block:: python

    #Import SalesforcePy
    import SalesforcePy as sfdc

    # Create an instance of a Salesforce client. Replace the credentials here with valid ones.
    client = sfdc.client(
        username="jsoap@universalcontainers.com",
        password="p@ssword1",
        client_id="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        client_secret="123456789123456789",
        login_url="test.salesforce.com",
        version = "38.0", # optional, defaults to the latest version for your instance.
        timeout = "30", # optional, defines a connect/read timeout value, if not specified requests can hang for minutes or more.
    )

    # Log in
    login_results = client.login()

In this example, ``login_results[0]`` is a dict with the response from the Salesforce OAuth resource. 
The only supported flow at present is username-password. For more information about the response, 
see `Understanding the Username-Password OAuth Authentication Flow <https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/intro_understanding_username_password_oauth_flow.htm>`_.

You can also use the context manager which handles ``login()`` and ``logout()`` automatically.

.. code-block:: python

    client_args = {'username' :'jsoap@universalcontainers.com',
        'password' :'p@ssword1',
        'client_id': 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
        'client_secret' : '123456789123456789'
        }
    with sfdc.client(**client_args) as client:
    search_result = client.search('FIND {"test"} RETURNING Case(Id)')
