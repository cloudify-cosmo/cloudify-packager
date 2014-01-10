from fabric.api import *
import config
from config import PACKAGES as PKGS

import logging
import logging.config

# __all__ = ['list']

logging.config.dictConfig(config.PACKAGER_LOGGER)
lgr = logging.getLogger('packager')


@task
def create_python_modules(component):
	"""
	"""

	package = PKGS[component]

	SRC_TYPE="dir"
	DST_TYPE="deb"
	BOOTSTRAP_SCRIPT="%s/%s-bootstrap.sh" % (config.PACKAGER_SCRIPTS_DIR, component)
	
	pack(SRC_TYPE, DST_TYPE, package['name'], package['version'], package['package_dir'], BOOTSTRAP_SCRIPT) 
		
	lgr.debug("isolating debs...")
	cp('%s/archives/*.deb' % package['package_dir'], package['bootstrap_dir'])
	

@task
def create_riemann():
	"""
	"""

	package = PKGS['riemann']

	lgr.debug("isolating debs...")
	cp('%s/archives/*.deb' % package['package_dir'], package['bootstrap_dir'])


@task
def create_rabbitmq():
	"""
	"""

	package = PKGS['rabbitmq-server']

	lgr.debug("isolating debs...")
	cp('%s/archives/*.deb' % package['package_dir'], package['bootstrap_dir'])


@task
def create_workflow_gems(component):
	"""
	"""

	package = PKGS[component]

	SRC_TYPE="dir"
	DST_TYPE="deb"
	BOOTSTRAP_SCRIPT="%s/%s-bootstrap.sh" % (config.PACKAGER_SCRIPTS_DIR, component)
	
	pack(SRC_TYPE, DST_TYPE, package['name'], package['version'], package['package_dir'], BOOTSTRAP_SCRIPT) 
	
	lgr.debug("isolating debs...")
	cp('%s/archives/*.deb' % package['package_dir'], package['bootstrap_dir'])


@task
def create_elasticsearch():
	"""
	"""

	package = PKGS['elasticsearch']

	SRC_TYPE="dir"
	DST_TYPE="deb"
	BOOTSTRAP_SCRIPT="%s/%s-bootstrap.sh" % (config.PACKAGER_SCRIPTS_DIR, package['name'])
	
	pack(SRC_TYPE, DST_TYPE, package['name'], package['version'], package['package_dir'], BOOTSTRAP_SCRIPT) 
	
	lgr.debug("isolating debs...")
	cp('%s/archives/*.deb' % package['package_dir'], package['bootstrap_dir'])


@task
def create_logstash():
	"""
	"""

	package = PKGS['logstash']

	SRC_TYPE="dir"
	DST_TYPE="deb"
	BOOTSTRAP_SCRIPT="%s/%s-bootstrap.sh" % (config.PACKAGER_SCRIPTS_DIR, package['name'])
	
	pack(SRC_TYPE, DST_TYPE, package['name'], package['version'], package['package_dir'], BOOTSTRAP_SCRIPT) 
	
	lgr.debug("isolating debs...")
	cp('%s/archives/*.deb' % package['package_dir'], package['bootstrap_dir'])


@task
def create_jruby():
	"""
	"""

	package = PKGS['jruby']

	SRC_TYPE="dir"
	DST_TYPE="deb"
	BOOTSTRAP_SCRIPT="%s/%s-bootstrap.sh" % (config.PACKAGER_SCRIPTS_DIR, package['name'])
	
	pack(SRC_TYPE, DST_TYPE, package['name'], package['version'], package['package_dir'], BOOTSTRAP_SCRIPT) 
	
	lgr.debug("isolating debs...")
	cp('%s/archives/*.deb' % package['package_dir'], package['bootstrap_dir'])


@task
def create_nginx():
	"""
	"""

	package = PKGS['nginx']

	lgr.debug("isolating debs...")
	cp('%s/archives/*.deb' % package['package_dir'], package['bootstrap_dir'])


@task
def create_nodejs():
	"""
	"""

	package = PKGS['nodejs']

	lgr.debug("isolating debs...")
	cp('%s/archives/*.deb' % package['package_dir'], package['bootstrap_dir'])


@task
def create_openjdk():
	"""
	"""

	package = PKGS['openjdk-7-jdk']

	lgr.debug("isolating debs...")
	cp('%s/archives/*.deb' % package['package_dir'], package['bootstrap_dir'])


def main():

    lgr.debug('VALIDATED!')


if __name__ == '__main__':
    main()