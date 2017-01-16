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

from .requests import (
    VoiceRequest,
    TextRequest,
    UserEntitiesRequest,
    events
)

import warnings

DEFAULT_VERSION = '20150910'


class ApiAI(object):
    """
        Main endpoint for using api.ai
        Provides request.

        Basic Usage::
            >>> ...
            >>> import apiai
            >>> ai = apiai.ApiAI(<CLIENT_ACCESS_TOKEN>)
            >>> text_request = ai.text_request()
            >>> ...

        :param client_access_token: client access token provided by https://api.ai/
        :type client_access_token: str or unicde
    """

    _connection_class = HTTPSConnection

    @property
    def client_access_token(self):
        """
            Client access token provided by https://api.ai/

            :rtype: str or unicode
        """

        return self._client_access_token

    @client_access_token.setter
    def client_access_token(self, client_access_token):
        """
            :type client_access_token: str or unicode
        """

        self._client_access_token = client_access_token

    @property
    def session_id(self):
        """
            session_id user for unique identifier of current application user.
            And it provide different contexts and entities for different users.
            Default it generated like uuid for every object of `ApiAI` class.


            :rtype: str or unicode
        """

        return self._session_id

    @session_id.setter
    def session_id(self, session_id):
        """
            :type session_id: str or unicode
        """

        self._session_id = session_id

    def __init__(self, client_access_token, session_id=None):
        super(ApiAI, self).__init__()
        self._client_access_token = client_access_token

        self._base_url = 'api.api.ai'
        self._version = DEFAULT_VERSION

        if session_id is None:
            self._session_id = uuid.uuid4().hex
        else:
            self._session_id = session_id

    def voice_request(self):
        """
            Construct a VoiceRequest, prepare it.
            Fields of request default filled from `ApiAI` parameters
            (session_id, version, client_access_token).

            This method is deprecated. Will be remove soon (1st feb 2017).
            The request working only for old paid account.

            Returns `VoiceRequest` object.

            :rtype VoiceRequest:
        """

        warnings.warn('This method is deprecated. Will be remove soon.', DeprecationWarning, stacklevel=2)

        request = VoiceRequest(
            self.client_access_token,
            self._base_url,
            self._version,
            self.session_id
        )

        return request

    def text_request(self):
        """
            Construct a `VoiceRequest`, prepare it.
            Fields of request default filled from `ApiAI` parameters
            (session_id, version,client_access_token).
            Returns `TextRequest` object.

            :rtype TextRequest:
        """

        request = TextRequest(
            self.client_access_token,
            self._base_url,
            self._version,
            self.session_id
        )

        return request

    def user_entities_request(self, user_entities=None):
        """
            Construct a `UserEntitiesRequest`, prepare it.
            Returns `UserEntitiesRequest` object.

            :rtype UserEntitiesRequest:
        """

        if user_entities is None:
            user_entities = []

        request = UserEntitiesRequest(
            self.client_access_token,
            self._base_url,
            user_entities
        )

        return request

    def event_request(self, event=None):
        """
            :type event: events.Event
            :rtype: events.EventRequest
        """

        request = events.EventRequest(
            self.client_access_token,
            self._base_url,
            self._version,
            self.session_id
        )

        request.event = event

        return request
