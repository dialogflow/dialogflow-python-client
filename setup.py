#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

import apiai

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
  # os.system('python setup.py sdist upload')
  os.system('python setup.py sdist bdist_wheel upload')
  sys.exit()

packages = [
    'apiai',
    'apiai.requests',
    'apiai.requests.query',
    'apiai.requests.user_entities'  
]

requires = [
    'numpy'
]

with open('README.rst', 'r') as f:
  readme = f.read()

with open('HISTORY.rst', 'r') as f:
  history = f.read()

setup(name='apiai',
      version=apiai.__version__,
      description='The API.AI iOS SDK makes it easy to integrate speech recognition with API.AI natural language processing API on iOS devices.',
      long_description=readme + '\n\n' + history,
      author='Dmitriy Kuragin',
      author_email='kuragin@speaktoit.com',
      license='Apache 2.0',
      url='https://api.ai/',
      packages=packages,
      install_requires=requires,
      package_data={'':['LICENSE']},
      classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4'
      ),
)