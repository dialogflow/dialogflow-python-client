# -*- coding: utf-8 -*-

from ..request import Request

from ..query import Entity
from ..query import Entry

import json


class UserEntity(Entity):
    """UserEntity object used for upload user entities.
    Detail information about user entities you can see at our site
    https://docs.api.ai/docs/userentities"""

    @property
    def session_id(self):
        """session_id parameter used for determinate of every unique users."""
        return self._session_id

    @session_id.setter
    def session_id(self, session_id):
        self._session_id = session_id

    @property
    def extend(self):
        return self._extend

    @extend.setter
    def extend(self, extend):
        """extend parameter used definition user entities logic. If True then
        uploaded user entities will be mixed with user entities specified in
        server side else currently uploaded entities witll uverride
        server entities."""
        self._extend = extend

    def __init__(self, name, entries, session_id=None, extend=False):
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
    """UserEntityEntry object used for upload user entities.
    Detail information about user entities you can see at our site
    https://docs.api.ai/docs/userentities"""

    pass


class UserEntitiesRequest(Request):
    """UserEntitiesRequest is request for upload user entities.
    Detail see http://docs.api.ai/"""

    @property
    def user_entities(self):
        "user_entities parameter for specification of same user entities."
        return self._user_entities

    @user_entities.setter
    def user_entities(self, user_entities):
        self._user_entities = user_entities

    def __init__(self, client_access_token, base_url, user_entities=[]):
        super(UserEntitiesRequest, self).__init__(client_access_token,
                                                  base_url,
                                                  '/v1/userEntities',
                                                  {})

        self._user_entities = user_entities

    def _prepare_headers(self):
        return {
            'Content-Type': 'application/json; charset=utf-8',
            'Content-Length': len(self._prepage_end_request_data())
        }

    def _prepage_begin_request_data(self):
        return None

    def _prepage_end_request_data(self):
        return json.dumps(list(map(lambda x: x._to_dict(), self._user_entities)))
