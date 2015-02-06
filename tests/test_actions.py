# -*- coding: utf-8 -*-

import unittest
import sys
import os
import json

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import apiai

CLIENT_ACCESS_TOKEN = '09604c7f91ce4cd8a4ede55eb5340b9d'
SUBSCRIBTION_KEY = '4c91a8e5-275f-4bf0-8f94-befa78ef92cd'

class TestActions(unittest.TestCase):
    def setUp(self):
        self.ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN, SUBSCRIBTION_KEY)

    def load_text_request_with_quiery(self, query=None, resetContexts=False):
        if not query:
            self.assertTrue(False)

        text_requset = self.ai.text_request()
        text_requset.query = query

        text_requset.resetContexts = resetContexts

        response = text_requset.getresponse()
        return json.loads(response.read())

    def test_hello(self):
        query = 'Hello'

        response = self.load_text_request_with_quiery(query)

        result = response['result']

        self.assertEqual(result['resolvedQuery'].lower(), query.lower())

        self.assertEqual(result['action'], 'greeting')
        self.assertEqual(result['speech'], 'Hi! How are you?')

    def test_you_name(self):
        query = 'What is your name?'

        response = self.load_text_request_with_quiery(query)

        result = response['result']

        self.assertEqual(result['resolvedQuery'].lower(), query.lower())
        self.assertEqual(result['action'], 'name')
        self.assertTrue(len(result['contexts']) == 1)

        context = result['contexts'][0]

        self.assertEqual(context['name'], 'name_question')
        self.assertTrue(len(context['parameters']) == 1)

        parameters = context['parameters']
        param = parameters.get('param', None)

        self.assertTrue(param)
        self.assertEqual(parameters['param'], 'blabla')

        hello_with_context = self.load_text_request_with_quiery('hello', resetContexts=False)

        self.assertTrue(len(hello_with_context['result']['contexts']) == 1)
        self.assertEqual(hello_with_context['result']['contexts'][0]['name'], 'name_question')

        hello_without_context = self.load_text_request_with_quiery('hello', resetContexts=True)

        self.assertTrue(len(hello_without_context['result']['contexts']) == 0)

if __name__ == '__main__':
    unittest.main()