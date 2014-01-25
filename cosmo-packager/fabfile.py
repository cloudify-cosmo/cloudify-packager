"""
DOCUMENTATION LINK:
https://github.com/CloudifySource/cosmo-packager
"""

from fabric.api import *  # NOQA
from packager import *  # NOQA
from get import *  # NOQA
from pkg import *  # NOQA
import config

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

    get_celery()
    get_cosmo_ui()
    if not check_if_package_is_installed('openjdk-7-jdk'):
        pkg_openjdk()
        local('sudo dpkg -i %s/*.deb' % config.PACKAGES['openjdk']['bootstrap_dir'])
    get_workflow_jruby()
    if not check_if_package_is_installed('maven'):
        apt_get(['maven'])
    get_manager()


@task
def pkg_cosmo_components():
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


@task
def pkg_cosmo_base():
    """
    ACT:    packages cosmo code
    EXEC:   fab pkg_comso_base
    """

    pkg_workflow_jruby()
    pkg_celery()
    pkg_cosmo_ui()
    pkg_manager()
