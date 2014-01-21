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
import packager
from get import *  # NOQA
from pkg import *  # NOQA
# from config import PACKAGES as PKGS

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
def get_cosmo():
    """
    ACT:    retrieves cosmo 3rd parties
    EXEC:   fab get_cosmo_components
    """

    get_openjdk()
    apt_get(['maven'])
    get_logstash()
    get_elasticsearch()
    get_riemann()
    get_rabbitmq()
    get_nodejs()
    get_cosmo_ui()
    get_nginx()
    get_kibana()
    get_celery()
    get_workflow_jruby()
    pkg_openjdk()
    # dpkg -i openjdk before getting manager...
    get_manager()
    get_python_modules('virtualenv')


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
    pkg_cosmo_ui()
    pkg_nginx()
    pkg_kibana()
    pkg_celery()
    pkg_manager()
    pkg_workflow_jruby()
    # pkg_virtualenv()


@task
def bootstrap_cosmo_components():
    """
    ACT:    bootstraps cosmo components (
        can be used to test the bootstrap scripts)
    EXEC:   fab bootstrap_cosmo_components
    """

    bootstrap('openjdk-7-jdk')  # TEST again
    bootstrap('jruby')
    bootstrap('riemann')
    bootstrap('rabbitmq-server')
    bootstrap('logstash')
    bootstrap('elasticsearch')
    bootstrap('nodejs')
    bootstrap('cosmo-ui')
    bootstrap('workflow-gems')  # FIX atomic installation problem
    bootstrap('dsl-parser-modules')
    bootstrap('celery-modules')  # FIX problem with celery common installation
    bootstrap('manager-rest-modules')


# @task
def bs():
    """
    ACT:    bootstraps cosmo
    EXEC:   fab bs
    """

    packager.run_script('cosmo', 'bootstrap')


# @task
def create(package_name, arg_s=''):
    """
    ACT:    creates a packages (
        and potentially appends a bootstrap script to it)
    ARGS:   package_name = name of package to create
    EXEC:   fab create:package_name
    """

    packager.run_script(package_name, 'pkg', arg_s)


# @task
def retrieve(package_name, arg_s=''):
    """
    ACT:    downloads a package
    ARGS:   package_name = name of package to create
    EXEC:   fab get:package_name
    """

    packager.run_script(package_name, 'get', arg_s)


@task
def remove(package_name, arg_s=''):
    """
    ACT:    removes a package
    ARGS:   package_name = name of package to create
    EXEC:   fab remove:package_name
    """

    packager.run_script(package_name, 'remove', arg_s)


@task
def bootstrap(package_name, arg_s=''):
    """
    ACT:    bootstraps a package
    ARGS:   package_name = name of package to create
    EXEC:   fab bootstrap:package_name
    """

    packager.run_script(package_name, 'bootstrap', arg_s)
