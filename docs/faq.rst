FAQs
====

How do I inspect my organisation schema? 
----------------------------------------

1. Log in to `Workbench <https://workbench.developerforce.com/login.php>`_.
2. Go to **Info > Standard and Custom Objects**.
3. In the Object dropdown, choose the object you wish to inspect (eg. Case) then click Select.
4. Expand Fields. You should find what you're looking for here.

How do I test a query?
----------------------

1. Log in to `Workbench <https://workbench.developerforce.com/login.php>`_.
2. Go to :guilabel:`Queries > SOQL Query`.
3. Enter your query or optionally use the form to help you build the query, then click :guilabel:`Query`.

Is it possible to debug requests being made by SalesforcePy?
------------------------------------------------------------

Yes. Here's an example of how to do it, and what to expect.

.. code-block:: python

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

Can I specify a proxy to talk to Salesforce Org in the code?
------------------------------------------------------------

Yes. Here's an example of how to do it.

.. code-block:: python

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
        proxies={"https": "localhost:8888/example/"}
	  # `proxies` kwarg takes a dict as required by the `requests` module.
    )
