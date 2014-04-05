#!/usr/bin/env python
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

from packager import init_logger

from fabric.api import *  # NOQA
from packager import pack

lgr = init_logger()

# __all__ = ['list']


@task
def pkg_cloudify3():
    """
    ACT:    packages cloudify3
    EXEC:   fab pkg_cloudify3
    """

    pack('cloudify3')


@task
def pkg_cloudify3_components():
    """
    ACT:    packages cloudify3-components
    EXEC:   fab pkg_cloudify3_components
    """

    pack('cloudify3-components')


@task
def pkg_ubuntu_agent():
    """
    ACT:    packages ubuntu agent
    EXEC:   fab pkg_ubuntu_agent
    """

    pack('ubuntu-agent')


@task
def pkg_linux_agent():
    """
    ACT:    packages linux agent
    EXEC:   fab pkg_linux_agent
    """

    pack('linux-agent')


@task
def pkg_graphite():
    """
    ACT:    packages graphite
    EXEC:   fab pkg_graphite
    """

    pack('graphite')


@task
def pkg_virtualenv():
    """
    ACT:    packages virtualenv
    EXEC:   fab pkg_virtualenv
    """

    pack('virtualenv')


@task
def pkg_celery():
    """
    ACT:    packages celery
    EXEC:   fab pkg_celery
    """

    pack('celery')


@task
def pkg_manager():
    """
    ACT:    packages manager
    EXEC:   fab pkg_manager
    """

    pack('manager')


@task
def pkg_curl():
    """
    ACT:    packages curl
    EXEC:   fab pkg_curl
    """

    pack('curl')


@task
def pkg_make():
    """
    ACT:    packages make
    EXEC:   fab pkg_make
    """

    pack('make')


@task
def pkg_ruby():
    """
    ACT:    packages ruby
    EXEC:   fab pkg_ruby
    """

    pack('ruby')


@task
def pkg_workflow_gems():
    """
    ACT:    packages workflow-gems
    EXEC:   fab pkg_workflow_gems
    """

    pack('workflow-gems')


@task
def pkg_cosmo_ui():
    """
    ACT:    packages cosmo ui
    EXEC:   fab pkg_cosmo_ui
    """

    pack('cosmo-ui')


@task
def pkg_nodejs():
    """
    ACT:    packages nodejs
    EXEC:   fab pkg_nodejs
    """

    pack('nodejs')


@task
def pkg_riemann():
    """
    ACT:    packages riemann
    EXEC:   fab pkg_riemann
    """

    pack('riemann')
    # stream_id = str(uuid.uuid1())
    # se(event_origin="cosmo-packager",
    #     event_type="packager.pkg.%s" % package['name'],
    #     event_subtype="started",
    #     event_description='started packaging %s' % package['name'],
    #     event_stream_id=stream_id)

    # se(event_origin="cosmo-packager",
    #     event_type="packager.pkg.%s" % package['name'],
    #     event_subtype="success",
    #     event_description='finished packaging %s' % package['name'],
    #     event_stream_id=stream_id)


@task
def pkg_rabbitmq():
    """
    ACT:    packages rabbitmq
    EXEC:   fab pkg_rabbitmq
    """

    pack('rabbitmq-server')


@task
def pkg_logstash():
    """
    ACT:    packages logstash
    EXEC:   fab pkg_logstash
    """

    pack('logstash')


@task
def pkg_elasticsearch():
    """
    ACT:    packages elasticsearch
    EXEC:   fab pkg_elasticsearch
    """

    pack('elasticsearch')


@task
def pkg_kibana():
    """
    ACT:    packages kibana
    EXEC:   fab pkg_kibana
    """

    pack('kibana3')


@task
def pkg_nginx():
    """
    ACT:    packages nginx
    EXEC:   fab pkg_nginx
    """

    pack('nginx')


@task
def pkg_openjdk():
    """
    ACT:    packages openjdk
    EXEC:   fab pkg_openjdk
    """

    pack('openjdk-7-jdk')


# @task
# def pkg_zlib():
#     """
#     ACT:    packages zlib
#     EXEC:   fab pkg_zlib
#     """

#     create_bootstrap_script(
#         package, package['bootstrap_template'], package['bootstrap_script'])
#     pack(
#         package['src_package_type'],
#         package['dst_package_type'],
#         package['name'],
#         package['sources_path'],
#         '{0}/archives/'.format(package['sources_path']),
#         package['version'],
#         package['bootstrap_script'],
#         package['depends'])

#     if not is_dir(package['package_path']):
#         mkdir(package['package_path'])
#     lgr.debug("isolating debs...")
#     cp('%s/archives/*.deb' % package['sources_path'],
    # package['package_path'])

# @task
# def pkg_gcc():
#     """
#     ACT:    packages gcc
#     EXEC:   fab pkg_gcc
#     """

#     if not is_dir(package['package_path']):
#         mkdir(package['package_path'])
#     lgr.debug("isolating debs...")
#     cp('%s/archives/*.deb' % package['sources_path'],
    # package['package_path'])


def main():

    lgr.debug('VALIDATED!')


if __name__ == '__main__':
    main()
