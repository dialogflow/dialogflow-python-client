# -*- coding: utf-8 -*-

import urllib

try:  # Python 3
    from http.client import HTTPSConnection
except ImportError:
    from httplib import HTTPSConnection

try:
    import urllib.parse
except ImportError:
    import urllib


class Request(object):
    """Abstract request class
    Contain share information for all requests."""

    __connection__class = HTTPSConnection

    @property
    def client_access_token(self):
        """client access token provided by http://api.ai/"""
        return self._client_access_token

    @client_access_token.setter
    def client_access_token(self, client_access_token):
        self._client_access_token = client_access_token

    def __init__(self,
                 client_access_token,
                 base_url,
                 path,
                 query_parameters=[]
                 ):
        super(Request, self).__init__()

        self.base_url = base_url
        self.path = path
        self.query_parameters = query_parameters

        self.client_access_token = client_access_token

        self._prepare_request()

    def _prepare_entities(self):
        if self.entities:
            return list(map(lambda x: x._to_dict(), self.entities))
        return None

    def _prepare_request(self, debug=False):
        self._connection = self.__connection__class(self.base_url)

    def _connect(self):
        self._connection.connect()

        query = None

        try:
            query = urllib.urlencode(self.query_parameters)
        except AttributeError:
            query = urllib.parse.urlencode(self.query_parameters)

        full_path = self.path + '?' + query

        self._connection.putrequest('POST', full_path, skip_accept_encoding=1)

        headers = {
            'Accept': 'application/json',
            'Authorization': ('Bearer %s' % self.client_access_token)
        }

        headers.update(self._prepare_headers())

        for header_key, header_value in headers.items():
            self._connection.putheader(header_key, header_value)

        self._connection.endheaders()

        begin = self._prepage_begin_request_data()

        if begin is not None:
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

        if end is not None:
            self.send(end.encode('utf-8'))

        self._beforegetresponce()

        return self._connection.getresponse()

    def _prepare_headers(self):
        raise NotImplementedError("Please Implement this method")

    def _prepage_begin_request_data(self):
        raise NotImplementedError("Please Implement this method")

    def _prepage_end_request_data(self):
        raise NotImplementedError("Please Implement this method")
