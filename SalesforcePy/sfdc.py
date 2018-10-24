"""
.. module:: sfdc
   :synopsis: A Salesforce Rest API module

.. moduleauthor:: Aaron Caffrey <acaffrey@salesforce.com>, Jose Garcia Ponce <jgarciaponce@salesforce.com>,
    Colin Cheevers <ccheevers@salesforce.com>, Tania Prince <tania.prince@salesforce.com>

"""
from __future__ import absolute_import

from . import chatter
from . import commons
from . import wave

import json
import logging
import re
import requests

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

DEFAULT_API_VERSION = commons.DEFAULT_API_VERSION
SOBJ_SERVICE = '/services/data/v%s/sobjects%s'
REVOKE_SERVICE = '/services/oauth2/revoke'
VERSIONS_SERVICE = '/services/data/'
QUERY_SERVICE = '/services/data/v%s/query/?%s'
SEARCH_SERVICE = '/services/data/v%s/search/?%s'
TOOLING_ANONYMOUS = '/services/data/v%s/tooling/executeAnonymous/?%s'
APPROVAL_SERVICE = '/services/data/v%s/process/approvals/'

INSERT_BINARY_BODY_TEMPLATE = """--boundary_string
Content-Disposition: form-data; name="entity_%s";
Content-Type: application/json

%s

--boundary_string
Content-Type: %s
Content-Disposition: form-data; name="%s"; filename="%s"

%s

--boundary_string--"""


class ApprovalProcess(commons.BaseRequest):
    """ Returns a list of all approval processes. Can also be used to submit a particular record if that entity supports
            an approval process and one has already been defined. It also supports specifying a collection of different
            Process Approvals requests to have them all executed in bulk.

        .. versionadded:: 1.0.0
    """

    def __init__(self, session_id, instance_url, **kwargs):
        super(
            ApprovalProcess,
            self).__init__(
            session_id,
            instance_url,
            **kwargs)

        self.service = APPROVAL_SERVICE % self.api_version

        if self.request_body is None:
            self.http_method = 'GET'
        elif self.request_body is not None:
            self.http_method = 'POST'


