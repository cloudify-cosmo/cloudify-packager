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
from packager import get_package_configuration as get_conf

lgr = init_logger()

# __all__ = ['list']


@task
def pkg_cloudify3():
    """
    ACT:    packages cloudify3
    EXEC:   fab pkg_cloudify3
    """

    package = get_conf('cloudify3')
    pack(package)


@task
def pkg_cloudify3_components():
    """
    ACT:    packages cloudify3-components
    EXEC:   fab pkg_cloudify3_components
    """

    package = get_conf('cloudify3-components')
    pack(package)


@task
def pkg_ubuntu_agent():
    """
    ACT:    packages ubuntu agent
    EXEC:   fab pkg_ubuntu_agent
    """

    package = get_conf('ubuntu-agent')
    pack(package)


@task
def pkg_linux_agent():
    """
    ACT:    packages linux agent
    EXEC:   fab pkg_linux_agent
    """

    package = get_conf('linux-agent')
    pack(package)


@task
def pkg_graphite():
    """
    ACT:    packages graphite
    EXEC:   fab pkg_graphite
    """

    package = get_conf('graphite')
    pack(package)


@task
def pkg_virtualenv():
    """
    ACT:    packages virtualenv
    EXEC:   fab pkg_virtualenv
    """

    package = get_conf('virtualenv')
    pack(package)


@task
def pkg_celery():
    """
    ACT:    packages celery
    EXEC:   fab pkg_celery
    """

    package = get_conf('celery')
    pack(package)


@task
def pkg_manager():
    """
    ACT:    packages manager
    EXEC:   fab pkg_manager
    """

    package = get_conf('manager')
    pack(package)


@task
def pkg_curl():
    """
    ACT:    packages curl
    EXEC:   fab pkg_curl
    """

    package = get_conf('curl')
    pack(package)


@task
def pkg_make():
    """
    ACT:    packages make
    EXEC:   fab pkg_make
    """

    package = get_conf('make')
    pack(package)


@task
def pkg_ruby():
    """
    ACT:    packages ruby
    EXEC:   fab pkg_ruby
    """

    package = get_conf('ruby')
    pack(package)


@task
def pkg_workflow_gems():
    """
    ACT:    packages workflow-gems
    EXEC:   fab pkg_workflow_gems
    """

    package = get_conf('workflow-gems')
    pack(package)


@task
def pkg_cosmo_ui():
    """
    ACT:    packages cosmo ui
    EXEC:   fab pkg_cosmo_ui
    """

    package = get_conf('cosmo-ui')
    pack(package)


@task
def pkg_nodejs():
    """
    ACT:    packages nodejs
    EXEC:   fab pkg_nodejs
    """

    package = get_conf('nodejs')
    pack(package)


@task
def pkg_riemann():
    """
    ACT:    packages riemann
    EXEC:   fab pkg_riemann
    """

    package = get_conf('riemann')

    # stream_id = str(uuid.uuid1())
    # se(event_origin="cosmo-packager",
    #     event_type="packager.pkg.%s" % package['name'],
    #     event_subtype="started",
    #     event_description='started packaging %s' % package['name'],
    #     event_stream_id=stream_id)

    pack(package)

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

    package = get_conf('rabbitmq-server')
    pack(package)


@task
def pkg_logstash():
    """
    ACT:    packages logstash
    EXEC:   fab pkg_logstash
    """

    package = get_conf('logstash')
    pack(package)


@task
def pkg_elasticsearch():
    """
    ACT:    packages elasticsearch
    EXEC:   fab pkg_elasticsearch
    """

    package = get_conf('elasticsearch')
    pack(package)


@task
def pkg_kibana():
    """
    ACT:    packages kibana
    EXEC:   fab pkg_kibana
    """

    package = get_conf('kibana3')
    pack(package)


@task
def pkg_nginx():
    """
    ACT:    packages nginx
    EXEC:   fab pkg_nginx
    """

    package = get_conf('nginx')
    pack(package)


@task
def pkg_openjdk():
    """
    ACT:    packages openjdk
    EXEC:   fab pkg_openjdk
    """

    package = get_conf('openjdk-7-jdk')
    pack(package)


# @task
# def pkg_zlib():
#     """
#     ACT:    packages zlib
#     EXEC:   fab pkg_zlib
#     """

#     package = get_conf('zlib')

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

#     package = get_conf('gcc')

#     if not is_dir(package['package_path']):
#         mkdir(package['package_path'])
#     lgr.debug("isolating debs...")
#     cp('%s/archives/*.deb' % package['sources_path'],
    # package['package_path'])


def main():

    lgr.debug('VALIDATED!')


if __name__ == '__main__':
    main()
