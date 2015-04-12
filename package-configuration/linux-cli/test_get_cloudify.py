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
import urllib
import tempfile
from StringIO import StringIO
from mock import MagicMock

get_cloudify = __import__("get_cloudify")


class CliBuilderUnitTests(unittest.TestCase):
    """Unit tests for functions in get_cloudify.py"""

    def setUp(self):
        self.get_cloudify = get_cloudify
        self.get_cloudify.SUDO = False
        self.get_cloudify.IS_VIRTUALENV = False

    def test_validate_urls(self):
        self._validate_url(self.get_cloudify.PIP_URL)
        self._validate_url(self.get_cloudify.PYCR64_URL)
        self._validate_url(self.get_cloudify.PYCR32_URL)

    def _validate_url(self, url):
        try:
            status = urllib.urlopen(url).getcode()
            if not status == 200:
                raise AssertionError('url {} is not valid.'.format(url))
        except:
            raise AssertionError('url {} is not valid.'.format(url))

    def test_run_valid_command(self):
        self.get_cloudify.VERBOSE = True
        builder_stdout = StringIO()
        # replacing builder stdout
        self.get_cloudify.sys.stdout = builder_stdout
        proc = get_cloudify.run('echo just another STDOUT && '
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
        self.get_cloudify.VERBOSE = True
        builder_stdout = StringIO()
        # replacing builder stdout
        self.get_cloudify.sys.stdout = builder_stdout
        cmd = 'this is not a valid command'
        proc = get_cloudify.run(cmd)
        self.assertIsNot(proc.returncode, 0, 'command \'{}\' execution was '
                                             'expected to fail'.format(cmd))

    def test_install_pip_failed_download(self):
        mock_boom = MagicMock()
        mock_boom.side_effect = StandardError('Boom!')
        self.get_cloudify.download_file = mock_boom

        args = ArgsObject()
        args.installpip = 'true'
        args.force = 'false'
        installer = self.get_cloudify.CloudifyInstaller(args)
        try:
            installer.execute()
            self.fail('installation did not trigger error as expected')
        except SystemExit as e:
            self.assertEqual(e.message, 'failed downloading pip from '
                                        'https://bootstrap.pypa.io/get-pip.py.'
                                        ' reason: Boom!')

    def test_install_pip_fail(self):
        self.get_cloudify.download_file = MagicMock(return_value=None)

        args = ArgsObject()
        args.pythonpath = 'non_existing_path'
        installer = self.get_cloudify.CloudifyInstaller(args)
        try:
            installer.install_pip()
            self.fail('installation did not trigger error as expected')
        except SystemExit as e:
            self.assertEqual(e.message, 'pip installation failed. reason: '
                                        'failed executing command '
                                        '\'non_existing_path get-pip.py\'')

    def test_make_virtualenv_fail(self):
        try:
            self.get_cloudify.make_virtualenv('/path/to/dir',
                                              'non_existing_path')
            self.fail('installation did not trigger error as expected')
        except SystemExit as e:
            self.assertEqual(e.message,
                             'Could not create virtualenv: /path/to/dir')

    def test_install_non_existing_module(self):
        try:
            self.get_cloudify.install_module('nonexisting_module')
            self.fail('installation did not trigger error as expected')
        except SystemExit as e:
            self.assertEqual(e.message, 'Could not install module: '
                                        'nonexisting_module')

    def test_get_os_props(self):
        os = self.get_cloudify.get_os_props()[0]
        supported_os_list = ('windows', 'linux', 'darwin')
        if os.lower() not in supported_os_list:
            self.fail('os prop \'{0}\' should be equal to one of these names: '
                      '{1}'.format(os, supported_os_list))

    def test_download_file(self):
        self.get_cloudify.VERBOSE = True
        tmp_file = tempfile.NamedTemporaryFile(delete=True)
        self.get_cloudify.download_file('http://www.google.com', tmp_file.name)
        with open(tmp_file.name) as f:
            content = f.readlines()
            self.assertIsNotNone(content)

    def test_args_parser(self):
        self.get_cloudify.OS = 'linux'
        linux_args = self.get_cloudify.parse_args([])
        self.assertEqual(linux_args.pythonpath, 'python',
                         'wrong default python path {} set for linux'
                         .format(linux_args.pythonpath))

        self.get_cloudify.OS = 'windows'
        win_args = self.get_cloudify.parse_args([])
        self.assertEqual(win_args.pythonpath, 'c:/python27/python.exe',
                         'wrong default python path {} set for windows'
                         .format(win_args.pythonpath))

        default_args = self.get_cloudify.parse_args([])
        self.assertFalse(default_args.force)
        self.assertFalse(default_args.forceonline)
        self.assertFalse(default_args.installpip)
        self.assertFalse(default_args.installpycrypto)
        self.assertFalse(default_args.installvirtualenv)
        self.assertFalse(default_args.pre)
        self.assertFalse(default_args.quiet)
        self.assertFalse(default_args.verbose)
        self.assertIsNone(default_args.version)
        self.assertIsNone(default_args.virtualenv)
        self.assertEqual(default_args.wheelspath, 'wheelhouse')

        self.get_cloudify.OS = 'linux'
        set_args = self.get_cloudify.parse_args(['-f',
                                                 '--forceonline',
                                                 '--installpip',
                                                 '--virtualenv=venv_path',
                                                 '--quiet',
                                                 '--version=3.2',
                                                 '--installpip',
                                                 '--installpythondev'])

        self.assertTrue(set_args.force)
        self.assertTrue(set_args.forceonline)
        self.assertTrue(set_args.installpip)
        self.assertTrue(set_args.quiet)
        self.assertEqual(set_args.version, '3.2')
        self.assertEqual(set_args.virtualenv, 'venv_path')

        # test with args that do not go together
        try:
            self.get_cloudify.parse_args(['--version', '--pre'])
            self.fail('args {} iare expected to raise exception'
                      .format(['--version', '--pre']))
        except BaseException as e:
            print e.message

        try:
            self.get_cloudify.parse_args(['--verbose', '--quiet'])
            self.fail('args {} iare expected to raise exception'
                      .format(['--verbose', '--quiet']))
        except BaseException as e:
            print e.message


class ArgsObject(object):
    pass