class Client(object):
    """ The client class from which all API calls to a Salesforce organisation are made.
        .. versionadded:: 1.0.0
    """
    def __init__(self, *args, **kwargs):
        """ Constructor.

            :Parameters:
                - `*username` (`string`) - Salesforce username.
                - `*password` (`string`) - Salesforce password.
                - `*login_url` (`string`) - Salesforce login URL.
                - `*client_id` (`string`) - Salesforce client ID.
                - `*client_secret` (`string`) - Salesforce client secret.
                - `\**kwargs` - kwargs (see below)

            :Keyword Arguments:
                * *protocol* (`string`) --
                    Protocol (future use)
                * *proxies* (`dict`) --
                    A dict containing proxies to be used by `requests` module. Ex:
                        `{"https": "example.org:443"}`
                    Default: `None`
                * *version* (`string`) --
                   SFDC API version to use e.g. '39.0'
        """

        self.username = args[0]
        self.password = args[1]
        self.client_id = args[2]
        self.client_secret = args[3]
        self.protocol = kwargs.get('protocol')
        self.proxies = kwargs.get('proxies')
        self.instance_url = None
        self.logger = logging.getLogger('sfdc_py')
        self.logger.setLevel(logging.FATAL)
        self.logger.addHandler(logging.StreamHandler())
        self.client_api_version = None
        self.client_kwargs = kwargs
        self.session_id = None
        self.chatter = chatter.Chatter(self)
        self.wave = wave.Wave(self)

    def set_instance_url(self, url):
        """ Strips the protocol from `url` and assigns the value to `self.instance_url`

          :param url: Instance URL used to make requests (eg. `'https://eu11.salesforce.com'`)
          :type url: string
        """

        host_only_regex = re.compile('(?:https://)(.*)(?:/*)')
        match = re.match(host_only_regex, url)
        instance_url = match.group(1)
        self.instance_url = instance_url

    @commons.kwarg_adder
    def login(self, **kwargs):
        """ Performs a login request.

          :param: **kwargs: kwargs
          :type: **kwargs: dict
          :return: Login response
          :rtype: (dict, Login)
          :raises: LoginException
        """

        login_response = Login(
            self.username,
            self.password,
            self.client_id,
            self.client_secret,
            **kwargs
        )
        req = login_response.request()
        if req is None:
            raise LoginException("Failed to perform `login` request")
        self.session_id = login_response.get_session_id()
        self.set_instance_url(req.get('instance_url', str()))
        self.set_api_version()
        return req, login_response

    @commons.kwarg_adder
    def set_api_version(self, **kwargs):
        """
        Sets the api version to be used by the client. If not provided, it will get the latest version
        available
        :return: set version kwarg on client if not defined
        """
        # If 'version' was already in the client kwargs, then 'commons.kwarg_adder' decorator will take care of
        # passing it around between functions. Therefore, an else statement is not needed here.
        if 'version' not in self.client_kwargs:
            service = 'https://' + self.instance_url + VERSIONS_SERVICE
            headers = {'Content-Type': 'application/json'}
            r = requests.get(service, headers=headers, proxies=self.proxies)
            if r.status_code == 200:
                versions = []
                for i in r.json():
                    versions.append(i['version'])
                self.client_kwargs.update({'version': max(versions)})
            else:
                # return a known recent api version
                self.client_kwargs.update({'version': DEFAULT_API_VERSION})

    @commons.kwarg_adder
    def logout(self, **kwargs):
        """ Performs a logout request.

          :param: **kwargs: kwargs
          :type: **kwargs: dict
          :return: Logout response
          :rtype: (dict, Logout)
        """

        logout_response = Logout(self.session_id, self.instance_url, **kwargs)
        req = logout_response.request()
        return req, logout_response

    @commons.kwarg_adder
    def query(self, qs, **kwargs):
        """ Performs a query request.

          :param: qs: Query string. eg `'SELECT Id FROM Account LIMIT 10'`
          :type: qs: string
          :param: **kwargs: kwargs
          :type: **kwargs: dict
          :return: Query response
          :rtype: (dict, Query)
        """

        q = Query(self.session_id, self.instance_url, qs, **kwargs)
        req = q.request()
        return req, q

    @commons.kwarg_adder
    def query_more(self, qs, **kwargs):
        """ Performs a query more request.

          :param: qs: Query string. eg `'SELECT Id FROM Lead'`
          :type: qs: string
          :param: **kwargs: kwargs
          :type: **kwargs: dict
          :return: QueryMore response
          :rtype: ([dict], QueryMore)
        """

        qm = QueryMore(self.session_id, self.instance_url, qs, **kwargs)
        req = qm.request()
        return req, qm

    @commons.kwarg_adder
    def sobjects(self, **kwargs):
        """ Prepares an SObject controller with which make various API requests.

          :param: **kwargs: kwargs
          :type: **kwargs: dict
          :return: SObjects response
          :rtype: SObjectController
        """

        _id = kwargs['id'] if 'id' in kwargs else None
        object_type = kwargs['object_type'] if 'object_type' in kwargs else None
        binary_field = kwargs['binary_field'] if 'binary_field' in kwargs else None
        api_version = kwargs.get('version')
        external_id = kwargs['external_id'] if 'external_id' in kwargs else None
        return SObjectController(self, object_type, _id, binary_field, api_version, external_id)

    @commons.kwarg_adder
    def search(self, ss, **kwargs):
        """ Performs a search request.

          :param: ss: Search string. eg `'FIND {sfdc_py} RETURNING Account(Id, Name) LIMIT 5'`
          :type: ss: string
          :param: **kwargs: kwargs
          :type: **kwargs: dict
          :return: Search response
          :rtype: (dict, Search)
        """

        s = Search(self.session_id, self.instance_url, ss, **kwargs)
        req = s.request()
        return req, s

    @commons.kwarg_adder
    def execute_anonymous(self, ab, **kwargs):
        """ Performs an anonymous Apex execution request.

          :param: ab: Anonymous block of Apex code, eg: `'system.debug("Hello world")'`
          :type: ab: string
          :param: **kwargs: kwargs
          :type: **kwargs: dict
          :return: Execute anonymous response
          :rtype: (dict, ExecuteAnonymous)
        """

        ea = ExecuteAnonymous(
            self.session_id,
            self.instance_url,
            ab,
            **kwargs)
        req = ea.request()
        return req, ea

    @commons.kwarg_adder
    def approvals(self, body=None, **kwargs):
        """ Performs an approval process request.

          :param: body: Body of approval process request, if any.
          :type: body: dict
          :return: Approval response
          :rtype: (dict, ApprovalProcess)
        """

        k = {
            'request_body': body,
            'proxies': self.proxies
        }
        k.update(kwargs)
        ar = ApprovalProcess(
            session_id=self.session_id,
            instance_url=self.instance_url,
            **k)
        req = ar.request()
        return req, ar

    @commons.kwarg_adder
    def debug(self, **kwargs):
        """ Sets up debugging for the client at the level provided in the `level` kwarg.

        If this method is called but no `level` kwarg is provided, the client sets the debug level to `logging.INFO` by
        default.

        .. versionadded:: 1.0.0

          :param: **kwargs: kwargs
          :type: **kwargs: dict
        """

        logger = self.logger
        if 'level' in kwargs:
            level = kwargs['level']
            logger.setLevel(level)
        else:
            logger.setLevel(logging.INFO)

    def __enter__(self):
        """
        Invoked on entry to this class, handle login automatically for context managers
        :return: self
        """
        self.login()
        return self

    def __exit__(self, _type, value, traceback):
        """
        Handle logout automatically upon exiting the statement's body
        https://docs.python.org/2/reference/datamodel.html#with-statement-context-managers
        :param type: exception type
        :param value: exception value
        :param traceback: traceback for the exception
        :return:None
        """
        try:
            self.logout()
        except Exception as e:
            self.logger.warning('Unable to logout. Reason: {}'.format(e.args[0]))
            self.logger.info('__exit__ params: (%s, %s, %s)' % (_type, value, traceback))


