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

from packager import init_logger
from packager import get_package_configuration as get_conf
from packager import CommonHandler
from packager import PythonHandler
from packager import DownloadsHandler
from packager import AptHandler

# import shutil
from fabric.api import *  # NOQA
from packager import *  # NOQA

lgr = init_logger()

# __all__ = ['list']


def _prepare(package):

    common = CommonHandler()
    common.rmdir(package['sources_path'])
    # DEPRACATE!
    common.make_package_paths(
        package['package_path'],
        package['sources_path'])


@task
def get_linux_agent():
    """
    ACT:    retrives linux agent
    EXEC:   fab get_linux_agent
    """

    package = get_conf('linux-agent')

    dl_handler = DownloadsHandler()
    common = CommonHandler()
    py_handler = PythonHandler()
    _prepare(package)
    py_handler.venv(package['sources_path'])
    tar_file = '{0}/{1}.tar.gz'.format(
        package['sources_path'], package['name'])
    dl_handler.wget(package['source_url'], file=tar_file)
    common.untar(package['sources_path'], tar_file)
    py_handler.venv(package['sources_path'])
    for module in package['modules']:
        py_handler.pip(module, '%s/bin' % package['sources_path'])
    # TODO: remove redundant data after module installation


@task
def get_python_modules(component):
    """
    ACT:    retrives python modules
    ARGS:   component = Cosmo component to downloads modules for.
    EXEC:   fab get_python_modules:component
    """

    package = get_conf(component)

    py_handler = PythonHandler()
    _prepare(package)
    for module in package['modules']:
        py_handler.get_python_module(module, package['sources_path'])


@task
def get_graphite():
    """
    ACT:    retrives graphite
    EXEC:   fab get_graphite
    """

    package = get_conf('graphite')

    py_handler = PythonHandler()
    _prepare(package)
    py_handler.venv(package['sources_path'])
    for module in package['modules']:
        py_handler.pip(module, '%s/bin' % package['sources_path'])


@task
def get_celery(download=False):
    """
    ACT:    retrives celery
    EXEC:   fab get_celery
    """

    package = get_conf('celery')

    dl_handler = DownloadsHandler()
    common = CommonHandler()
    py_handler = PythonHandler()
    _prepare(package)
    py_handler.venv(package['sources_path'])
    tar_file = '{0}/{1}.tar.gz'.format(
        package['sources_path'], package['name'])
    dl_handler.wget(package['source_url'], file=tar_file)
    common.untar(package['sources_path'], tar_file)
    if download:
        for module in package['modules']:
            py_handler.pip(module, '{0}/bin'.format(package['sources_path']))
    # TODO: remove redundant data after module installation


@task
def get_manager(download=False):
    """
    ACT:    retrives cosmo manager and its config, creates a virtualenv,
            installs all modules and builds cosmo.jar
    EXEC:   fab get_manager
    """

    package = get_conf('manager')

    dl_handler = DownloadsHandler()
    common = CommonHandler()
    py_handler = PythonHandler()
    _prepare(package)
    py_handler.venv(package['sources_path'])
    # if download:
    tar_file = '{0}/{1}.tar.gz'.format(
        package['sources_path'], package['name'])
    dl_handler.wget(package['source_url'], file=tar_file)
    common.untar(package['sources_path'], tar_file)

    common.mkdir(package['file_server_dir'])
    common.cp(package['resources_path'], package['file_server_dir'])
    # DEPRACATED!
    # shutil.copytree('%s/src/main/resources/cloudify' %
    #                 package['resources_path'],
    #                 '%s/cloudify' % package['file_server_dir'])
    # alias_mapping_resource = ('%s/src/main/resources/org/cloudifysource/cosmo/'  # NOQA
    #                           'dsl/alias-mappings.yaml' %
    #                           package['resources_path'])
    # common.cp(alias_mapping_resource, '%s/cloudify/' %
    #              package['file_server_dir'])
    if download:
        for module in package['modules']:
            py_handler.pip(module, '{0}/bin'.format(package['sources_path']))
    # TODO: remove redundant data after module installation


