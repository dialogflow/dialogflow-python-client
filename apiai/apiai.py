#!/usr/bin/env python
# -*- coding: utf-8 -*-

try: # Python 3
    from http.client import HTTPConnection, HTTPSConnection
except ImportError:
    from httplib import HTTPConnection, HTTPSConnection

import sys
import json
import uuid

PY3 = sys.version_info[0] == 3

if PY3:
    def b(s):
        return s.encode("latin-1")
else:
    def b(s):
        return s

class ApiAI(object):
    """docstring for ApiAI"""

    __connection__class = HTTPSConnection

    def __init__(self, client_access_token, subscribtion_key):
        super(ApiAI, self).__init__()
        self.client_access_token = client_access_token
        self.subscribtion_key = subscribtion_key

        self.url = 'api.api.ai'

    def voice_request(self):
        return VoiceRequest(self.client_access_token, self.subscribtion_key, self.url, self.__connection__class)

    def text_request(self):
        return TextRequest(self.client_access_token, self.subscribtion_key, self.url, self.__connection__class)


class Request(object):
    """docstring for Request"""

    __connection__class = None

    lang = 'en'
    resetContexts = False
    contexts = []
    sessionId = None

    def __init__(self, client_access_token, subscribtion_key, url, __connection__class):
        super(Request, self).__init__()

        self.__connection__class = __connection__class

        self.client_access_token = client_access_token
        self.subscribtion_key = subscribtion_key
        self.url = url

        self._prepare_request()

    def _prepare_request(self):
        self._connection = self.__connection__class(self.url)

        self._connection.debuglevel = 999

    def connect(self):
        self._connection.connect()

        self._connection.putrequest('POST', '/v1/query', skip_accept_encoding=1)

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
        if self._connection.sock is None:
            self.connect()

        self._connection.send(chunk)

    def beforegetresponce(self):
        pass

    def getresponse(self):
        if self._connection.sock is None:
            self.connect()

        end = self._prepage_end_request_data()

        if not end is None:
            self.send(end.encode('utf-8'))

        self.beforegetresponce()

        return self._connection.getresponse()

    def _prepare_headers(self):
        raise NotImplementedError("Please Implement this method")

    def _prepage_begin_request_data(self):
        raise NotImplementedError("Please Implement this method")

    def _prepage_end_request_data(self):
        raise NotImplementedError("Please Implement this method")


class TextRequest(Request):
    """docstring for TextRequest"""
    def __init__(self, client_access_token, subscribtion_key, url, __connection__class):
        super(TextRequest, self).__init__(client_access_token, subscribtion_key, url, __connection__class)
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
            }

        return json.dumps(data)


class VoiceRequest(Request):
    """docstring for VoiceRequest"""
    def __init__(self, client_access_token, subscribtion_key, url, __connection__class):
        super(VoiceRequest, self).__init__(client_access_token, subscribtion_key, url, __connection__class)
        self.query = None

    def send(self, chunk):
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
            'Expect': '100-continue'
            } 

    def _prepage_begin_request_data(self):
        data = '--%s\r\n' % self.boundary
        data += 'Content-Disposition: form-data; name="request"\r\n'
        data += "Content-Type: application/json\r\n\r\n"


        data += json.dumps(
                {
                'lang': self.lang or 'en',
                'sessionId': 'ce37f7dddb021aa51f856f1f8c548af7'
                }
            )

        data += '\r\n'

        data += '--%s\r\n' % self.boundary
        data += 'Content-Disposition: form-data; name="voiceData"\r\n'
        data += "Content-Type: audio/wav\r\n\r\n"

        return data

    def _prepage_end_request_data(self):
        return "\r\n--%s--\r\n" % self.boundary

    def beforegetresponce(self):
        self._connection.send(b('0\r\n\r\n'))
        