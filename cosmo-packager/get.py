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

from event_handler import send_event as se
import uuid
import sys
from fabric.api import *  # NOQA
from packager import *  # NOQA

# __all__ = ['list']

try:
    logging.config.dictConfig(config.PACKAGER_LOGGER)
    lgr = logging.getLogger('packager')
except ValueError:
    sys.exit('could not initiate logger. try sudo...')


@task
def get_python_modules(component):
    """
    ACT:    retrives python modules
    ARGS:   component = Cosmo component to downloads modules for.
    EXEC:   fab get_python_modules:component
    """

    package = get_package_configuration(component)

    rmdir(package['package_dir'])
    make_package_dirs(
        package['bootstrap_dir'],
        package['package_dir'])
    for module in package['modules']:
        get_python_module(module, package['package_dir'])


@task
def get_graphite():
    """
    ACT:    retrives graphite
    EXEC:   fab get_graphite
    """

    package = get_package_configuration('graphite')

    rmdir(package['package_dir'])
    make_package_dirs(
        package['bootstrap_dir'],
        package['package_dir'])
    venv(package['package_dir'])
    for module in package['modules']:
        pip(module, '%s/bin' % package['package_dir'])

    # CONF_DIR = "%s/%s/*" % (config.PACKAGER_CONF_DIR, package['name'])
    # cp(CONF_DIR, package['package_dir'])


@task
def get_celery():
    """
    ACT:    retrives celery
    EXEC:   fab get_celery
    """

    package = get_package_configuration('celery')

    rmdir(package['package_dir'])
    make_package_dirs(
        package['bootstrap_dir'],
        package['package_dir'])
    venv(package['package_dir'])
    for module in package['modules']:
        pip(module, '%s/bin' % package['package_dir'])

    CONF_DIR = "%s/%s/*" % (config.PACKAGER_CONF_DIR, package['name'])
    cp(CONF_DIR, package['package_dir'])


@task
def get_manager():
    """
    ACT:    retrives cosmo manager and its config, creates a virtualenv,
            installs all modules and builds cosmo.jar
    EXEC:   fab get_manager
    """

    package = get_package_configuration('manager')

    rmdir(package['package_dir'])
    make_package_dirs(
        package['bootstrap_dir'],
        package['package_dir'])
    venv(package['package_dir'])
    wget(
        package['source_url'],
        file='%s/%s.tar.gz' % (package['package_dir'], package['name']))
    untar('%s' % package['package_dir'],
          '%s/%s.tar.gz' % (package['package_dir'], package['name']))
    for module in package['modules']:
        pip(module, '%s/bin' % package['package_dir'])

    CONF_DIR = "%s/%s/*" % (config.PACKAGER_CONF_DIR, package['name'])
    cp(CONF_DIR, package['package_dir'])

    # x = check_if_package_is_installed('openjdk-7-jdk')
    # if not x:
        # lgr.debug('prereq package is not installed. terminating...')
        # sys.exit()
    # mvn('%s/cosmo-manager-develop/orchestrator/pom.xml' %
        # package['package_dir'])


@task
def get_rvm():
    """
    ACT:    retrives rvm
    EXEC:   fab get_rvm
    """

    package = get_package_configuration('rvm')

    rmdir(package['package_dir'])
    make_package_dirs(
        package['bootstrap_dir'],
        package['package_dir'])
    apt_get(package['prereqs'])
    do('sudo curl -sSL %s -o %s/rvm-stable.tar.gz' % (package['source_url'],
                                                      package['package_dir']))


@task
def get_make():
    """
    ACT:    retrives make
    EXEC:   fab get_make
    """

    package = get_package_configuration('make')

    rmdir(package['package_dir'])
    make_package_dirs(
        package['bootstrap_dir'],
        package['package_dir'])
    apt_download(
        package['name'],
        package['package_dir'])


