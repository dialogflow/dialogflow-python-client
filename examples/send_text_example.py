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

# CLIENT_ACCESS_TOKEN = 'YOUR_ACCESS_TOKEN'
CLIENT_ACCESS_TOKEN = '138c6f0337a34cfa8022c9aa29ade48a'


def main():
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

    request = ai.text_request()

    request.lang = 'de'  # optional, default value equal 'en'

    # request.session_id = "<SESSION ID, UNIQUE FOR EACH USER>"

    request.query = "Hello"

    response = request.getresponse()

    print (response.read())


if __name__ == '__main__':
    main()
