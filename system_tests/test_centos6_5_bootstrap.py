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

from fabric.context_managers import cd

from test_cli_package import TestCliPackage


class TestCentos65Bootstrap(TestCliPackage):

    def get_package_parameter_name(self):
        return 'CENTOS_6_5_CLI_PACKAGE_URL'

    def get_image_name(self):
        return self.env.centos_image_name

    def get_client_user(self):
        return self.env.centos_image_user

    # runs on hp, so not changing urls
    def change_to_tarzan_urls(self):
        pass

    def additional_setup(self):
        super(TestCentos65Bootstrap, self).additional_setup()

        self.logger.info('installing python 2.7...')

        self._execute_command('yum -y update', sudo=True)
        self._execute_command('yum install yum-downloadonly wget '
                              'mlocate yum-utils python-devel '
                              'libyaml-devel ruby rubygems '
                              'ruby-devel make gcc git -y'
                              '', sudo=True)
        self._execute_command('yum groupinstall -y \'development '
                              'tools\'', sudo=True)
        self._execute_command('yum install -y zlib-devel bzip2-devel '
                              'openssl-devel xz-libs', sudo=True)
        self._execute_command('curl -LO http://www.python.org/ftp/python/2.7.8'
                              '/Python-2.7.8.tar.xz', sudo=True)
        self._execute_command('xz -d Python-2.7.8.tar.xz', sudo=True)
        self._execute_command('tar -xvf Python-2.7.8.tar', sudo=True)
        with cd('Python-2.7.8'):
            self._execute_command('./configure --prefix=/usr', sudo=True)
            self._execute_command('make', sudo=True)
            self._execute_command('make altinstall', sudo=True)
        self._execute_command('alias python=python2.7', sudo=True)

    def test_centos6_5_cli_package(self):
        self._test_cli_package()
