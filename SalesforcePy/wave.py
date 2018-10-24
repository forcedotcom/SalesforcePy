"""
.. module:: wave
   :synopsis: Module dedicated to Wave requests.

.. moduleauthor:: Aaron Caffrey <acaffrey@salesforce.com>
.. versionadded:: 1.0.0

"""

from __future__ import absolute_import
from . import commons


WAVE_DATASET_SERVICE = '/services/data/v%s/wave/datasets/%s'
WAVE_QUERY_SERVICE = '/services/data/v%s/wave/query'


class Wave(commons.ApiNamespace):
    """ The Wave namespace class from which all API calls to a Salesforce organisation are made.
        .. versionadded:: 1.0.0
    """
    @commons.kwarg_adder
    def dataset(self, api_name, **kwargs):
        """ Performs a dataset request.

          :param: api_name: API name of data set (eg. "opportunities")
          :type: api_name: string
          :param: **kwargs: kwargs
          :type: **kwargs: dict
          :return: Dataset response
          :rtype: (dict, wave.WaveDataSet)
        """
        client = self.client
        wds = WaveDataSet(client.session_id, client.instance_url, api_name, **kwargs)
        res = wds.request()

        return res, wds

    @commons.kwarg_adder
    def query(self, q, **kwargs):
        """ Performs a query request.

          :param: q: Query dict
          :type: q: dict
          :param: **kwargs: kwargs
          :type: **kwargs: dict
          :return: Query response
          :rtype: (dict, wave.WaveQuery)
        """
        client = self.client
        wq = WaveQuery(client.session_id, client.instance_url, q, **kwargs)
        res = wq.request()

        return res, wq


class WaveDataSet(commons.BaseRequest):
    """ Performs a request to `'/services/data/<api_version>/wave/datasets/<api_name>'`
        .. versionadded:: 1.0.0
    """

    def __init__(self, session_id, instance_url, api_name, **kwargs):
        """ Constructor. Calls `super`, then encodes the `service` including the `query_string` provided

          :param: session_id: Session ID used to make request
          :type: session_id: string
          :param: instance_url: Instance URL used to make the request (eg. `'eu11.salesforce.com'`)
          :type: instance_url: string
          :param: api_name: API name of data set requested.
          :type: api_name: string
          :param: **kwargs: kwargs
          :type: **kwargs: dict
        """
        super(WaveDataSet, self).__init__(session_id, instance_url, **kwargs)
        self.service = WAVE_DATASET_SERVICE % (self.api_version, api_name)


class WaveQuery(commons.BaseRequest):
    """ Performs a request to `'/services/data/<api_version>/wave/query'`
        .. versionadded:: 1.0.0
    """
    def __init__(self, session_id, instance_url, query, **kwargs):
        """ Constructor. Calls `super`, prepares the request body with the `query` provided.

          :param: session_id: Session ID used to make request
          :type: session_id: string
          :param: instance_url: Instance URL used to make the request (eg. `'eu11.salesforce.com'`)
          :type: instance_url: string
          :param: query: Query dict.
          :type: query: string
          :param: **kwargs: kwargs
          :type: **kwargs: dict
        """
        super(WaveQuery, self).__init__(session_id, instance_url, **kwargs)
        self.http_method = 'POST'
        self.request_body = query
        self.service = WAVE_QUERY_SERVICE % self.api_version
