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
UPDATE_URI = '/services/data/v%s/jobs/ingest/%s'


class Batches(commons.BaseRequest):
    """ Performs a PUT request to `'/services/data/vX.XX/jobs/ingest/<job_id>/batches'`
        .. versionadded:: 1.1.0
    """
    def __init__(self, session_id, instance_url, api_version, job_id, csv_file, **kwargs):
        super(Batches, self).__init__(session_id, instance_url, **kwargs)

        self.request_body = csv_file
        self.http_method = 'PUT'
        self.service = BATCHES_URI % (api_version, job_id)
        self.headers = {
            'Content-Type': 'text/csv',
            'Authorization': 'OAuth %s' % self.session_id}


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


class Ingest(commons.ApiNamespace):
    def batches(self, job_id, csv_file, **kwargs):
        client = self.client
        api_version = self.client_kwargs.get('version')
        batches = Batches(client.session_id, client.instance_url, api_version, job_id, csv_file, **kwargs)
        response = batches.request()

        return response, batches

    def create(self, job_resource, **kwargs):
        client = self.client
        api_version = self.client_kwargs.get('version')
        create_job = CreateJob(client.session_id, client.instance_url, api_version, job_resource, **kwargs)
        response = create_job.request()

        return response, create_job

    def get(self):
        pass

    def delete(self):
        pass

    def update(self, job_id, state, **kwargs):
        client = self.client
        api_version = self.client_kwargs.get('version')
        instance_url = client.instance_url
        request_body = {'state': state}
        session_id = client.session_id
        update_job = UpdateJob(session_id, instance_url, api_version, job_id, request_body, **kwargs)
        response = update_job.request()

        return response, update_job


class UpdateJob(commons.BaseRequest):
    """ Performs a PATCH request to `'/services/data/vX.XX/jobs/ingest/<job_id>'`
        .. versionadded:: 1.1.0
    """
    def __init__(self, session_id, instance_url, api_version, job_id, request_body, **kwargs):
        """ Constructor.

          :param: session_id: Session ID used to make request
          :type: session_id: string
          :param: instance_url: Instance URL used to make the request (eg. `'eu11.salesforce.com'`)
          :type: instance_url: string
          :param: api_version: API version
          :type: api_version: string
          :param: job_id: API version
          :type: job_id: string
          :param: request_body: Request body
          :type: request_body: dict
          :param: **kwargs: kwargs
          :type: **kwargs: dict
        """
        super(UpdateJob, self).__init__(session_id, instance_url, **kwargs)

        self.http_method = 'PATCH'
        self.request_body = request_body
        self.service = UPDATE_URI % (api_version, job_id)


class Jobs(commons.ApiNamespace):
    def __init__(self, client):
        super(Jobs, self).__init__(client)

        self.ingest = Ingest(client)
