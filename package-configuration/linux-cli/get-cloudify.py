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

# Install Cloudify on Debian and Ubuntu
# apt-get update
# apt-get install -y curl
# curl -L https://www.dropbox.com/s/ibwdmqhwnf4bewc/get-cloudify.py -o get-cloudify.py && python get-cloudify.py -f  # NOQA

# Install Cloudify on Arch Linux
# pacman -Syu --noconfirm
# pacman-db-upgrade
# pacman -S python2 --noconfirm
# curl -L https://www.dropbox.com/s/ibwdmqhwnf4bewc/get-cloudify.py -o get-cloudify.py && python2 get-cloudify.py -f --pythonpath=python2 # NOQA

# Install Cloudify on CentOS/RHEL
# yum -y update
# yum groupinstall -y development
# yum install -y zlib-dev openssl-devel sqlite-devel bzip2-devel wget gcc tar
# wget http://www.python.org/ftp/python/2.7.6/Python-2.7.6.tgz
# tar -xzvf Python-2.7.6.tgz
# cd Python-2.7.6
# ./configure --prefix=/usr/local && make && make altinstall
# curl -L https://www.dropbox.com/s/ibwdmqhwnf4bewc/get-cloudify.py -o get-cloudify.py && python2.7 get-cloudify.py --pythonpath=python2.7 -f # NOQA

# Install Cloudify on Windows (Python 32/64bit)
# Install Python 2.7.x 32/64bit from https://www.python.org/downloads/release/python-279/  # NOQA
# Make sure that when you install, you choose to add Python to the system path.
# Download the script to any directory
# Run python get-cloudify.py -f


import sys
import subprocess
import argparse
import platform
import os
import urllib
import struct
import tempfile
import logging
import shutil
import time
import tarfile


DESCRIPTION = '''This script attempts(!) to install Cloudify's CLI on Linux,
Windows (with Python32 AND 64), and OS X (Darwin).
On the linux front, it supports Debian/Ubuntu, CentOS/RHEL and Arch.

Note that the script attempts to not be instrusive by forcing the user
to explicitly declare installation of various dependencies.

Installations are supported for both system python, the currently active
virtualenv and a declared virtualenv (using the --virtualenv flag).

If you're already running the script from within a virtualenv and you're not
providing a --virtualenv path, Cloudify will be installed within the virtualenv
you're in.

The script allows you to install requirement txt files when installing from
--source.
If --withrequirements is provided with a value (a URL or path to
a requirements file) it will use it. If it's provided without a value, it
will try to download the archive provided in --source, extract it, and look for
dev-requirements.txt and requirements.txt files within it.

Passing the --wheelspath allows for an offline installation of Cloudify
from predownloaded Cloudify dependency wheels. Note that if wheels are found
within the default wheels directory or within --wheelspath, they will (unless
the --forceonline flag is set) be used instead of performing an online
installation.

The script will attempt to install all necessary requirements including
python-dev and gcc (for Fabric on Linux), pycrypto (for Fabric on Windows),
pip and virtualenv (if --virtualenv was specified) depending on the OS and
Distro you're running on.
Note that to install certain dependencies (like pip or pythondev), you must
run the script as sudo.

It's important to note that even if you're running as sudo, if you're
installing in a declared virtualenv, the script will drop the root privileges
since you probably declared a virtualenv so that it can be installed using
the current user.
Also note, that if you're running with sudo and you have an active virtualenv,
much like any other python script, the installation will occur in the system
python.

By default, the script assumes that the Python executable is in the
path and is called 'python' on Linux and 'c:\python27\python.exe on Windows.
The Python path can be overriden by using the --pythonpath flag.

Please refer to Cloudify's documentation at http://getcloudify.org for
additional information.'''

IS_VIRTUALENV = hasattr(sys, 'real_prefix')

REQUIREMENT_FILE_NAMES = ['dev-requirements.txt', 'requirements.txt']
# TODO: put these in a private storage
PIP_URL = 'https://bootstrap.pypa.io/get-pip.py'
PYCR64_URL = 'http://www.voidspace.org.uk/downloads/pycrypto26/pycrypto-2.6.win-amd64-py2.7.exe'  # NOQA
PYCR32_URL = 'http://www.voidspace.org.uk/downloads/pycrypto26/pycrypto-2.6.win32-py2.7.exe'  # NOQA

