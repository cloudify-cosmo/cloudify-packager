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
#    * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    * See the License for the specific language governing permissions and
#    * limitations under the License.

from test_cli_package import TestCliPackage, env
from test_offline_cli_package import TestOfflineCliPackage
from test_rhel_bootstrap import TestRHELBase


class TestRHEL65Base(TestRHELBase):
    @property
    def package_parameter_name(self):
        return 'CENTOS_6_5_CLI_PACKAGE_URL'

    @property
    def manager_blueprint_file_name(self):
        return 'aws-ec2-manager-blueprint.yaml'

    @property
    def local_env_blueprint_file_name(self):
        return 'start-ec2-worker-vm.yaml'

    @property
    def client_user(self):
        return self.env.rhel_7_image_user

    @property
    def image_name(self):
        return self.env.rhel_65_image_id

    def get_local_env_inputs(self):
        return {
            'prefix': self.prefix,
            'image_id': self.image_name,
            'instance_type': self.env.medium_instance_type,
            'aws_access_key_id': self.env.aws_access_key_id,
            'aws_secret_access_key': self.env.aws_secret_access_key,
            'ec2_region_name': self.env.ec2_region_name,
            'key_pair_path': '{0}/{1}-keypair.pem'.format(self.workdir,
                                                          self.prefix)
        }

    def get_bootstrap_inputs(self):
        return {
            'aws_access_key_id': self.env.aws_access_key_id,
            'aws_secret_access_key': self.env.aws_secret_access_key,
            'ec2_region_name': self.env.ec2_region_name,
            'manager_keypair_name': '{0}-manager-keypair'.format(self.prefix),
            'agent_keypair_name': '{0}-agent-keypair'.format(self.prefix),
            'ssh_user': self.env.rhel_7_image_user,
            'agents_user': self.env.rhel_7_image_user,
            'image_id': self.image_name,
            'instance_type': self.env.medium_instance_type,
        }

    def get_deployment_inputs(self):
        return {
            'image_id': self.image_name,
            'instance_type': self.env.medium_instance_type,
            'agent_user': self.env.rhel_7_image_user,
        }


class TestRHEL65(TestRHEL65Base, TestCliPackage):

    def additional_setup(self):
        super(TestRHEL65, self).additional_setup()
        self.install_python27()

    def test_rhel65_cli_package(self):
        self.wait_for_vm_to_become_ssh_available(env, self._execute_command)
        with self.dns():
            self._test_cli_package()


class TestOfflineRHEL65(TestRHEL65Base, TestOfflineCliPackage):

    def additional_setup(self):
        super(TestOfflineRHEL65, self).additional_setup()
        self.install_python27()

    def test_offline_rhel65_cli_package(self):
        self._test_cli_package()
