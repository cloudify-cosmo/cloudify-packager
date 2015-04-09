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
sys.path.append('../')
import get_cloudify as cli_builder
import unittest
import urllib
from mock import MagicMock
from StringIO import StringIO


class CliBuilderUnitTests(unittest.TestCase):
    """Unit tests for functions in get_cloudify.py"""

    def setUp(self):
        self.cli_builder = cli_builder
        self.installer = self.cli_builder.CloudifyInstaller
        # self.installer.install_pycrypto()

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

    def test_run_command(self):
        self.cli_builder.VERBOSE = True
        builder_stdout = StringIO()
        # replacing builder stdout
        self.cli_builder.sys.stdout = builder_stdout
        proc = cli_builder.run('echo just another STDOUT && '
                               '>&2 echo just another STDERR')

        self.assertIn('STDOUT: just another STDOUT', builder_stdout.getvalue(),
                      'expected stdout was not printed')
        self.assertIn('STDERR: just another STDERR', builder_stdout.getvalue(),
                      'expected stderr was not printed')
        self.assertEqual(proc.returncode, 0, 'process execution failed')

    def test_install_failed_download(self):
        mock_boom = MagicMock()
        mock_boom.side_effect = StandardError('Boom!')
        self.cli_builder.download_file = mock_boom

        args = Object()
        args.installpip = 'true'
        args.force = 'false'
        installer = self.cli_builder.CloudifyInstaller(args)
        try:
            installer.install()
        except StandardError as e:
            self.assertEqual(e.message, 'Boom!')


class Object(object):
    pass