PLATFORM = sys.platform
IS_WIN = (PLATFORM == 'win32')
IS_DARWIN = (PLATFORM == 'darwin')
IS_LINUX = (PLATFORM == 'linux2')
# defined below
lgr = None

if not (IS_LINUX or IS_DARWIN or IS_WIN):
    sys.exit('Platform {0} not supported.'.format(PLATFORM))


def init_logger(logger_name):
    logger = logging.getLogger(logger_name)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(fmt='%(asctime)s [%(levelname)s] '
                                      '[%(name)s] %(message)s',
                                  datefmt='%H:%M:%S')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


def run(cmd, suppress_errors=False):
    """Executes a command
    """
    lgr.debug('Executing: {0}...'.format(cmd))
    pipe = subprocess.PIPE
    proc = subprocess.Popen(
        cmd, shell=True, stdout=pipe, stderr=pipe)
    proc.aggr_stdout = ''
    # while the process is still running, print output
    while proc.poll() is None:
        output = proc.stdout.readline()
        if len(output) > 0:
            proc.aggr_stdout += output
            lgr.debug(output)
        time.sleep(0.2)
    output = proc.stdout.readline()
    if len(output) > 0:
        proc.aggr_stdout += output
        lgr.debug(output)
    proc.aggr_stderr = proc.stderr.read()
    if len(proc.aggr_stderr) > 0 and not suppress_errors:
        lgr.error(proc.aggr_stderr)
    return proc


def drop_root_privileges():
    """Drop root privileges

    This is used so that when installing cloudify within a virtualenv
    using sudo, the default behavior will not be to install using sudo
    as a virtualenv is created especially so that users don't have to
    install in the system Python or using a Sudoer.
    """
    # maybe we're not root
    if not os.getuid() == 0:
        return

    lgr.info('Dropping root permissions...')
    os.setegid(int(os.environ.get('SUDO_GID', 0)))
    os.seteuid(int(os.environ.get('SUDO_UID', 0)))


def make_virtualenv(virtualenv_dir, python_path):
    """This will create a virtualenv. If no `python_path` is supplied,
    will assume that `python` is in path. This default assumption is provided
    via the argument parser.
    """
    lgr.info('Creating Virtualenv {0}...'.format(virtualenv_dir))
    result = run('virtualenv -p {0} {1}'.format(python_path, virtualenv_dir))
    if not result.returncode == 0:
        sys.exit('Could not create virtualenv: {0}'.format(virtualenv_dir))


def install_module(module, version=False, pre=False, virtualenv_path=False,
                   wheelspath=False, requirement_files=None, upgrade=False):
    """This will install a Python module.

    Can specify a specific version.
    Can specify a prerelease.
    Can specify a virtualenv to install in.
    Can specify a list of paths or urls to requirement txt files.
    Can specify a local wheelspath to use for offline installation.
    Can request an upgrade.
    """
    lgr.info('Installing {0}...'.format(module))
    pip_cmd = ['pip', 'install']
    if virtualenv_path:
        pip_cmd[0] = os.path.join(
            _get_env_bin_path(virtualenv_path), pip_cmd[0])
    if requirement_files:
        for req_file in requirement_files:
            pip_cmd.extend(['-r', req_file])
    pip_cmd.append(module)
    if version:
        pip_cmd.append(version)
    if wheelspath:
        pip_cmd.extend(
            ['--use-wheel', '--no-index', '--find-links', wheelspath])
    if pre:
        pip_cmd.append('--pre')
    if upgrade:
        pip_cmd.append('--upgrade')
    if IS_VIRTUALENV and not virtualenv_path:
        lgr.info('Installing within current virtualenv: {0}...'.format(
            IS_VIRTUALENV))
    result = run(' '.join(pip_cmd))
    if not result.returncode == 0:
        lgr.error(result.aggr_stdout)
        sys.exit('Could not install module: {0}.'.format(module))


def untar_requirement_files(archive, destination):
    """This will extract requirement files from an archive.
    """
    with tarfile.open(name=archive) as tar:
        req_files = [req_file for req_file in tar.getmembers()
                     if os.path.basename(req_file.name)
                     in REQUIREMENT_FILE_NAMES]
        tar.extractall(path=destination, members=req_files)