class ExecuteAnonymous(commons.BaseRequest):
    """ Performs a request to '/services/data/vX.XX/tooling/executeAnonymous/'
        .. versionadded:: 1.0.0
    """
    def __init__(self, session_id, instance_url, ab, **kwargs):
        """ Constructor. Calls `super`, then encodes the `service` query string including the abstract block (`ab`)
        passed in.

          :param: session_id: Session ID used to make request
          :type: session_id: string
          :param: instance_url: Instance URL used to make the request (eg. `'eu11.salesforce.com'`)
          :type: instance_url: string
          :param: ab: Anonymous block of Apex code, eg: `'system.debug("Hello world")'`
          :type: ab: string
          :param: **kwargs: kwargs
          :type: **kwargs: dict
        """

        super(
            ExecuteAnonymous,
            self).__init__(
            session_id,
            instance_url,
            **kwargs)
        exec_anon = urlencode(
            {'anonymousBody': ab.encode('utf-8')})
        self.service = TOOLING_ANONYMOUS % (self.api_version, exec_anon)


class Login(commons.OAuthRequest):
    """ Performs a request to `'/services/oauth2/token'`
        .. versionadded:: 1.0.0
    """
    def __init__(
            self,
            username,
            password,
            client_id,
            client_secret,
            **kwargs):
        """ Constructor. Calls `super`, assigns all params to their equivalent instance variables, sets `http_method` to
        POST, and prepares the request service and payload.

          :param: username: Salesforce username
          :type: username: string
          :param: password: Salesforce password
          :type: password: string
          :param: login_url: Salesforce login URL
          :type: login_url: string
          :param: client_id: Salesforce client ID
          :type: client_id: string
          :param: client_secret: Salesforce client secret
          :type: client_secret: string
          :param: **kwargs: kwargs
          :type: **kwargs: dict
        """

        super(Login, self).__init__(None, None, **kwargs)
        self.username = username
        self.password = password
        self.login_url = kwargs['login_url'] if 'login_url' in kwargs else 'login.salesforce.com'
        self.client_id = client_id
        self.client_secret = client_secret
        self.http_method = 'POST'
        self.service = '/services/oauth2/token'
        self.payload = self.get_payload()

    def get_payload(self):
        """ Returns the payload dict to be used in the request.

          :return: OAuth2 request body required to obtain access token.
          :rtype: dict
        """

        return {
            'grant_type': 'password',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'username': self.username,
            'password': self.password
        }

    def request(self):
        """ Gets the result of `super` for this method, then assigns the `access_token` to `session_id`.  Returns
        request response.

          :return: Response dict
          :rtype: dict
        """
        response = super(Login, self).request()
        if response is not None:
            if 'access_token' in response:
                self.session_id = response['access_token']
            return response

    def get_session_id(self):
        """ Returns the session ID obtained if the login request was successful

          :return: Session ID
          :rtype: string
        """

        return self.session_id