@task
def get_curl():
    """
    ACT:    retrives curl
    EXEC:   fab get_curl
    """

    package = get_conf('curl')

    apt_handler = AptHandler()
    _prepare(package)
    for req in package['reqs']:
        apt_handler.apt_purge(req)
    apt_handler.apt_download(
        package['name'],
        package['sources_path'])
    apt_handler.apt_get([package['name']])


@task
def get_make():
    """
    ACT:    retrives make
    EXEC:   fab get_make
    """

    package = get_conf('make')

    apt_handler = AptHandler()
    _prepare(package)
    apt_handler.apt_purge(package['name'])
    apt_handler.apt_download(
        package['name'],
        package['sources_path'])
    apt_handler.apt_get([package['name']])


# @task
# def get_gcc():
#     """
#     ACT:    retrives gcc
#     EXEC:   fab get_gcc
#     """

#     package = get_conf('gcc')

#     if package['reqs']:
#         for req in package['reqs']:
#             apt_purge(req)
#             apt_autoremove(req)
#             apt_download(req, package['sources_path'])
#     apt_download(
#         package['name'],
#         package['sources_path'])
#     if package['reqs']:
#             apt_get(package['reqs'])
#     apt_get(['dpkg-dev'])
    # dpkg_name('%s/archives' % package['sources_path'])


@task
def get_ruby():
    """
    ACT:    retrives ruby
    EXEC:   fab get_ruby
    """

    package = get_conf('ruby')

    _prepare(package)
    # RELEVANT IF COMPILING RUBY IN PLACE - CURRENTLY NOT USED
    # wget(
        # package['source_url'],
        # file='%s/ruby.tar.gz' % package['sources_path'])
    do('sudo /opt/ruby-build/bin/ruby-build -v %s %s' %
        (package['version'], package['sources_path']))


# @task
# def get_zlib():
#     """
#     ACT:    retrives zlib
#     EXEC:   fab get_zlib
#     """

#     package = get_conf('zlib')

#     wget(
#         package['source_url'],
#         file='%s/zlib.tar.gz' % package['sources_path'])


@task
def get_workflow_gems():
    """
    ACT:    retrives workflow gems
    EXEC:   fab get_workflow_gems
    """

    package = get_conf('workflow-gems')

    apt_handler = AptHandler()
    common = CommonHandler()
    dl_handler = DownloadsHandler()
    _prepare(package)
    apt_handler.apt_get(package['reqs'])

    # RELEVANT IF COMPILING RUBY IN PLACE - CURRENTLY NOT USED
    # do('sudo dpkg -i %s/archives/*.deb' %
        # config.PACKAGES['ruby']['sources_path'])
    # do('sudo tar -C {0} -xzvf {0}/ruby.tar.gz'.format(
        # config.PACKAGES['ruby']['sources_path']))
    # do('cd {0}/ruby-2.1.0 && sudo ./configure --prefix=/usr/local'.format(
        # config.PACKAGES['ruby']['sources_path']))
    # do('cd {0}/ruby-2.1.0 && sudo make'.format(
        # config.PACKAGES['ruby']['sources_path']))
    # do('cd {0}/ruby-2.1.0 && sudo make install'.format(
        # config.PACKAGES['ruby']['sources_path']))

    dl_handler.wget(
        package['source_url'],
        package['sources_path'])
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


@task
def get_cosmo_ui(download=False):
    """
    ACT:    retrives cosmo_ui
    EXEC:   fab get_cosmo_ui
    """

    package = get_conf('cosmo-ui')

    dl_handler = DownloadsHandler()
    _prepare(package)
    if download:
        dl_handler.wget(
            package['source_url'],
            dir=package['sources_path'])


