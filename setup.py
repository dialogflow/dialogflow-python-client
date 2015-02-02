#!/usr/bin/env python
# -*- coding: utf-8 -*-

import apiai

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

packages = [
    'apiai',        
]

requires = [
    'numpy',
    'scipy',
]

with open('README.rst', 'r') as f:
  readme = f.read()

setup(name='apiai',
      version='1.0',
      description='The API.AI iOS SDK makes it easy to integrate speech recognition with API.AI natural language processing API on iOS devices.',
      long_description=readme,
      author='Dmitriy Kuragin',
      author_email='kuragin@speaktoit.com',
      license='Apache 2.0',
      url='https://api.ai/',
      packages=packages,
      install_requires=requires,
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