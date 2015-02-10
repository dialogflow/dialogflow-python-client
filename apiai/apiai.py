# -*- coding: utf-8 -*-

"""
apiai
~~~~~~~~~~~~~~~~
This module provides a ApiAI class to manage requests.
"""

try: # Python 3
    from http.client import HTTPConnection, HTTPSConnection
except ImportError:
    from httplib import HTTPConnection, HTTPSConnection

import sys
import json
import uuid

try:
    import urllib.parse
except ImportError:
    import urllib

DEFAULT_VERSION = '20150204'

PY3 = sys.version_info[0] == 3

if PY3:
    def b(s):
        return s.encode("latin-1")
else:
    def b(s):
        return s

class ApiAI(object):
    """Main andpoint for using API

    Provides request.

    Basic Usage::

        >>> import apiai
        >>> ai = apiai.ApiAI(<CLIENT_ACCESS_TOKEN>, <SUBSCRIBTION_KEY>)
        >>> text_request = ai.text_request()
        >>> ...
    """

    __connection__class = HTTPSConnection

    def __init__(self, client_access_token, subscribtion_key, version=DEFAULT_VERSION):
        """Construct a :class:`ApiAI <ApiAI>`

        :param client_access_token: client access token provided by http://api.ai/
        :param subscribtion_key: subscribtion key provided by http://api.ai/
        """

        super(ApiAI, self).__init__()
        self.client_access_token = client_access_token
        self.subscribtion_key = subscribtion_key

        self.url = 'api.api.ai'
        self.version = version

        self.session_id = uuid.uuid4().hex

    def voice_request(self):
        """Construct a :class:`VoiceRequest <VoiceRequest>`, prepare it.
        Returns :class:`VoiceRequest <VoiceRequest>` object.
        """

        request = VoiceRequest(self.client_access_token, self.subscribtion_key, self.url, self.__connection__class, self.version, self.session_id)

        return request

    def text_request(self):
        """Construct a :class:`VoiceRequest <TextRequest>`, prepare it.
        Returns :class:`TextRequest <TextRequest>` object.
        """

        request = TextRequest(self.client_access_token, self.subscribtion_key, self.url, self.__connection__class, self.version, self.session_id)

        return request

class Request(object):
    """Abstract request class"""

    __attrs__ = [
        'lang',
        'resetContexts',
        'contexts',
        'sessionId',
    ]

    __connection__class = None

    lang = 'en'
    resetContexts = False
    contexts = []
    sessionId = None

    def __init__(self, client_access_token, subscribtion_key, url, __connection__class, version, session_id):
        super(Request, self).__init__()

        self.version = version
        self.session_id = session_id

        self.__connection__class = __connection__class

        self.client_access_token = client_access_token
        self.subscribtion_key = subscribtion_key
        self.url = url

        self._prepare_request()

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
        """Send a givet data chunk.
        :param chunk: data chunk.
        """

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

    Send simple text reques.
    Query can be string or array of strings.

    """

    __attrs__ = [
        'query',
    ]

    def __init__(self, client_access_token, subscribtion_key, url, __connection__class, version, session_id):
        super(TextRequest, self).__init__(client_access_token, subscribtion_key, url, __connection__class, version, session_id)

        #: Query parameter, can be string or array of strings.
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
            'resetContexts': self.resetContexts
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
        """Send a givet data chunk.
        :param chunk: data chunk.
        """

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
                'resetContexts': self.resetContexts,
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
        