@task
def get_ruby():
    """
    ACT:    retrives ruby
    EXEC:   fab get_ruby
    """

    package = get_package_configuration('ruby')

    rmdir(package['package_dir'])
    make_package_dirs(
        package['bootstrap_dir'],
        package['package_dir'])
    wget(
        package['source_url'],
        file='%s/ruby.tar.gz' % package['package_dir'])

    # mkdir(package['rvm_inst_dir'])
    # do('sudo tar -C %s --strip-components=1'
       # ' -xzf %s/rvm-stable.tar.gz' % (package['rvm_inst_dir'],
                                     # config.PACKAGES['rvm']['package_dir']))
    # do('cd %s && sudo ./install --auto-dotfiles' %
        # package['rvm_inst_dir'])
    # do('source /etc/profile.d/rvm.sh')
    # do('sudo dpkg-name %s/archives/*.deb' % package['package_dir'])
    # do('sudo dpkg -i %s/archives/*.deb' % package['package_dir'])
    # do('rvm install 2.1.0')
    # cp('$rvm_path/archives/*', package['package_dir'])


@task
def get_workflow_gems():
    """
    ACT:    retrives workflow gems
    EXEC:   fab get_workflow_gems
    """

    package = get_package_configuration('workflow-gems')

    rmdir(package['package_dir'])
    make_package_dirs(
        package['bootstrap_dir'],
        package['package_dir'])
    apt_get(package['reqs'])
    # do('sudo dpkg -i %s/archives/*.deb' %
        # config.PACKAGES['ruby']['package_dir'])
    do('sudo tar -C {0} -xzvf {0}/ruby.tar.gz'.format(
        config.PACKAGES['ruby']['package_dir']))
    do('cd {0}/ruby-2.1.0 && sudo ./configure --prefix=/usr/local'.format(
        config.PACKAGES['ruby']['package_dir']))
    do('cd {0}/ruby-2.1.0 && sudo make'.format(
        config.PACKAGES['ruby']['package_dir']))
    do('cd {0}/ruby-2.1.0 && sudo make install'.format(
        config.PACKAGES['ruby']['package_dir']))

    wget(
        package['gemfile_source_url'],
        package['package_dir'])
    untar(
        package['package_dir'],
        '%s/%s' % (package['package_dir'], '*.tar.gz'))
    rm('%s/%s' % (package['package_dir'], '*.tar.gz'))
    do('sudo gem install bundler')
    do('sudo bundle --gemfile %s' % package['gemfile_location'])
    rmdir(package['gemfile_base_dir'])
    cp('/usr/local/lib/ruby/gems/2.1.0/cache/*.gem', package['package_dir'])


@task
def get_cosmo_ui():
    """
    ACT:    retrives cosmo_ui
    EXEC:   fab get_cosmo_ui
    """

    package = get_package_configuration('cosmo-ui')

    rmdir(package['package_dir'])
    make_package_dirs(
        package['bootstrap_dir'],
        package['package_dir'])
    wget(
        package['source_url'],
        dir=package['package_dir'])

    CONF_DIR = "%s/%s/*" % (config.PACKAGER_CONF_DIR, package['name'])
    cp(CONF_DIR, package['package_dir'])


@task
def get_nodejs():
    """
    ACT:    retrives nodejs
    EXEC:   fab get_nodejs
    """

    package = get_package_configuration('nodejs')

    rmdir(package['package_dir'])
    make_package_dirs(
        package['bootstrap_dir'],
        package['package_dir'])

    apt_get(package['prereqs'])
    lgr.debug("adding package repo to src repo...")
    do('add-apt-repository -y %s' % package['source_url'])
    apt_update()
    apt_download(
        package['name'],
        package['package_dir'])


