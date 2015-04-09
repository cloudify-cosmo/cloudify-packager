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
import unittest
import cli_builer.get_cloudify as cli_bulider
import urllib
from mock import MagicMock



class CliBuilderUnitTests(unittest.TestCase):
    """Unit tests for functions in get_cloudify.py"""

    def setUp(self):
        self.installer = cli_bulider.CloudifyInstaller
        self.installer.install_pycrypto()

    def test_validate_urls(self):
        self._validate_url(cli_bulider.PIP_URL)

        self._validate_url(cli_bulider.PYCR64_URL)

        self._validate_url(cli_bulider.PYCR32_URL)

    def _validate_url(self, url):
        try:
            status = urllib.urlopen(url).getcode()
            if not status == 200:
                raise AssertionError('url {} is not valid.'.format(url))
        except:
            raise AssertionError('url {} is not valid.'.format(url))

    def test_run_command(self):
        cli_bulider.VERBOSE = True
        stdout = cli_bulider.run('echo just another STDOUT')
        self.assertEqual(stdout, )
        stderr = cli_bulider.run('>&2 echo just another STDERR')
