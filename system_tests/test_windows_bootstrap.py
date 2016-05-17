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
import os
from contextlib import contextmanager
import socket
import time
import stat
import base64

import winrm
import yaml

from cosmo_tester.framework.util import YamlPatcher
from test_cli_package import TestCliPackage, CHECK_URL
from test_offline_cli_package import TestOfflineCliPackage

WINRM_PORT = 5985
CLI_PACKAGE_EXE = 'windows-cli-package.exe'
TASK_RETRIES = 20


class TestWindowsBase(TestCliPackage):
    def setUp(self):
        self.session = None
        super(TestWindowsBase, self).setUp()

    @property
    def package_parameter_name(self):
        return 'WINDOWS_CLI_PACKAGE_URL'

    @property
    def client_cfy_work_dir(self):
        return 'C:/cloudify-cli'

    @property
    def app_blueprint_file(self):
        return 'ec2-blueprint.yaml'

    @property
    def manager_blueprint_file_name(self):
        return 'aws-ec2-manager-blueprint.yaml'

    @property
    def local_env_blueprint_file_name(self):
        return 'test-ec2-windows-vm-blueprint.yaml'

    @property
    def client_executor(self):
        return self._execute_command_on_windows

    @property
    def iaas_url(self):
        return 'https://ec2.{0}.amazonaws.com'.format(self.env.ec2_region_name)

    @property
    def local_env_inputs(self):
        return {
            'prefix': self.prefix,
            'image_id': self.env.windows_server_2012_r2_image_id,
            'instance_type': self.env.medium_instance_type,
            'aws_access_key_id': self.env.aws_access_key_id,
            'aws_secret_access_key': self.env.aws_secret_access_key,
            'ec2_region_name': self.env.ec2_region_name,
            'key_pair_path': '{0}/{1}-keypair.pem'.format(self.workdir,
                                                          self.prefix)
        }

    @property
    def bootstrap_inputs(self):
        return {
            'aws_access_key_id': self.env.aws_access_key_id,
            'aws_secret_access_key': self.env.aws_secret_access_key,
            'ec2_region_name': self.env.ec2_region_name,
            'manager_keypair_name': '{0}-manager-keypair'.format(self.prefix),
            'agent_keypair_name': '{0}-agent-keypair'.format(self.prefix),
            'manager_security_group_name': '{0}-manager'.format(self.prefix),
            'agent_security_group_name': '{0}-agent'.format(self.prefix),
            'ssh_user': 'centos',
            'ignore_bootstrap_validations': 'true',
            'agents_user': 'centos',
            'image_id': self.env.centos_7_image_id,
            'instance_type': self.env.medium_instance_type,
            'ssh_key_filename': '{0}\\manager-kp.pem'.format(
                self.client_cfy_work_dir),
            'agent_private_key_path': '{0}\\agent-kp.pem'.format(
                self.client_cfy_work_dir)
        }

    @property
    def file_server_inputs(self):
        return {
            'aws_access_key_id': self.env.aws_access_key_id,
            'aws_secret_access_key': self.env.aws_secret_access_key,
            'ec2_region_name': self.env.ec2_region_name,
            'image_id': self.env.centos_7_image_id,
            'instance_type': self.env.medium_instance_type,
            'key_pair_path': '{0}\\fileserver-kp.pem'.format(self.workdir),
            'prefix': '{0}-FileServer'.format(self.prefix)
        }

    @property
    def fileserver_blueprint(self):
        return 'test-ec2-fileserver-vm-blueprint.yaml'

    @property
    def deployment_inputs(self):
        return {
            'image_id': self.env.centos_7_image_id,
            'instance_type': self.env.medium_instance_type,
            'agent_user': 'centos',
        }

    @property
    def image_name(self):
        return self.env.windows_image_name

    @property
    def client_user(self):
        return self.env.windows_server_2012_user

    def prepare_cli(self):
        self.logger.info('Downloading Windows CLI package from: {0}'
                         .format(self.cli_package_url))
        self._get_windows_resource(self.cli_package_url, CLI_PACKAGE_EXE)

    def install_cli(self):
        self.logger.info('Installing CLI...')
        self._execute_command_on_windows(
            '.\{0} /SILENT /VERYSILENT /SUPPRESSMSGBOXES /DIR="{1}"'
            ''.format(CLI_PACKAGE_EXE, self.client_cfy_work_dir))  # NOQA
        self.logger.info('Verifying CLI installation...')
        self.client_executor('--version', within_cfy_env=True)

    @staticmethod
    def _dns_cmdlet(dns_addresses):
        dns_cmdlet = 'Set-DnsClientServerAddress -InterfaceIndex 12 ' \
                     '-ServerAddresses {0}'
        if isinstance(dns_addresses, basestring):
            return dns_cmdlet.format(dns_addresses)
        elif isinstance(dns_addresses, (list, tuple)):
            return dns_cmdlet.format(','.join(dns_addresses))
        else:
            raise SyntaxError('{0} is not a list or a tuple'
                              .format(dns_addresses))

    def get_write_file_script(self,
                              data,
                              remote_file_path,
                              writing_method):
        ps_script = """
$filePath = "{0}"
$s = @"
{1}
"@

$data = [System.Convert]::FromBase64String($s)
{2} -value $data -encoding byte -path $filePath
             """.format(remote_file_path,
                        base64.b64encode(data),
                        writing_method)
        return ps_script

    def get_remote_file(self, remote_file_path, destination_file_name):
        cmd = 'Get-Content {0}'.format(remote_file_path)
        content = self._execute_command_on_windows(cmd)

        with open(destination_file_name, 'w') as f:
            f.write(content)

    def write_file_remotely(self,
                            local_file_path,
                            remote_file_path,
                            chars_per_chunk=500, **kwargs):
        self.logger.info(
            'writing local file from {0} to remote path {1}...'.format(
                local_file_path,
                remote_file_path))
        with open(local_file_path, 'r') as f:
                data = f.read()

        progress_index = 0
        data_chunk = \
            data[progress_index:progress_index + chars_per_chunk]
        writing_method = 'set-content'
        ps_script = self.get_write_file_script(data_chunk,
                                               remote_file_path,
                                               writing_method)
        self._execute_command_on_windows(ps_script)

        writing_method = 'add-content'
        while True:
            progress_index += chars_per_chunk
            data_chunk = \
                data[progress_index:progress_index + chars_per_chunk]
            ps_script = self.get_write_file_script(data_chunk,
                                                   remote_file_path,
                                                   writing_method)

            if not data_chunk:
                break
            self._execute_command_on_windows(ps_script)

    def _execute_command_on_windows(
            self,
            cmd,
            within_cfy_env=False,
            log_cmd=True,
            silent=False,
            warn_only=False,
            *_, **__):
        if within_cfy_env:
            cmd = '{0}\embedded\Scripts\cfy.exe {1}' \
                .format(self.client_cfy_work_dir, cmd)

        if log_cmd:
            self.logger.info('Executing command using winrm: {0}'.format(cmd))
        else:
            self.logger.info('Executing command using winrm: ***')
        r = self.session.run_ps(cmd)
        if not silent:
            self.logger.info("""Command execution result:
Status code: {0}
STDOUT:
{1}
STDERR:
{2}""".format(r.status_code, r.std_out, r.std_err))
        if not warn_only and r.status_code != 0:
            raise Exception('Command: {0} exited with code: {1}'.format(
                            cmd, r.status_code))
        else:
            return r.std_out

    def get_local_env_outputs(self):
        self.public_ip_address = \
            self.local_env.outputs()['vm_public_ip_address']
        self.password = self.local_env.outputs()['windows_vm_password']

    def _get_windows_resource(
            self,
            resource_address,
            resource_destination=None):
        if not resource_destination:
            resource_destination = os.path.basename(resource_address)

        # Downloading the resource
        wget_cmdlet = """
$client = New-Object System.Net.WebClient
$url = "{0}"
$file = "{1}"
$client.DownloadFile($url, $file)""".format(resource_address,
                                            resource_destination)

        self._execute_command_on_windows(wget_cmdlet)
        return resource_destination

    def verify_connection(self):
        # Make sure cli machine ready for incoming connections
        self.wait_for_windows_connection()

    def wait_for_windows_connection(self):
        self._wait_for_connection_availability(self.public_ip_address,
                                               WINRM_PORT, 1200)
        self._establish_session()

    def _wait_for_connection_availability(self, ip_address, port, timeout=300):
        deadline = time.time() + timeout
        while time.time() < deadline:
            try:
                socket.create_connection((ip_address, port), timeout=10)
                return
            except IOError, e:
                self.logger.info(
                    'Connection to {0}:{1} is not available: {2} - retrying...'
                    .format(ip_address, port, str(e)))
                time.sleep(5)
        raise Exception('Connection to {0}:{1} failed'
                        .format(ip_address, port))

    def _establish_session(self):
        url = 'http://{0}:{1}/wsman'.format(self.public_ip_address, WINRM_PORT)
        user = 'Administrator'
        self.session = winrm.Session(url, auth=(user, self.password))

    def _add_dns_on_windows(self, dns_name_servers=('8.8.8.8', '8.8.4.4')):
        self.logger.info('Adding {0} to dns list'.format(dns_name_servers))
        self._execute_command_on_windows(
            self._dns_cmdlet(dns_name_servers),
            silent=True)

    def _remove_dns_on_windows(self, *_):
        self._execute_command_on_windows(
            self._dns_cmdlet('1.1.1.1'),
            silent=True)

    def assert_windows_offline(self):
        out = self._execute_command_on_windows(
            'ping -n 2 {0}'.format(CHECK_URL),
            warn_only=True)
        self.assertIn(
            'Ping request could not find host {0}.'.format(CHECK_URL), out)
        self.assertNotIn('Reply from', out)

    def _manager_ip(self):
        return self._execute_command_on_windows("""
{0}\embedded\python.exe -c "from cloudify_cli import utils;
print utils.get_management_server_ip()"
""".format(self.client_cfy_work_dir)).strip()

    def go_offline(self, *_):
        self._execute_command_on_windows(
            self._dns_cmdlet('1.1.1.1'),
            silent=True)

    def get_dns(self, *args):
        return self.dns_on_windows()

    @contextmanager
    def dns_on_windows(self, dns_name_servers=('8.8.8.8', '8.8.4.4')):
        """
        Enables setting custom dns servers on the local machine.
        This is useful mainly when the bootstrap doesn't contain a
        dns_nameservers.

        :param dns_name_servers: an iterable of dns addresses.
        defaults to ('8.8.8.8', '8.8.4.4').
        :return: None
        """

        self._add_dns_on_windows(dns_name_servers)
        yield
        self._remove_dns_on_windows()
        self.assert_windows_offline()

    def get_example(self, example_url):
        """
        Retrieves hello_world blueprint
        :return: the name of the package on the cli vm.
        """
        self.logger.info('Downloading hello-world example '
                         'from {0} onto the cli vm'
                         .format(example_url))

        self._get_windows_resource(example_url)

        return os.path.basename(example_url)

    def prepare_inputs_and_bootstrap(self, inputs):
        # using inputs file and not passing all inputs in the cmd line
        # prevents "The command line is too long" in windows.
        bootstrap_inputs_path = self.create_inputs_file(
            inputs,
            'bootstrap_inputs')
        self.logger.info('Bootstrapping...')
        self.bootstrap_manager(bootstrap_inputs_path,
                               inputs_is_file=True)