def download_file(url, destination):
    lgr.info('Downloading {0} to {1}'.format(url, destination))
    final_url = urllib.urlopen(url).geturl()
    if final_url != url:
        lgr.debug('Redirected to {0}'.format(final_url))
    f = urllib.URLopener()
    f.retrieve(final_url, destination)


def get_os_props():
    distro, _, release = platform.linux_distribution(
        full_distribution_name=False)
    return distro, release


def _get_env_bin_path(env_path):
    """returns the bin path for a virtualenv
    """
    try:
        import virtualenv
        return virtualenv.path_locations(env_path)[3]
    except ImportError:
        # this is a fallback for a race condition in which you're trying
        # to use the script and create a virtualenv from within
        # a virtualenv in which virtualenv isn't installed and so
        # is not importable.
        return os.path.join(env_path, 'scripts' if IS_WIN else 'bin')


class CloudifyInstaller():
    def __init__(self, force=False, upgrade=False, virtualenv='',
                 version='', pre=False, source='', withrequirements='',
                 forceonline=False, wheelspath='wheelhouse',
                 pythonpath='python', installpip=False,
                 installvirtualenv=False, installpythondev=False,
                 installpycrypto=False, os_distro=None, os_release=None,
                 **kwargs):
        self.force = force
        self.upgrade = upgrade
        self.virtualenv = virtualenv
        self.version = version
        self.pre = pre
        self.source = source
        self.withrequirements = withrequirements
        self.force_online = forceonline
        self.wheels_path = wheelspath
        self.python_path = pythonpath
        self.installpip = installpip
        self.installvirtualenv = installvirtualenv
        self.installpythondev = installpythondev
        self.installpycrypto = installpycrypto

        # TODO: we should test all mutually exclusive arguments.
        if not IS_WIN and self.installpycrypto:
            lgr.warning('Pycrypto only relevant on Windows.')
        if not (IS_LINUX or IS_DARWIN) and self.installpythondev:
            lgr.warning('Pythondev only relevant on Linux or OSx.')

        os_props = get_os_props()
        self.distro = os_distro or os_props[0].lower()
        self.release = os_release or os_props[1].lower()

    def execute(self):
        """Installation Logic

        --force argument forces installation of all prerequisites.
        If a wheels directory is found, it will be used for offline
        installation unless explicitly prevented using the --forceonline flag.
        If an offline installation fails (for instance, not all wheels were
        found), an online installation process will commence.
        """
        lgr.debug('Identified Platform: {0}'.format(PLATFORM))
        lgr.debug('Identified Distribution: {0}'.format(self.distro))
        lgr.debug('Identified Release: {0}'.format(self.release))

        module = self.source or 'cloudify'

        if self.force or self.installpip:
            self.install_pip()

        if self.virtualenv:
            if self.force or self.installvirtualenv:
                self.install_virtualenv()
            env_bin_path = _get_env_bin_path(self.virtualenv)

        if IS_LINUX and (self.force or self.installpythondev):
            self.install_pythondev(self.distro)
        if (IS_VIRTUALENV or self.virtualenv) and not IS_WIN:
            # drop root permissions so that installation is done using the
            # current user.
            drop_root_privileges()
        if self.virtualenv:
            if not os.path.isfile(os.path.join(
                    env_bin_path, ('activate.bat' if IS_WIN else 'activate'))):
                make_virtualenv(self.virtualenv, self.python_path)

        if IS_WIN and (self.force or self.installpycrypto):
            self.install_pycrypto(self.virtualenv)

        # if withrequirements is not provided, this will be False.
        # if it's provided without a value, it will be a list.
        if isinstance(self.withrequirements, list):
            self.withrequirements = self.withrequirements \
                or self._get_default_requirement_files(self.source)

        if self.force_online or not os.path.isdir(self.wheels_path):
            install_module(module=module,
                           version=self.version,
                           pre=self.pre,
                           virtualenv_path=self.virtualenv,
                           requirement_files=self.withrequirements,
                           upgrade=self.upgrade)
        elif os.path.isdir(self.wheels_path):
            lgr.info('Wheels directory found: "{0}". '
                     'Attemping offline installation...'.format(
                         self.wheels_path))
            try:
                install_module(module=module,
                               pre=True,
                               virtualenv_path=self.virtualenv,
                               wheelspath=self.wheels_path,
                               requirement_files=self.withrequirements,
                               upgrade=self.upgrade)
            except Exception as ex:
                lgr.warning('Offline installation failed ({0}).'.format(
                    str(ex)))
                install_module(module=module,
                               version=self.version,
                               pre=self.pre,
                               virtualenv_path=self.virtualenv,
                               requirement_files=self.withrequirements,
                               upgrade=self.upgrade)
        if self.virtualenv:
            activate_path = os.path.join(env_bin_path, 'activate')
            activate_command = \
                '{0}.bat'.format(activate_path) if IS_WIN \
                else 'source {0}'.format(activate_path)
            lgr.info('You can now run: "{0}" to activate '
                     'the Virtualenv.'.format(activate_command))

    @staticmethod
    def find_virtualenv():
        try:
            import virtualenv  # NOQA
            return True
        except:
            return False

    def install_virtualenv(self):
        if not self.find_virtualenv():
            lgr.info('Installing virtualenv...')
            install_module('virtualenv')
        else:
            lgr.info('virtualenv is already installed in the path.')

    @staticmethod
    def find_pip():
        try:
            import pip  # NOQA
            return True
        except:
            return False

    def install_pip(self):
        lgr.info('Installing pip...')
        if not self.find_pip():
            try:
                tempdir = tempfile.mkdtemp()
                get_pip_path = os.path.join(tempdir, 'get-pip.py')
                try:
                    download_file(PIP_URL, get_pip_path)
                except StandardError as e:
                    sys.exit('Failed downloading pip from {0}. ({1})'.format(
                             PIP_URL, e.message))
                result = run('{0} {1}'.format(
                    self.python_path, get_pip_path))
                if not result.returncode == 0:
                    sys.exit('Could not install pip')
            finally:
                shutil.rmtree(tempdir)
        else:
            lgr.info('pip is already installed in the path.')

    @staticmethod
    def _get_default_requirement_files(source):
        if os.path.isdir(source):
            return [os.path.join(source, f) for f in REQUIREMENT_FILE_NAMES
                    if os.path.isfile(os.path.join(source, f))]
        else:
            tempdir = tempfile.mkdtemp()
            archive = os.path.join(tempdir, 'cli_source')
            # TODO: need to handle deletion of the temp source dir
            try:
                download_file(source, archive)
            except Exception as ex:
                lgr.error('Could not download {0} ({1})'.format(
                    source, str(ex)))
                sys.exit(1)
            try:
                untar_requirement_files(archive, tempdir)
            except Exception as ex:
                lgr.error('Could not extract {0} ({1})'.format(
                    archive, str(ex)))
                sys.exit(1)
            finally:
                os.remove(archive)
            # GitHub always adds a single parent directory to the tree.
            # TODO: look in parent dir, then one level underneath.
            # the GitHub style tar assumption isn't a very good one.
            req_dir = os.path.join(tempdir, os.listdir(tempdir)[0])
            return [os.path.join(req_dir, f) for f in REQUIREMENT_FILE_NAMES
                    if os.path.isfile(os.path.join(req_dir, f))]

    def install_pythondev(self, distro):
        """Installs python-dev and gcc

        This will try to match a command for your platform and distribution.
        """
        lgr.info('Installing python-dev...')
        if distro in ('ubuntu', 'debian'):
            cmd = 'apt-get install -y gcc python-dev'
        elif distro in ('centos', 'redhat', 'fedora'):
            cmd = 'yum -y install gcc python-devel'
        elif os.path.isfile('/etc/arch-release'):
            # Arch doesn't require a python-dev package.
            # It's already supplied with Python.
            cmd = 'pacman -S gcc --noconfirm'
        elif IS_DARWIN:
            lgr.info('python-dev package not required on Darwin.')
            return
        else:
            sys.exit('python-dev package installation not supported '
                     'in current distribution.')
        run(cmd)

    # Windows only
    def install_pycrypto(self, virtualenv_path):
        """This will install PyCrypto to be used by Fabric.
        PyCrypto isn't compiled with Fabric on Windows by default thus it needs
        to be provided explicitly.
        It will attempt to install the 32 or 64 bit version according to the
        Python version installed.
        """
        # check 32/64bit to choose the correct PyCrypto installation
        is_pyx32 = True if struct.calcsize("P") == 4 else False

        lgr.info('Installing PyCrypto {0}bit...'.format(
            '32' if is_pyx32 else '64'))
        # easy install is used instead of pip as pip doesn't handle windows
        # executables.
        cmd = 'easy_install {0}'.format(PYCR32_URL if is_pyx32 else PYCR64_URL)
        if virtualenv_path:
            cmd = os.path.join(_get_env_bin_path(virtualenv_path), cmd)
        run(cmd)


