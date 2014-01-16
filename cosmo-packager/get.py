#!/usr/bin/env python

import logging
import logging.config

import config
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
def get_kibana():  # TESTED
    """
    ACT:    retrives kibana
    EXEC:   fab get_kibana
    """

    package = get_package_configuration('kibana')

    rmdir(package['package_dir'])
    make_package_dirs(
        package['bootstrap_dir'],
        package['package_dir'])
    wget(
        package['source_url'],
        dir=package['package_dir'])


@task
def get_pip():  # TESTED
    """
    ACT:    retrives pip
    EXEC:   fab get_pip
    """

    package = get_package_configuration('python-pip')

    rmdir(package['package_dir'])
    make_package_dirs(
        package['bootstrap_dir'],
        package['package_dir'])
    apt_download(
        package['name'],
        package['package_dir'])


@task
def get_python_modules(component):  # TESTED (failed on manager-modules due to no setup.py file)
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
def get_manager():  # TESTED
    """
    ACT:    retrives manager
    EXEC:   fab get_manager
    """

    package = get_package_configuration('manager')

    stream_id = str(uuid.uuid1())
    se(event_type="packager.get", event_name="get_manager_start", event_description='getting manager', stream_id=stream_id)

    rmdir(package['package_dir'])
    make_package_dirs(
        package['bootstrap_dir'],
        package['package_dir'])
    wget(
        package['source_url'],
        file='%s/%s.tar.gz' % (package['package_dir'], package['name']))

    se(event_type="packager.get", event_name="get_manager_success", event_description='getting manager', stream_id=stream_id)


@task
def get_cosmo_ui():  # TESTED
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

    PKG_INIT_DIR = "%s/init" % package['package_dir']
    INIT_DIR = "%s/%s/init" % (config.PACKAGER_CONF_DIR, package['name'])

    lgr.debug("creating init dir...")
    mkdir(PKG_INIT_DIR)
    lgr.debug("getting init file...")
    cp('%s/%s.conf' % (INIT_DIR, package['name']), PKG_INIT_DIR)


@task
def get_ruby_gems(component):  # TESTED
    """
    ACT:    retrives ruby gems
    ARGS:   component = Cosmo component to download gems for.
    EXEC:   fab get_ruby_gems:component
    """

    package = get_package_configuration(component)

    rmdir(package['package_dir'])
    make_package_dirs(
        package['bootstrap_dir'],
        package['package_dir'])
    for gem in package['gems']:
        get_ruby_gem(gem, package['package_dir'])
    # sudo gem install --no-ri --no-rdoc --install-dir ${PKG_DIR} rack-test -v 0.6.2
    # sudo gem install --no-ri --no-rdoc --install-dir ${PKG_DIR} test-unit -v 2.5.5


@task
def get_riemann():  # TESTED
    """
    ACT:    retrives riemann
    EXEC:   fab get_riemann
    """

    package = get_package_configuration('riemann')

    rmdir(package['package_dir'])
    make_package_dirs(
        package['bootstrap_dir'],
        package['package_dir'])
    wget(
        package['source_url'],
        dir=package['package_dir'])


@task
def get_rabbitmq():  # TESTED
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
    local('sudo sed -i "2i deb %s" /etc/apt/sources.list' % package['source_url'])
    wget(package['source_key'], package['package_dir'])
    add_key('%s/%s' % (package['package_dir'], package['key_file']))
    apt_update()
    apt_download(
        package['erlang'],
        package['package_dir'])
    apt_download(
        package['name'],
        package['package_dir'])


@task
def get_elasticsearch():  # TESTED
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

    PKG_INIT_DIR = "%s/init" % package['package_dir']
    INIT_DIR = "%s/%s/init" % (config.PACKAGER_CONF_DIR, package['name'])

    lgr.debug("creating init dir...")
    mkdir(PKG_INIT_DIR)
    lgr.debug("getting init file...")
    cp('%s/%s.conf' % (INIT_DIR, package['name']), PKG_INIT_DIR)


@task
def get_logstash():  # TESTED
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

    PKG_INIT_DIR = "%s/init" % package['package_dir']
    INIT_DIR = "%s/%s/init" % (config.PACKAGER_CONF_DIR, package['name'])

    PKG_CONF_DIR = "%s/conf" % package['package_dir']
    CONF_DIR = "%s/%s/conf" % (config.PACKAGER_CONF_DIR, package['name'])

    lgr.debug("creating init dir...")
    mkdir(PKG_INIT_DIR)
    lgr.debug("getting init file...")
    cp('%s/%s.conf' % (INIT_DIR, package['name']), PKG_INIT_DIR)

    lgr.debug("creating conf dir...")
    mkdir(PKG_CONF_DIR)
    lgr.debug("getting conf file...")
    cp('%s/%s.conf' % (CONF_DIR, package['name']), PKG_CONF_DIR)


@task
def get_jruby():  # TESTED
    """
    ACT:    retrives jruby
    EXEC:   fab get_jruby
    """

    package = get_package_configuration('jruby')

    rmdir(package['package_dir'])
    make_package_dirs(
        package['bootstrap_dir'],
        package['package_dir'])
    wget(
        package['source_url'],
        dir=package['package_dir'])


@task
def get_nginx():  # TESTED
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
    local('sudo sed -i "2i deb %s" /etc/apt/sources.list' % package['source_url'])
    local('sudo sed -i "2i deb-src %s" /etc/apt/sources.list' % package['source_url'])
    wget(package['source_key'], package['package_dir'])
    add_key('%s/%s' % (package['package_dir'], package['key_file']))
    apt_update()
    apt_download(
        package['name'],
        package['package_dir'])


@task
def get_nodejs():  # TESTED
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
    local('add-apt-repository -y %s' % package['source_url'])
    apt_update()
    apt_download(
        package['name'],
        package['package_dir'])


@task
def get_openjdk():  # TESTED
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
