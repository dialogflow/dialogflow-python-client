# -*- coding: utf-8 -*-

from .request import Request
from .query import QueryRequest
from .query import TextRequest
from .query import VoiceRequest
from .query import events

from .user_entities import UserEntitiesRequest

"""
apiai
~~~~~~~~~~~~~~~~
This module provides a ApiAI classes to manage requests.
"""

__all__ = [
    'Request',
    'QueryRequest',
    'TextRequest',
    'VoiceRequest',
    'UserEntitiesRequest',
    'EventRequest',
    'Event',
    'events'
]
