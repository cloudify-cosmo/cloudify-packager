"""
DOCUMENTATION LINK:
https://github.com/CloudifySource/cosmo-packager
"""


# TODO:
# add external components configuration to packager
# write logstash base config
# write elasticsearch base config (threading, storage, etc...)
# write packager tests
# add cosmo base packages
# create external components bootstrap script
# create external components package task
# create cosmo components bootstrap script
# create cosmo components package task
# parse setup.py for each cosmo component and get deps from there..

# CONFIGURATION
# 3rd party components configuration
# how to bootstrap each module

# get maven
# cosmo.jar bootstrap (see bootstrap_lxc...) put jar file in orchestrator/target

# plugins to install in celery's venv
# plugin install
# agent install
# reimann configurer
# openstack provisioner
# vagrant (on hold)

from fabric.api import *  # NOQA
from packager import *  # NOQA
from get import *  # NOQA
from pkg import *  # NOQA
# import config

#env.user = ''
#env.password = ''
#env.port = ''

env.warn_only = 0
env.abort_on_prompts = False
env.connection_attempts = 5
env.keepalive = 0
env.linewise = False
env.pool_size = 0
env.skip_bad_hosts = False
env.timeout = 10
env.forward_agent = True
env.status = False
#env.use_ssh_config = True
#env.key_filename = ["~/.ssh/id_rsa.pub"]


#TASKS
@task
def get_cosmo_components():
    """
    ACT:    retrieves cosmo 3rd parties
    EXEC:   fab get_cosmo_components
    """

    # get_openjdk()
    get_logstash()
    get_elasticsearch()
    get_riemann()
    get_rabbitmq()
    get_nodejs()
    get_nginx()
    get_kibana()
    get_python_modules('virtualenv')


@task
def get_cosmo_base():
    """
    ACT:    retrieves cosmo code
    EXEC:   fab get_cosmo_base
    """

    get_workflow_jruby()
    get_celery()
    get_cosmo_ui()
    if not check_if_package_is_installed('openjdk-7-jdk'):
        pkg_openjdk()
        local('sudo dpkg -i %s/*.deb' % config.PACKAGES['openjdk']['bootstrap_dir'])
    if not check_if_package_is_installed('maven'):
        apt_get(['maven'])
    get_manager()


@task
def pkg_cosmo():
    """
    ACT:    packages cosmo 3rd parties
    EXEC:   fab pkg_comso_components
    """

    # pkg_openjdk()  # already packaged at get_ process
    pkg_logstash()
    pkg_elasticsearch()
    pkg_riemann()
    pkg_rabbitmq()
    pkg_nodejs()
    pkg_nginx()
    pkg_kibana()
    pkg_virtualenv()
    pkg_workflow_jruby()
    pkg_celery()
    pkg_cosmo_ui()
    pkg_manager()
