#!/usr/bin/env python

import logging
import logging.config

import config

from fabric.api import *  # NOQA
from packager import *  # NOQA
from templgen import *  # NOQA

# __all__ = ['list']

logging.config.dictConfig(config.PACKAGER_LOGGER)
lgr = logging.getLogger('packager')


@task
def pkg_python_modules(component):  # celery installs successfully. dsl-parser can't install due to the missing celery common module.
    """
    """

    package = get_package_configuration(component)

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
def pkg_cosmo_ui():  # TESTED (lacking upstart and monit scripts)
    """
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
def pkg_ruby_gems(component):
    """
    """

    package = get_package_configuration(component)

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
def pkg_riemann():  # TESTED
    """
    """

    package = get_package_configuration('riemann')

    if not is_dir(package['bootstrap_dir']):
        mkdir(package['bootstrap_dir'])
    lgr.debug("isolating debs...")
    cp('%s/*.deb' % package['package_dir'], package['bootstrap_dir'])


@task
def pkg_rabbitmq():  # TESTED
    """
    """

    package = get_package_configuration('rabbitmq-server')

    if not is_dir(package['bootstrap_dir']):
        mkdir(package['bootstrap_dir'])
    lgr.debug("isolating debs...")
    cp('%s/archives/*.deb' % package['package_dir'], package['bootstrap_dir'])


@task
def pkg_elasticsearch():  # TESTED
    """
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
def pkg_logstash():  # TESTED
    """
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
def pkg_jruby():  # TESTED
    """
    """

    package = get_package_configuration('jruby')

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
def pkg_nginx():  # TESTED
    """
    """

    package = get_package_configuration('nginx')

    if not is_dir(package['bootstrap_dir']):
        mkdir(package['bootstrap_dir'])
    lgr.debug("isolating debs...")
    cp('%s/archives/*.deb' % package['package_dir'], package['bootstrap_dir'])


@task
def pkg_nodejs():  # TESTED
    """
    """

    package = get_package_configuration('nodejs')

    if not is_dir(package['bootstrap_dir']):
        mkdir(package['bootstrap_dir'])
    lgr.debug("isolating debs...")
    cp('%s/archives/*.deb' % package['package_dir'], package['bootstrap_dir'])


@task
def pkg_openjdk():  # TESTED
    """
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
