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

#!/usr/bin/env python

import logging
import logging.config
import config
# run_env = os.environ['RUN_ENV']
# config = __import__(run_env)

# from event_handler import send_event as se
# import uuid
import sys
import os
from fabric.api import *  # NOQA
from packager import *  # NOQA

# __all__ = ['list']

try:
    d = os.path.dirname(config.LOGGER['handlers']['file']['filename'])
    if not os.path.exists(d):
        os.makedirs(d)
    logging.config.dictConfig(config.LOGGER)
    lgr = logging.getLogger('main')
    lgr.setLevel(logging.DEBUG)
except ValueError:
    sys.exit('could not initialize logger.'
             ' verify your logger config'
             ' and permissions to write to {0}'
             .format(config.LOGGER['handlers']['file']['filename']))


def _prepare(package):

    rmdir(package['sources_path'])
    make_package_paths(
        package['package_path'],
        package['sources_path'])
    # if 'conf_dir' in package:
        # cp('%s/*' % package['conf_dir'], package['sources_path'])


@task
def get_linux_agent():
    """
    ACT:    retrives linux agent
    EXEC:   fab get_linux_agent
    """

    package = get_package_configuration('linux-agent')

    _prepare(package)
    venv(package['sources_path'])
    for module in package['modules']:
        pip(module, '%s/bin' % package['sources_path'])


@task
def get_python_modules(component):
    """
    ACT:    retrives python modules
    ARGS:   component = Cosmo component to downloads modules for.
    EXEC:   fab get_python_modules:component
    """

    package = get_package_configuration(component)

    _prepare(package)
    for module in package['modules']:
        get_python_module(module, package['sources_path'])


@task
def get_graphite():
    """
    ACT:    retrives graphite
    EXEC:   fab get_graphite
    """

    package = get_package_configuration('graphite')

    _prepare(package)
    venv(package['sources_path'])
    for module in package['modules']:
        pip(module, '%s/bin' % package['sources_path'])


@task
def get_celery(download=False):
    """
    ACT:    retrives celery
    EXEC:   fab get_celery
    """

    package = get_package_configuration('celery')

    _prepare(package)
    venv(package['sources_path'])
    if download:
        for module in package['modules']:
            pip(module, '%s/bin' % package['sources_path'])


@task
def get_manager(download=False):
    """
    ACT:    retrives cosmo manager and its config, creates a virtualenv,
            installs all modules and builds cosmo.jar
    EXEC:   fab get_manager
    """

    package = get_package_configuration('manager')

    _prepare(package)
    venv(package['sources_path'])
    # if download:
    wget(
        package['source_url'],
        file='%s/%s.tar.gz' % (package['sources_path'],
                               package['name']))
    untar(package['sources_path'],
          '%s/%s.tar.gz' % (package['sources_path'],
                            package['name']))
        # TODO: DELETE TAR FILE
    # else:
        # cp(local_manager_repo, package['sources_path'])

    mkdir(package['file_server_dir'])
    import shutil
    shutil.copytree('%s/src/main/resources/cloudify' %
                    package['resources_path'],
                    '%s/cloudify' % package['file_server_dir'])
    # cp('%s/src/main/resources/cloudify' % package['resources_path'],
    #    '%s/cloudify' % package['file_server_dir'])
    alias_mapping_resource = ('%s/src/main/resources/org/cloudifysource/cosmo/'
                              'dsl/alias-mappings.yaml' %
                              package['resources_path'])
    cp(alias_mapping_resource, '%s/cloudify/' % package['file_server_dir'])
    if download:
        for module in package['modules']:
            pip(module, '%s/bin' % package['sources_path'])


@task
def get_curl():
    """
    ACT:    retrives curl
    EXEC:   fab get_curl
    """

    package = get_package_configuration('curl')

    _prepare(package)
    for req in package['reqs']:
        apt_purge(req)
    apt_download(
        package['name'],
        package['sources_path'])
    apt_get([package['name']])


@task
def get_make():
    """
    ACT:    retrives make
    EXEC:   fab get_make
    """

    package = get_package_configuration('make')

    _prepare(package)
    apt_purge(package['name'])
    apt_download(
        package['name'],
        package['sources_path'])
    apt_get([package['name']])


