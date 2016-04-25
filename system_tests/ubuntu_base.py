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


class UbuntuBase(object):

    @property
    def local_env_blueprint_file_name(self):
        return 'test-ec2-linux-vm-blueprint.yaml'

    @property
    def manager_blueprint_file_name(self):
        return 'aws-ec2-manager-blueprint.yaml'

    @property
    def app_blueprint_file(self):
        return 'ec2-blueprint.yaml'

    @property
    def client_cfy_work_dir(self):
        return '/opt/cfy'

    @property
    def region(self):
        return self.env.ec2_region_name

    @property
    def deployment_inputs(self):
        return {
            'image_id': self.env.rhel_7_image_id,
            'instance_type': self.env.medium_instance_type,
            'agent_user': self.env.rhel_7_image_user
        }

    @property
    def bootstrap_inputs(self):
        return {
            'aws_access_key_id': self.env.aws_access_key_id,
            'aws_secret_access_key': self.env.aws_secret_access_key,
            'ec2_region_name': self.env.ec2_region_name,
            'manager_keypair_name': '{0}-manager-keypair'.format(self.prefix),
            'agent_keypair_name': '{0}-agent-keypair'.format(self.prefix),
            'ssh_user': self.env.rhel_7_image_user,
            'agents_user': self.env.rhel_7_image_user,
            'image_id': self.env.rhel_7_image_id,
            'instance_type': self.env.medium_instance_type,
            'ssh_key_filename':
                '~/.ssh/{0}-cloudify-manager-kp.pem'.format(self.prefix),
        }

    @property
    def local_env_inputs(self):
        return {
            'prefix': self.prefix,
            'image_id': self.image_name,
            'instance_type': self.env.medium_instance_type,
            'aws_access_key_id': self.env.aws_access_key_id,
            'aws_secret_access_key': self.env.aws_secret_access_key,
            'ec2_region_name': self.region,
            'key_pair_path': '{0}/{1}-keypair.pem'.format(self.workdir,
                                                          self.prefix)
        }

    @property
    def iaas_url(self):
        return 'ec2.{0}.amazonaws.com'.format(self.env.ec2_region_name)

    def add_dns_nameservers_to_manager_blueprint(self, *args, **kwargs):
        pass


class Ubuntu14Base(UbuntuBase):
    @property
    def client_user(self):
        return self.env.ubuntu_image_user

    @property
    def image_name(self):
        return self.env.ubuntu_trusty_image_id

    @property
    def package_parameter_name(self):
        return 'DEBIAN_CLI_PACKAGE_URL'
