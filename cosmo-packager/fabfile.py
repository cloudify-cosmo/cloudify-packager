########
# Copyright (c) 2014 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
#    * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    * See the License for the specific language governing permissions and
#    * limitations under the License.

"""
DOCUMENTATION LINK:
https://github.com/CloudifySource/cosmo-packager
"""

from fabric.api import *  # NOQA
from fabric.contrib.files import exists
from packager import *  # NOQA
from get import *  # NOQA
from pkg import *  # NOQA
# import os

# run_env = os.environ['RUN_ENV']
# config = __import__(run_env)

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

    get_openjdk()
    get_curl()
    get_logstash()
    get_elasticsearch()
    get_riemann()
    get_rabbitmq()
    get_nodejs()
    get_nginx()
    get_kibana()
    get_python_modules('virtualenv')
    get_make()
    get_ruby()
    get_workflow_gems()


@task
def get_cosmo():
    """
    ACT:    retrieves cosmo code
    EXEC:   fab get_cosmo_base
    """

    do('sudo apt-get install -y python-dev')
    get_celery(download=True)
    get_manager(download=True)
    # get_cosmo_ui(download=True)


@task
def pkg_cosmo_components():
    """
    ACT:    packages cosmo 3rd parties
    EXEC:   fab pkg_comso_components
    """

    pkg_openjdk()
    pkg_curl()
    pkg_logstash()
    pkg_elasticsearch()
    pkg_riemann()
    pkg_rabbitmq()
    pkg_nodejs()
    pkg_nginx()
    pkg_kibana()
    pkg_virtualenv()
    pkg_make()
    pkg_ruby()


@task
def pkg_cosmo():
    """
    ACT:    packages cosmo code
    EXEC:   fab pkg_comso_base
    """

    pkg_workflow_gems()
    pkg_celery()
    pkg_manager()
    # pkg_cosmo_ui()


@task
def make(more=False, extra=False):

    if extra:
        get_cosmo_components()
        get_cosmo()
    if more:
        pkg_cosmo_components()
        pkg_cosmo()
    pkg_cloudify3_components()
    pkg_cloudify3()
    cp('/cloudify/*.deb', '/vagrant/debs')


@task
def transfer():
    env.user = 'tgrid'
    env.password = 'tgrid'
    server = '192.168.9.228'

    with settings(host_string=server):
        if exists('/opt/cosmo/packages'):
            # put('/cloudify/*.deb', '/opt/cosmo/packages')
            put('/cloudify3/cosmo-ui/*.deb', '/opt/cosmo/packages')
        else:
            print 'wooha!'
