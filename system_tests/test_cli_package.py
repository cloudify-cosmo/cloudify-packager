########
# Copyright (c) 2014 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# * See the License for the specific language governing permissions and
#    * limitations under the License.

import os
import time
import uuid

import requests
from retrying import retry

from cloudify.workflows import local
from cloudify_cli import constants as cli_constants
import fabric.api as fab
from fabric.api import env

from cosmo_tester.framework.testenv import TestCase

HELLO_WORLD_URL = 'https://github.com/cloudify-cosmo/' \
                  'cloudify-hello-world-example/archive/{0}.zip'


class TestCliPackage(TestCase):

    def get_package_parameter_name(self):
        return 'CENTOS_7_CLI_PACKAGE_URL'

    def get_image_name(self):
        return self.env.centos_7_image_name

    def get_cli_package_url(self):
        return os.environ[self.get_package_parameter_name()]

    def get_client_user(self):
        return self.env.centos_7_image_user

    def get_client_cfy_work_dir(self):
        return '/cfy'

    def get_local_env_outputs(self):
        self.public_ip_address = \
            self.local_env.outputs()['vm_public_ip_address']

    def is_install_plugins(self):
        return False

    def additional_setup(self):
        if self.get_package_parameter_name() not in os.environ:
            raise ValueError(
                '{0} environment variable not set'
                ''.format(self.get_package_parameter_name()))

        blueprint_filename = self.get_local_env_blueprint_file_name()
        blueprint_path = os.path.join(os.path.dirname(__file__),
                                      'resources',
                                      blueprint_filename)
        self.prefix = '{0}-cli-host'.format(self.test_id)
        self.bootstrap_prefix = 'cloudify-{0}'.format(self.test_id)
        self.cfy_work_dir = self.get_client_cfy_work_dir()
        self.cli_package_url = self.get_cli_package_url()

        self.inputs = self.get_local_env_inputs()
        self.bootstrap_inputs = self.get_bootstrap_inputs()
        self.deployment_inputs = self.get_deployment_inputs()

        self.branch = os.environ.get('BRANCH_NAME_CORE', 'master')
        self.logger.info('Using branch/tag: {0}'.format(self.branch))

        self.logger.info('initialize local env for running the '
                         'blueprint that starts a vm')
        self.local_env = local.init_env(
            blueprint_path,
            inputs=self.inputs,
            name=self._testMethodName,
            ignored_modules=cli_constants.IGNORED_LOCAL_WORKFLOW_MODULES)

        self.logger.info('starting vm to serve as the management vm')
        self.addCleanup(self.cleanup)
        self.local_env.execute('install',
                               task_retries=40,
                               task_retry_interval=30)

        self.get_local_env_outputs()
        self.logger.info('Outputs: {0}'.format(self.local_env.outputs()))

        env.update({
            'timeout': 30,
            'user': self.get_client_user(),
            'key_filename': self.inputs['key_pair_path'],
            'host_string': self.public_ip_address,
            'connection_attempts': 10
        })

    def get_local_env_inputs(self):
        return {
            'prefix': self.prefix,
            'external_network': self.env.external_network_name,
            'os_username': self.env.keystone_username,
            'os_password': self.env.keystone_password,
            'os_tenant_name': self.env.keystone_tenant_name,
            'os_region': self.env.region,
            'os_auth_url': self.env.keystone_url,
            'image_name': self.get_image_name(),
            'flavor': self.env.medium_flavor_id,
            'key_pair_path': '{0}/{1}-keypair.pem'.format(self.workdir,
                                                          self.prefix)
        }

    def get_bootstrap_inputs(self):
        return {
            'keystone_username': self.env.keystone_username,
            'keystone_password': self.env.keystone_password,
            'keystone_tenant_name': self.env.keystone_tenant_name,
            'keystone_url': self.env.keystone_url,
            'region': self.env.region,
            'image_id': self.env.centos_7_image_id,
            'flavor_id': self.env.medium_flavor_id,
            'external_network_name': self.env.external_network_name,
            'manager_public_key_name': '{0}-manager-keypair'.format(
                self.prefix),
            'agent_public_key_name': '{0}-agent-keypair'.format(
                self.prefix),
        }

    def get_local_env_blueprint_file_name(self):
        return 'test-start-vm-blueprint.yaml'

    def get_deployment_inputs(self):
        return {
            'agent_user': 'ubuntu',
            'image': self.env.ubuntu_trusty_image_id,
            'flavor': self.env.medium_flavor_id
        }

    def setUp(self):
        super(TestCliPackage, self).setUp()
        self.additional_setup()

    def _execute_command(self, cmd, within_cfy_env=False,
                         sudo=False, log_cmd=True, retries=0):
        if within_cfy_env:
            cmd = 'source {0}/env/bin/activate && cfy {1}' \
                  ''.format(self.cfy_work_dir, cmd)

        if log_cmd:
            self.logger.info('Executing command: {0}'.format(cmd))
        else:
            self.logger.info('Executing command: ***')

        while True:
            if sudo:
                out = fab.sudo(cmd)
            else:
                out = fab.run(cmd)

            self.logger.info("""Command execution result:
    Status code: {0}
    STDOUT:
    {1}
    STDERR:
    {2}""".format(out.return_code, out, out.stderr))
            if out.succeeded:
                return out
            else:
                if retries > 0:
                    time.sleep(30)
                    retries -= 1
                else:
                    raise Exception('Command: {0} exited with code: '
                                    '{1}. Tried {2} times.'
                                    ''.format(cmd, out.return_code,
                                              retries + 1))

    def install_cli(self):
        self.logger.info('installing cli...')

        self._execute_command('sudo curl -O {0}'
                              ''.format(self.get_cli_package_url()))
        self._execute_command('curl https://raw.githubusercontent.com/pypa/'
                              'pip/master/contrib/get-pip.py'
                              ' | sudo python2.7 -'
                              '', sudo=True)
        self._execute_command('pip install virtualenv', sudo=True)

        last_ind = self.get_cli_package_url().rindex('/')
        package_name = self.get_cli_package_url()[last_ind + 1:]
        self._execute_command('rpm -i {0}'.format(package_name), sudo=True)

    def change_to_tarzan_urls(self):
        pass

    def add_dns_nameservers_to_manager_blueprint(self, local_modify_script):
        remote_modify_script = os.path.join(self.cfy_work_dir, 'modify.py')
        self.logger.info(
            'Uploading {0} to {1} on manager...'.format(local_modify_script,
                                                        remote_modify_script))
        fab.put(local_modify_script, remote_modify_script, use_sudo=True)
        self.logger.info(
            'Adding DNS name servers to remote manager blueprint...')
        fab.run('sudo python {0} {1}'.format(
            remote_modify_script, self.test_openstack_manager_blueprint_path))

    def prepare_manager_blueprint(self):
        self.manager_blueprints_repo_dir = '{0}/cloudify-manager-blueprints' \
                                           '-commercial/' \
                                           ''.format(self.cfy_work_dir)
        self.test_openstack_manager_blueprint_path = \
            os.path.join(self.manager_blueprints_repo_dir,
                         'new', 'openstack-manager-blueprint.yaml')

        self.local_bootstrap_inputs_path = \
            self.cfy._get_inputs_in_temp_file(self.bootstrap_inputs,
                                              self._testMethodName)
        self.remote_bootstrap_inputs_path = \
            os.path.join(self.cfy_work_dir, 'bootstrap_inputs.json')
        fab.put(self.local_bootstrap_inputs_path,
                self.remote_bootstrap_inputs_path, use_sudo=True)

        self.change_to_tarzan_urls()

    def bootstrap_manager(self):
        self.logger.info('Bootstrapping Cloudify manager...')

        self._execute_command('init', within_cfy_env=True)

        install_plugins = ''
        if self.is_install_plugins():
            install_plugins = '--install-plugins'

        self._execute_command(
            'bootstrap -p {0} -i {1} {2}'.format(
                self.test_openstack_manager_blueprint_path,
                self.remote_bootstrap_inputs_path,
                install_plugins),
            within_cfy_env=True)
        self.addCleanup(self.teardown_manager)

    def publish_hello_world_blueprint(self):
        hello_world_url = HELLO_WORLD_URL.format(self.branch)
        blueprint_id = 'blueprint-{0}'.format(uuid.uuid4())
        self.logger.info(
            'Publishing hello-world example from: {0} [{1}]'.format(
                hello_world_url, blueprint_id))
        self._execute_command('blueprints publish-archive '
                              '-l {0} -n blueprint.yaml -b {1}'
                              ''.format(hello_world_url,
                                        blueprint_id),
                              within_cfy_env=True)
        return blueprint_id

    def prepare_deployment(self):
        self.local_deployment_inputs_path = \
            self.cfy._get_inputs_in_temp_file(self.deployment_inputs,
                                              self._testMethodName)
        self.remote_deployment_inputs_path = \
            os.path.join(self.cfy_work_dir,
                         'deployment_inputs.json')
        fab.put(self.local_deployment_inputs_path,
                self.remote_deployment_inputs_path, use_sudo=True)

    def create_deployment(self, blueprint_id):
        deployment_id = 'deployment-{0}'.format(uuid.uuid4())
        self.prepare_deployment()

        self.logger.info('Creating deployment: {0}'.format(deployment_id))
        self._execute_command(
            'deployments create -b {0} -d {1} -i {2}'
            ''.format(blueprint_id, deployment_id,
                      self.remote_deployment_inputs_path),
            within_cfy_env=True)

        return deployment_id

    def install_deployment(self, deployment_id):
        self.logger.info('Installing deployment...')
        self._execute_command('executions start -d {0} -w install'
                              ''.format(deployment_id),
                              within_cfy_env=True, retries=2)

    def uninstall_deployment(self, deployment_id):
        self.logger.info('Uninstalling deployment...')
        self._execute_command('executions start -d {0} -w uninstall'
                              ''.format(deployment_id), within_cfy_env=True)

    def _test_cli_package(self):
        self.install_cli()
        self.prepare_manager_blueprint()
        self.add_dns_nameservers_to_manager_blueprint(
            os.path.join(os.path.dirname(__file__),
                         'resources/add_nameservers_to_subnet.py'))
        self.bootstrap_manager()
        blueprint_id = self.publish_hello_world_blueprint()
        self.deployment_id = self.create_deployment(blueprint_id)
        self.install_deployment(self.deployment_id)
        self.assert_deployment_working(
            self._get_app_property('http_endpoint'))
        self.uninstall_deployment(self.deployment_id)

    def _get_app_property(self, property_name):

        out = self._execute_command('deployments outputs -d {0}'
                                    ''.format(self.deployment_id),
                                    within_cfy_env=True)
        value_index = out.find('Value:', out.find(property_name))
        property_start = value_index + len('Value:') + 1
        property_end = out.find('\r', property_start)
        if property_end == -1:
            property_end = out.find('\n', property_start)
        if property_end == -1:
            return out[property_start:]
        return out[property_start:property_end]

    @retry(stop_max_attempt_number=3, wait_fixed=3000)
    def assert_deployment_working(self, url):
        nodejs_server_page_response = requests.get(url)
        self.assertEqual(200, nodejs_server_page_response.status_code,
                         'Failed to get home page of app')

    def cleanup(self):
        self.local_env.execute('uninstall',
                               task_retries=40,
                               task_retry_interval=30)

    def teardown_manager(self):
        self.logger.info('Tearing down Cloudify manager...')
        self._execute_command('teardown -f --ignore-deployments',
                              within_cfy_env=True)
