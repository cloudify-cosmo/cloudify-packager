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
# * limitations under the License.
import stat
import tempfile
import urlparse
import os
import time
from socket import gethostbyname
from StringIO import StringIO

import yaml

from cloudify.workflows import local
from test_cli_package import TestCliPackage, fab_env, fab, wait_for_connection
from cloudify_cli import constants as cli_constants

FILE_SERVER_PORT = 8080


class TestOfflineCliPackage(TestCliPackage):
    def _test_cli_package(self):
        """
        Tests cli package in offline mode (Only Linux compatible)
        :return:
        """
        iaas_mapping = '{0} {1}'\
            .format(*self._get_ip_and_netloc(self.iaas_url))

        with self.get_dns():
            self.logger.info('Preparing CLI and downloading example')
            self.prepare_cli()
            example_archive_path = self.get_example(self.helloworld_url)

        self.install_cli()
        self.prepare_manager_blueprint()
        self.prepare_hosts_file(iaas_mapping, self.centos_client_env)

        # Getting the remote manager blueprint and preparing resources
        self.logger.info('Retrieving remote manager blueprint file...')
        resources_to_download = \
            self._get_resource_list(self._get_remote_blueprint())

        with FileServer(self.fileserver_blueprint, self.file_server_inputs,
                        resources_to_download, FILE_SERVER_PORT,
                        self.logger) as fs:
            additional_inputs = fs.get_processed_inputs()
            additional_inputs.update(self.bootstrap_inputs)

            self.prepare_inputs_and_bootstrap(additional_inputs)
            self.manager_fab_conf = {
                'user': 'centos',
                'key_filename': self._get_manager_kp(),
                'host_string': self.manager_ip,
                'timeout': 30,
                'connection_attempts': 10
            }
            self.assert_offline(self.manager_fab_conf, run_on_client=False)

            # Adding iaas resolver for the manager machine.
            self.logger.info('adding {0} to /etc/hosts of the manager vm'
                             .format(iaas_mapping))
            wait_for_connection(self.manager_fab_conf,
                                self._execute_command_on_linux,
                                self.logger)
            self._execute_command_on_linux(
                'echo {0} >> /etc/hosts'.format(iaas_mapping),
                fabric_env=self.manager_fab_conf,
                sudo=True)

            self.logger.info('Testing the example deployment cycle...')

            blueprint_id = \
                self.publish_hello_world_blueprint(example_archive_path)
            self.deployment_id = self.create_deployment(blueprint_id)
            self.addCleanup(self.uninstall_deployment)
            self.install_deployment(self.deployment_id)
            self.assert_deployment_working(
                self._get_app_property('http_endpoint'))

    def _get_yaml_in_temp_file(self, dict_to_write, dict_prefix):
        yaml_to_write = dict_to_write or {}
        yaml_file = tempfile.mktemp(prefix='{0}-'.format(dict_prefix),
                                    suffix='-dict_to_write.json',
                                    dir=self.workdir)
        with open(yaml_file, 'w') as f:
            f.write(yaml.dump(yaml_to_write))
        return yaml_file

    def _get_remote_blueprint(self, env=None):
        env = env or self.centos_client_env
        manager_blueprint = StringIO()
        with fab_env(**env):
            fab.get(self.manager_blueprint_path, manager_blueprint)
        return yaml.load(manager_blueprint.getvalue())

    def prepare_hosts_file(self, iaas_mapping, fabric_env):
        self.update_hosts_file(iaas_mapping, fabric_env)

    def update_hosts_file(self, resolution, fabric_env):
        self._execute_command_on_linux(
            'echo {0} >> /etc/hosts'.format(resolution),
            fabric_env,
            sudo=True)

    def _get_resource_list(self, blueprint):
        """
        Prepares a list of resources required by the manager blueprint.

        :return: A dict of resources to download
        """
        additional_inputs = {}

        inputs = blueprint.get('inputs')
        if inputs:
            for section in ['agent_package_urls', 'plugin_resources',
                            'dsl_resources']:
                additional_inputs[section] = inputs[section]['default']

            additional_inputs.update(self._get_modules_and_components(inputs))

        return additional_inputs

    def _get_modules_and_components(self, inputs):
        """
        Creates a dictionary of modules and components needed by the manager.
        :param inputs: inputs section of the manager blueprint
        :return: a dict of the cloudfiy modules and external components urls
        """
        resources = {}
        for k, v in inputs.items():
            if urlparse.urlsplit(str(v.get('default', ''))).scheme:
                resources[k] = v['default']
        return resources

    def get_example(self, example_url):
        """
        Retrieves hello_world blueprint
        :return: the name of the package on the cli vm.
        """
        self.logger.info('Downloading hello-world example '
                         'from {0} onto the cli vm'
                         .format(example_url))

        self._get_resource(example_url, curl_ops='-LOk')

        return os.path.basename(example_url)

    def _get_ip_and_netloc(self, url):
        """
        Receives an url and translate the netloc part (portless) to an ip, and
        retrieves a tuple with the source netloc and the translated ip
        :param url: the url to resolve
        :return: (original netloc, ip netloc)
        """
        netloc = urlparse.urlsplit(url).netloc
        url_base = netloc.split(':')[0] if ':' in netloc else netloc
        return gethostbyname(url_base), url_base

    def _get_manager_kp(self):
        """
        Retrieves manager kp to the local machine.
        :return: path to the local manager kp.
        """
        remote_manager_kp_path = self.bootstrap_inputs['ssh_key_filename']
        with fab_env(**self.centos_client_env):
            local_manager_kp = fab.get(remote_manager_kp_path, self.workdir)[0]
        os.chmod(local_manager_kp, stat.S_IRUSR | stat.S_IWUSR)
        return local_manager_kp

    def _get_agent_kp(self):
        """
        Retrieves manager kp to the local machine.
        :return: path to the local manager kp.
        """
        remote_agent_kp_path = \
            self.bootstrap_inputs['agent_private_key_path']
        with fab_env(**self.centos_client_env):
            local_agent_kp = fab.get(remote_agent_kp_path, self.workdir)[0]
        os.chmod(local_agent_kp, stat.S_IRUSR | stat.S_IWUSR)
        return local_agent_kp

    @property
    def file_server_inputs(self):
        """
        Returns inputs for the file server vm.
        :return: inputs for the file server vm.
        """
        return {
            'prefix': '{0}-FileServer'.format(self.prefix),
            'external_network': self.env.external_network_name,
            'os_username': self.env.keystone_username,
            'os_password': self.env.keystone_password,
            'os_tenant_name': self.env.keystone_tenant_name,
            'os_region': self.env.region,
            'os_auth_url': self.env.keystone_url,
            'image_name': self.env.centos_7_image_id,
            'flavor': self.env.medium_flavor_id,
            'key_pair_path': '{0}/{1}-keypair-FileServer.pem'
                             .format(self.workdir, self.prefix)
        }

    @property
    def fileserver_blueprint(self):
        return 'test-os-fileserver-vm-blueprint.yaml'


