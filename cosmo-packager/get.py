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
def get_python_modules(component):
	"""
	ACT:    retrives python modules for Cosmo components
    ARGS:   component = Cosmo component to downloads packages for.
    EXEC:   fab get.get_python_modules:component
	"""

	package = get_package_configuration(component)

	rmdir(package['package_dir'])
	make_package_dirs(
		package['bootstrap_dir'],
		package['package_dir']
		)
	for module in package['modules']:
		get_python_module(module, package['package_dir'])


@task
def get_riemann():
	"""
	ACT:    retrives riemann
    EXEC:   fab get.get_riemann
	"""

	package = get_package_configuration('riemann')

	rmdir(package['package_dir'])
	make_package_dirs(
		package['bootstrap_dir'],
		package['package_dir']
		)
	wget(
		package['source_url'],
		package['package_dir']
		)


@task
def get_rabbitmq():
	"""
	ACT:    retrives rabbitmq
    EXEC:   fab get.get_rabbitmq
	"""

	package = get_package_configuration('rabbitmq-server')

	rmdir(package['package_dir'])
	make_package_dirs(
		package['bootstrap_dir'],
		package['package_dir']
		)

	lgr.debug("adding package repo to src repo...")
	local('sudo sed -i "2i deb %s" /etc/apt/sources.list' % package['source_url'])
	wget(package['source_key'], package['package_dir'])
	add_key('%s/%s' % (package['package_dir'], package['key_file']))
	apt_update()
	apt_download(
		package['erlang'],
		package['package_dir']
		)
	apt_download(
		package['name'],
		package['package_dir']
		)


@task
def get_ruby_gems(component):
	"""
	ACT:    retrives workflow gems
    EXEC:   fab get.get_ruby_gems:component
	"""

	package = get_package_configuration(component)

	rmdir(package['package_dir'])
	make_package_dirs(
		package['bootstrap_dir'],
		package['package_dir']
		)
	for gem in package['gems']:
		get_ruby_gem(gem, package['package_dir'])
	# sudo gem install --no-ri --no-rdoc --install-dir ${PKG_DIR} rack-test -v 0.6.2
	# sudo gem install --no-ri --no-rdoc --install-dir ${PKG_DIR} test-unit -v 2.5.5


@task
def get_elasticsearch():
	"""
	ACT:    retrives elasticsearch
    EXEC:   fab get.get_elasticsearch
	"""

	package = get_package_configuration('elasticsearch')

	rmdir(package['package_dir'])
	make_package_dirs(
		package['bootstrap_dir'],
		package['package_dir']
		)
	wget(
		package['source_url'],
		package['package_dir']
		)
	
	PKG_INIT_DIR = "%s/init" % package['package_dir']
	INIT_DIR = "%s/%s/init" % (config.PACKAGER_CONF_DIR, package['name'])

	lgr.debug("creating init dir...")
	mkdir(PKG_INIT_DIR)
	lgr.debug("getting init file...")
	cp('%s/%s.conf' % (INIT_DIR, package['name']), PKG_INIT_DIR)


@task
def get_logstash():
	"""
	ACT:    retrives logstash
    EXEC:   fab get.get_logstash
	"""

	package = get_package_configuration('logstash')

	rmdir(package['package_dir'])
	make_package_dirs(
		package['bootstrap_dir'],
		package['package_dir']
		)
	wget(
		package['source_url'],
		package['package_dir']
		)

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
def get_jruby():
	"""
	"""

	package = get_package_configuration('jruby')

	rmdir(package['package_dir'])
	make_package_dirs(
		package['bootstrap_dir'],
		package['package_dir']
		)
	wget(
		package['source_url'],
		package['package_dir']
		)


@task
def get_nginx():
	"""
	"""

	package = get_package_configuration('nginx')

	rmdir(package['package_dir'])
	make_package_dirs(
		package['bootstrap_dir'],
		package['package_dir']
		)

	lgr.debug("adding package repo to src repo...")
	local('sudo sed -i "2i deb %s" /etc/apt/sources.list' % package['source_url'])
	local('sudo sed -i "2i deb-src %s" /etc/apt/sources.list' % package['source_url'])
	wget(package['source_key'], package['package_dir'])
	add_key('%s/%s' % (package['package_dir'], package['key_file']))
	apt_update()
	apt_download(
		package['name'],
		package['package_dir']
		)


@task
def get_nodejs():
	"""
	"""

	package = get_package_configuration('nodejs')

	rmdir(package['package_dir'])
	make_package_dirs(
		package['bootstrap_dir'],
		package['package_dir']
		)

	apt_get(package['prereqs'])
	lgr.debug("adding package repo to src repo...")
	local('add-apt-repository -y %s' % package['source_url'])
	apt_update()
	apt_download(
		package['name'],
		package['package_dir']
		)


@task
def get_openjdk():
	"""
	"""

	package = get_package_configuration('openjdk-7-jdk')

	rmdir(package['package_dir'])
	make_package_dirs(
		package['bootstrap_dir'],
		package['package_dir']
		)
	apt_download(
		package['name'],
		package['package_dir']
		)


def main():

    lgr.debug('VALIDATED!')


if __name__ == '__main__':
    main()