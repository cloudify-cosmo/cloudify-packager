########
# Copyright (c) 2015 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
#    * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    * See the License for the specific language governing permissions and
#    * limitations under the License.


import base64
import os
import socket
import time
import json

import winrm

from test_cli_package import TestCliPackage


WINRM_PORT = 5985
CLI_PACKAGE_EXE = 'windows-cli-package.exe'
HELLO_WORLD_URL = 'https://github.com/cloudify-cosmo/cloudify-hello-world-example/archive/{0}.zip'  # NOQA
TASK_RETRIES = 20


class TestWindowsBootstrap(TestCliPackage):
    def setUp(self):
        self.session = None
        super(TestWindowsBootstrap, self).setUp()

    def get_package_parameter_name(self):
        return 'WINDOWS_CLI_PACKAGE_URL'

    def get_local_env_blueprint_file_name(self):
        return 'test-windows-bootstrap-blueprint.yaml'

    def get_client_cfy_work_dir(self):
        return 'C:\cloudify-cli'

    def get_local_env_outputs(self):
        self.public_ip_address = \
            self.local_env.outputs()['windows_vm_ip_address']
        self.password = self.local_env.outputs()['windows_vm_password']

    def is_install_plugins(self):
        return True

    def change_to_tarzan_urls(self):
        self._execute_command(
            """
$path = "{0}"
$text = "{1}"
$replace = "{2}"
$content = get-content $path
$content = $content -replace $text, $replace
$content = $content -replace "task_retries: .*$", "task_retries: {3}"
$content > $path""".format(
                self.test_openstack_manager_blueprint_path,
                'http://gigaspaces-repository-eu.s3.amazonaws.com/org',
                'http://tarzan/builds/GigaSpacesBuilds',
                TASK_RETRIES))

    def additional_setup(self):
        if 'BRANCH_NAME_CORE' not in os.environ:
            raise ValueError('BRANCH_NAME_CORE environment variable not set')

        super(TestWindowsBootstrap, self).additional_setup()

        self._wait_for_connection_availability(self.public_ip_address,
                                               WINRM_PORT, 300)

        url = 'http://{0}:{1}/wsman'.format(self.public_ip_address, WINRM_PORT)
        user = 'Admin'
        self.session = winrm.Session(url, auth=(user, self.password))

    def get_image_name(self):
        return self.env.windows_image_name

    def test_windows_cli_package(self):
        self._test_cli_package()

    def _wait_for_connection_availability(self, ip_address, port, timeout=300):
        deadline = time.time() + timeout
        while time.time() < deadline:
            try:
                socket.create_connection((ip_address, port), timeout=10)
                break
            except IOError, e:
                self.logger.info(
                    'Connection to {0}:{1} is not available: {2} - retrying...'
                    .format(ip_address, port, str(e)))
                time.sleep(5)

    def _execute_command(self, cmd, within_cfy_env=False,
                         sudo=False, log_cmd=True, retries=0):
        if within_cfy_env:
            cmd = '{0}\Scripts\cfy.exe {1}'.format(self.cfy_work_dir, cmd)

        if log_cmd:
            self.logger.info('Executing command using winrm: {0}'.format(cmd))
        else:
            self.logger.info('Executing command using winrm: ***')
        r = self.session.run_ps(cmd)
        self.logger.info("""Command execution result:
Status code: {0}
STDOUT:
{1}
STDERR:
{2}""".format(r.status_code, r.std_out, r.std_err))
        if r.status_code != 0:
            raise Exception('Command: {0} exited with code: {1}'.format(
                cmd, r.status_code))
        else:
            return r.std_out

    def install_cli(self):
        wget_cmd = """
$client = New-Object System.Net.WebClient
$url = "{0}"
$file = "{1}"
$client.DownloadFile($url, $file)""".format(self.cli_package_url,
                                            CLI_PACKAGE_EXE)
        self.logger.info(
            'Downloading Windows CLI package from: {0}'.format(
                self.cli_package_url))
        self._execute_command(wget_cmd)
        self.logger.info('Installing CLI...')
        self._execute_command(
            '.\{0} /SILENT /VERYSILENT /SUPPRESSMSGBOXES /DIR="{1}"'
            ''.format(CLI_PACKAGE_EXE, self.cfy_work_dir))  # NOQA
        self.logger.info('Verifying CLI installation...')
        self._execute_command('--version', within_cfy_env=True)

    def add_dns_nameservers_to_manager_blueprint(self, local_modify_script):
        remote_modify_script = '{0}\{1}'.format(self.cfy_work_dir, 'modify.py')
        self.logger.info(
            'Uploading {0} to {1} on manager...'.format(local_modify_script,
                                                        remote_modify_script))
        with open(local_modify_script, 'r') as f:
            modify_script = f.read()

        ps_script = """
$filePath = "{0}"
$s = @"
{1}
"@
$data = [System.Convert]::FromBase64String($s)
set-content -value $data -encoding byte -path $filePath
                """.format(remote_modify_script,
                           base64.b64encode(modify_script))
        self._execute_command(ps_script)
        self.logger.info(
            'Adding DNS name servers to remote manager blueprint...')
        self._execute_command('{0}\Scripts\python.exe {1} {2}'.format(
            self.cfy_work_dir,
            remote_modify_script,
            self.test_openstack_manager_blueprint_path))

    def prepare_manager_blueprint(self):
        manager_blueprints_url = \
            'https://github.com/cloudify-cosmo/cloudify-manager-blueprints/' \
            'archive/{0}.zip'.format(
            self.branch)  # NOQA
        wget_cmd = """
$client = New-Object System.Net.WebClient
$url = "{0}"
$file = "{1}"
$client.DownloadFile($url, $file)
7za x {1} -o{2} -y""".format(
            manager_blueprints_url, 'cloudify-manager-blueprints.zip',
            self.cfy_work_dir)
        self.logger.info(
            'Downloading and extracting cloudify-manager-blueprints from: {0}'
            .format(manager_blueprints_url))
        self._execute_command(wget_cmd)
        self.test_openstack_manager_blueprint_path = \
            '{0}\cloudify-manager-blueprints-{1}\openstack' \
            '\openstack-manager-blueprint.yaml'.format(
            self.cfy_work_dir, self.branch)  # NOQA

        # self.change_to_tarzan_urls()

        self._execute_command("""$inputs = '{0}'
$inputs | Out-File {1}\inputs.json""".format(
            json.dumps(self.bootstrap_inputs),
            self.cfy_work_dir), log_cmd=False)
        self.remote_bootstrap_inputs_path = \
            '{0}\inputs.json'.format(self.cfy_work_dir)

    def prepare_deployment(self):
        deployment_inputs = self.get_deployment_inputs()

        self._execute_command("""$inputs = '{0}'
$inputs | Out-File {1}\deployment-inputs.json""".format(
            json.dumps(deployment_inputs), self.cfy_work_dir))
        self.remote_deployment_inputs_path = \
            '{0}\deployment-inputs.json'.format(self.cfy_work_dir)