class LoginException(Exception):
    """ Exception thrown during due to login failure.
        .. versionadded:: 1.0.0
    """
    pass


class Logout(commons.OAuthRequest):
    """ Performs a request to `'/services/oauth2/revoke'`
        .. versionadded:: 1.0.0
    """
    def __init__(self, session_id, instance_url, **kwargs):
        """ Constructor. Calls `super`, assigns the service from the hardcoded value, and sets a `payload`
        instance variable with a dict where key is `'token'` and value is `session_id`

          :param: session_id: Session ID used to make request
          :type: session_id: string
          :param: instance_url: Instance URL used to make the request (eg. `'eu11.salesforce.com'`)
          :type: instance_url: string
          :param: **kwargs: kwargs
          :type: **kwargs: dict
        """

        super(Logout, self).__init__(session_id, instance_url, **kwargs)
        self.service = REVOKE_SERVICE
        self.payload = {'token': self.session_id}


class Query(commons.BaseRequest):
    """ Performs a request to `'/services/data/vX.XX/query/'`
        .. versionadded:: 1.0.0
    """
    def __init__(self, session_id, instance_url, query_string, **kwargs):
        """ Constructor. Calls `super`, then encodes the `service` including the `query_string` provided

          :param: session_id: Session ID used to make request
          :type: session_id: string
          :param: instance_url: Instance URL used to make the request (eg. `'eu11.salesforce.com'`)
          :type: instance_url: string
          :param: query_string: Query string. eg `'SELECT Id FROM Account LIMIT 10'`
          :type: query_string: string
          :param: **kwargs: kwargs
          :type: **kwargs: dict
        """
        super(Query, self).__init__(session_id, instance_url, **kwargs)
        qry = urlencode({'q': query_string.encode('utf-8')})
        self.service = QUERY_SERVICE % (self.api_version, qry)


