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
import tempfile
import shutil


get_cloudify = __import__("get-cloudify")


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
        try:
            self.run_get_cloudify('-v -e={0}'.format(tempdir))
        finally:
            shutil.rmtree(tempdir)

    def test_full_cli_install_and_upgrade(self):
        tempdir = tempfile.mkdtemp()
        try:
            self.run_get_cloudify('-v -e={0}'.format(tempdir))
            self.assertRaises(
                SystemExit, self.run_get_cloudify,
                '-v -e={0} --upgrade'.format(tempdir))
        finally:
            shutil.rmtree(tempdir)
