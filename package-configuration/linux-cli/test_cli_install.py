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
import shutil
import tempfile
import os


get_cloudify = __import__("get-cloudify")

cloudify_cli_url = \
    'https://github.com/cloudify-cosmo/cloudify-cli/archive/3.2.tar.gz'


class CliInstallTests(testtools.TestCase):
    @staticmethod
    def install_cloudify(args):
        installer = get_cloudify.CloudifyInstaller(**args)
        installer.execute()

    def setUp(self):
        super(CliInstallTests, self).setUp()
        self.get_cloudify = get_cloudify

    def test_full_cli_install(self):
        tempdir = tempfile.mkdtemp()
        install_args = {
            'force': True,
            'virtualenv': tempdir,
        }

        try:
            self.install_cloudify(install_args)
            cfy_path = os.path.join(
                self.get_cloudify._get_env_bin_path(tempdir), 'cfy')
            proc = self.get_cloudify.run('{0} --version'.format(cfy_path))
            self.assertIn('Cloudify CLI 3', proc.aggr_stderr)
        finally:
            shutil.rmtree(tempdir)

    def test_install_from_source(self):
        tempdir = tempfile.mkdtemp()
        install_args = {
            'source': cloudify_cli_url,
            'virtualenv': tempdir,
        }

        try:
            self.install_cloudify(install_args)
            cfy_path = os.path.join(
                self.get_cloudify._get_env_bin_path(tempdir), 'cfy')
            proc = self.get_cloudify.run('{0} --version'.format(cfy_path))
            self.assertIn('Cloudify CLI 3', proc.aggr_stderr)
        finally:
            shutil.rmtree(tempdir)

    def test_cli_installed_and_upgrade(self):
        tempdir = tempfile.mkdtemp()
        install_args = {
            'virtualenv': tempdir,
            'upgrade': True
        }

        try:
            self.install_cloudify(install_args)
            self.get_cloudify.handle_upgrade(**install_args)
        finally:
            shutil.rmtree(tempdir)

    def test_cli_installed_and_no_upgrade(self):
        tempdir = tempfile.mkdtemp()
        install_args = {
            'virtualenv': tempdir,
            'upgrade': False
        }

        try:
            self.install_cloudify(install_args)
            ex = self.assertRaises(
                SystemExit, self.get_cloudify.handle_upgrade, **install_args)
            self.assertEqual(1, ex.message)
        finally:
            shutil.rmtree(tempdir)
