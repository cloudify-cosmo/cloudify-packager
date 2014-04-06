
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
from setuptools import setup, find_packages
import re
import os
import codecs

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    # intentionally *not* adding an encoding option to open
    return codecs.open(os.path.join(here, *parts), 'r').read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

setup(
    name='packman',
    version=find_version('packman', '__init__.py'),
    url='https://github.com/cloudify-cosmo/cloudify-packager',
    author='nir0s',
    author_email='nirc@gigaspaces.com',
    # packages=['cosmo-packager'],
    license='LICENSE',
    platforms='Ubuntu',
    description='Gigaspaces Package Generator',
    # package_data={'cosmo_cli': ['cosmo-config.example.json']},
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "fabric==1.8.3",
        "pika==0.9.13",
        "jinja2==2.7.2",
    ],
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'Environment :: Shell Environment',
        'Intended Audience :: System Admins',
        'License :: Apache Software License',
        'Operating System :: Ubuntu/Debian',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System Administration :: Utility :: Package Creation',
    ],
)
