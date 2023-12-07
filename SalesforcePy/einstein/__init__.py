""" 
    ..module:: einstein
    :synopsis: The Connect API Einstein namespace.

.. moduleauthor:: Aaron Caffrey <acaffrey@salesforce.com>
"""
from __future__ import absolute_import

from .. import commons
from . import llm


class Einstein(commons.ApiNamespace):
    def __init__(self, client):
        super(Einstein, self).__init__(client)

        self.llm = llm.LLM(client)