# -*- coding: utf-8 -*-

from ..request import Request

from ..query import Entity
from ..query import Entry

import json

class UserEntity(Entity):
    """docstring for UserEntity"""

    @property
    def session_id(self):
        return self._session_id

    @session_id.setter
    def session_id(self, session_id):
        self._session_id = session_id

    @property
    def extend(self):
        return self._extend

    @extend.setter
    def extend(self, extend):
        self._extend = extend

    def __init__(self, name, entries, session_id = None, extend = False):
        super(UserEntity, self).__init__(name, entries)

        self._session_id = session_id
        self._extend = extend

    """Private method used for object serialization."""
    def _to_dict(self):
        parent_data = super(UserEntity, self)._to_dict()
        if self._session_id is not None:
            parent_data['sessionId'] = self._session_id

        parent_data['extend'] = self._extend

        return parent_data


class UserEntityEntry(Entry):
    """docstring for Entry"""
    pass


class UserEntitiesRequest(Request):
    """docstring for UserEntitiesRequest"""

    @property
    def user_entities(self):
        return self._user_entities

    @user_entities.setter
    def user_entities(self, user_entities):
        self._user_entities = user_entities

    def __init__(self, client_access_token, subscribtion_key, base_url, user_entities = []):
        super(UserEntitiesRequest, self).__init__(client_access_token, subscribtion_key, base_url, '/v1/userEntities', {})

        self._user_entities = user_entities

    def _prepare_headers(self):
        return {
            'Content-Type': 'application/json; charset=utf-8',
            'Content-Length': len(self._prepage_end_request_data())
            } 

    def _prepage_begin_request_data(self):
        return None

    def _prepage_end_request_data(self):
        return json.dumps(map(lambda x: x._to_dict(), self._user_entities))