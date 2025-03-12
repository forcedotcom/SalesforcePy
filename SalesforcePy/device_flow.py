from .commons import OAuthRequest


class AuthNRequest(OAuthRequest):
    """ OAuth device flow authentication request implementation
    """
    def __init__(self, client_id, device_code, **kwargs):
        super(AuthNRequest, self).__init__(None, None, **kwargs)
        self.login_url = kwargs.get('login_url', 'login.salesforce.com')
        self.client_id = client_id
        self.device_code = device_code
        self.http_method = 'POST'
        self.service = '/services/oauth2/token'
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Host': self.login_url} # 'orgfarm-f3cf690995-dev-ed.develop.my.salesforce.com'
        self.payload = self.get_payload()

    def get_payload(self):
        """ Returns the payload dict to be used in the request.

        :return: OAuth2 request body required to obtain code.
        :rtype: dict
        """

        return {
            'grant_type': 'device',
            'client_id': self.client_id,
            'code': self.device_code
        }
    
    def request(self):
        """ Gets the result of `super` for this method, then assigns the `access_token` to `session_id`.
        Returns request response.

          :return: Response dict
          :rtype: dict
        """
        response = super(AuthNRequest, self).request()
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


class AuthZRequest(OAuthRequest):
    """ OAuth device flow authorisation request implementation
    """
    def __init__(self, client_id, **kwargs):
        super(AuthZRequest, self).__init__(None, None, **kwargs)

        self.login_url = kwargs.get('login_url', 'login.salesforce.com')
        self.client_id = client_id
        self.device_code = None
        self.http_method = 'POST'
        self.service = '/services/oauth2/token'
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Host': self.login_url}
        self.scope = kwargs.get('scope')
        self.payload = self.get_payload()

    def get_payload(self):
        """ Returns the payload dict to be used in the request.

        :return: OAuth2 request body required to obtain code.
        :rtype: dict
        """

        payload = {
            'response_type': 'device_code',
            'client_id': self.client_id
        }

        if self.scope is not None:
            payload['scope'] = self.scope

        return payload

    def request(self):
        """ Gets the result of `super` for this method, then assigns the `device_code`.
        Returns request response.

        :return: Response dict
        :rtype: dict
        """
        response = super(AuthZRequest, self).request()
        if response is not None:
            if 'device_code' in response:
                self.device_code = response['device_code']
            return response
