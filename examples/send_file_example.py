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

from codecs import open

CLIENT_ACCESS_TOKEN = '03cbf8fe4ebc4b928f99d6ba111f0976'


def main():
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

    request = ai.voice_request()

    request.audio_mime_type = 'audio/mp4'

    request.lang = 'en'  # optional, default value equal 'en'

    bytessize = 2048

    # with open('log.raw', 'rb') as f:
    with open('how_are_you.mp4', 'rb') as f:
        data = f.read(bytessize)
        while data:
            request.send(data)
            data = f.read(bytessize)

    response = request.getresponse()

    print (response.read())

if __name__ == '__main__':
    main()
