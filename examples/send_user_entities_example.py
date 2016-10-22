#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

    print 'Uplaod user entities response: ', (user_entities_response.read())

    request = ai.text_request()

    request.session_id = session_id
    request.query = "Open application Firefox"

    response = request.getresponse()

    print 'Query response: ', (response.read())


if __name__ == '__main__':
    main()
