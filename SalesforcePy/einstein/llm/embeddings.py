""" 
    ..module:: einstein.llm.embeddings
    :synopsis: The Connect API Einstein LLM Embeddings implementation

.. moduleauthor:: Aaron Caffrey <acaffrey@salesforce.com>
"""
from __future__ import absolute_import

from .. import commons

EMBEDDINGS_SERVICE = "/services/data/v%s/einstein/llm/embeddings"


class Embeddings(commons.BaseRequest):
    """ Performs a POST request to /services/data/vX.XX/einstein/llm/embeddings

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
        super(Embeddings, self).__init__(session_id, instance_url, **kwargs)

        self.http_method = 'POST'
        self.service = EMBEDDINGS_SERVICE % api_version
        self.request_body = request_body
