# -*- coding: utf-8 -*-

import sys

try:
    import simplejson as json
except ImportError:
    import json

PY3 = sys.version_info[0] == 3


class Response(object):
    """
    Response from api.ai

    :type original_response: http.client.HTTPResponse or \
        http.client.HTTPSResponse or httplib.HTTPResponse or \
        httplib.HTTPSResponse
    """

    def __init__(self, original_response):
        super(Response, self).__init__()

        self._original_response = original_response
        self._status_code = original_response.status

        self._headers = dict(original_response.getheaders())

        _body = original_response.read()
        if PY3:
            _body = _body.decode('unicode-escape')

        self._body = _body

        self._json = None

    @property
    def original_response(self):
        """
        :rtype: original_response: http.client.HTTPResponse or \
            http.client.HTTPSResponse or httplib.HTTPResponse or \
            httplib.HTTPSResponse
        """
        return self._original_response

    @property
    def status_code(self):
        """
        :rtype: Int
        """
        return self._status_code

    @property
    def headers(self):
        """
        :rtype: dict
        """
        return self._headers

    @property
    def body(self):
        """
        :rtype: str or unicode
        """
        return self._body

    @property
    def json(self):
        """
        :rtype: dict or list
        """
        if self._json is None:
            self._json = json.loads(self.body)
        return self._json
