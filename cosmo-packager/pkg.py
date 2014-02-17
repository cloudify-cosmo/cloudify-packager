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

#!/usr/bin/env python

import logging
import logging.config

import config
# run_env = os.environ['RUN_ENV']
# config = __import__(run_env)

from event_handler import send_event as se
import uuid

import sys
from fabric.api import *  # NOQA
from packager import *  # NOQA
from templgen import *  # NOQA

# __all__ = ['list']

try:
    logging.config.dictConfig(config.PACKAGER_LOGGER)
    lgr = logging.getLogger('packager')
except ValueError:
    sys.exit('could not initiate logger. try sudo...')


@task
def pkg_cloudify3():
    """
    ACT:    packages cloudify3
    EXEC:   fab pkg_cloudify3
    """

    package = get_package_configuration('cloudify3')

    rm('%s/cloudify*' % package['package_dir'])
    create_bootstrap_script(
        package, package['bootstrap_template'], package['bootstrap_script'])
    cp(package['bootstrap_script'], package['package_dir'])
    local('chmod +x %s/*.sh' % package['package_dir'])
    cp(package['conf_dir'], package['package_dir'])
    pack(
        package['src_package_type'], package['dst_package_type'],
        package['name'],
        package['package_dir'], '%s' % package['package_dir'],
        package['version'], depends=package['depends'])

    if not is_dir(package['bootstrap_dir']):
        mkdir(package['bootstrap_dir'])
    lgr.debug("isolating debs...")
    cp('%s/*.deb' % package['package_dir'], package['bootstrap_dir'])


@task
def pkg_cloudify3_components():
    """
    ACT:    packages cloudify3-components
    EXEC:   fab pkg_cloudify3_components
    """

    package = get_package_configuration('cloudify3-components')

    rm('%s/cloudify*' % package['package_dir'])
    create_bootstrap_script(
        package, package['bootstrap_template'], package['bootstrap_script'])
    cp(package['bootstrap_script'], package['package_dir'])
    local('chmod +x %s/*.sh' % package['package_dir'])
    cp(package['conf_dir'], package['package_dir'])
    pack(
        package['src_package_type'], package['dst_package_type'],
        package['name'],
        package['package_dir'], '%s' % package['package_dir'],
        package['version'])

    if not is_dir(package['bootstrap_dir']):
        mkdir(package['bootstrap_dir'])
    lgr.debug("isolating debs...")
    cp('%s/*.deb' % package['package_dir'], package['bootstrap_dir'])


@task
def pkg_graphite():
    """
    ACT:    packages graphite
    EXEC:   fab pkg_graphite
    """

    package = get_package_configuration('graphite')

    rm('%s/archives/*.deb' % package['package_dir'])
    # create_bootstrap_script(
        # package, package['bootstrap_template'], package['bootstrap_script'])
    pack(
        package['src_package_type'], package['dst_package_type'],
        package['name'],
        package['package_dir'], '%s/archives/' % package['package_dir'],
        package['version'], package['bootstrap_script'])

    if not is_dir(package['bootstrap_dir']):
        mkdir(package['bootstrap_dir'])
    lgr.debug("isolating debs...")
    cp('%s/archives/*.deb' % package['package_dir'], package['bootstrap_dir'])


@task
def pkg_virtualenv():
    """
    ACT:    packages virtualenv
    EXEC:   fab pkg_virtualenv
    """

    package = get_package_configuration('virtualenv')

    rm('%s/archives/*.deb' % package['package_dir'])
    create_bootstrap_script(
        package, package['bootstrap_template'], package['bootstrap_script'])
    pack(
        package['src_package_type'], package['dst_package_type'],
        package['name'],
        package['package_dir'], '%s/archives/' % package['package_dir'],
        package['version'], package['bootstrap_script'])

    if not is_dir(package['bootstrap_dir']):
        mkdir(package['bootstrap_dir'])
    lgr.debug("isolating debs...")
    cp('%s/archives/*.deb' % package['package_dir'], package['bootstrap_dir'])


