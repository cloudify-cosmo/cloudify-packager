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
    venv(package['package_dir'],
         package['name'])
    for module in package['modules']:
        pip(module,
            '%s/%s/bin' % (package['package_dir'], package['name']))

    PKG_INIT_DIR = "%s/init" % package['package_dir']
    INIT_DIR = "%s/%s/init" % (config.PACKAGER_CONF_DIR, package['name'])

    PKG_CONF_DIR = "%s/conf" % package['package_dir']
    CONF_DIR = "%s/%s/conf" % (config.PACKAGER_CONF_DIR, package['name'])

    lgr.debug("creating init dir...")
    mkdir(PKG_INIT_DIR)
    lgr.debug("getting init file...")
    cp('%s/*' % INIT_DIR, PKG_INIT_DIR)

    lgr.debug("creating conf dir...")
    mkdir(PKG_CONF_DIR)
    lgr.debug("getting conf files...")
    cp('%s/*' % CONF_DIR, PKG_CONF_DIR)


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
    venv(package['package_dir'],
         package['name'])
    wget(
        package['source_url'],
        file='%s/%s.tar.gz' % (package['package_dir'], package['name']))
    untar('%s/%s' % (package['package_dir'], package['name']),
          '%s/%s.tar.gz' % (package['package_dir'], package['name']))
    for module in package['modules']:
        pip(module,
            '%s/%s/bin' % (package['package_dir'], package['name']))

    PKG_INIT_DIR = "%s/init" % package['package_dir']
    INIT_DIR = "%s/%s/init" % (config.PACKAGER_CONF_DIR, package['name'])

    lgr.debug("creating init dir...")
    mkdir(PKG_INIT_DIR)
    lgr.debug("getting init file...")
    cp('%s/*.conf' % INIT_DIR, PKG_INIT_DIR)

    x = check_if_package_is_installed('openjdk-7-jdk')
    if not x:
        lgr.debug('prereq package is not installed. terminating...')
        sys.exit()
    mvn('%s/%s/cosmo-manager-develop/orchestrator/pom.xml' % (package['package_dir'],
                                                              package['name']))


@task
def get_workflow_jruby():
    """
    ACT:    retrives jruby and its workflow gems
    EXEC:   fab get_workflow_jruby
    """

    package = get_package_configuration('workflow-jruby')

    rmdir(package['package_dir'])
    make_package_dirs(
        package['bootstrap_dir'],
        package['package_dir'])
    wget(package['source_url'], package['package_dir'])
    untar(package['package_dir'], '%s/%s' % (package['package_dir'], '*.tar.gz'))
    rm('%s/%s' % (package['package_dir'], '*.tar.gz'))
    wget(package['gemfile_source_url'], package['package_dir'])
    untar(package['package_dir'], '%s/%s' % (package['package_dir'], '*.tar.gz'))
    rm('%s/%s' % (package['package_dir'], '*.tar.gz'))
    local('ln -sf %s/%s/jruby %s' % (package['package_dir'],
                                     package['bin_home_dir'],
                                     '/usr/bin/jruby'))
    local('%s/%s/jruby -S gem install bundler' % (package['package_dir'],
                                                  package['bin_home_dir']))
    local('%s/%s/jruby -S bundle --gemfile %s' % (package['package_dir'],
                                                  package['bin_home_dir'],
                                                  package['gemfile_location']))
    # TODO: USE FIND_IN_DIR TO GET GEMFILE
    # sudo gem install --no-ri --no-rdoc --install-dir ${PKG_DIR} rack-test -v 0.6.2
    # sudo gem install --no-ri --no-rdoc --install-dir ${PKG_DIR} test-unit -v 2.5.5


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

    PKG_INIT_DIR = "%s/init" % package['package_dir']
    INIT_DIR = "%s/%s/init" % (config.PACKAGER_CONF_DIR, package['name'])

    lgr.debug("creating init dir...")
    mkdir(PKG_INIT_DIR)
    lgr.debug("getting init file...")
    cp('%s/%s.conf' % (INIT_DIR, package['name']), PKG_INIT_DIR)


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
    local('add-apt-repository -y %s' % package['source_url'])
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

    PKG_INIT_DIR = "%s/init" % package['package_dir']
    INIT_DIR = "%s/%s/init" % (config.PACKAGER_CONF_DIR, package['name'])

    lgr.debug("creating init dir...")
    mkdir(PKG_INIT_DIR)
    lgr.debug("getting init file...")
    cp('%s/%s.conf' % (INIT_DIR, package['name']), PKG_INIT_DIR)


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
    local('sudo sed -i "2i deb %s" /etc/apt/sources.list' % package['source_url'])
    local('sudo sed -i "2i deb-src %s" /etc/apt/sources.list' % package['source_url'])
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
