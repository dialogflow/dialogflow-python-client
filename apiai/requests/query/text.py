# -*- coding: utf-8 -*-

from . import QueryRequest

import json


class TextRequest(QueryRequest):
    """
        TextRequest request class

        Send simple text queries.
        Query can be string or array of strings.
    """

    @property
    def query(self):
        """
            Query parameter, can be string or array of strings.
            Default equal None, nut your should fill this field before send
            request.

            :rtype: str or unicode
        """

        return self._query

    @query.setter
    def query(self, query):
        self._query = query

    def __init__(self, client_access_token, base_url, version, session_id):
        super(TextRequest, self).__init__(client_access_token,
                                          base_url,
                                          version,
                                          session_id)

        self.query = None

    def _prepare_headers(self):
        return {
            'Content-Type': 'application/json; charset=utf-8',
            'Content-Length': len(self._prepage_end_request_data()),
            'devMode': 'true'
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
