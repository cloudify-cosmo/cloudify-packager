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
import sys
import unittest
import urllib
import tempfile
from StringIO import StringIO
from mock import MagicMock

sys.path.append('../')
from get_cloudify import InstallerError
import get_cloudify as cli_builder


class CliBuilderUnitTests(unittest.TestCase):
    """Unit tests for functions in get_cloudify.py"""

    def setUp(self):
        self.cli_builder = cli_builder
        self.cli_builder.SUDO = False
        self.cli_builder.IS_VIRTUALENV = False

    def test_validate_urls(self):
        self._validate_url(self.cli_builder.PIP_URL)
        self._validate_url(self.cli_builder.PYCR64_URL)
        self._validate_url(self.cli_builder.PYCR32_URL)

    def _validate_url(self, url):
        try:
            status = urllib.urlopen(url).getcode()
            if not status == 200:
                raise AssertionError('url {} is not valid.'.format(url))
        except:
            raise AssertionError('url {} is not valid.'.format(url))

    def test_run_valid_command(self):
        self.cli_builder.VERBOSE = True
        builder_stdout = StringIO()
        # replacing builder stdout
        self.cli_builder.sys.stdout = builder_stdout
        proc = cli_builder.run('echo just another STDOUT && '
                               '>&2 echo just another STDERR')
        self.assertIn('STDOUT: just another STDOUT',
                      builder_stdout.getvalue(),
                      'expected stdout was not printed')
        self.assertIn('STDERR: just another STDERR',
                      builder_stdout.getvalue(),
                      'expected stderr was not printed')
        builder_stdout.close()
        self.assertEqual(proc.returncode, 0, 'process execution failed')

    def test_run_invalid_command(self):
        self.cli_builder.VERBOSE = True
        builder_stdout = StringIO()
        # replacing builder stdout
        self.cli_builder.sys.stdout = builder_stdout
        cmd = 'this is not a valid command'
        try:
            cli_builder.run(cmd)
            self.fail('command \'{}\' execution was expected to fail'
                      .format(cmd))
        except RuntimeError as e:
            self.assertEqual(e.message, 'failed executing command \'{}\''
                                        .format(cmd))

    def test_install_failed_download(self):
        mock_boom = MagicMock()
        mock_boom.side_effect = StandardError('Boom!')
        self.cli_builder.download_file = mock_boom

        args = ArgsObject()
        args.installpip = 'true'
        args.force = 'false'
        installer = self.cli_builder.CloudifyInstaller(args)
        try:
            installer.install()
            self.fail('installation did not trigger error as expected')
        except InstallerError as e:
            self.assertEqual(e.message, 'failed downloading pip. '
                                        'reason: Boom!')

    def test_install_pip_fail(self):
        self.cli_builder.download_file = MagicMock(return_value=None)

        args = ArgsObject()
        args.pythonpath = 'non_existing_path'
        installer = self.cli_builder.CloudifyInstaller(args)
        try:
            installer.install_pip()
            self.fail('installation did not trigger error as expected')
        except InstallerError as e:
            self.assertEqual(e.message, 'pip installation failed. reason: '
                                        'failed executing command '
                                        '\'non_existing_path get-pip.py\'')

    def test_make_virtualenv_fail(self):
        try:
            self.cli_builder.make_virtualenv('/path/to/dir',
                                             'non_existing_path')
            self.fail('installation did not trigger error as expected')
        except InstallerError as e:
            self.assertEqual(e.message, 'failed creating virtualenv '
                                        '/path/to/dir. reason failed '
                                        'executing command \'virtualenv -p '
                                        'non_existing_path /path/to/dir\'')

    def test_install_non_existing_module(self):
        try:
            self.cli_builder.install_module('nonexisting_module')
            self.fail('installation did not trigger error as expected')
        except InstallerError as e:
            self.assertEqual(e.message, 'module \'nonexisting_module\' '
                                        'installation failed. reason failed '
                                        'executing command \'pip install '
                                        'nonexisting_module\'')

    def test_get_os_props(self):
        os = self.cli_builder.get_os_props()[0]
        supported_os_list = ('windows', 'linux', 'darwin')
        if os.lower() not in supported_os_list:
            self.fail('os prop \'{0}\' should be equal to one of these names: '
                      '{1}'.format(os, supported_os_list))

    def test_download_file(self):
        self.cli_builder.VERBOSE = True
        tmp_file = tempfile.NamedTemporaryFile(delete=True)
        self.cli_builder.download_file('http://www.google.com', tmp_file.name)
        with open(tmp_file.name) as f:
            content = f.readlines()
            self.assertIsNotNone(content)


class ArgsObject(object):
    pass
