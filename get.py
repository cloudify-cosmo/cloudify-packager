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
from packman.packman import AptHandler
from packman.packman import do

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
    tar_file = '{0}/{1}.tar.gz'.format(
        package['sources_path'], package['name'])
    for url in package['source_urls']:
        dl_handler.download(url, file=tar_file)
    common.untar(package['sources_path'], tar_file)
    if download:
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


def get_ruby():
    package = get_conf('ruby')

    _prepare(package)
    apt_handler = AptHandler()
    for dep in package['prereqs']:
        apt_handler.install(dep)
    with lcd('/opt'):
        do('git clone '
           'https://github.com/sstephenson/ruby-build.git')
    do('export PREFIX=/opt/ruby-build', sudo=False)
    do('/opt/ruby-build/install.sh')
    do('/opt/ruby-build/bin/ruby-build -v {} {}'.format(
        package['version'], package['sources_path']))


def get_workflow_gems():
    package = get_conf('workflow_gems')

    apt_handler = AptHandler()
    common = CommonHandler()
    dl_handler = WgetHandler()
    _prepare(package)
    apt_handler.installs(package['prereqs'])

    dl_handler.downloads(package['source_urls'], package['sources_path'])
    common.untar(
        package['sources_path'],
        '{0}/{1}'.format(package['sources_path'], '*.tar.gz'))
    common.rm('{0}/{1}'.format(package['sources_path'], '*.tar.gz'))
    do('sudo /opt/ruby/bin/gem install bundler')
    do('sudo /opt/ruby/bin/bundle --gemfile {0}'
       .format(package['gemfile_location']))
    common.rmdir(package['gemfile_base_dir'])
    common.cp('/opt/ruby/lib/ruby/gems/2.1.0/cache/*.gem',
              package['sources_path'])


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
