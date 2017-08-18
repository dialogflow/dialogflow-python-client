# -*- coding:utf8 -*-
# !/usr/bin/env python
# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
