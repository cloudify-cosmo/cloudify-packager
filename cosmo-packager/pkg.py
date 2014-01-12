#!/usr/bin/env python

from fabric.api import *
import config

import logging
import logging.config

from packager import *

# __all__ = ['list']

logging.config.dictConfig(config.PACKAGER_LOGGER)
lgr = logging.getLogger('packager')


@task
def pkg_python_modules(component):
    """
    """

    package = get_package_configuration(component)

    pack(package['src_package_type'], package['dst_package_type'], 
        package['name'],
        package['package_dir'],
        '%s/archives/' % package['package_dir'],
        package['version'],
        package['bootstrap_script']
        )
    
    if not is_dir(package['bootstrap_dir']):
        mkdir(package['bootstrap_dir'])
    lgr.debug("isolating debs...")
    cp('%s/archives/*.deb' % package['package_dir'], package['bootstrap_dir'])
    

@task
def pkg_riemann():
    """
    """

    package = get_package_configuration('riemann')

    if not is_dir(package['bootstrap_dir']):
        mkdir(package['bootstrap_dir'])
    lgr.debug("isolating debs...")
    cp('%s/*.deb' % package['package_dir'], package['bootstrap_dir'])


@task
def pkg_rabbitmq():
    """
    """

    package = get_package_configuration('rabbitmq-server')

    if not is_dir(package['bootstrap_dir']):
        mkdir(package['bootstrap_dir'])
    lgr.debug("isolating debs...")
    cp('%s/archives/*.deb' % package['package_dir'], package['bootstrap_dir'])


@task
def pkg_ruby_gems(component):
    """
    """

    package = get_package_configuration(component)

    pack(package['src_package_type'], package['dst_package_type'], 
        package['name'],
        package['package_dir'],
        '%s/archives/' % package['package_dir'],
        package['version'],
        package['bootstrap_script']
        )

    if not is_dir(package['bootstrap_dir']):
        mkdir(package['bootstrap_dir'])
    lgr.debug("isolating debs...")
    cp('%s/archives/*.deb' % package['package_dir'], package['bootstrap_dir'])


@task
def pkg_elasticsearch():
    """
    """

    package = get_package_configuration('elasticsearch')

    pack(package['src_package_type'], package['dst_package_type'], 
        package['name'],
        package['package_dir'],
        '%s/archives/' % package['package_dir'],
        package['version'],
        package['bootstrap_script']
        )

    if not is_dir(package['bootstrap_dir']):
        mkdir(package['bootstrap_dir'])
    lgr.debug("isolating debs...")
    cp('%s/archives/*.deb' % package['package_dir'], package['bootstrap_dir'])


@task
def pkg_logstash():
    """
    """

    package = get_package_configuration('logstash')

    pack(package['src_package_type'], package['dst_package_type'], 
        package['name'],
        package['package_dir'],
        '%s/archives/' % package['package_dir'],
        package['version'],
        package['bootstrap_script']
        )

    if not is_dir(package['bootstrap_dir']):
        mkdir(package['bootstrap_dir'])
    lgr.debug("isolating debs...")
    cp('%s/archives/*.deb' % package['package_dir'], package['bootstrap_dir'])


@task
def pkg_jruby():
    """
    """

    package = get_package_configuration('jruby')

    pack(package['src_package_type'], package['dst_package_type'], 
        package['name'],
        package['package_dir'],
        '%s/archives/' % package['package_dir'],
        package['version'],
        package['bootstrap_script']
        )

    if not is_dir(package['bootstrap_dir']):
        mkdir(package['bootstrap_dir'])
    lgr.debug("isolating debs...")
    cp('%s/archives/*.deb' % package['package_dir'], package['bootstrap_dir'])


@task
def pkg_nginx():
    """
    """

    package = get_package_configuration('nginx')

    if not is_dir(package['bootstrap_dir']):
        mkdir(package['bootstrap_dir'])
    lgr.debug("isolating debs...")
    cp('%s/archives/*.deb' % package['package_dir'], package['bootstrap_dir'])


@task
def pkg_nodejs():
    """
    """

    package = get_package_configuration('nodejs')

    if not is_dir(package['bootstrap_dir']):
        mkdir(package['bootstrap_dir'])
    lgr.debug("isolating debs...")
    cp('%s/archives/*.deb' % package['package_dir'], package['bootstrap_dir'])


@task
def pkg_openjdk():
    """
    """

    package = get_package_configuration('openjdk-7-jdk')

    if not is_dir(package['bootstrap_dir']):
        mkdir(package['bootstrap_dir'])
    lgr.debug("isolating debs...")
    cp('%s/archives/*.deb' % package['package_dir'], package['bootstrap_dir'])


@task
def pkg_cosmo_modules():
    """
    """

    package = get_package_configuration(component)

    if not is_dir(package['bootstrap_dir']):
        mkdir(package['bootstrap_dir'])
    lgr.debug("isolating debs...")
    cp('%s/archives/*.deb' % package['package_dir'], package['bootstrap_dir'])


def main():

    lgr.debug('VALIDATED!')


if __name__ == '__main__':
    main()