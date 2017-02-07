# -*- coding: utf-8 -*-

"""
apiai
~~~~~~~~~~~~~~~~
This module provides a ApiAI classes to manage requests.
"""

from .requests.query import Entry
from .requests.query import Entity

from .requests import Request
from .requests import QueryRequest
from .requests import events

from .apiai import ApiAI
from .apiai import TextRequest
from .apiai import VoiceRequest
from .apiai import UserEntitiesRequest

from .requests.user_entities import UserEntity
from .requests.user_entities import UserEntityEntry

from .VAD import VAD
from .resampler import Resampler

__author__ = "Dmitriy Kuragin"
__copyright__ = "Copyright 2016 api.ai"
__contributors__ = []
__license__ = "Apache 2.0"
__version__ = "1.2.3"

__all__ = [
    'apiai',
    'ApiAI',
    'Request',
    'Entry',
    'Entity',
    'QueryRequest',
    'TextRequest',
    'VoiceRequest',
    'UserEntitiesRequest',
    'UserEntity',
    'UserEntityEntry',
    'VAD',
    'Resampler',
    'events'
]
