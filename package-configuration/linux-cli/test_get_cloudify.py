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
import urllib
import tempfile
from StringIO import StringIO
from mock import MagicMock
import shutil
import os
import tarfile


get_cloudify = __import__("get-cloudify")

cloudify_cli_url = \
    'https://github.com/cloudify-cosmo/cloudify-cli/archive/master.tar.gz'


class CliBuilderUnitTests(testtools.TestCase):
    """Unit tests for functions in get_cloudify.py"""

    def setUp(self):
        super(CliBuilderUnitTests, self).setUp()
        self.get_cloudify = get_cloudify
        self.get_cloudify.IS_VIRTUALENV = False

    def _create_dummy_requirements_tar(self, destination):
        tempdir = os.path.dirname(destination)
        fpath = self._generate_requirements_file(tempdir)
        try:
            tar = tarfile.open(name=destination, mode='w:gz')
            tar.add(name=tempdir, arcname='maindir')
            tar.close()
        finally:
            os.remove(fpath)
        return destination

    def _generate_requirements_file(self, path):
        fpath = os.path.join(path, 'dev-requirements.txt')
        with open(fpath, 'w') as f:
            f.write('sh==1.11\n')
        return fpath

    def test_validate_urls(self):
        self._validate_url(self.get_cloudify.PIP_URL)
        self._validate_url(self.get_cloudify.PYCR64_URL)
        self._validate_url(self.get_cloudify.PYCR32_URL)

    @staticmethod
    def _validate_url(url):
        try:
            status = urllib.urlopen(url).getcode()
            if not status == 200:
                raise AssertionError('url {} is not valid.'.format(url))
        except:
            raise AssertionError('url {} is not valid.'.format(url))

    def test_run_valid_command(self):
        proc = self.get_cloudify.run('echo Hi!')
        self.assertEqual(proc.returncode, 0, 'process execution failed')

    def test_run_invalid_command(self):
        builder_stdout = StringIO()
        # replacing builder stdout
        self.get_cloudify.sys.stdout = builder_stdout
        cmd = 'this is not a valid command'
        proc = self.get_cloudify.run(cmd)
        self.assertIsNot(proc.returncode, 0, 'command \'{}\' execution was '
                                             'expected to fail'.format(cmd))

    def test_install_pip_failed_download(self):
        installer = self.get_cloudify.CloudifyInstaller()

        mock_boom = MagicMock()
        mock_boom.side_effect = StandardError('Boom!')
        self.get_cloudify.download_file = mock_boom

        mock_false = MagicMock()

        def side_effect():
            return False
        mock_false.side_effect = side_effect
        installer.find_pip = mock_false

        ex = self.assertRaises(SystemExit, installer.install_pip)
        self.assertEqual(
            'Failed downloading pip from {0}. (Boom!)'.format(
                self.get_cloudify.PIP_URL), ex.message)

    def test_install_pip_fail(self):
        self.get_cloudify.download_file = MagicMock(return_value=None)

        pythonpath = 'non_existing_path'
        installer = self.get_cloudify.CloudifyInstaller(pythonpath=pythonpath)

        mock_false = MagicMock()

        def side_effect():
            return False
        mock_false.side_effect = side_effect
        installer.find_pip = mock_false

        ex = self.assertRaises(SystemExit, installer.install_pip)
        self.assertIn('Could not install pip', ex.message)

    def test_make_virtualenv_fail(self):
        ex = self.assertRaises(
            SystemExit, self.get_cloudify.make_virtualenv,
            '/path/to/dir', 'non_existing_path')
        self.assertEqual(
            'Could not create virtualenv: /path/to/dir', ex.message)

    def test_install_non_existing_module(self):
        ex = self.assertRaises(
            SystemExit, self.get_cloudify.install_module, 'nonexisting_module')
        self.assertEqual(
            'Could not install module: nonexisting_module.', ex.message)

    def test_get_os_props(self):
        distro = self.get_cloudify.get_os_props()[0]
        distros = ('ubuntu', 'redhat', 'debian', 'fedora', 'centos',
                   'archlinux')
        if distro.lower() not in distros:
            self.fail('distro prop \'{0}\' should be equal to one of: '
                      '{1}'.format(distro, distros))

    def test_download_file(self):
        self.get_cloudify.VERBOSE = True
        tmp_file = tempfile.NamedTemporaryFile(delete=True)
        self.get_cloudify.download_file('http://www.google.com', tmp_file.name)
        with open(tmp_file.name) as f:
            content = f.readlines()
            self.assertIsNotNone(content)

    def test_check_cloudify_not_installed_in_venv(self):
        tmp_venv = tempfile.mkdtemp()
        try:
            self.get_cloudify.make_virtualenv(tmp_venv, 'python')
            self.assertFalse(
                self.get_cloudify.check_cloudify_installed(tmp_venv))
        finally:
            shutil.rmtree(tmp_venv)

    def test_check_cloudify_installed_in_venv(self):
        tmp_venv = tempfile.mkdtemp()
        try:
            self.get_cloudify.make_virtualenv(tmp_venv, 'python')
            installer = get_cloudify.CloudifyInstaller(virtualenv=tmp_venv)
            installer.execute()
            self.assertTrue(
                self.get_cloudify.check_cloudify_installed(tmp_venv))
        finally:
            shutil.rmtree(tmp_venv)

    def test_get_requirements_from_source_url(self):
        def get(url, destination):
            return self._create_dummy_requirements_tar(destination)

        self.get_cloudify.download_file = get
        try:
            installer = self.get_cloudify.CloudifyInstaller()
            req_list = installer._get_default_requirement_files(
                cloudify_cli_url)
            self.assertEquals(len(req_list), 1)
            self.assertIn('dev-requirements.txt', req_list[0])
        finally:
            self.get_cloudify.download_file = get_cloudify.download_file

    def test_get_requirements_from_source_path(self):
        tempdir = tempfile.mkdtemp()
        self._generate_requirements_file(tempdir)
        try:
            installer = self.get_cloudify.CloudifyInstaller()
            req_list = installer._get_default_requirement_files(tempdir)
            self.assertEquals(len(req_list), 1)
            self.assertIn('dev-requirements.txt', req_list[0])
        finally:
            shutil.rmtree(tempdir)


