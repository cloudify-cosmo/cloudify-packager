#!/usr/bin/env python

import logging
import logging.config

import config
from event_handler import send_event as se
import uuid

import sys
from fabric.api import *  # NOQA
from packager import *  # NOQA
from templgen import *  # NOQA

# __all__ = ['list']

try:
    logging.config.dictConfig(config.PACKAGER_LOGGER)
    lgr = logging.getLogger('packager')
except ValueError:
    sys.exit('could not initiate logger. try sudo...')


@task
def pkg_celery():
    """
    ACT:    packages celery
    EXEC:   fab pkg_celery
    """

    package = get_package_configuration('celery')

    create_bootstrap_script(
        package, package['bootstrap_template'], package['bootstrap_script'])
    pack(
        package['src_package_type'], package['dst_package_type'], package['name'],
        package['package_dir'], '%s/archives/' % package['package_dir'],
        package['version'], package['bootstrap_script'])

    if not is_dir(package['bootstrap_dir']):
        mkdir(package['bootstrap_dir'])
    lgr.debug("isolating debs...")
    cp('%s/archives/*.deb' % package['package_dir'], package['bootstrap_dir'])


@task
def pkg_manager():
    """
    ACT:    packages manager
    EXEC:   fab pkg_manager
    """

    package = get_package_configuration('manager')

    create_bootstrap_script(
        package, package['bootstrap_template'], package['bootstrap_script'])
    pack(
        package['src_package_type'], package['dst_package_type'], package['name'],
        package['package_dir'], '%s/archives/' % package['package_dir'],
        package['version'], package['bootstrap_script'])

    if not is_dir(package['bootstrap_dir']):
        mkdir(package['bootstrap_dir'])
    lgr.debug("isolating debs...")
    cp('%s/archives/*.deb' % package['package_dir'], package['bootstrap_dir'])


@task
def pkg_workflow_jruby():
    """
    ACT:    packages workflow-jruby
    EXEC:   fab pkg_workflow-jruby
    """

    package = get_package_configuration('workflow-jruby')

    create_bootstrap_script(
        package, package['bootstrap_template'], package['bootstrap_script'])
    pack(
        package['src_package_type'], package['dst_package_type'], package['name'],
        package['package_dir'], '%s/archives/' % package['package_dir'],
        package['version'], package['bootstrap_script'])

    if not is_dir(package['bootstrap_dir']):
        mkdir(package['bootstrap_dir'])
    lgr.debug("isolating debs...")
    cp('%s/archives/*.deb' % package['package_dir'], package['bootstrap_dir'])


@task
def pkg_cosmo_ui():
    """
    ACT:    packages cosmo ui
    EXEC:   fab pkg_cosmo_ui
    """

    package = get_package_configuration('cosmo-ui')

    create_bootstrap_script(
        package, package['bootstrap_template'], package['bootstrap_script'])
    pack(
        package['src_package_type'], package['dst_package_type'], package['name'],
        package['package_dir'], '%s/archives/' % package['package_dir'],
        package['version'], package['bootstrap_script'])

    if not is_dir(package['bootstrap_dir']):
        mkdir(package['bootstrap_dir'])
    lgr.debug("isolating debs...")
    cp('%s/archives/*.deb' % package['package_dir'], package['bootstrap_dir'])


@task
def pkg_nodejs():
    """
    ACT:    packages nodejs
    EXEC:   fab pkg_nodejs
    """

    package = get_package_configuration('nodejs')

    if not is_dir(package['bootstrap_dir']):
        mkdir(package['bootstrap_dir'])
    lgr.debug("isolating debs...")
    cp('%s/archives/*.deb' % package['package_dir'], package['bootstrap_dir'])


