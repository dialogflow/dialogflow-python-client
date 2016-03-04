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

class _Serializable(object):
    """Abstract serializable class.
    All classes implemended this used for request parameters.
    It can be serializable to JSON values for request parameters."""

    """Private method used for object serialization."""
    def _to_dict(self):
        raise NotImplementedError()
        

class Entry(_Serializable):
    """User entry for class `Entity`
    Entry objects, which contain reference names and synonyms for `Entity`.
    For detail information about entries see https://docs.api.ai/v6/docs/concept-entities
    """

    @property
    def value(self):
        """Entry's value A canonical name to be used in place of the synonyms.
        Example: `New York`"""
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def synonyms(self):
        """The array of synonyms.
        Example: `["New York", "@big Apple", "city that @{never, seldom, rarely} sleeps"]`"""
        return self._synonyms

    @synonyms.setter
    def synonyms(self, synonyms):
        self._synonyms = synonyms

    def __init__(self, value, synonyms):
        """Construct a `Entry` and fill default values."""
        super(Entry, self).__init__()

        self._value = value
        self._synonyms = synonyms

    """Private method used for object serialization."""
    def _to_dict(self):
        return {
            'value': self.value,
            'synonyms': self.synonyms
        }
        

class Entity(_Serializable):
    """
    User entity for `Request`
    `Entity` is used to create, retrieve and update user-defined entity objects.
    For detail information about entities see https://docs.api.ai/v6/docs/concept-entities
    """

    @property
    def name(self):
        "Entity name"
        return self._name
    
    @name.setter
    def name(self, name):
        self._name = name

    @property
    def entries(self):
        "Entity entries. Array of `Entry` class objects"
        return self._entries

    @entries.setter
    def entries(self, entries):
        self._entries = entries
    
    def __init__(self, name, entries):
        super(Entity, self).__init__()

        self.name = name
        self.entries = entries

    """Private method used for object serialization."""
    def _to_dict(self):
        return {
            'name': self.name,
            'entries': list(map(lambda x: x._to_dict(), self.entries))
        }

