########
# Copyright (c) 2014 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
############
import testtools
import sys
import shutil


get_cloudify = __import__("get-cloudify")

cloudify_cli_url = \
    'https://github.com/cloudify-cosmo/cloudify-cli/archive/3.2.tar.gz'


class CliInstallTests(testtools.TestCase):
    @staticmethod
    def run_get_cloudify(params):
        sys.argv = params.split()
        sys.argv.insert(0, 'get-cloudify')
        get_cloudify.main()

    def setUp(self):
        super(CliInstallTests, self).setUp()
        self.get_cloudify = get_cloudify

    def test_full_cli_install(self):
        self.run_get_cloudify('-f -v -e=/tmp/temp_env/ --nosudo')
        p = self.get_cloudify.run('/tmp/temp_env/bin/cfy --version')
        self.assertIn('Cloudify CLI 3', p.stderr)
        shutil.rmtree('/tmp/temp_env')

    def test_install_from_source(self):
        self.run_get_cloudify('-s {0} -v -e=/tmp/temp_env'.format(
            cloudify_cli_url))
        p = self.get_cloudify.run('/tmp/temp_env/bin/cfy --version')
        self.assertIn('Cloudify CLI 3', p.stderr)
        shutil.rmtree('/tmp/temp_env')
