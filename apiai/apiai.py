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

import sys
import json
import uuid
from time import gmtime
from time import strftime

try:
    import urllib.parse
except ImportError:
    import urllib

DEFAULT_VERSION = '20150910'

PY3 = sys.version_info[0] == 3

if PY3:
    def b(s):
        return s.encode("latin-1")
else:
    def b(s):
        return s

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

        self._url = 'api.api.ai'
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
            self._url, 
            self.__connection__class, 
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
            self._url, 
            self.__connection__class, 
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

class Request(object):
    """Abstract request class
    Contain share information for all requests."""

    __connection__class = None

    @property
    def lang(self):
        """lang property used for server determination current request language. 
        In `VoiceRequest` used for determinate language for ASR (Speech Recognitions) service.
        Default equal 'en'. For detail information about support language see https://docs.api.ai/docs/languages"""
        return self._lang

    @lang.setter
    def lang(self, lang):
        self._lang = lang

    @property
    def resetContexts(self):
        """resetContexts used for reset (cancel/disable) all previous all contexts.
        All contexts provided in current request will be setted after reset.
        Default equal False."""
        return self._resetContexts
    
    @resetContexts.setter
    def resetContexts(self, resetContexts):
        self._resetContexts = resetContexts

    @property
    def contexts(self):
        "Array of context objects. for detail information see https://docs.api.ai/v6/docs/concept-contexts"
        return self._contexts
    
    @contexts.setter
    def contexts(self, contexts):
        self._contexts = contexts

    @property
    def session_id(self):
        """session_id user for unique identifier of current application user.
        And it provide different contexts and entities for different users."""
        return self._session_id

    @session_id.setter
    def session_id(self, session_id):
        self._session_id = session_id

    @property
    def time_zone(self):
        """Time zone from IANA Time Zone Database (see http://www.iana.org/time-zones).
        Examples: `America/New_York`, `Europe/Paris`
        Time zone used for provide information about time and other parameters depended by time zone.
        Default equal `strftime("%z", gmtime())` -> used current system time zone."""
        return self._time_zone

    @time_zone.setter
    def time_zone(self, time_zone):
        self._time_zone = time_zone
    
    @property
    def entities(self):
        """Array of entities that replace developer defined entities for this request only. 
        The entity(ies) need to exist in the developer console."""
        return self._entities
    
    @entities.setter
    def entities(self, entities):
        self._entities = entities

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

    def __init__(self, client_access_token, subscribtion_key, url, __connection__class, version, session_id):
        super(Request, self).__init__()

        self.lang = 'en'
        self.resetContexts = False
        self.contexts = []
        self.entities = None

        self.version = version
        self.session_id = session_id

        self.__connection__class = __connection__class

        self.client_access_token = client_access_token
        self.subscribtion_key = subscribtion_key
        self.url = url

        self.time_zone = strftime("%z", gmtime())

        self._prepare_request()

    def _prepare_entities(self):
        if self.entities: 
            return list(map(lambda x: x._to_dict(), self.entities))
        return None

    def _prepare_request(self, debug=False):
        self._connection = self.__connection__class(self.url)

        if debug:
            self._connection.debuglevel = 1

    def _connect(self):
        self._connection.connect()

        path = '/v1/query'

        parameters = {
            'v': self.version
        }

        full_path = None

        try:
            full_path = path + '?' + urllib.urlencode(parameters)
        except AttributeError:
            full_path = path + '?' + urllib.parse.urlencode(parameters)

        self._connection.putrequest('POST', full_path, skip_accept_encoding=1)

        headers = {
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip, deflate',
            'Authorization': ('Bearer %s' % self.client_access_token),
            'ocp-apim-subscription-key': self.subscribtion_key,
        }

        headers.update(self._prepare_headers())

        for header_key, header_value in headers.items():
            self._connection.putheader(header_key, header_value)

        self._connection.endheaders()

        begin = self._prepage_begin_request_data()

        if not begin is None:
            self.send(begin.encode('utf-8'))

    def send(self, chunk):
        """Send a given data chunk of voice data."""

        if self._connection.sock is None:
            self._connect()

        self._connection.send(chunk)

    def _beforegetresponce(self):
        pass

    def getresponse(self):
        """Send all data and wait for response.
        """

        if self._connection.sock is None:
            self._connect()

        end = self._prepage_end_request_data()

        if not end is None:
            self.send(end.encode('utf-8'))

        self._beforegetresponce()

        return self._connection.getresponse()

    def _prepare_headers(self):
        raise NotImplementedError("Please Implement this method")

    def _prepage_begin_request_data(self):
        raise NotImplementedError("Please Implement this method")

    def _prepage_end_request_data(self):
        raise NotImplementedError("Please Implement this method")