@task
def pkg_celery():
    """
    ACT:    packages celery
    EXEC:   fab pkg_celery
    """

    package = get_package_configuration('celery')

    rm('%s/archives/*.deb' % package['package_dir'])
    create_bootstrap_script(
        package, package['bootstrap_template'], package['bootstrap_script'])
    pack(
        package['src_package_type'], package['dst_package_type'],
        package['name'],
        package['package_dir'], '%s/archives/' % package['package_dir'],
        package['version'], package['bootstrap_script'])

    if not is_dir(package['bootstrap_dir']):
        mkdir(package['bootstrap_dir'])
    lgr.debug("isolating debs...")
    cp('%s/archives/*.deb' % package['package_dir'], package['bootstrap_dir'])


@task
def pkg_manager():
    """
    ACT:    packages manager
    EXEC:   fab pkg_manager
    """

    package = get_package_configuration('manager')

    rm('%s/archives/*.deb' % package['package_dir'])
    create_bootstrap_script(
        package, package['bootstrap_template'], package['bootstrap_script'])
    pack(
        package['src_package_type'], package['dst_package_type'],
        package['name'],
        package['package_dir'], '%s/archives/' % package['package_dir'],
        package['version'], package['bootstrap_script'], package['depends'])

    if not is_dir(package['bootstrap_dir']):
        mkdir(package['bootstrap_dir'])
    lgr.debug("isolating debs...")
    cp('%s/archives/*.deb' % package['package_dir'], package['bootstrap_dir'])


@task
def pkg_make():
    """
    ACT:    packages make
    EXEC:   fab pkg_make
    """

    package = get_package_configuration('make')

    if not is_dir(package['bootstrap_dir']):
        mkdir(package['bootstrap_dir'])
    lgr.debug("isolating debs...")
    cp('%s/archives/*.deb' % package['package_dir'], package['bootstrap_dir'])


@task
def pkg_ruby():
    """
    ACT:    packages ruby
    EXEC:   fab pkg_ruby
    """

    package = get_package_configuration('ruby')

    create_bootstrap_script(
        package, package['bootstrap_template'], package['bootstrap_script'])
    pack(
        package['src_package_type'], package['dst_package_type'],
        package['name'],
        package['package_dir'], '%s/archives/' % package['package_dir'],
        package['version'], package['bootstrap_script'], package['depends'])

    if not is_dir(package['bootstrap_dir']):
        mkdir(package['bootstrap_dir'])
    lgr.debug("isolating debs...")
    cp('%s/archives/*.deb' % package['package_dir'], package['bootstrap_dir'])


@task
def pkg_workflow_gems():
    """
    ACT:    packages workflow-gems
    EXEC:   fab pkg_workflow_gems
    """

    package = get_package_configuration('workflow-gems')

    create_bootstrap_script(
        package, package['bootstrap_template'], package['bootstrap_script'])
    pack(
        package['src_package_type'], package['dst_package_type'],
        package['name'],
        package['package_dir'], '%s/archives/' % package['package_dir'],
        package['version'], package['bootstrap_script'], package['depends'])

    if not is_dir(package['bootstrap_dir']):
        mkdir(package['bootstrap_dir'])
    lgr.debug("isolating debs...")
    cp('%s/archives/*.deb' % package['package_dir'], package['bootstrap_dir'])


@task
def pkg_cosmo_ui():
    """
    ACT:    packages cosmo ui
    EXEC:   fab pkg_cosmo_ui
    """

    package = get_package_configuration('cosmo-ui')

    rm('%s/archives/*.deb' % package['package_dir'])
    create_bootstrap_script(
        package, package['bootstrap_template'], package['bootstrap_script'])
    pack(
        package['src_package_type'], package['dst_package_type'],
        package['name'],
        package['package_dir'], '%s/archives/' % package['package_dir'],
        package['version'], package['bootstrap_script'], package['depends'])

    if not is_dir(package['bootstrap_dir']):
        mkdir(package['bootstrap_dir'])
    lgr.debug("isolating debs...")
    cp('%s/archives/*.deb' % package['package_dir'], package['bootstrap_dir'])


@task
def pkg_nodejs():
    """
    ACT:    packages nodejs
    EXEC:   fab pkg_nodejs
    """

    package = get_package_configuration('nodejs')

    if not is_dir(package['bootstrap_dir']):
        mkdir(package['bootstrap_dir'])
    lgr.debug("isolating debs...")
    cp('%s/archives/*.deb' % package['package_dir'], package['bootstrap_dir'])


