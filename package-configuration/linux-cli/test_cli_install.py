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
import getpass


get_cloudify = __import__("get-cloudify")

cloudify_cli_url = \
    'https://github.com/cloudify-cosmo/cloudify-cli/archive/3.2.tar.gz'


class CliInstallInSystemPythonTests(testtools.TestCase):
    @staticmethod
    def run_get_cloudify(params):
        get_cloudify.install(get_cloudify.parse_args(params.split()))

    def setUp(self):
        if getpass.getuser() != 'travis':
            raise self.skipTest('Not Running in Travis.')
        super(CliInstallInSystemPythonTests, self).setUp()
        self.get_cloudify = get_cloudify

    def test_full_cli_install(self):
        try:
            tempdir = tempfile.mkdtemp()
            self.run_get_cloudify('-f -v'.format(tempdir))
            proc = self.get_cloudify.run(
                '{0}/bin/cfy --version'.format(tempdir))
            self.assertIn('Cloudify CLI 3', proc.aggr_stderr)
        finally:
            shutil.rmtree(tempdir)


class CliInstallTests(testtools.TestCase):
    @staticmethod
    def run_get_cloudify(params):
        get_cloudify.install(get_cloudify.parse_args(params.split()))

    def setUp(self):
        super(CliInstallTests, self).setUp()
        self.get_cloudify = get_cloudify

    def test_full_cli_install(self):
        try:
            tempdir = tempfile.mkdtemp()
            self.run_get_cloudify('-f -v -e={0} --installpip'.format(tempdir))
            proc = self.get_cloudify.run(
                '{0}/bin/cfy --version'.format(tempdir))
            self.assertIn('Cloudify CLI 3', proc.aggr_stderr)
        finally:
            shutil.rmtree(tempdir)

    def test_install_from_source(self):
        tempdir = tempfile.mkdtemp()
        try:
            self.run_get_cloudify('-s {0} -v -e={1}'.format(
                cloudify_cli_url, tempdir))
            proc = self.get_cloudify.run(
                '{0}/bin/cfy --version'.format(tempdir))
            self.assertIn('Cloudify CLI 3', proc.aggr_stderr)
        finally:
            shutil.rmtree(tempdir)

    def test_cli_installed_and_upgrade(self):
        tempdir = tempfile.mkdtemp()
        try:
            self.run_get_cloudify('-v -e={0}'.format(tempdir))
            self.run_get_cloudify('-v -e={0} --upgrade'.format(tempdir))
        finally:
            shutil.rmtree(tempdir)

    def test_cli_installed_and_no_upgrade(self):
        tempdir = tempfile.mkdtemp()
        try:
            self.run_get_cloudify('-v -e={0}'.format(tempdir))
            self.assertRaises(
                SystemExit, self.run_get_cloudify,
                '-v -e={0}'.format(tempdir))
        finally:
            shutil.rmtree(tempdir)

    def test_cli_not_installed_and_upgrade(self):
        tempdir = tempfile.mkdtemp()
        try:
            self.get_cloudify.make_virtualenv(tempdir, 'python')
            self.assertRaises(
                SystemExit, self.run_get_cloudify,
                '-e {0} -v --upgrade'.format(tempdir))
        finally:
            shutil.rmtree(tempdir)
