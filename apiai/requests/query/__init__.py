# -*- coding: utf-8 -*-

from .query import QueryRequest
from .text import TextRequest
from .voice import VoiceRequest

from .query import Entry
from .query import Entity

from . import events

"""
apiai
~~~~~~~~~~~~~~~~
This module provides a ApiAI classes to manage requests.
"""

__all__ = [
    'QueryRequest',
    'TextRequest',
    'VoiceRequest',
    'Entry',
    'Entity',
    'events'
]