@task
def pkg_riemann():
    """
    ACT:    packages riemann
    EXEC:   fab pkg_riemann
    """

    package = get_package_configuration('riemann')

    stream_id = str(uuid.uuid1())
    se(event_origin="cosmo-packager",
        event_type="packager.pkg.%s" % package['name'],
        event_subtype="started",
        event_description='started packaging %s' % package['name'],
        event_stream_id=stream_id)

    if not is_dir(package['bootstrap_dir']):
        mkdir(package['bootstrap_dir'])
    lgr.debug("isolating debs...")
    cp('%s/*.deb' % package['package_dir'], package['bootstrap_dir'])

    se(event_origin="cosmo-packager",
        event_type="packager.pkg.%s" % package['name'],
        event_subtype="success",
        event_description='finished packaging %s' % package['name'],
        event_stream_id=stream_id)


@task
def pkg_rabbitmq():
    """
    ACT:    packages rabbitmq
    EXEC:   fab pkg_rabbitmq
    """

    package = get_package_configuration('rabbitmq-server')

    if not is_dir(package['bootstrap_dir']):
        mkdir(package['bootstrap_dir'])
    lgr.debug("isolating debs...")
    cp('%s/archives/*.deb' % package['package_dir'], package['bootstrap_dir'])


@task
def pkg_logstash():
    """
    ACT:    packages logstash
    EXEC:   fab pkg_logstash
    """

    package = get_package_configuration('logstash')

    create_bootstrap_script(
        package, package['bootstrap_template'], package['bootstrap_script'])
    pack(
        package['src_package_type'], package['dst_package_type'], package['name'],
        package['package_dir'], '%s/archives/' % package['package_dir'],
        package['version'], package['bootstrap_script'])

    if not is_dir(package['bootstrap_dir']):
        mkdir(package['bootstrap_dir'])
    lgr.debug("isolating debs...")
    cp('%s/archives/*.deb' % package['package_dir'], package['bootstrap_dir'])


@task
def pkg_elasticsearch():
    """
    ACT:    packages elasticsearch
    EXEC:   fab pkg_elasticsearch
    """

    package = get_package_configuration('elasticsearch')

    create_bootstrap_script(
        package, package['bootstrap_template'], package['bootstrap_script'])
    pack(
        package['src_package_type'], package['dst_package_type'], package['name'],
        package['package_dir'], '%s/archives/' % package['package_dir'],
        package['version'], package['bootstrap_script'])

    if not is_dir(package['bootstrap_dir']):
        mkdir(package['bootstrap_dir'])
    lgr.debug("isolating debs...")
    cp('%s/archives/*.deb' % package['package_dir'], package['bootstrap_dir'])


@task
def pkg_kibana():
    """
    ACT:    packages kibana
    EXEC:   fab pkg_kibana
    """

    package = get_package_configuration('kibana3')

    create_bootstrap_script(
        package, package['bootstrap_template'], package['bootstrap_script'])
    pack(
        package['src_package_type'], package['dst_package_type'], package['name'],
        package['package_dir'], '%s/archives/' % package['package_dir'],
        package['version'], package['bootstrap_script'])

    if not is_dir(package['bootstrap_dir']):
        mkdir(package['bootstrap_dir'])
    lgr.debug("isolating debs...")
    cp('%s/archives/*.deb' % package['package_dir'], package['bootstrap_dir'])


@task
def pkg_nginx():
    """
    ACT:    packages nginx
    EXEC:   fab pkg_nginx
    """

    package = get_package_configuration('nginx')

    if not is_dir(package['bootstrap_dir']):
        mkdir(package['bootstrap_dir'])
    lgr.debug("isolating debs...")
    cp('%s/archives/*.deb' % package['package_dir'], package['bootstrap_dir'])


@task
def pkg_openjdk():
    """
    ACT:    packages openjdk
    EXEC:   fab pkg_openjdk
    """

    package = get_package_configuration('openjdk-7-jdk')

    if not is_dir(package['bootstrap_dir']):
        mkdir(package['bootstrap_dir'])
    lgr.debug("isolating debs...")
    cp('%s/archives/*.deb' % package['package_dir'], package['bootstrap_dir'])


def main():

    lgr.debug('VALIDATED!')


if __name__ == '__main__':
    main()
