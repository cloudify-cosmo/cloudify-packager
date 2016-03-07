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


class CentosBase(object):

    @property
    def local_env_blueprint_file_name(self):
        return 'test-os-linux-vm-blueprint.yaml'

    @property
    def client_cfy_work_dir(self):
        return '/opt/cfy'

    @property
    def manager_blueprint_file_name(self):
        return 'openstack-manager-blueprint.yaml'

    @property
    def app_blueprint_file(self):
        return 'blueprint.yaml'

    @property
    def deployment_inputs(self):
        return {
            'image': self.env.ubuntu_trusty_image_id,
            'agent_user': 'ubuntu',
            'flavor': self.env.medium_flavor_id
        }

    @property
    def bootstrap_inputs(self):
        return {
            'keystone_username': self.env.keystone_username,
            'keystone_password': self.env.keystone_password,
            'keystone_tenant_name': self.env.keystone_tenant_name,
            'keystone_url': self.env.keystone_url,
            'region': self.env.region,
            'image_id': self.env.centos_7_image_id,
            'flavor_id': self.env.medium_flavor_id,
            'external_network_name': self.env.external_network_name,
            'manager_server_name': self.env.management_server_name,
            'management_network_name': self.env.management_network_name,
            'manager_public_key_name': '{0}-manager-keypair'.format(
                self.prefix),
            'ssh_key_filename': '~/.ssh/{0}-cloudify-manager-kp.pem'.format(
                self.prefix),
            'agent_public_key_name': '{0}-agent-keypair'.format(self.prefix)
        }

    @property
    def local_env_inputs(self):
        return {
            'prefix': self.prefix,
            'external_network': self.env.external_network_name,
            'os_username': self.env.keystone_username,
            'os_password': self.env.keystone_password,
            'os_tenant_name': self.env.keystone_tenant_name,
            'os_region': self.env.region,
            'os_auth_url': self.env.keystone_url,
            'image_name': self.image_name,
            'flavor': self.env.medium_flavor_id,
            'key_pair_path': '{0}/{1}-keypair.pem'.format(self.workdir,
                                                          self.prefix)
        }

    @property
    def iaas_url(self):
        return self.bootstrap_inputs['keystone_url']


class Centos7Base(CentosBase):

    @property
    def package_parameter_name(self):
        return 'CENTOS_7_CLI_PACKAGE_URL'

    @property
    def image_name(self):
        return self.env.centos_7_image_name

    @property
    def client_user(self):
        return self.env.centos_7_image_user


class Centos65Base(CentosBase):

    @property
    def package_parameter_name(self):
        return 'CENTOS_6_5_CLI_PACKAGE_URL'

    @property
    def image_name(self):
        return self.env.centos_image_name

    @property
    def client_user(self):
        return self.env.centos_image_user

    def additional_setup(self):
        super(Centos65Base, self).additional_setup()
        self.install_python27()
