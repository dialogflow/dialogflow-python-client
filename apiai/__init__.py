"""
apiai
~~~~~~~~~~~~~~~~
This module provides a ApiAI classes to manage requests.
"""

__author__ = "Dmitriy Kuragin"
__copyright__ = "Copyright 2015 api.ai"
__contributors__ = []
__license__ = "Apache 2.0"
__version__ = "0.0.6"

__all__ = ['apiai', 'ApiAI', 'Request', 'TextRequest', 'VoiceRequest', 'VAD', 'Resampler', 'Entry', 'Entity']

from .apiai import ApiAI, Request, TextRequest, VoiceRequest, Entry, Entity
from .VAD import VAD
from .resampler import Resampler
