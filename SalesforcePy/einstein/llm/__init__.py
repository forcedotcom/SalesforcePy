""" 
    ..module:: einstein
    :synopsis: The Connect API Einstein LLM namespace.

.. moduleauthor:: Aaron Caffrey <acaffrey@salesforce.com>
"""
from __future__ import absolute_import

from .. import commons
from . import embeddings
from . import prompt

class LLM(commons.ApiNamespace):
    def __init__(self, client):
        super(LLM, self).__init__(client)
        self.prompt = prompt.Prompt(client)

    @commons.kwarg_adder
    def embeddings(self, request_body, **kwargs):
        client = self.client
        api_version = self.client_kwargs.get('version')

        embedding_vector = embeddings.Embeddings(
            client.session_id, client.instance_url, api_version, request_body, **kwargs)

        response = embedding_vector.request()

        return response, embedding_vector