class QueryMore(commons.BaseRequest):
    """ Performs recursive requests to `'/services/data/vX.XX/query/'` when there are multiple batches to process.
        .. versionadded:: 1.0.0
    """
    def __init__(self, session_id, instance_url, query_string, **kwargs):
        """ Constructor. Calls `super`, then assigns the `query_string` to an instance variable.

          :param: session_id: Session ID used to make request
          :type: session_id: string
          :param: instance_url: Instance URL used to make the request (eg. `'eu11.salesforce.com'`)
          :type: instance_url: string
          :param: query_string: Query string. eg `'SELECT Id FROM Account LIMIT 10'`
          :type: query_string: string
          :param: **kwargs: kwargs
          :type: **kwargs: dict
        """
        super(QueryMore, self).__init__(session_id, instance_url, **kwargs)
        self.query_string = query_string

    def request(self, *args):
        """ Makes a `Query` request for the initial query string, then calls itself recursively to request all remaining
        batches, if there are any.  This method will break the recursion and return all when the last batch processed
        contains a `done` value equal to `True`.

          :param: results: All queried batch results obtained in prior recursions of this method.
          :type: results: [dict]
          :return: A list of dicts where each dict is a batch of query results
          :rtype: [dict]
        """

        (last, results) = (
            dict(),
            list() if len(args) is 0 else args[0],
        )

        len_results = len(results)

        if len_results == 0:
            q = Query(self.session_id, self.instance_url, self.query_string)
            q.set_proxies(self.proxies)
            response = q.request()
            results.append(response)
            last = response
        elif len_results > 0:
            last = results[len_results - 1]
            if last.get('done') is False:
                (headers, logger, request_object, response, service) = self.get_request_vars()
                service = 'https://%s%s' % (self.instance_url, last.get('nextRecordsUrl'))
                logging.getLogger('sfdc_py').info('%s %s' %
                                                  (self.http_method, service))
                try:
                    request_object = requests.get(
                        service, headers=headers, proxies=self.proxies)
                    self.status = request_object.status_code
                    if request_object.content.decode('utf-8') == 'null':
                        raise commons.SFDCRequestException('Request body is null')
                    else:
                        last = request_object.json()
                except Exception as e:
                    self.exceptions.append(e)
                    logger.error('%s %s %s' % (self.http_method, service, self.status))
                    logger.error(e.args[0])
                    return
                else:
                    results.append(last)

        if last.get('done') is True:
            return results
        elif last.get('done') is False:
            return self.request(results)


class Search(commons.BaseRequest):
    """ Performs a request to `'/services/data/vX.XX/search/'`
        .. versionadded:: 1.0.0
    """
    def __init__(self, session_id, instance_url, search_string, **kwargs):
        """ Constructor. Calls `super`, then encodes the `service` including the `search_string` provided

          :param: session_id: Session ID used to make request
          :type: session_id: string
          :param: instance_url: Instance URL used to make the request (eg. `'eu11.salesforce.com'`)
          :type: instance_url: string
          :param: search_string: Search string. eg `'FIND {sfdc_py} RETURNING Account(Id, Name) LIMIT 5'`
          :type: search_string: string
          :param: **kwargs: kwargs
          :type: **kwargs: dict
        """
        super(Search, self).__init__(session_id, instance_url, **kwargs)
        s = urlencode({'q': search_string.encode('utf-8')})
        self.service = SEARCH_SERVICE % (self.api_version, s)


class SObjectBlob(commons.BaseRequest):
    """ Perform a request to `'/services/data/vX.XX/sobjects'` where file i/o is necessary.
        .. versionadded:: 1.0.0
    """

    def __init__(self, _client, service, http_method):
        """ Constructor. Calls `super`, then sets `service` and `http_method` instance variables.

          :param: session_id: Session ID used to make request
          :type: session_id: string
          :param: instance_url: Instance URL used to make the request (eg. `'eu11.salesforce.com'`)
          :type: instance_url: string
          :param: service: The service to append to /services/data/vX.XX/sobjects
          :type: service: string
          :param: http_method: Method to use with request (`'GET'` and `'POST'` currently supported.)
          :type: http_method: string
          :param: **kwargs: kwargs
          :type: **kwargs: dict
        """

        k = {'http_method': http_method}
        k.update(_client.client_kwargs)
        super(SObjectBlob, self).__init__(_client.session_id, _client.instance_url, **k)
        self.service = service

    def set_request_body(self, **kwargs):
        """ Creates binary request body by merging `entity`, `json_body`, `file_content_type`, `field`, `filename` and
        `content` from `**kwargs**` into a binary body template.  Sets `request_body` instance variable with the result.

        Note: `content` can be either a `file` or a raw value.

          :param: **kwargs:
          :type: **kwargs: string
        """

        if self.http_method == 'POST':
            content = kwargs['content']
            self.request_body = INSERT_BINARY_BODY_TEMPLATE % (
                kwargs['entity'],
                kwargs['json_body'],
                kwargs['file_content_type'],
                kwargs['field'],
                kwargs['filename'],
                content)

    def request(self):
        """ Returns the request response.

        :return: response
        :rtype: dict
        """

        (headers, logger, request_object, response, service) = self.get_request_vars()
        logging.getLogger('sfdc_py').info('%s %s' %
                                          (self.http_method, service))
        if self.http_method == 'GET':
            headers['Content-Type'] = 'application/octet-stream'
            try:
                request_object = requests.get(
                    service, headers=headers, proxies=self.proxies, stream=True)
                self.status = request_object.status_code
                if request_object.content.decode('utf-8') == 'null':
                    raise commons.SFDCRequestException('Request body is null')
                else:
                    self.response = response = request_object
            except Exception as e:
                self.exceptions.append(e)
                logger.error('%s %s %s' %
                             (self.http_method, service, self.status))

                logger.error(e.args[0])
                return
            finally:
                return response
        elif self.http_method == 'POST':
            headers['Content-Type'] = 'multipart/form-data;boundary="boundary_string"'
            try:
                request_object = requests.post(
                    service,
                    headers=headers,
                    proxies=self.proxies,
                    data=self.request_body)
                self.status = request_object.status_code
                if request_object.content.decode('utf-8') == 'null':
                    raise commons.SFDCRequestException('Request body is null')
                else:
                    self.response = response = request_object.json()
            except Exception as e:
                self.exceptions.append(e)
                logger.error('%s %s %s' %
                             (self.http_method, service, self.status))
                logger.error(e.args[0])
                return
            finally:
                return response


