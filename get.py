#!/usr/bin/env python
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

from packman import logger
from packman.packman import get_package_config as get_conf
from packman import utils
from packman import python
from packman import retrieve

from fabric.api import *  # NOQA

lgr = logger.init()


def _prepare(package):

    common = utils.Handler()
    common.rmdir(package['sources_path'])
    common.mkdir('{0}/archives'.format(package['sources_path']))
    common.mkdir(package['package_path'])


def create_agent(package, download=False):
    dl_handler = retrieve.Handler()
    common = utils.Handler()
    py_handler = python.Handler()
    _prepare(package)
    py_handler.make_venv(package['sources_path'])
    if download:
        tar_file = '{0}/{1}.tar.gz'.format(
            package['sources_path'], package['name'])
        for url in package['source_urls']:
            dl_handler.download(url, file=tar_file)
        common.untar(package['sources_path'], tar_file)
        for module in package['modules']:
            py_handler.pip(module, package['sources_path'])


def get_ubuntu_precise_agent(download=False):
    package = get_conf('Ubuntu-precise-agent')
    create_agent(package, download)


def get_ubuntu_trusty_agent(download=False):
    package = get_conf('Ubuntu-trusty-agent')
    create_agent(package, download)


def get_centos_final_agent(download=False):
    package = get_conf('centos-Final-agent')
    create_agent(package, download)


def get_debian_jessie_agent(download=False):
    package = get_conf('debian-jessie-agent')
    create_agent(package, download)


def get_celery(download=False):
    package = get_conf('celery')

    dl_handler = retrieve.Handler()
    common = utils.Handler()
    py_handler = python.Handler()
    _prepare(package)
    py_handler.make_venv(package['sources_path'])
    tar_file = '{0}/{1}.tar.gz'.format(
        package['sources_path'], package['name'])
    for url in package['source_urls']:
        dl_handler.download(url, file=tar_file)
    common.untar(package['sources_path'], tar_file)
    if download:
        for module in package['modules']:
            py_handler.pip(module, package['sources_path'])


def get_manager(download=False):
    package = get_conf('manager')

    dl_handler = retrieve.Handler()
    common = utils.Handler()
    py_handler = python.Handler()
    _prepare(package)
    py_handler.make_venv(package['sources_path'])
    tar_file = '{0}/{1}.tar.gz'.format(
        package['sources_path'], package['name'])
    for url in package['source_urls']:
        dl_handler.download(url, file=tar_file)
    common.untar(package['sources_path'], tar_file)

    common.mkdir(package['file_server_dir'])
    common.cp(package['resources_path'], package['file_server_dir'])
    if download:
        for module in package['modules']:
            py_handler.pip(module, package['sources_path'])


def main():

    lgr.debug('VALIDATED!')


if __name__ == '__main__':
    main()
