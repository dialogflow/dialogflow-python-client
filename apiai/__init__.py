# -*- coding:utf8 -*-
# !/usr/bin/env python
# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
