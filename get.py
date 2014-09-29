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

from packman.packman import init_logger
from packman.packman import get_component_config as get_conf
from packman.packman import CommonHandler
from packman.packman import PythonHandler
from packman.packman import WgetHandler

from fabric.api import *  # NOQA

lgr = init_logger()

# __all__ = ['list']


def _prepare(package):

    common = CommonHandler()
    common.rmdir(package['sources_path'])
    common.mkdir('{}/archives'.format(package['sources_path']))
    common.mkdir(package['package_path'])


def get_ubuntu_agent(download=False):
    package = get_conf('Ubuntu-agent')

    dl_handler = WgetHandler()
    common = CommonHandler()
    py_handler = PythonHandler()
    _prepare(package)
    py_handler.venv(package['sources_path'])
    if download:
        tar_file = '{0}/{1}.tar.gz'.format(
            package['sources_path'], package['name'])
        for url in package['source_urls']:
            dl_handler.download(url, file=tar_file)
        common.untar(package['sources_path'], tar_file)
        for module in package['modules']:
            py_handler.pip(module, package['sources_path'])
    # TODO: remove redundant data after module installation


def get_centos_agent(download=False):
    package = get_conf('centos-agent')

    dl_handler = WgetHandler()
    common = CommonHandler()
    py_handler = PythonHandler()
    _prepare(package)
    py_handler.venv(package['sources_path'])
    if download:
        tar_file = '{0}/{1}.tar.gz'.format(
            package['sources_path'], package['name'])
        for url in package['source_urls']:
            dl_handler.download(url, file=tar_file)
        common.untar(package['sources_path'], tar_file)
        for module in package['modules']:
            py_handler.pip(module, package['sources_path'])
    # TODO: remove redundant data after module installation
    
    
def get_celery(download=False):
    package = get_conf('celery')

    dl_handler = WgetHandler()
    common = CommonHandler()
    py_handler = PythonHandler()
    _prepare(package)
    py_handler.venv(package['sources_path'])
    tar_file = '{0}/{1}.tar.gz'.format(
        package['sources_path'], package['name'])
    for url in package['source_urls']:
        dl_handler.download(url, file=tar_file)
    common.untar(package['sources_path'], tar_file)
    if download:
        for module in package['modules']:
            py_handler.pip(module, package['sources_path'])
    # TODO: remove redundant data after module installation


def get_manager(download=False):
    package = get_conf('manager')

    dl_handler = WgetHandler()
    common = CommonHandler()
    py_handler = PythonHandler()
    _prepare(package)
    py_handler.venv(package['sources_path'])
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
    # TODO: remove redundant data after module installation


# @task
# def get_riemann():
#     package = get_conf('riemann')

#     dl_handler = WgetHandler()
#     _prepare(package)
#     # stream_id = str(uuid.uuid1())
#     # se(event_origin="cosmo-packman",
#     #     event_type="packman.get.%s" % package['name'],
#     #     event_subtype="started",
#     #     event_description='started downloading %s' % package['name'],
#     #     event_stream_id=stream_id)

#     for url in package['source_urls']:
#         dl_handler.download(
#             url,
#             dir='{0}/archives'.format(package['sources_path']))

#     # se(event_origin="cosmo-packman",
#     #     event_type="packman.get.%s" % package['name'],
#     #     event_subtype="success",
#     #     event_description='finished downloading %s' % package['name'],
#     #     event_stream_id=stream_id)


def main():

    lgr.debug('VALIDATED!')


if __name__ == '__main__':
    main()