class SObjectController(object):
    """ A special class that controls insert/update/delete/query/describe of SObject resources.
        .. versionadded:: 1.0.0
    """
    def __init__(self, _client, object_type, _id, binary_field, api_version, external_id):
        """ Constructor.

          :param: _client: Salesforce client object
          :type: _client: Client
          :param: object_type: Name of the SObject, eg. `'Case'`
          :type: object_type: string
          :param: _id: Resource ID, if available
          :type: _id: string
          :param: binary_field: Binary field name, if available on object, eg. `'Body'`
          :type: binary_field: string
        """

        self.__client__ = _client
        self.id = _id
        self.object_type = object_type
        self.binary_field = binary_field
        self.api_version = api_version
        self.external_id = external_id
        # Maintain client kwargs
        self.client_kwargs = _client.client_kwargs

    def get_service(self):
        """ Returns the correct sobject service depending on whether the countroller contains an `id` instance variable

        :return: service
        :rtype: string
        """

        if self.binary_field is not None and self.object_type is not None and self.id is None:
            return SOBJ_SERVICE % (
                self.api_version, '/' + self.object_type)
        elif self.id is not None and self.object_type is not None and self.external_id is None:
            return '/%s/%s' % (self.object_type, self.id)
        elif self.id is not None and self.object_type is not None and self.external_id is not None:
            return '/%s/%s/%s' % (self.object_type, self.external_id, self.id)
        elif self.object_type is None:
            return ''
        return '/%s' % self.object_type

    @commons.kwarg_adder
    def insert(self, body, **kwargs):
        """ Creates an SObject in Salesforce.

        Note: if `binary_field` is defined in kwargs, an `SObjectBlob` request will be made and returned, otherwise an
        `SObject` request will be made.

          :param: body: Body of SObject request.
          :type: body: dict
          :param: **kwargs: kwargs
          :type: **kwargs: dict
          :return: Insert result from Salesforce
          :rtype: (dict, SObject|SObjectBlob)
        """

        sobj = None
        _client = self.__client__
        resource_id = self.get_service()
        if self.binary_field is None:
            k = {
                'http_method': 'POST',
                'request_body': body,
                'resource_id': resource_id
            }
            k.update(kwargs)
            sobj = SObjects(_client, **k)
        elif self.binary_field is not None and 'binary' in kwargs:
            sobj = SObjectBlob(
                _client,
                resource_id,
                'POST')

            # Prep request body properties
            entity = self.object_type.lower()
            json_body = json.dumps(body)
            field = self.binary_field
            filename = kwargs['binary'][0]
            content = kwargs['binary'][1]
            file_content_type = kwargs['binary'][2]

            # Set the request body
            sobj.set_request_body(
                entity=entity,
                json_body=json_body,
                field=field,
                filename=filename,
                content=content,
                file_content_type=file_content_type)
        req = sobj.request()
        return req, sobj

    @commons.kwarg_adder
    def update(self, body, **kwargs):
        """ Updates an SObject in Salesforce.

          :param: body: Body of SObject request.
          :type: body: dict
          :return: Update result from Salesforce
          :rtype: (None, SObject)
        """

        _client = self.__client__
        resource_id = self.get_service()
        k = {
            'http_method': 'PATCH',
            'request_body': body,
            'resource_id': resource_id
        }
        k.update(kwargs)
        sobj = SObjects(_client, **k)
        req = sobj.request()
        return req, sobj

    @commons.kwarg_adder
    def upsert(self, body, **kwargs):
        """ Upserts an SObject in Salesforce.

          :param: body: Body of SObject request.
          :type: body: dict
          :return: Upserts result from Salesforce
          :rtype: (None, SObject)
        """

        _client = self.__client__
        resource_id = self.get_service()
        k = {
            'http_method': 'PATCH',
            'request_body': body,
            'resource_id': resource_id
        }
        k.update(kwargs)
        sobj = SObjects(_client, **k)
        req = sobj.request()
        return req, sobj

    @commons.kwarg_adder
    def delete(self, **kwargs):
        """ Deletes an SObject in Salesforce.

          :return: Delete result from Salesforce
          :rtype: (None, SObject)
        """

        _client = self.__client__
        resource_id = self.get_service()
        k = {
            'http_method': 'DELETE',
            'resource_id': resource_id
        }
        k.update(kwargs)
        sobj = SObjects(_client, **k)
        req = sobj.request()
        return req, sobj

    @commons.kwarg_adder
    def query(self, **kwargs):
        """ Queries an SObject in Salesforce. If a `binary_field` instance variable is defined, this method will further
        query the binary field content and return it accordingly.

          :return: Query result from Salesforce
          :rtype: (dict, SObject)|(dict, SObject, SObjectBlob)
        """
        (_client, resource_id) = (self.__client__, self.get_service())
        k = {
            'http_method': 'GET',
            'resource_id': resource_id
        }
        k.update(kwargs)
        sobj = SObjects(_client, **k)
        req = sobj.request()
        if self.binary_field is not None and isinstance(
                req, dict) and self.binary_field in req:
            bin_service = req[self.binary_field]
            sob_blob = SObjectBlob(
                _client,
                bin_service,
                'GET')
            sob_blob.request()
            return req, sobj, sob_blob
        return req, sobj

    @commons.kwarg_adder
    def describe(self, **kwargs):
        """ Describes the metadata for an SObject in Salesforce.

        .. versionadded:: 1.0.0

          :return: Describe result from Salesforce
          :rtype: (dict, SObject)
        """

        _client = self.__client__
        resource_id = self.get_service()
        k = {
            'http_method': 'GET',
            'resource_id': resource_id + '/describe'
        }
        k.update(kwargs)
        sobj = SObjects(_client, **k)
        req = sobj.request()
        return req, sobj

    @commons.kwarg_adder
    def describe_global(self, **kwargs):
        """ Lists the available objects and their metadata for the organizations data.

        .. versionadded:: 1.0.0

          :return: Describe global result from Salesforce
          :rtype: (dict, SObject)
        """

        _client = self.__client__
        resource_id = self.get_service()
        k = {
            'http_method': 'GET',
            'resource_id': resource_id
        }
        k.update(kwargs)
        sobj = SObjects(_client, **k)
        req = sobj.request()
        return req, sobj