def check_cloudify_installed(virtualenv_path=None):
    if virtualenv_path:
        result = run(
            os.path.join(_get_env_bin_path(virtualenv_path),
                         'python -c "import cloudify"'),
            suppress_errors=True)
        return result.returncode == 0
    else:
        try:
            import cloudify  # NOQA
            return True
        except ImportError:
            return False


def handle_upgrade(upgrade=False, virtualenv=''):
    if check_cloudify_installed(virtualenv):
        lgr.info('Cloudify is already installed in the path.')
        if upgrade:
            lgr.info('Upgrading...')
        else:
            lgr.error('Use the --upgrade flag to upgrade.')
            sys.exit(1)


def parse_args(args=None):
    class VerifySource(argparse.Action):
        def __call__(self, parser, args, values, option_string=None):
            if not args.source:
                parser.error(
                    '--source is required when calling --withrequirements.')
            setattr(args, self.dest, values)

    parser = argparse.ArgumentParser(
        description=DESCRIPTION, formatter_class=argparse.RawTextHelpFormatter)
    default_group = parser.add_mutually_exclusive_group()
    version_group = parser.add_mutually_exclusive_group()
    online_group = parser.add_mutually_exclusive_group()
    default_group.add_argument('-v', '--verbose', action='store_true',
                               help='Verbose level logging to shell.')
    default_group.add_argument('-q', '--quiet', action='store_true',
                               help='Only print errors.')
    parser.add_argument(
        '-f', '--force', action='store_true',
        help='Force install any requirements (USE WITH CARE!).')
    parser.add_argument(
        '-e', '--virtualenv', type=str,
        help='Path to a Virtualenv to install Cloudify in.')
    version_group.add_argument(
        '--version', type=str,
        help='Attempt to install a specific version of Cloudify.')
    version_group.add_argument(
        '--pre', action='store_true',
        help='Attempt to install the latest Cloudify Milestone.')
    version_group.add_argument(
        '-s', '--source', type=str,
        help='Install from the provided URL or local path.')
    parser.add_argument(
        '-r', '--withrequirements', nargs='*',
        help='Install default or provided requirements file.',
        action=VerifySource)
    parser.add_argument(
        '-u', '--upgrade', action='store_true',
        help='Upgrades Cloudify if already installed.')
    online_group.add_argument(
        '--forceonline', action='store_true',
        help='Even if wheels are found locally, install from PyPI.')
    online_group.add_argument(
        '--wheelspath', type=str, default='wheelhouse',
        help='Path to wheels (defaults to "<cwd>/wheelhouse").')
    if IS_WIN:
        parser.add_argument(
            '--pythonpath', type=str, default='c:/python27/python.exe',
            help='Python path to use (defaults to "c:/python27/python.exe") '
                 'when creating a virtualenv.')
    else:
        parser.add_argument(
            '--pythonpath', type=str, default='python',
            help='Python path to use (defaults to "python") '
                 'when creating a virtualenv.')
    parser.add_argument(
        '--installpip', action='store_true',
        help='Attempt to install pip.')
    parser.add_argument(
        '--installvirtualenv', action='store_true',
        help='Attempt to install Virtualenv.')
    if IS_LINUX:
        parser.add_argument(
            '--installpythondev', action='store_true',
            help='Attempt to install Python Developers Package.')
    elif IS_WIN:
        parser.add_argument(
            '--installpycrypto', action='store_true',
            help='Attempt to install PyCrypto.')
    return parser.parse_args(args)


lgr = init_logger(__file__)


if __name__ == '__main__':
    args = parse_args()
    if args.quiet:
        lgr.setLevel(logging.ERROR)
    elif args.verbose:
        lgr.setLevel(logging.DEBUG)
    else:
        lgr.setLevel(logging.INFO)
    handle_upgrade(args.upgrade, args.virtualenv)

    xargs = ['quiet', 'verbose']
    args = {arg: v for arg, v in vars(args).items() if arg not in xargs}
    installer = CloudifyInstaller(**args)
    installer.execute()
