""" 
    ..module:: einstein.llm.prompt
    :synopsis: The Connect API Einstein LLM Prompt implementation

.. moduleauthor:: Aaron Caffrey <acaffrey@salesforce.com>
"""
from __future__ import absolute_import

from .. import commons

GENERATIONS_SERVICE = "/services/data/v%s/einstein/llm/prompt/generations"


class Generations(commons.BaseRequest):
    """ Performs a POST request to /services/data/vX.XX/einstein/llm/prompt/generations

        .. versionadded:: 2.1.0
    """
    def __init__(self, session_id, instance_url, api_version, request_body, **kwargs):
        """ Constructor. Calls `super`, enocdes the `service`, and assigns the `request_body`

          :param: session_id: Session ID used to make request
          :type: session_id: string
          :param: instance_url: Instance URL used to make the request (eg. `'eu11.salesforce.com'`)
          :type: instance_url: string
          :param: api_version: API version
          :type: api_version: string
          :param: request_body: Request body
          :type: request_body: dict
          :param: **kwargs: kwargs
          :type: **kwargs: dict
        """
        super(Generations, self).__init__(session_id, instance_url, **kwargs)

        self.http_method = 'POST'
        self.service = GENERATIONS_SERVICE % api_version
        self.request_body = request_body


class Prompt(commons.ApiNamespace):
    def __init__(self, client):
        super(Prompt, self).__init__(client)

    @commons.kwarg_adder
    def generations(self, request_body, **kwargs):
        client = self.client
        api_version = self.client_kwargs.get('version')

        generated = Generations(
            client.session_id, client.instance_url, api_version, request_body, **kwargs)

        response = generated.request()

        return response, generated
