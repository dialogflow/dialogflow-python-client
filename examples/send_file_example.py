#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))


import apiai
import time
import scipy.io.wavfile as wav

from codecs import open

CLIENT_ACCESS_TOKEN = '417a7fbdda844ac1ae922d10d4c4e4be'
SUBSCRIBTION_KEY = '6123ebe7185a4d9e94e441b7959cf2bc' 

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