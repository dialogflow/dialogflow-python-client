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


class Event(object):
    """
        Event model for EventRequest.
    """

    def __init__(self, name):
        super(Event, self).__init__()

        self._name = name
        self._data = None

    @property
    def name(self):
        """
            :rtype: str or unicode
        """
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def data(self):
        """
            :rtype: dict
        """
        return self._data

    @data.setter
    def data(self, data):
        self._data = data


class EventRequest(QueryRequest):
    """
        EventRequest request class

        Send simple event queries.
    """

    def __init__(self, client_access_token, base_url, version, session_id):
        super(EventRequest, self).__init__(
            client_access_token,
            base_url,
            version,
            session_id
        )

        self._event = None

    @property
    def event(self):
        """
            :rtype: Event
        """
        return self._event

    @event.setter
    def event(self, event):
        self._event = event

    def _prepare_headers(self):
        return {
            'Content-Type': 'application/json; charset=utf-8',
            'Content-Length': len(self._prepage_end_request_data()),
            'devMode': 'true'
        }

    def _prepage_begin_request_data(self):
        return None

    def _prepage_end_request_data(self):
        event = {
            'name': self._event.name
        }

        if self._event.data:
            event['data'] = self._event.data

        data = {
            'event': event,
            'lang': self.lang,
            'sessionId': self.session_id,
            'contexts': self.contexts,
            'timezone': self.time_zone,
            'resetContexts': self.resetContexts,
            'entities': self._prepare_entities(),
        }

        return json.dumps(data)
