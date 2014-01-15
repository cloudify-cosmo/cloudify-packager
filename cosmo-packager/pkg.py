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
    ACT:    packages python modules
    EXEC:   fab pkg_python_modules
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
def pkg_cosmo_ui():  # TESTED
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
def pkg_ruby_gems(component):  # TESTED
    """
    ACT:    packages ruby gems
    ARGS:   component = Cosmo component to package gems for
    EXEC:   fab pkg_ruby_gems
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
    ACT:    packages riemann
    EXEC:   fab pkg_riemann
    """

    package = get_package_configuration('riemann')

    if not is_dir(package['bootstrap_dir']):
        mkdir(package['bootstrap_dir'])
    lgr.debug("isolating debs...")
    cp('%s/*.deb' % package['package_dir'], package['bootstrap_dir'])


@task
def pkg_rabbitmq():  # TESTED
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
def pkg_elasticsearch():  # TESTED
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
def pkg_logstash():  # TESTED
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
def pkg_jruby():  # TESTED
    """
    ACT:    packages jruby
    EXEC:   fab pkg_jruby
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
    ACT:    packages nginx
    EXEC:   fab pkg_nginx
    """

    package = get_package_configuration('nginx')

    if not is_dir(package['bootstrap_dir']):
        mkdir(package['bootstrap_dir'])
    lgr.debug("isolating debs...")
    cp('%s/archives/*.deb' % package['package_dir'], package['bootstrap_dir'])


@task
def pkg_nodejs():  # TESTED
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
def pkg_openjdk():  # TESTED
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
