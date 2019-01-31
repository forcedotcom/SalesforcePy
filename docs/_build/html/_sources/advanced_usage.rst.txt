Advanced Usage
==============

Using Keyword Arguments
-----------------------

Some of the parameters that are optionally defined at the client level can be defined at the function level as well. 
Function level arguments supersede the client arguments.

For example, you may want to define an overall timeout value of ``30`` for all requests but specify a higher value for query calls.

.. code-block:: python

    client = sfdc.client(
        username=username,
        password=password,
        client_id=client_id,
        client_secret=client_secret,
        timeout="30"
    )
    query_kwarg= {"timeout" : "60"}
    client.query("Select Id FROM Account",**query_kwarg)

The following parameters support function level overriding:

- ``proxies``
- ``timeout``
- ``version``