@task
def pkg_riemann():
    """
    ACT:    packages riemann
    EXEC:   fab pkg_riemann
    """

    package = get_package_configuration('riemann')

    stream_id = str(uuid.uuid1())
    se(event_origin="cosmo-packager",
        event_type="packager.pkg.%s" % package['name'],
        event_subtype="started",
        event_description='started packaging %s' % package['name'],
        event_stream_id=stream_id)

    if not is_dir(package['bootstrap_dir']):
        mkdir(package['bootstrap_dir'])
    lgr.debug("isolating debs...")
    cp('%s/*.deb' % package['package_dir'], package['bootstrap_dir'])

    se(event_origin="cosmo-packager",
        event_type="packager.pkg.%s" % package['name'],
        event_subtype="success",
        event_description='finished packaging %s' % package['name'],
        event_stream_id=stream_id)


@task
def pkg_rabbitmq():
    """
    ACT:    packages rabbitmq
    EXEC:   fab pkg_rabbitmq
    """

    package = get_package_configuration('rabbitmq-server')

    if not is_dir(package['bootstrap_dir']):
        mkdir(package['bootstrap_dir'])
    lgr.debug("isolating debs...")
    cp('%s/archives/*.deb' % package['package_dir'], package['bootstrap_dir'])


@task
def pkg_logstash():
    """
    ACT:    packages logstash
    EXEC:   fab pkg_logstash
    """

    package = get_package_configuration('logstash')

    rm('%s/archives/*.deb' % package['package_dir'])
    create_bootstrap_script(
        package, package['bootstrap_template'], package['bootstrap_script'])
    pack(
        package['src_package_type'], package['dst_package_type'],
        package['name'],
        package['package_dir'], '%s/archives/' % package['package_dir'],
        package['version'], package['bootstrap_script'], package['depends'])

    if not is_dir(package['bootstrap_dir']):
        mkdir(package['bootstrap_dir'])
    lgr.debug("isolating debs...")
    cp('%s/archives/*.deb' % package['package_dir'], package['bootstrap_dir'])


@task
def pkg_elasticsearch():
    """
    ACT:    packages elasticsearch
    EXEC:   fab pkg_elasticsearch
    """

    package = get_package_configuration('elasticsearch')

    rm('%s/archives/*.deb' % package['package_dir'])
    create_bootstrap_script(
        package, package['bootstrap_template'], package['bootstrap_script'])
    pack(
        package['src_package_type'], package['dst_package_type'],
        package['name'],
        package['package_dir'], '%s/archives/' % package['package_dir'],
        package['version'], package['bootstrap_script'], package['depends'])

    if not is_dir(package['bootstrap_dir']):
        mkdir(package['bootstrap_dir'])
    lgr.debug("isolating debs...")
    cp('%s/archives/*.deb' % package['package_dir'], package['bootstrap_dir'])


@task
def pkg_kibana():
    """
    ACT:    packages kibana
    EXEC:   fab pkg_kibana
    """

    package = get_package_configuration('kibana3')

    rm('%s/archives/*.deb' % package['package_dir'])
    create_bootstrap_script(
        package, package['bootstrap_template'], package['bootstrap_script'])
    pack(
        package['src_package_type'], package['dst_package_type'],
        package['name'],
        package['package_dir'], '%s/archives/' % package['package_dir'],
        package['version'], package['bootstrap_script'], package['depends'])

    if not is_dir(package['bootstrap_dir']):
        mkdir(package['bootstrap_dir'])
    lgr.debug("isolating debs...")
    cp('%s/archives/*.deb' % package['package_dir'], package['bootstrap_dir'])


@task
def pkg_nginx():
    """
    ACT:    packages nginx
    EXEC:   fab pkg_nginx
    """

    package = get_package_configuration('nginx')

    if not is_dir(package['bootstrap_dir']):
        mkdir(package['bootstrap_dir'])
    lgr.debug("isolating debs...")
    cp('%s/archives/*.deb' % package['package_dir'], package['bootstrap_dir'])


@task
def pkg_openjdk():
    """
    ACT:    packages openjdk
    EXEC:   fab pkg_openjdk
    """

    package = get_package_configuration('openjdk-7-jdk')

    if not is_dir(package['bootstrap_dir']):
        mkdir(package['bootstrap_dir'])
    lgr.debug("isolating debs...")
    cp('%s/archives/*.deb' % package['package_dir'], package['bootstrap_dir'])


def main():

    lgr.debug('VALIDATED!')


if __name__ == '__main__':
    main()
