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

import os.path
import sys

try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai

import uuid

CLIENT_ACCESS_TOKEN = 'YOUR_ACCESS_TOKEN'


def main():
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

    # some unuque session id for user identification
    session_id = uuid.uuid4().hex

    entries = [
        apiai.UserEntityEntry('Firefox', ['Firefox']),
        apiai.UserEntityEntry('XCode', ['XCode']),
        apiai.UserEntityEntry('Sublime Text', ['Sublime Text'])
    ]

    user_entities_request = ai.user_entities_request(
        [
            apiai.UserEntity("Application", entries, session_id)
        ]
    )

    user_entities_response = user_entities_request.getresponse()

    print 'Upload user entities response: ', (user_entities_response.read())

    request = ai.text_request()

    request.session_id = session_id
    request.query = "Open application Firefox"

    response = request.getresponse()

    print 'Query response: ', (response.read())


if __name__ == '__main__':
    main()
