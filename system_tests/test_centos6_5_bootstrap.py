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
from test_offline_cli_package import TestOfflineCliPackage, env


class TestCentos65Base(object):

    @property
    def package_parameter_name(self):
        return 'CENTOS_6_5_CLI_PACKAGE_URL'

    @property
    def image_name(self):
        return self.env.centos_image_name

    @property
    def client_user(self):
        return self.env.centos_image_user

    @property
    def local_env_blueprint_file_name(self):
        return 'test-start-vm-blueprint.yaml'

    @property
    def client_cfy_work_dir(self):
        return '/opt/cfy'

        # runs on hp, so not changing urls
    def change_to_tarzan_urls(self):
        pass


# The _test_cli_package() remains in the actual test classes for readability.
class TestCentos65Bootstrap(TestCentos65Base, TestCliPackage):

    def additional_setup(self):
        super(TestCentos65Bootstrap, self).additional_setup()
        self.install_python27()

    def test_centos6_5_cli_package(self):
        self.wait_for_vm_to_become_ssh_available(env, self._execute_command)
        with self.dns():
            self._test_cli_package()


class TestCentos65OfflineBootstrap(TestCentos65Base, TestOfflineCliPackage):

    def additional_setup(self):
        super(TestCentos65OfflineBootstrap, self).additional_setup()
        self.install_python27()

    def test_offline_centos6_5_cli_package(self):
        self._test_cli_package()