class TestArgParser(testtools.TestCase):
    """Unit tests for functions in get_cloudify.py"""

    def setUp(self):
        super(TestArgParser, self).setUp()
        self.get_cloudify = get_cloudify
        self.get_cloudify.IS_VIRTUALENV = False

    def test_args_parser_linux(self):
        self.get_cloudify.IS_LINUX = True
        self.get_cloudify.IS_WIN = False
        args = self.get_cloudify.parse_args([])
        self.assertEqual(args.pythonpath, 'python',
                         'wrong default python path {} set for linux'
                         .format(args.pythonpath))
        self.assertFalse(hasattr(args, 'installpycrypto'))
        self.assertTrue(hasattr(args, 'installpythondev'))

    def test_args_parser_windows(self):
        self.get_cloudify.IS_LINUX = False
        self.get_cloudify.IS_WIN = True
        args = self.get_cloudify.parse_args([])
        self.assertEqual(args.pythonpath, 'c:/python27/python.exe',
                         'wrong default python path {} set for win32'
                         .format(args.pythonpath))
        self.assertTrue(hasattr(args, 'installpycrypto'))
        self.assertFalse(hasattr(args, 'installpythondev'))

    def test_default_args(self):
        args = self.get_cloudify.parse_args([])
        self.assertFalse(args.force)
        self.assertFalse(args.forceonline)
        self.assertFalse(args.installpip)
        self.assertFalse(args.installvirtualenv)
        self.assertFalse(args.pre)
        self.assertFalse(args.quiet)
        self.assertFalse(args.verbose)
        self.assertIsNone(args.version)
        self.assertIsNone(args.virtualenv)
        self.assertEqual(args.wheelspath, 'wheelhouse')

    def test_args_chosen(self):
        self.get_cloudify.IS_LINUX = True
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

    def test_mutually_exclude_groups(self):
        # # test with args that do not go together
        ex = self.assertRaises(
            SystemExit, self.get_cloudify.parse_args, ['--version', '--pre'])
        self.assertEqual(2, ex.message)

        ex = self.assertRaises(
            SystemExit, self.get_cloudify.parse_args, ['--verbose', '--quiet'])
        self.assertEqual(2, ex.message)

        ex = self.assertRaises(
            SystemExit, self.get_cloudify.parse_args,
            ['--wheelspath', '--forceonline'])
        self.assertEqual(2, ex.message)


class ArgsObject(object):
    pass