class FileServer(object):
    def __init__(self, fileserver_blueprint, inputs, resources, port, logger):
        """
        A class which manager a file server vm.

        :param inputs: the server vm credentials
        :param resources: a dict of resources to put on the filer server.
        :param port: the port for the file server to start on.
        :param logger: for logging purposes only.
        :return:
        """
        self.inputs = inputs
        self.port = port
        self.logger = logger
        self.resources = resources
        self.fileserver_path = 'File-Server'
        self.blueprint = fileserver_blueprint
        self.blueprint_path = os.path.join(os.path.dirname(__file__),
                                           'resources', self.blueprint)
        self.server_cmd = 'python -m SimpleHTTPServer {0}'.format(self.port)
        self.fs_base_url = None
        self.local_env = None
        self.processed_inputs = None
        self.fab_env_conf = {}

    def boot(self):
        """
        Boots up the file server vm.
        :return:
        """
        self.logger.info('Initializing file server env')
        self.local_env = local.init_env(self.blueprint_path,
                                        inputs=self.inputs,
                                        name='File-Server',
                                        ignored_modules=cli_constants.
                                        IGNORED_LOCAL_WORKFLOW_MODULES)

        self.logger.info('Starting up a file server vm')
        self.local_env.execute('install', task_retries=40,
                               task_retry_interval=30)

        self.fab_env_conf = {
            'user': 'centos',
            'key_filename': self.inputs['key_pair_path'],
            'host_string': self.local_env.outputs()['vm_public_ip_address'],
            'timeout': 30,
            'connection_attempts': 10,
            'abort_on_prompts': True
        }

        self.fs_base_url = '{0}:{1}'.format(self.fab_env_conf['host_string'],
                                            FILE_SERVER_PORT)
        wait_for_connection(self.fab_env_conf,
                            self._execute_command,
                            self.logger)

    def process_resources(self):
        """
        A helper method which calls the _process_resources method.
        :return: a list of processed resources.
        """
        self.processed_inputs = self._process_resources(self.resources)
        return self.processed_inputs

    def _process_resources(self, resources):
        """
        Downloads the specified resources and returns the translated resources
        dict.
        :param resources: the resources to download and process.
        :return: a dict of translated resources
        """
        section = {}
        for k, v in resources.items():
            if isinstance(v, dict):
                section[k] = self._process_resources(v)
            elif isinstance(v, list):
                new_list = []
                for entry in v:
                    if isinstance(entry, basestring):
                        new_list.append(self._process_resource(entry))
                    else:
                        new_list.append(self._process_resources(entry))
                section[k] = new_list
            else:
                url_parts = urlparse.urlsplit(v)
                if url_parts.scheme:
                    section[k] = self._process_resource(v)
                else:
                    section[k] = v

        return section

    def _process_resource(self, url):
        """
        Downloads the supplied resource to the file server and returns an url
        on the file server
        :param url: the url of the resource to download
        :return: a new url on the file server.
        """
        url_parts = urlparse.urlsplit(url)
        rel_path = url_parts.path[1:]
        fs_path = os.path.join(self.fileserver_path, rel_path)
        self.logger.info('Downloading {0} to {1}'.format(url, fs_path))
        self._execute_command(
            'curl --create-dirs -Lo {0} {1}'
            .format(fs_path, url), retries=2)
        url = url.replace(url_parts.netloc, self.fs_base_url)
        url = url.replace(url_parts.scheme, 'http')
        return url

    def teardown(self):
        """
        tears down the file server vm
        :return:
        """
        self.logger.info('Tearing down file server vm')
        self.local_env.execute('uninstall', task_retries=40,
                               task_retry_interval=30)

    def run(self):
        """
        Starts up the file server service on the running vm
        :return:
        """
        # Needed in order to start the file server in detached mode.
        self._execute_command(
            'yum install -y screen',
            sudo=True,
            retries=5)

        self.logger.info('Starting up SimpleHTTPServer on {0}'
                         .format(self.port))
        self._execute_command('cd {0} && screen -dm {1}'
                              .format(self.fileserver_path,
                                      self.server_cmd),
                              pty=False)

    def stop(self):
        """
        stops the file server service
        :return:
        """
        self.logger.info('Shutting down SimpleHTTPServer')
        stop_cmd = "pkill -9 -f '{0}'".format(self.server_cmd)
        self._execute_command(stop_cmd)

    def get_processed_inputs(self):
        """
        Retrieves the list of translated resources urls.
        :return:
        """
        return self.processed_inputs

    def _execute_command(
            self,
            cmd,
            sudo=False,
            pty=True,
            log_cmd=True,
            retries=0,
            warn_only=False,
            **_):
        """
        Executed the given command on the file server vm.

        :param cmd: the command to execute.
        :param sudo: whether to use sudo or not.
        :param pty: passed as an arg to fabric run/sudo.
        :param log_cmd: Specifies whether to log the command executing.
        :param retries: number of command retries.
        :return:
        """
        if log_cmd:
            self.logger.info('Executing command: {0}'.format(cmd))
        else:
            self.logger.info('Executing command: ***')

        with fab_env(**self.fab_env_conf):
            while True:
                if sudo:
                    out = fab.sudo(cmd, pty=pty, warn_only=warn_only)
                else:
                    out = fab.run(cmd, pty=pty, warn_only=warn_only)

                self.logger.info("""Command execution result:
        Status code: {0}
        STDOUT:
        {1}
        STDERR:
        {2}""".format(out.return_code, out, out.stderr))
                if out.succeeded or (warn_only and retries == 0):
                    return out
                else:
                    if retries > 0:
                        time.sleep(30)
                        retries -= 1
                    else:
                        raise Exception('Command: {0} exited with code: '
                                        '{1}. Tried {2} times.'
                                        .format(cmd, out.return_code,
                                                retries + 1))

    def __enter__(self):
        """
        Starts up the file server.
        :return: File server object
        """
        self.boot()
        self.process_resources()
        self.run()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Teardown the file server.
        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return:
        """
        if any([exc_type, exc_val, exc_tb]):
            self.teardown()
        else:
            try:
                self.stop()
            finally:
                self.teardown()
        return False
