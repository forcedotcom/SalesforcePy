"""
.. module:: jobs
   :synopsis: A Salesforce Bulk API 2.0 jobs implementation.

.. moduleauthor:: Aaron Caffrey <acaffrey@salesforce.com>

"""
from __future__ import absolute_import
from . import commons
import logging
import requests

BATCHES_URI = '/services/data/v%s/jobs/ingest/%s/batches'
CREATE_URI = '/services/data/v%s/jobs/ingest'


class Batches(commons.BaseRequest):
    """ Performs a POST request to `'/services/data/vX.XX/jobs/ingest/<job_id>/batches'`
        .. versionadded:: 1.1.0
    """
    def __init__(self, session_id, instance_url, api_version, job_id, csv_file, **kwargs):
        super(Batches, self).__init__(session_id, instance_url, **kwargs)

        self.csv_file = csv_file
        self.http_method = 'PUT'
        self.service = BATCHES_URI % (api_version, job_id)

    def request(self):
        (headers, logger, request, response, service) = self.get_request_vars()
        csv_file = self.csv_file

        logging.getLogger('sfdc_py').info('%s %s' % (self.http_method, service))
        headers.set('Content-Type', 'text/csv')

        # TODO: Compose and make request with file stream...


class CreateJob(commons.BaseRequest):
    """ Performs a POST request to `'/services/data/vX.XX/jobs/ingest'`
        .. versionadded:: 1.1.0
    """
    def __init__(self, session_id, instance_url, api_version, request_body, **kwargs):
        """ Constructor. Calls `super`, then encodes the `service` including the `query_string` provided

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
        super(CreateJob, self).__init__(session_id, instance_url, **kwargs)

        self.http_method = 'POST'
        self.request_body = request_body
        self.service = CREATE_URI % api_version

    def request(self):
        """ Return created job response from Salesforce.

          :return: A dict containing created job info
          :rtype: dict
        """
        (headers, logger, request, response, service) = self.get_request_vars()

        logging.getLogger('sfdc_py').info('%s %s' % (self.http_method, service))

        request = requests.post(
            service,
            headers=headers,
            json=self.request_body,
            proxies=self.proxies)
        self.status = request.status_code

        try:
            response = request.json()
        except Exception as e:
            logger.error('%s %s %s' % (self.http_method, service, self.status))
            logger.error(e.args[0])
            return
        finally:
            return response


class Ingest(commons.ApiNamespace):
    def batches(self, job_id, csv_file, **kwargs):
        client = self.client
        api_version = self.client_kwargs.get('version')
        batches = Batches(client.session_id, client.instance_url, api_version, job_id, csv_file, **kwargs)
        response = batches.request()

        return response, batches

    def create(self, job_resource):
        client = self.client
        api_version = self.client_kwargs.get('version')
        create_job = CreateJob(client.session_id, client.instance_url, api_version, job_resource)
        response = create_job.request()

        return response, create_job

    def get(self):
        pass

    def delete(self):
        pass

    def update(self):
        pass


class Jobs(commons.ApiNamespace):
    def __init__(self, client):
        super(Jobs, self).__init__(client)

        self.ingest = Ingest(client)
