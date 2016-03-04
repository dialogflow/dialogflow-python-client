# -*- coding: utf-8 -*-

"""
apiai
~~~~~~~~~~~~~~~~
This module provides a ApiAI classes to manage requests.
"""

try: # Python 3
    from http.client import HTTPSConnection
except ImportError:
    from httplib import HTTPSConnection

import uuid

from requests import VoiceRequest
from requests import TextRequest

DEFAULT_VERSION = '20150910'

class ApiAI(object):
    """Main endpoint for using api.ai

    Provides request.

    Basic Usage::
        >>> ...
        >>> import apiai
        >>> ai = apiai.ApiAI(<CLIENT_ACCESS_TOKEN>, <SUBSCRIPTION_KEY>)
        >>> text_request = ai.text_request()
        >>> ...
    """

    __connection__class = HTTPSConnection

    @property
    def client_access_token(self):
        """client access token provided by http://api.ai/"""
        return self._client_access_token

    @client_access_token.setter
    def client_access_token(self, client_access_token):
        self._client_access_token = client_access_token

    @property
    def subscibtion_key(self):
        """subscribtion key provided by http://api.ai/"""
        return self._subscibtion_key

    @subscibtion_key.setter
    def subscibtion_key(self, subscibtion_key):
        self._subscibtion_key = subscibtion_key
    
    @property
    def session_id(self):
        """session_id user for unique identifier of current application user.
        And it provide different contexts and entities for different users.
        Default it generated like uuid for every object of `ApiAI` class."""
        return self._session_id

    @session_id.setter
    def session_id(self, session_id):
        self._session_id = session_id
    

    def __init__(self, client_access_token, subscribtion_key):
        """Construct a `ApiAI`

        client_access_token: client access token provided by http://api.ai/
        subscribtion_key: subscribtion key provided by http://api.ai/
        """

        super(ApiAI, self).__init__()
        self.client_access_token = client_access_token
        self.subscribtion_key = subscribtion_key

        self._base_url = 'api.api.ai'
        self._version = DEFAULT_VERSION

        self.session_id = uuid.uuid4().hex

    def voice_request(self):
        """Construct a VoiceRequest, prepare it. 
        Fields of request default filled from `ApiAI` parameters 
        (session_id, version, client_access_token, subscribtion_key).
        Returns `VoiceRequest` object.
        """

        request = VoiceRequest(
            self.client_access_token, 
            self.subscribtion_key, 
            self._base_url, 
            self._version, 
            self.session_id)

        return request

    def text_request(self):
        """Construct a `VoiceRequest`, prepare it.
        Fields of request default filled from `ApiAI` parameters 
        (session_id, version,client_access_token, subscribtion_key).
        Returns `TextRequest` object.
        """

        request = TextRequest(
            self.client_access_token, 
            self.subscribtion_key, 
            self._base_url, 
            self._version, 
            self.session_id)

        return request