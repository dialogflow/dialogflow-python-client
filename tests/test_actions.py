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

import unittest
import sys
import os
import json

try:
    import apiai
except ImportError:
    sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
    import apiai

CLIENT_ACCESS_TOKEN = '09604c7f91ce4cd8a4ede55eb5340b9d'


class TestActions(unittest.TestCase):
    def setUp(self):
        self.ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

    def load_text_request_with_quiery(self, query=None, resetContexts=False, entities=None):
        if not query:
            self.assertTrue(False)

        text_requset = self.ai.text_request()
        text_requset.query = query

        text_requset.resetContexts = resetContexts

        text_requset.entities = entities

        response = text_requset.getresponse()
        return json.loads(response.read().decode())

    def test_hello(self):
        query = 'Hello'

        response = self.load_text_request_with_quiery(query)

        result = response['result']

        self.assertEqual(result['resolvedQuery'].lower(), query.lower())

        self.assertEqual(result['action'], 'greeting')
        self.assertEqual(result['fulfillment']['speech'], 'Hi! How are you?')

    def test_you_name(self):
        query = 'What is your name?'

        response = self.load_text_request_with_quiery(query)

        result = response['result']

        self.assertEqual(result['resolvedQuery'].lower(), query.lower())
        self.assertEqual(result['action'], 'name')
        self.assertTrue(len(result['contexts']) == 1)

        context = result['contexts'][0]

        self.assertEqual(context['name'], 'name_question')
        self.assertTrue(len(context['parameters']) == 4)

        parameters = context['parameters']
        param = parameters.get('param', None)

        self.assertTrue(param)
        self.assertEqual(parameters['param'], 'blabla')

        hello_with_context = self.load_text_request_with_quiery('hello', resetContexts=False)

        self.assertTrue(len(hello_with_context['result']['contexts']) == 1)
        self.assertEqual(hello_with_context['result']['contexts'][0]['name'], 'name_question')

        hello_without_context = self.load_text_request_with_quiery('hello', resetContexts=True)

        self.assertTrue(len(hello_without_context['result']['contexts']) == 0)

    def test_user_entities(self):
        query = 'hi nori'

        entities = [
            apiai.Entity(
                'dwarfs',
                [
                    apiai.Entry('Ori', ['ori', 'Nori']),
                    apiai.Entry('bifur', ['Bofur', 'Bombur']),
                ]
            )
        ]

        response = self.load_text_request_with_quiery(query, entities=entities)
        self.assertTrue(response['result']['metadata']['intentName'] == 'hi dwarf')
        self.assertTrue(response['result']['fulfillment']['speech'] == 'hi Bilbo, I am Ori')


if __name__ == '__main__':
    unittest.main()
