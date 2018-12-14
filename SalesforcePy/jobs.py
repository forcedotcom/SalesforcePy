"""
.. module:: jobs
   :synopsis: A Salesforce Bulk API 2.0 jobs implementation.

.. moduleauthor:: Aaron Caffrey <acaffrey@salesforce.com>

"""
from __future__ import absolute_import
from . import commons

BATCHES_URI = '/services/data/v%s/jobs/ingest/%s/batches'
CREATE_URI = '/services/data/v%s/jobs/ingest'
DELETE_URI = '/services/data/v%s/jobs/ingest/%s'
GET_ALL_URI = '/services/data/v%s/jobs/ingest'
GET_INFO_URI = '/services/data/v%s/jobs/ingest/%s'
GET_SUCCESSES_URI = '/services/data/v%s/jobs/ingest/%s/successfulResults'
GET_FAILURES_URI = '/services/data/v%s/jobs/ingest/%s/failedResults'
GET_UNPROCESSED_URI = '/services/data/v%s/jobs/ingest/%s/unprocessedrecords'
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


class DeleteJob(commons.BaseRequest):
    """ Performs a DELETE request to `'/services/data/vX.XX/jobs/ingest/<job_id>'`
        .. versionadded:: 1.1.0
    """
    def __init__(self, session_id, instance_url, api_version, job_id, **kwargs):
        """ Constructor. Calls `super`, then encodes the `service` including the `query_string` provided

          :param: session_id: Session ID used to make request
          :type: session_id: string
          :param: instance_url: Instance URL used to make the request (eg. `'eu11.salesforce.com'`)
          :type: instance_url: string
          :param: api_version: API version
          :type: api_version: string
          :param: job_id: Job ID
          :type: job_id: string
          :param: **kwargs: kwargs
          :type: **kwargs: dict
        """
        super(DeleteJob, self).__init__(session_id, instance_url, **kwargs)

        self.http_method = 'DELETE'
        self.service = DELETE_URI % (api_version, job_id)


class GetJob(commons.BaseRequest):
    """ Performs a GET request to `'/services/data/vX.XX/jobs/ingest'`
        .. versionadded:: 1.1.0
    """
    def __init__(self, session_id, instance_url, api_version, **kwargs):
        """ Constructor. Calls `super`, then encodes the `service` including the `query_string` provided

          :param: session_id: Session ID used to make request
          :type: session_id: string
          :param: instance_url: Instance URL used to make the request (eg. `'eu11.salesforce.com'`)
          :type: instance_url: string
          :param: api_version: API version
          :type: api_version: string
          :param: **kwargs: kwargs
          :type: **kwargs: dict
        """
        super(GetJob, self).__init__(session_id, instance_url, **kwargs)

        successes = kwargs.get('successes', False)
        failures = kwargs.get('failures', False)
        unprocessed = kwargs.get('unprocessed', False)
        job_id = kwargs.get('job_id', None)
        job_info = kwargs.get('job_info', successes is False and failures is False and unprocessed is False)

        self.http_method = 'GET'

        if successes:
            self.service = GET_SUCCESSES_URI % (api_version, job_id)
        elif failures:
            self.service = GET_FAILURES_URI % (api_version, job_id)
        elif unprocessed:
            self.service = GET_UNPROCESSED_URI % (api_version, job_id)
        elif job_info and job_id is not None:
            self.service = GET_INFO_URI % (api_version, job_id)
        else:
            self.service = GET_ALL_URI % api_version


class Ingest(commons.ApiNamespace):
    @commons.kwarg_adder
    def batches(self, job_id, csv_file, **kwargs):
        client = self.client
        api_version = self.client_kwargs.get('version')
        batches = Batches(client.session_id, client.instance_url, api_version, job_id, csv_file, **kwargs)
        response = batches.request()

        return response, batches

    @commons.kwarg_adder
    def create(self, job_resource, **kwargs):
        client = self.client
        api_version = self.client_kwargs.get('version')
        create_job = CreateJob(client.session_id, client.instance_url, api_version, job_resource, **kwargs)
        response = create_job.request()

        return response, create_job

    @commons.kwarg_adder
    def get(self, **kwargs):
        client = self.client
        api_version = self.client_kwargs.get('version')
        get_job = GetJob(client.session_id, client.instance_url, api_version, **kwargs)
        response = get_job.request()

        return response, get_job

    @commons.kwarg_adder
    def delete(self, job_id, **kwargs):
        client = self.client
        api_version = self.client_kwargs.get('version')
        delete_job = DeleteJob(client.session_id, client.instance_url, api_version, job_id, **kwargs)
        response = delete_job.request()

        return response, delete_job

    @commons.kwarg_adder
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
          :param: job_id: Job ID
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
