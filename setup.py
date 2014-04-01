########
# Copyright (c) 2014 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
#    * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    * See the License for the specific language governing permissions and
#    * limitations under the License.

from __future__ import print_function
from setuptools import setup
import io

version = '0.1.0'


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read('README.txt')

setup(
    name='cloudify-packager',
    version=version,
    url='https://github.com/CloudifySource/cosmo-packager',
    author='nir0s',
    author_email='nirc@gigaspaces.com',
    packages=['cosmo-packager'],
    license='LICENSE',
    platforms='Ubuntu',
    description='Cloudify3 Package Generator',
    package_data={'cosmo_cli': ['cosmo-config.example.json']},
    install_requires=[
        "fabric",
        "pika",
        "jinja2",
    ],
)
