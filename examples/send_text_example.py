#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path, sys

try:
    import apiai
except ImportError:
    sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
    import apiai

import time
import scipy.io.wavfile as wav

CLIENT_ACCESS_TOKEN = 'YOUR_ACCESS_TOKEN'
SUBSCRIBTION_KEY = 'YOUR_SUBSCRIPTION_KEY' 

def main():
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN, SUBSCRIBTION_KEY)

    request = ai.text_request()

    request.query = "Hello"

    response = request.getresponse()

    print (response.read())

if __name__ == '__main__':
    main()
