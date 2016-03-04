# -*- coding: utf-8 -*-

"""
apiai
~~~~~~~~~~~~~~~~
This module provides a ApiAI classes to manage requests.
"""

__all__ = [
            'QueryRequest', 
            'TextRequest', 
            'VoiceRequest'
            ]

from .query import QueryRequest
from .text import TextRequest
from .voice import VoiceRequest