# @task
# def get_gcc():
#     """
#     ACT:    retrives gcc
#     EXEC:   fab get_gcc
#     """

#     package = get_package_configuration('gcc')

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

    package = get_package_configuration('ruby')

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

#     package = get_package_configuration('zlib')

#     wget(
#         package['source_url'],
#         file='%s/zlib.tar.gz' % package['sources_path'])


@task
def get_workflow_gems():
    """
    ACT:    retrives workflow gems
    EXEC:   fab get_workflow_gems
    """

    package = get_package_configuration('workflow-gems')

    _prepare(package)
    apt_get(package['reqs'])

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

    wget(
        package['gemfile_source_url'],
        package['sources_path'])
    untar(
        package['sources_path'],
        '%s/%s' % (package['sources_path'], '*.tar.gz'))
    rm('%s/%s' % (package['sources_path'], '*.tar.gz'))
    do('sudo /opt/ruby/bin/gem install bundler')
    do('sudo /opt/ruby/bin/bundle --gemfile %s' % package['gemfile_location'])
    rmdir(package['gemfile_base_dir'])
    cp('/opt/ruby/lib/ruby/gems/2.1.0/cache/*.gem', package['sources_path'])


@task
def get_cosmo_ui(download=False):
    """
    ACT:    retrives cosmo_ui
    EXEC:   fab get_cosmo_ui
    """

    package = get_package_configuration('cosmo-ui')

    _prepare(package)
    if download:
        wget(
            package['source_url'],
            dir=package['sources_path'])


@task
def get_nodejs():
    """
    ACT:    retrives nodejs
    EXEC:   fab get_nodejs
    """

    package = get_package_configuration('nodejs')

    _prepare(package)
    apt_get(package['prereqs'])
    lgr.debug("adding package repo to src repo...")
    add_ppa_repo(package['source_ppa'])
    apt_update()
    apt_download(
        package['name'],
        package['sources_path'])


@task
def get_riemann():
    """
    ACT:    retrives riemann
    EXEC:   fab get_riemann
    """

    package = get_package_configuration('riemann')

    _prepare(package)
    # stream_id = str(uuid.uuid1())
    # se(event_origin="cosmo-packager",
    #     event_type="packager.get.%s" % package['name'],
    #     event_subtype="started",
    #     event_description='started downloading %s' % package['name'],
    #     event_stream_id=stream_id)

    wget(
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

    package = get_package_configuration('rabbitmq-server')

    _prepare(package)
    add_src_repo(package['source_repo'], 'deb')
    wget(
        package['source_key'],
        package['sources_path'])
    add_key(package['key_file'])
    apt_update()
    apt_download_reqs(package['reqs'], package['sources_path'])
    apt_download(
        package['name'],
        package['sources_path'])


@task
def get_logstash():
    """
    ACT:    retrives logstash
    EXEC:   fab get_logstash
    """

    package = get_package_configuration('logstash')

    _prepare(package)
    wget(
        package['source_url'],
        dir=package['sources_path'])


@task
def get_elasticsearch():
    """
    ACT:    retrives elasticsearch
    EXEC:   fab get_elasticsearch
    """

    package = get_package_configuration('elasticsearch')

    _prepare(package)
    wget(
        package['source_url'],
        dir=package['sources_path'])


@task
def get_kibana():
    """
    ACT:    retrives kibana
    EXEC:   fab get_kibana
    """

    package = get_package_configuration('kibana3')

    _prepare(package)
    wget(
        package['source_url'],
        dir=package['sources_path'])


@task
def get_nginx():
    """
    ACT:    retrives nginx
    EXEC:   fab get_nginx
    """

    package = get_package_configuration('nginx')

    _prepare(package)
    add_src_repo(package['source_repo'], 'deb')
    add_src_repo(package['source_repo'], 'deb-src')
    wget(package['source_key'], package['sources_path'])
    add_key(package['key_file'])
    apt_update()
    apt_download(
        package['name'],
        package['sources_path'])


@task
def get_openjdk():
    """
    ACT:    retrives openjdk
    EXEC:   fab get_openjdk
    """

    package = get_package_configuration('openjdk-7-jdk')

    _prepare(package)
    apt_download(
        package['name'],
        package['sources_path'])


def main():

    lgr.debug('VALIDATED!')


if __name__ == '__main__':
    main()
