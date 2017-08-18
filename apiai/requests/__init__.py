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
