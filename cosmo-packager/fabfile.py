"""
PROVIDE DOCUMENTATION LINK
"""

from fabric.api import *
import packager
import getters
import creators
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
def g3po():
    """
    ACT:    retrieves cosmo 3rd parties
    EXEC:   fab g3po
    """
    #TODO: CREATE ARG_S FROM ARGDICT
    # for package in PKGS.iteritems():
        # package_name = package[0]

    package_name = 'jruby'
    get_arg_s = '"%s" "%s" "%s"' % (
        PKGS[package_name]['name'],
        PKGS[package_name]['version'],
        PKGS[package_name]['source_url']
        )
    packager.run_script(package_name, 'get', get_arg_s)

    package_name = 'logstash'
    get_arg_s = '"%s" "%s" "%s"' % (
        PKGS[package_name]['name'],
        PKGS[package_name]['version'],
        PKGS[package_name]['source_url']
        )
    packager.run_script(package_name, 'get', get_arg_s)

    package_name = 'elasticsearch'
    get_arg_s = '"%s" "%s" "%s"' % (
        PKGS[package_name]['name'],
        PKGS[package_name]['version'],
        PKGS[package_name]['source_url']
        )
    packager.run_script(package_name, 'get', get_arg_s)

    package_name = 'openjdk-7-jdk'
    get_arg_s = '"%s"' % (
        PKGS[package_name]['name']
        )
    packager.run_script(package_name, 'get', get_arg_s)

    package_name = 'nginx'
    get_arg_s = '"%s" "%s" "%s" "%s" "%s"' % (
        PKGS[package_name]['name'],
        PKGS[package_name]['version'],
        PKGS[package_name]['source_url'],
        PKGS[package_name]['source_key'],
        PKGS[package_name]['key_file']
        )
    packager.run_script(package_name, 'get', get_arg_s)

    package_name = 'riemann'
    get_arg_s = '"%s" "%s" "%s"' % (
        PKGS[package_name]['name'],
        PKGS[package_name]['version'],
        PKGS[package_name]['source_url']
        )
    packager.run_script(package_name, 'get', get_arg_s)

    package_name = 'rabbitmq-server'
    get_arg_s = '"%s" "%s" "%s" "%s" "%s"' % (
        PKGS[package_name]['name'],
        PKGS[package_name]['version'],
        PKGS[package_name]['source_url'],
        PKGS[package_name]['source_key'],
        PKGS[package_name]['key_file']
        )
    packager.run_script(package_name, 'get', get_arg_s)

    package_name = 'nodejs'
    get_arg_s = '"%s" "%s" "%s"' % (
        PKGS[package_name]['name'],
        PKGS[package_name]['version'],
        PKGS[package_name]['source_url']
        )
    packager.run_script(package_name, 'get', get_arg_s)

    # package_name = 'workflow-gems'
    # get_arg_s = '"%s" "%s" "%s"' % (
        # PKGS[package_name]['name'],
        # PKGS[package_name]['version'],
        # PKGS[package_name]['source_url']
        # )
    # packager.run_script(package_name, 'get', get_arg_s)

    # package_name = 'python-modules'
    # get_arg_s = '"%s" "%s" "%s"' % (
        # PKGS[package_name]['name'],
        # PKGS[package_name]['version'],
        # PKGS[package_name]['source_url']
        # )
    # packager.run_script(package_name, 'get', get_arg_s)


@task
def c3po():
    """
    ACT:    packages cosmo 3rd parties
    EXEC:   fab c3po
    """

    #TODO: CREATE ARG_S FROM ARGDICT
    # for package in PKGS.iteritems():
        # package_name = package[0]

    package_name = 'jruby'
    pkg_arg_s = '"%s" "%s"' % (
        PKGS[package_name]['name'],
        PKGS[package_name]['version'],
        )
    packager.run_script(package_name, 'pkg', pkg_arg_s)

    package_name = 'logstash'
    pkg_arg_s = '"%s" "%s"' % (
        PKGS[package_name]['name'],
        PKGS[package_name]['version'],
        )
    packager.run_script(package_name, 'pkg', pkg_arg_s)

    package_name = 'elasticsearch'
    pkg_arg_s = '"%s" "%s"' % (
        PKGS[package_name]['name'],
        PKGS[package_name]['version'],
        )
    packager.run_script(package_name, 'pkg', pkg_arg_s)

    # package_name = 'workflow-gems'
    # get_arg_s = '"%s" "%s" "%s"' % (
        # PKGS[package_name]['name'],
        # PKGS[package_name]['version'],
        # PKGS[package_name]['source_url']
        # )
    # packager.run_script(package_name, 'get', get_arg_s)

    # package_name = 'python-modules'
    # get_arg_s = '"%s" "%s" "%s"' % (
        # PKGS[package_name]['name'],
        # PKGS[package_name]['version'],
        # PKGS[package_name]['source_url']
        # )
    # packager.run_script(package_name, 'get', get_arg_s)


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
def get(package_name, arg_s=''):
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
