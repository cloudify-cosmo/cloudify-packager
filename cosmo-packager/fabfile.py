"""
PROVIDE DOCUMENTATION LINK
"""

from fabric.api import *
import packager

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


#ACTIONS

@task
def create(package_name):
    """
    ACT:    creates a package
    ARGS:   package_name = name of package to create
    EXEC:   fab create:package_name
    """

    packager.create_package(package_name)
