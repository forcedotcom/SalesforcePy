"""
.. module:: commons
   :synopsis: Classes to be inherited within `sfdc` module.

.. moduleauthor:: Jose Garcia Ponce <jgarciaponce@salesforce.com>, Aaron Caffrey <acaffrey@salesforce.com>
.. versionadded:: 1.0.0

"""
from __future__ import absolute_import

import logging
import requests

DEFAULT_API_VERSION = '37.0'


def get_request(base_request):
    """
    Performs GET request for the class provided.
    :param: base_request: Class with which to make request.
    :type: BaseRequest
    :return: response
    :rtype: requests.Response
    """
    (headers, _, _, _, service) = base_request.get_request_vars()

    return requests.get(
        service, headers=headers, proxies=base_request.proxies, timeout=base_request.timeout)


def post_request(base_request):
    """
    Performs POST request for the class provided.
    :param: base_request: Class with which to make request.
    :type: BaseRequest
    :return: response
    :rtype: requests.Response
    """
    (headers, _, _, _, service) = base_request.get_request_vars()

    return requests.post(
        service, headers=headers, proxies=base_request.proxies, timeout=base_request.timeout,
        json=base_request.request_body)


def kwarg_adder(func):
    """
    Decorator to add the kwargs from the client to the kwargs at the function level. If the same
    parameters are used in both, the function level kwarg will supersede the one at the client level.
    :param func: client function to add client kwargs to
    :return: the function with updated kwargs
    """
    def decorated(self, *args, **function_kwarg):
        if hasattr(self, 'client_kwargs'):
            client_args = {key: val for key, val in self.client_kwargs.items()
                           if key not in function_kwarg.keys()}

            function_kwarg.update(client_args)
        return func(self, *args, **function_kwarg)

    return decorated


class SFDCRequestException(Exception):
    """
    This exception is raised when we fail to complete requests to the SFDC REST API.
    .. versionadded:: 1.0.0
    """
    pass


class ApiNamespace(object):
    """ Base class for API namespaces.

        .. versionadded:: 1.0.0
    """
    def __init__(self, client):
        self.client = client
        self.client_kwargs = client.client_kwargs


class BaseRequest(object):
    """ Base class for all request objects, for convenience, new request types should inherit from this

        .. versionadded:: 1.0.0
    """
    def __init__(self, session_id, instance_url, **kwargs):
        """ Constructor.

            :param: session_id: Session ID used to make request
            :type: session_id: string
            :param: instance_url: Instance URL used to make the request (eg. `'eu11.salesforce.com'`)
            :type: instance_url: string
            :param: **kwargs: kwargs
            :type: **kwargs: dict
            :Keyword Arguments:
                * *api_version* (`string`) --
                    API version for the request
                    Default: `'37.0'`
                * *http_method* (`string`) --
                    HTTP method for the request
                    Default: `'GET'`
                * *proxies* (`dict`) --
                    A dict containing proxies to be used by `requests` module. Ex:
                        `{"https": "example.org:443"}`
                    Default: `None`
                * *timeout* (`string`) --
                    A dict indicating the timeout value for connect and read to be used by `requests` module. Ex:
                        `{"timeout": "30"}`
                    Default: `None`
                * *request_body* (`dict`) --
                    A dict containing the request body
                    Default: `None`
        """
        self.proxies = kwargs.get('proxies', None)
        self.session_id = session_id
        self.http_method = kwargs.get('http_method', 'GET')
        self.instance_url = instance_url
        self.request_body = kwargs.get('request_body', None)
        self.api_version = kwargs.get('version', DEFAULT_API_VERSION)
        self.timeout = float(kwargs['timeout']) if 'timeout' in kwargs else None
        self.service = None
        self.status = None
        self.response = None
        self.headers = None
        self.request_url = None
        self.exceptions = []

    def get_request_url(self):
        """ Returns the request URL. (default: `'https://<instance_url><service>'`)

          :return: request_url
          :rtype: string
        """
        self.request_url = 'https://%s%s' % (self.instance_url,
                                             self.service) if self.request_url is None else self.request_url
        return self.request_url

    def get_headers(self):
        """ Returns headers dict for the request.

          :return: headers
          :rtype: dict
        """
        self.headers = {
            'Content-Type': 'application/json',
            'Accept-Encoding': 'application/json',
            'Authorization': 'OAuth %s' %
            self.session_id} if self.headers is None else self.headers
        return self.headers

    def get_request_vars(self):
        """ Returns the variables required by request()` and other functions.

          :return: (headers, logger, request_object, response, service)
          :rtype: (dict, logging.Logger, requests.Request|None, list|dict|None, string)
        """
        return (
            self.get_headers(),
            logging.getLogger('sfdc_py'),
            None,
            None,
            self.get_request_url()
        )

    def request(self):
        """ Makes request to Salesforce and returns serialised response. Catches any exceptions and appends them to
        `self.exceptions`.

          :return: response: Salesforce response, if available
          :rtype: list|dict|None
        """
        (headers, logger, request_object, response, service) = self.get_request_vars()
        logging.getLogger('sfdc_py').info('%s %s' %
                                          (self.http_method, service))

        if self.http_method == 'POST':
            request_fn = post_request
        else:
            request_fn = get_request

        try:
            request_object = request_fn(self)
            self.status = request_object.status_code

            if request_object.content.decode('utf-8') == 'null':
                raise SFDCRequestException('Request body is null')
            else:
                response = request_object.json()
        except Exception as e:
            self.exceptions.append(e)
            logger.error('%s %s %s' % (self.http_method, service, self.status))
            logger.error(e.message)
            return
        finally:
            return response

    def set_proxies(self, proxies):
        """ Sets `proxies` for this class.
        :param proxies: A dict containing proxies to use (see:
        http://docs.python-requests.org/en/master/user/advanced/#proxies)
        :type: dict
        """
        self.proxies = proxies


class OAuthRequest(BaseRequest):
    """ Base class for all OAuth request objects

        .. versionadded:: 1.0.0
    """
    def __init__(self, session_id, instance_url, **kwargs):
        super(OAuthRequest, self).__init__(session_id, instance_url, **kwargs)
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        self.login_url = None
        self.payload = None

    def request(self):
        (headers, logger, request_object, response,
         service) = self.get_request_vars()
        payload = self.payload
        logging.getLogger('sfdc_py').info('%s %s' % ('POST', service))
        try:
            request_object = requests.post(
                service, headers=headers, data=payload, proxies=self.proxies, timeout=self.timeout)
            self.status = request_object.status_code
            if self.status == requests.codes.ok:
                response = request_object.json()
            else:
                raise SFDCRequestException('OAuth call failed. Received %s status code' % self.status)
        except Exception as e:
            self.exceptions.append(e)
            logger.error('%s %s %s' % (self.http_method, service, self.status))
            logger.error(e.message)
            return
        finally:
            return response

    def get_request_url(self):
        url = self.instance_url if self.login_url is None else self.login_url
        self.request_url = 'https://%s%s' % (
            url, self.service) if self.request_url is None else self.request_url
        return self.request_url
