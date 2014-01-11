"""
PROVIDE DOCUMENTATION LINK
"""

from fabric.api import *
import packager
import get
import pkg
from config import PACKAGES as PKGS

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
    EXEC:   fab g3po
    """

    get.get_jruby()
    get.get_openjdk()
    get.get_logstash()
    get.get_elasticsearch()
    get.get_openjdk()
    get.get_riemann()
    get.get_rabbitmq()
    get.get_nodejs()
    get.get_python_modules('dsl-parser-modules')
    get.get_python_modules('celery-modules')
    get.get_python_modules('manager-rest-modules')
    get.get_workflow_gems()


@task
def pkg_cosmo():
    """
    ACT:    packages cosmo 3rd parties
    EXEC:   fab c3po
    """

    pkg.pkg_jruby()
    pkg.pkg_openjdk()
    pkg.pkg_logstash()
    pkg.pkg_elasticsearch()
    pkg.pkg_openjdk()
    pkg.pkg_riemann()
    pkg.pkg_rabbitmq()
    pkg.pkg_nodejs()
    pkg.pkg_python_modules('dsl-parser-modules')
    pkg.pkg_python_modules('celery-modules')
    pkg.pkg_python_modules('manager-rest-modules')
    get.get_workflow_gems()



@task
def bs():
    """
    ACT:    bootstraps cosmo
    EXEC:   fab bs
    """

    packager.run_script('cosmo', 'bootstrap')


@task
def create(package_name, arg_s=''):
    """
    ACT:    creates a packages (and potentially appends a bootstrap script to it)
    ARGS:   package_name = name of package to create
    EXEC:   fab create:package_name
    """

    packager.run_script(package_name, 'pkg', arg_s)


@task
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
