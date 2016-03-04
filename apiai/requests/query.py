# -*- coding: utf-8 -*-

from request import Request

from time import gmtime
from time import strftime

class QueryRequest(Request):
    """Abstract request class
    Contain share information for all query requests."""

    @property
    def lang(self):
        """lang property used for server determination current request language. 
        In `VoiceRequest` used for determinate language for ASR (Speech Recognitions) service.
        Default equal 'en'. For detail information about support language see https://docs.api.ai/docs/languages"""
        return self._lang

    @lang.setter
    def lang(self, lang):
        self._lang = lang

    @property
    def resetContexts(self):
        """resetContexts used for reset (cancel/disable) all previous all contexts.
        All contexts provided in current request will be setted after reset.
        Default equal False."""
        return self._resetContexts
    
    @resetContexts.setter
    def resetContexts(self, resetContexts):
        self._resetContexts = resetContexts

    @property
    def contexts(self):
        "Array of context objects. for detail information see https://docs.api.ai/v6/docs/concept-contexts"
        return self._contexts
    
    @contexts.setter
    def contexts(self, contexts):
        self._contexts = contexts

    @property
    def session_id(self):
        """session_id user for unique identifier of current application user.
        And it provide different contexts and entities for different users."""
        return self._session_id

    @session_id.setter
    def session_id(self, session_id):
        self._session_id = session_id

    @property
    def time_zone(self):
        """Time zone from IANA Time Zone Database (see http://www.iana.org/time-zones).
        Examples: `America/New_York`, `Europe/Paris`
        Time zone used for provide information about time and other parameters depended by time zone.
        Default equal `strftime("%z", gmtime())` -> used current system time zone."""
        return self._time_zone

    @time_zone.setter
    def time_zone(self, time_zone):
        self._time_zone = time_zone
    
    @property
    def entities(self):
        """Array of entities that replace developer defined entities for this request only. 
        The entity(ies) need to exist in the developer console."""
        return self._entities
    
    @entities.setter
    def entities(self, entities):
        self._entities = entities

    def __init__(self, client_access_token, subscribtion_key, base_url, version, session_id):
        super(QueryRequest, self).__init__(client_access_token, subscribtion_key, base_url, '/v1/query', {'v': version})

        self.lang = 'en'
        self.resetContexts = False
        self.contexts = []
        self.entities = None

        self.version = version
        self.session_id = session_id

        self.time_zone = strftime("%z", gmtime())

    def _prepare_entities(self):
        if self.entities: 
            return list(map(lambda x: x._to_dict(), self.entities))
        return None

    def _prepare_headers(self):
        raise NotImplementedError("Please Implement this method")

    def _prepage_begin_request_data(self):
        raise NotImplementedError("Please Implement this method")

    def _prepage_end_request_data(self):
        raise NotImplementedError("Please Implement this method")