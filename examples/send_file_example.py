#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path, sys

try:
    import apiai
except ImportError:
    sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
    import apiai


import apiai
import time
import scipy.io.wavfile as wav

from codecs import open

CLIENT_ACCESS_TOKEN = 'YOUR_ACCESS_TOKEN'
SUBSCRIBTION_KEY = 'YOUR_SUBSCRIPTION_KEY' 

def main():
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN, SUBSCRIBTION_KEY)

    request = ai.voice_request()

    bytessize = 2048

    with open('log.raw', 'rb') as f:
        data = f.read(bytessize)
        while data:
            request.send(data)
            data = f.read(bytessize)

    response = request.getresponse()

    print (response.read())

if __name__ == '__main__':
    main()
