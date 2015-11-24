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

from test_cli_package import TestCliPackage


class TestRHEL(TestCliPackage):

    def _manager_ip(self):
        return self._execute_command(
            'source {0}/env/bin/activate && {1}'.format(
                self.cfy_work_dir,
                'python -c "from cloudify_cli import utils;'
                'print utils.get_management_server_ip()"'
            )
        )

    def get_package_parameter_name(self):
        return 'RHEL_CLI_PACKAGE_URL'

    def get_local_env_blueprint_file_name(self):
        return 'start-ec2-worker-vm.yaml'

    def get_manager_blueprint_file_name(self):
        return 'aws-ec2-manager-blueprint.yaml'

    def get_client_user(self):
        return self.env.rhel_7_image_user

    def get_app_blueprint_file(self):
        return 'ec2-blueprint.yaml'

    def get_local_env_inputs(self):
        return {
            'prefix': self.prefix,
            'image_id': self.env.aws_ec2_eu_west_1_ami_rhel_7_image_id,
            'instance_type': self.env.medium_instance_type,
            'aws_access_key_id': self.env.aws_access_key_id,
            'aws_secret_access_key': self.env.aws_secret_access_key,
            'ec2_region_name': self.env.aws_ec2_eu_west_1_region_name,
            'key_pair_path': '{0}/{1}-keypair.pem'.format(self.workdir,
                                                          self.prefix)
        }

    def get_bootstrap_inputs(self):
        return {
            'aws_access_key_id': self.env.aws_access_key_id,
            'aws_secret_access_key': self.env.aws_secret_access_key,
            'ec2_region_name': self.env.aws_ec2_eu_west_1_region_name,
            'manager_keypair_name': '{0}-manager-keypair'.format(self.prefix),
            'agent_keypair_name': '{0}-agent-keypair'.format(self.prefix),
            'ssh_user': self.env.rhel_7_image_user,
            'agents_user': self.env.rhel_7_image_user,
            'image_id': self.env.aws_ec2_eu_west_1_ami_rhel_7_image_id,
            'instance_type': self.env.medium_instance_type,
        }

    def get_deployment_inputs(self):
        return {
            'image_id': self.env.aws_ec2_eu_west_1_ami_rhel_7_image_id,
            'instance_type': self.env.medium_instance_type,
            'agent_user': self.env.rhel_7_image_user,
        }

    def add_dns_nameservers_to_manager_blueprint(self, *args, **kwargs):
        pass

    def test_rhel7_cli_package(self):
        self._test_cli_package()
