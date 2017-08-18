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

"""
    Setup script for using and create package for pip.
"""

import sys
import os

# import apiai

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    # os.system('python setup.py sdist upload')
    os.system('python setup.py sdist bdist_wheel upload')
    sys.exit()

PACKAGES = [
    'apiai',
    'apiai.requests',
    'apiai.requests.query',
    'apiai.requests.user_entities'
]

REQUIRES = [
    'numpy'
]

EXTRAS_REQUIRE = {
    'numpy': ['numpy']
}

with open('README.rst', 'r') as f:
    README = f.read()

with open('HISTORY.rst', 'r') as f:
    HISTORY = f.read()

setup(
    name='apiai',
    version='1.2.3',
    description=(
        'The API.AI iOS SDK makes it easy to integrate speech '
        'recognition with API.AI natural language processing '
        'API on iOS devices.'
    ),
    long_description=README + '\n\n' + HISTORY,
    author='Dmitriy Kuragin',
    author_email='kuragin@speaktoit.com',
    license='Apache 2.0',
    url='https://api.ai/',
    packages=PACKAGES,
    install_requires=REQUIRES,
    # extras_require=EXTRAS_REQUIRE,
    package_data={'': ['LICENSE']},
    classifiers=(
        # 'Development Status :: 5 - Production/Stable',
        # 'Intended Audience :: Developers',
        # 'Natural Language :: English',
        # 'License :: OSI Approved :: Apache Software License',
        # 'Programming Language :: Python',
        # 'Programming Language :: Python :: 2.7',
        # 'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.3',
        # 'Programming Language :: Python :: 3.4'
    ),
)