class SObjects(commons.BaseRequest):
    """ Perform a request to `'/services/data/vX.XX/sobjects'`
        .. versionadded:: 1.0.0
    """
    def __init__(self, _client, **kwargs):
        """ Constructor. Calls `super`, retrieves `resource_id` from `**kwargs` if present, then creates `self.service`
        instance variable.

          :param: session_id: Session ID used to make request
          :type: session_id: string
          :param: instance_url: Instance URL used to make the request (eg. `'eu11.salesforce.com'`)
          :type: instance_url: string
          :param: **kwargs: kwargs
          :type: **kwargs: dict
        """
        super(SObjects, self).__init__(_client.session_id, _client.instance_url, **kwargs)
        resource_id = kwargs.get('resource_id')
        self.service = SOBJ_SERVICE % (self.api_version, resource_id)

    def request(self):
        """ Makes the appropriate request depending on the `http_method`.  Supported now are: `'GET'`, `'POST'`,
        `'PATCH'`, and `'DELETE'`. Returns request response.

        Note: As successful `'PATCH'` and `'DELETE'` responses return `NO CONTENT`, this method will return `None`.
        It may be advisable to check the `status` of the `SObject` instance returned as an additional factor in
        determining whether the request succeeded.

          :return: response dict
          :rtype: dict|None
        """
        sobjects_headers = {
            'Content-Type': 'application/json',
            'Accept-Encoding': 'application/json',
            'Sforce-Auto-Assign': 'FALSE'
        }

        (headers, logger, request_object, response, service) = (
            sobjects_headers,
            logging.getLogger('sfdc_py'),
            None,
            None,
            'https://%s%s' % (self.instance_url, self.service)
        )
        headers['Authorization'] = 'OAuth %s' % self.session_id

        logger.info('%s %s' % (self.http_method, service))

        if self.http_method == 'POST':
            request_object = requests.post(
                service,
                headers=headers,
                json=self.request_body,
                proxies=self.proxies)
        elif self.http_method == 'PATCH':
            request_object = requests.patch(
                service,
                headers=headers,
                json=self.request_body,
                proxies=self.proxies)
            self.status = request_object.status_code
            if request_object.status_code == requests.codes.no_content:
                return None
        elif self.http_method == 'DELETE':
            request_object = requests.delete(
                service, headers=headers, proxies=self.proxies)
            self.status = request_object.status_code
            if request_object.status_code == requests.codes.no_content:
                return None
        elif self.http_method == 'GET':
            request_object = requests.get(
                service, headers=headers, proxies=self.proxies)

        self.status = request_object.status_code

        try:
            if request_object.content.decode('utf-8') == 'null':
                raise commons.SFDCRequestException('Request body is null')
            else:
                response = request_object.json()
        except Exception as e:
            self.exceptions.append(e)
            logger.error('%s %s %s' % (self.http_method, service, self.status))
            logger.error(e.args[0])
            return
        finally:
            return response