class TestWindowsBootstrap(TestWindowsBase):

    def test_windows_cli_package(self):
        self._add_dns_on_windows()
        self._test_cli_package()

    def add_dns_nameservers_to_manager_blueprint(self, local_modify_script):
        pass


class TestWindowsOfflineBootstrap(TestWindowsBase, TestOfflineCliPackage):

    def test_offline_windows_cli_package(self):
        self._test_cli_package()

    def prepare_hosts_file(self, iaas_mapping, *_):
        self.update_windows_hosts_file(iaas_mapping)

    def update_windows_hosts_file(self, resolution):
        cmd = 'ac -Encoding UTF8  ' \
              'C:\Windows\system32\drivers\etc\hosts "{0}"'.format(resolution)
        self._execute_command_on_windows(cmd)

    def prepare_manager_blueprint(self):
        super(TestWindowsOfflineBootstrap, self).prepare_manager_blueprint()

        mng_blueprint = self._get_remote_blueprint()
        mng_blueprint_yaml = \
            self._get_yaml_in_temp_file(mng_blueprint, 'tmp_userdata_bp')
        # removing dns from the manager host
        user_data = """#!/bin/bash
    echo "" > /etc/resolv.conf
    chattr +i /etc/resolv.conf
    """
        with YamlPatcher(mng_blueprint_yaml) as patcher:
            patcher.set_value('node_templates.manager_host.properties'
                              '.parameters.user_data', user_data)

        self.write_file_remotely(mng_blueprint_yaml,
                                 self.manager_blueprint_path)

    def _get_remote_blueprint(self):
        get_content_cmdlet = \
            "Get-Content {0}".format(self.manager_blueprint_path)
        return yaml.load(self._execute_command_on_windows(
            get_content_cmdlet,
            silent=True))

    def _get_manager_kp(self):
        """
        Retrieves manager kp to the local machine.
        :return: path to the local manager kp.
        """
        remote_manager_kp_path = self.bootstrap_inputs['ssh_key_filename']
        local_manager_kp = os.path.join(self.workdir, 'mng-kp.pem')
        self.get_remote_file(remote_manager_kp_path, local_manager_kp)
        os.chmod(local_manager_kp, stat.S_IRUSR | stat.S_IWUSR)
        return local_manager_kp