class TextRequest(Request):
    """TextRequest request class

    Send simple text queries.
    Query can be string or array of strings.

    """

    @property
    def query(self):
        """Query parameter, can be string or array of strings.
        Default equal None, nut your should fill this field before send request."""
        return self._query

    @query.setter
    def query(self, query):
        self._query = query

    def __init__(self, client_access_token, subscribtion_key, url, __connection__class, version, session_id):
        super(TextRequest, self).__init__(client_access_token, subscribtion_key, url, __connection__class, version, session_id)

        self.query = None

    def _prepare_headers(self):
        return {
            'Content-Type': 'application/json; charset=utf-8',
            'Content-Length': len(self._prepage_end_request_data())
            } 

    def _prepage_begin_request_data(self):
        return None

    def _prepage_end_request_data(self):
        data = {
            'query': self.query,
            'lang': self.lang,
            'sessionId': self.session_id,
            'contexts': self.contexts,
            'timezone': self.time_zone,
            'resetContexts': self.resetContexts,
            'entities': self._prepare_entities(),
            }

        return json.dumps(data)


class VoiceRequest(Request):
    """VoiceRequest request class

    Send voice data by chunks.

    Basic Usage::

        >>> ...
        >>> voice_request = ai.text_request()
        >>> bytessize = 2048
        >>>
        >>> with open('log.raw', 'rb') as f:
        >>>     data = f.read(bytessize)
        >>>     while data:
        >>>         request.send(data)
        >>>         data = f.read(bytessize)
        >>>
        >>> request.getresponse()
        <JSON response>
    """

    def __init__(self, client_access_token, subscribtion_key, url, __connection__class, version, session_id):
        super(VoiceRequest, self).__init__(client_access_token, subscribtion_key, url, __connection__class, version, session_id)
        self.query = None

    def send(self, chunk):
        """Send a given data chunk of voice data."""

        parts = []

        parts.append('%x' % len(chunk))

        if PY3:
            parts.append(chunk.decode('latin-1'))
        else:
            parts.append(chunk)
            
        parts.append('')

        newChunk = '\r\n'.join(parts)

        super(VoiceRequest, self).send(b(newChunk))

    def _prepare_headers(self):
        self.boundary = ('--------{0}'.format(uuid.uuid4().hex)).encode('utf-8')

        return {
            'Content-Type': 'multipart/form-data; boundary=%s' % self.boundary,
            'Transfer-Encoding': 'chunked',
            'Connection': 'keep-alive',
            } 

    def _prepage_begin_request_data(self):
        data = '--%s\r\n' % self.boundary
        data += 'Content-Disposition: form-data; name="request"\r\n'
        data += "Content-Type: application/json\r\n\r\n"


        data += json.dumps(
                {
                'lang': self.lang or 'en',
                'sessionId': self.session_id,
                'contexts': self.contexts,
                'timezone': self.time_zone,
                'resetContexts': self.resetContexts,
                'entities': self._prepare_entities()
                }
            )

        data += '\r\n'

        data += '--%s\r\n' % self.boundary
        data += 'Content-Disposition: form-data; name="voiceData"\r\n'
        data += "Content-Type: audio/wav\r\n\r\n"

        return data

    def _prepage_end_request_data(self):
        return "\r\n--%s--\r\n" % self.boundary

    def _beforegetresponce(self):
        self._connection.send(b('0\r\n\r\n'))
        