def client(username, password, client_id, client_secret, **kwargs):
    """ Builds a `Client` and returns it.

        .. versionadded:: 1.0.0

    Note: if any of the required parameters are missing, a `ValueError` will be raised.

        :Parameters:
            - `*username` (`string`) - Salesforce username.
            - `*password` (`string`) - Salesforce password.
            - `*client_id` (`string`) - Salesforce client ID.
            - `*client_secret` (`string`) - Salesforce client secret.
            - `\**kwargs` - kwargs (see below)

        :Keyword Arguments:
            * *login_url* (`string`) --
                Salesforce login URL without protocol
                Default: `'login.salesforce.com'`
            * *protocol* (`string`) --
                Protocol (future use)
            * *proxies* (`dict`) --
                A dict containing proxies to be used by `requests` module. Ex:
                    `{"https": "example.org:443"}`
                Default: `None`
            * *timeout* ('string') --
                Tell Requests to stop waiting for a response after a given number of seconds

        :returns: client
        :rtype: Client
        :raises: ValueError
    """

    if username is None:
        raise ValueError('`username` cannot be None')
    elif password is None:
        raise ValueError('`password` cannot be None')
    elif client_id is None:
        raise ValueError('`client_id` cannot be None')
    elif client_secret is None:
        raise ValueError('`client_secret` cannot be None')
    return Client(
        username,
        password,
        client_id,
        client_secret,
        **kwargs)