@task
def get_nodejs():
    """
    ACT:    retrives nodejs
    EXEC:   fab get_nodejs
    """

    package = get_conf('nodejs')

    apt_handler = AptHandler()
    _prepare(package)
    apt_handler.apt_get(package['prereqs'])
    lgr.debug("adding package repo to src repo...")
    apt_handler.add_ppa_repo(package['source_ppa'])
    apt_handler.apt_update()
    apt_handler.apt_download(
        package['name'],
        package['sources_path'])


@task
def get_riemann():
    """
    ACT:    retrives riemann
    EXEC:   fab get_riemann
    """

    package = get_conf('riemann')

    dl_handler = DownloadsHandler()
    _prepare(package)
    # stream_id = str(uuid.uuid1())
    # se(event_origin="cosmo-packager",
    #     event_type="packager.get.%s" % package['name'],
    #     event_subtype="started",
    #     event_description='started downloading %s' % package['name'],
    #     event_stream_id=stream_id)

    dl_handler.wget(
        package['source_url'],
        dir='{0}/archives'.format(package['sources_path']))

    # se(event_origin="cosmo-packager",
    #     event_type="packager.get.%s" % package['name'],
    #     event_subtype="success",
    #     event_description='finished downloading %s' % package['name'],
    #     event_stream_id=stream_id)


@task
def get_rabbitmq():
    """
    ACT:    retrives rabbitmq
    EXEC:   fab get_rabbitmq
    """

    package = get_conf('rabbitmq-server')

    dl_handler = DownloadsHandler()
    apt_handler = AptHandler()
    _prepare(package)
    apt_handler.add_src_repo(package['source_repo'], 'deb')
    dl_handler.wget(
        package['source_key'],
        package['sources_path'])
    apt_handler.add_key(package['key_file'])
    apt_handler.apt_update()
    apt_handler.apt_download_reqs(package['reqs'], package['sources_path'])
    apt_handler.apt_download(
        package['name'],
        package['sources_path'])


@task
def get_logstash():
    """
    ACT:    retrives logstash
    EXEC:   fab get_logstash
    """

    package = get_conf('logstash')

    dl_handler = DownloadsHandler()
    _prepare(package)
    dl_handler.wget(
        package['source_url'],
        dir=package['sources_path'])


@task
def get_elasticsearch():
    """
    ACT:    retrives elasticsearch
    EXEC:   fab get_elasticsearch
    """

    package = get_conf('elasticsearch')

    dl_handler = DownloadsHandler()
    _prepare(package)
    dl_handler.wget(
        package['source_url'],
        dir=package['sources_path'])


@task
def get_kibana():
    """
    ACT:    retrives kibana
    EXEC:   fab get_kibana
    """

    package = get_conf('kibana3')

    dl_handler = DownloadsHandler()
    _prepare(package)
    dl_handler.wget(
        package['source_url'],
        dir=package['sources_path'])


@task
def get_nginx():
    """
    ACT:    retrives nginx
    EXEC:   fab get_nginx
    """

    package = get_conf('nginx')

    apt_handler = AptHandler()
    dl_handler = DownloadsHandler()
    _prepare(package)
    apt_handler.add_src_repo(package['source_repo'], 'deb')
    apt_handler.add_src_repo(package['source_repo'], 'deb-src')
    dl_handler.wget(package['source_key'], package['sources_path'])
    apt_handler.add_key(package['key_file'])
    apt_handler.apt_update()
    apt_handler.apt_download(
        package['name'],
        package['sources_path'])


@task
def get_openjdk():
    """
    ACT:    retrives openjdk
    EXEC:   fab get_openjdk
    """

    package = get_conf('openjdk-7-jdk')

    apt_handler = AptHandler()
    _prepare(package)
    apt_handler.apt_download(
        package['name'],
        package['sources_path'])


def main():

    lgr.debug('VALIDATED!')


if __name__ == '__main__':
    main()