@task
def get_riemann():
    """
    ACT:    retrives riemann
    EXEC:   fab get_riemann
    """

    package = get_package_configuration('riemann')

    stream_id = str(uuid.uuid1())
    se(event_origin="cosmo-packager",
        event_type="packager.get.%s" % package['name'],
        event_subtype="started",
        event_description='started downloading %s' % package['name'],
        event_stream_id=stream_id)

    rmdir(package['package_dir'])
    make_package_dirs(
        package['bootstrap_dir'],
        package['package_dir'])
    wget(
        package['source_url'],
        dir=package['package_dir'])

    se(event_origin="cosmo-packager",
        event_type="packager.get.%s" % package['name'],
        event_subtype="success",
        event_description='finished downloading %s' % package['name'],
        event_stream_id=stream_id)


@task
def get_rabbitmq():
    """
    ACT:    retrives rabbitmq
    EXEC:   fab get_rabbitmq
    """

    package = get_package_configuration('rabbitmq-server')

    rmdir(package['package_dir'])
    make_package_dirs(
        package['bootstrap_dir'],
        package['package_dir'])

    lgr.debug("adding package repo to src repo...")
    do('sudo sed -i "2i deb %s" /etc/apt/sources.list' %
       package['source_url'])
    wget(
        package['source_key'],
        package['package_dir'])
    add_key('%s/%s' % (package['package_dir'], package['key_file']))
    apt_update()
    apt_download(
        package['erlang'],
        package['package_dir'])
    apt_download(
        package['name'],
        package['package_dir'])


@task
def get_logstash():
    """
    ACT:    retrives logstash
    EXEC:   fab get_logstash
    """

    package = get_package_configuration('logstash')

    rmdir(package['package_dir'])
    make_package_dirs(
        package['bootstrap_dir'],
        package['package_dir'])
    wget(
        package['source_url'],
        dir=package['package_dir'])

    CONF_DIR = "%s/%s/*" % (config.PACKAGER_CONF_DIR, package['name'])
    cp(CONF_DIR, package['package_dir'])


@task
def get_elasticsearch():
    """
    ACT:    retrives elasticsearch
    EXEC:   fab get_elasticsearch
    """

    package = get_package_configuration('elasticsearch')

    rmdir(package['package_dir'])
    make_package_dirs(
        package['bootstrap_dir'],
        package['package_dir'])
    wget(
        package['source_url'],
        dir=package['package_dir'])

    CONF_DIR = "%s/%s/*" % (config.PACKAGER_CONF_DIR, package['name'])
    cp(CONF_DIR, package['package_dir'])


@task
def get_kibana():
    """
    ACT:    retrives kibana
    EXEC:   fab get_kibana
    """

    package = get_package_configuration('kibana3')

    rmdir(package['package_dir'])
    make_package_dirs(
        package['bootstrap_dir'],
        package['package_dir'])
    wget(
        package['source_url'],
        dir=package['package_dir'])


@task
def get_nginx():
    """
    ACT:    retrives nginx
    EXEC:   fab get_nginx
    """

    package = get_package_configuration('nginx')

    rmdir(package['package_dir'])
    make_package_dirs(
        package['bootstrap_dir'],
        package['package_dir'])

    lgr.debug("adding package repo to src repo...")
    do('sudo sed -i "2i deb %s" /etc/apt/sources.list' %
       package['source_url'])
    do('sudo sed -i "2i deb-src %s" /etc/apt/sources.list' %
       package['source_url'])
    wget(package['source_key'], package['package_dir'])
    add_key('%s/%s' % (package['package_dir'], package['key_file']))
    apt_update()
    apt_download(
        package['name'],
        package['package_dir'])


@task
def get_openjdk():
    """
    ACT:    retrives openjdk
    EXEC:   fab get_openjdk
    """

    package = get_package_configuration('openjdk-7-jdk')

    rmdir(package['package_dir'])
    make_package_dirs(
        package['bootstrap_dir'],
        package['package_dir'])
    apt_download(
        package['name'],
        package['package_dir'])


def main():

    lgr.debug('VALIDATED!')


if __name__ == '__main__':
    main()
