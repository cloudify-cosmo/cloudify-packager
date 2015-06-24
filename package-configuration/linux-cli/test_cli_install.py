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
import tempfile


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
        tempdir = tempfile.mkdtemp()
        self.run_get_cloudify('-f -v -e={0} --nosudo'.format(tempdir))
        p = self.get_cloudify.run('{0}/bin/cfy --version'.format(tempdir))
        self.assertIn('Cloudify CLI 3', p[2])
        shutil.rmtree(tempdir)

    def test_install_from_source(self):
        tempdir = tempfile.mkdtemp()
        self.run_get_cloudify('-s {0} -v -e={1}'.format(
            cloudify_cli_url, tempdir))
        p = self.get_cloudify.run('{0}/bin/cfy --version'.format(tempdir))
        self.assertIn('Cloudify CLI 3', p[2])
        shutil.rmtree(tempdir)
