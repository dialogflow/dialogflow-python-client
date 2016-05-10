# -*- coding: utf-8 -*-

"""
apiai
~~~~~~~~~~~~~~~~
This module provides a ApiAI classes to manage requests.
"""

try:  # Python 3
    from http.client import HTTPSConnection
except ImportError:
    from httplib import HTTPSConnection

import uuid

from .requests import VoiceRequest
from .requests import TextRequest
from .requests import UserEntitiesRequest

DEFAULT_VERSION = '20150910'


class ApiAI(object):
    """Main endpoint for using api.ai

    Provides request.

    Basic Usage::
        >>> ...
        >>> import apiai
        >>> ai = apiai.ApiAI(<CLIENT_ACCESS_TOKEN>)
        >>> text_request = ai.text_request()
        >>> ...
    """

    __connection__class = HTTPSConnection

    @property
    def client_access_token(self):
        """client access token provided by https://api.ai/"""
        return self._client_access_token

    @client_access_token.setter
    def client_access_token(self, client_access_token):
        self._client_access_token = client_access_token

    @property
    def session_id(self):
        """session_id user for unique identifier of current application user.
        And it provide different contexts and entities for different users.
        Default it generated like uuid for every object of `ApiAI` class."""
        return self._session_id

    @session_id.setter
    def session_id(self, session_id):
        self._session_id = session_id

    def __init__(self, client_access_token, session_id=None):
        """Construct a `ApiAI`

        client_access_token: client access token provided by https://api.ai/
        """

        super(ApiAI, self).__init__()
        self.client_access_token = client_access_token

        self._base_url = 'api.api.ai'
        self._version = DEFAULT_VERSION

        if session_id is None:
            self.session_id = uuid.uuid4().hex
        else:
            self.session_id = session_id

    def voice_request(self):
        """Construct a VoiceRequest, prepare it.
        Fields of request default filled from `ApiAI` parameters
        (session_id, version, client_access_token).
        Returns `VoiceRequest` object.
        """

        request = VoiceRequest(
            self.client_access_token,
            self._base_url,
            self._version,
            self.session_id)

        return request

    def text_request(self):
        """Construct a `VoiceRequest`, prepare it.
        Fields of request default filled from `ApiAI` parameters
        (session_id, version,client_access_token).
        Returns `TextRequest` object.
        """

        request = TextRequest(
            self.client_access_token,
            self._base_url,
            self._version,
            self.session_id)

        return request

    def user_entities_request(self, user_entities=[]):
        """Construct a `UserEntitiesRequest`, prepare it.
        Returns `UserEntitiesRequest` object.
        """

        request = UserEntitiesRequest(
            self.client_access_token,
            self._base_url,
            user_entities)

        return request
