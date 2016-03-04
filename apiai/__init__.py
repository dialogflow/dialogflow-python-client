# -*- coding: utf-8 -*-

"""
apiai
~~~~~~~~~~~~~~~~
This module provides a ApiAI classes to manage requests.
"""

__author__ = "Dmitriy Kuragin"
__copyright__ = "Copyright 2016 api.ai"
__contributors__ = []
__license__ = "Apache 2.0"
__version__ = "0.0.9"

__all__ = [
            'apiai', 
            'ApiAI', 
            'Request', 
            'QueryRequest', 
            'TextRequest', 
            'VoiceRequest', 
            'VAD', 
            'Resampler', 
            'Entry', 
            'Entity'
            ]

from .requests.query.query import Entry
from .requests.query.query import Entity

from .requests  import Request
from .requests  import QueryRequest

from .apiai     import ApiAI
from .apiai     import TextRequest
from .apiai     import VoiceRequest
# from .apiai     import Entry
# from .apiai     import Entity

from .VAD       import VAD
from .resampler import Resampler
