#!/usr/bin/env python

from fabric.api import *
import config
from config import PACKAGES as PKGS

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

	package = PKGS[component]

	SRC_TYPE="dir"
	DST_TYPE="deb"
	BOOTSTRAP_SCRIPT="%s/%s-bootstrap.sh" % (config.PACKAGER_SCRIPTS_DIR, component)
	
	with lcd('%s/archives/' % package['package_dir']):
		pack(SRC_TYPE, DST_TYPE, 
			package['name'],
			package['package_dir'],
			package['version'],
			BOOTSTRAP_SCRIPT
			)
		
	lgr.debug("isolating debs...")
	cp('%s/archives/*.deb' % package['package_dir'], package['bootstrap_dir'])
	

@task
def pkg_riemann():
	"""
	"""

	package = PKGS['riemann']

	lgr.debug("isolating debs...")
	cp('%s/archives/*.deb' % package['package_dir'], package['bootstrap_dir'])


@task
def pkg_rabbitmq():
	"""
	"""

	package = PKGS['rabbitmq-server']

	lgr.debug("isolating debs...")
	cp('%s/archives/*.deb' % package['package_dir'], package['bootstrap_dir'])


@task
def pkg_workflow_gems(component):
	"""
	"""

	package = PKGS[component]

	SRC_TYPE="dir"
	DST_TYPE="deb"
	BOOTSTRAP_SCRIPT="%s/%s-bootstrap.sh" % (config.PACKAGER_SCRIPTS_DIR, component)
	
	with lcd('%s/archives/' % package['package_dir']):
		pack(SRC_TYPE, DST_TYPE, 
			package['name'],
			package['package_dir'],
			package['version'],
			BOOTSTRAP_SCRIPT
			)
	
	lgr.debug("isolating debs...")
	cp('%s/archives/*.deb' % package['package_dir'], package['bootstrap_dir'])


@task
def pkg_elasticsearch():
	"""
	"""

	package = PKGS['elasticsearch']

	SRC_TYPE="dir"
	DST_TYPE="deb"
	BOOTSTRAP_SCRIPT="%s/%s-bootstrap.sh" % (config.PACKAGER_SCRIPTS_DIR, package['name'])
	
	with lcd('%s/archives/' % package['package_dir']):
		pack(SRC_TYPE, DST_TYPE, 
			package['name'],
			package['package_dir'],
			package['version'],
			BOOTSTRAP_SCRIPT
			)
	
	lgr.debug("isolating debs...")
	cp('%s/archives/*.deb' % package['package_dir'], package['bootstrap_dir'])


@task
def pkg_logstash():
	"""
	"""

	package = PKGS['logstash']

	SRC_TYPE="dir"
	DST_TYPE="deb"
	BOOTSTRAP_SCRIPT="%s/%s-bootstrap.sh" % (config.PACKAGER_SCRIPTS_DIR, package['name'])
	
	with lcd('%s/archives/' % package['package_dir']):
		pack(SRC_TYPE, DST_TYPE, 
			package['name'],
			package['package_dir'],
			package['version'],
			BOOTSTRAP_SCRIPT
			)
		
	lgr.debug("isolating debs...")
	cp('%s/archives/*.deb' % package['package_dir'], package['bootstrap_dir'])


@task
def pkg_jruby():
	"""
	"""

	package = PKGS['jruby']

	SRC_TYPE="dir"
	DST_TYPE="deb"
	BOOTSTRAP_SCRIPT="%s/%s-bootstrap.sh" % (config.PACKAGER_SCRIPTS_DIR, package['name'])
	
	if is_dir(package['package_dir']):
		with lcd('%s/archives/' % package['package_dir']):
			pack(SRC_TYPE, DST_TYPE, 
				package['name'],
				package['package_dir'],
				package['version'],
				BOOTSTRAP_SCRIPT
				)
	else:
		lgr.error('package dir %s does\'nt exist, termintating...' % package['package_dir'])
		sys.exit()

	lgr.debug("isolating debs...")
	cp('%s/archives/*.deb' % package['package_dir'], package['bootstrap_dir'])


@task
def pkg_nginx():
	"""
	"""

	package = PKGS['nginx']

	lgr.debug("isolating debs...")
	cp('%s/archives/*.deb' % package['package_dir'], package['bootstrap_dir'])


@task
def pkg_nodejs():
	"""
	"""

	package = PKGS['nodejs']

	lgr.debug("isolating debs...")
	cp('%s/archives/*.deb' % package['package_dir'], package['bootstrap_dir'])


@task
def pkg_openjdk():
	"""
	"""

	package = PKGS['openjdk-7-jdk']

	lgr.debug("isolating debs...")
	cp('%s/archives/*.deb' % package['package_dir'], package['bootstrap_dir'])


def main():

    lgr.debug('VALIDATED!')


if __name__ == '__main__':
    main()