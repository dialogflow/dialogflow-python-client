# -*- coding: utf-8 -*-

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
