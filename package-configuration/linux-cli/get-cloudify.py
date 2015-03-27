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
# yum install -y zlib-dev openssl-devel sqlite-devel bzip2-devel wget gcc
# wget http://www.python.org/ftp/python/2.7.6/Python-2.7.6.tar.xz
# #optional
# yum install -y xz-libs xz tar
# xz -d Python-2.7.6.tar.xz
# tar -xvf Python-2.7.6.tar
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


DESCRIPTION = '''This script attempts(!) to install Cloudify's CLI on Linux,
Windows (with Python32 AND 64), and OS X.
On the linux front, it supports Debian/Ubuntu, CentOS/RHEL and Arch.
Installations are supported for both system python and virtualenv
(using the --virtualenv flag).
If you're already running the script from within a virtualenv and you're not
providing a --virtualenv path, Cloudify will be installed within the virtualenv
you're in.
Passing the --wheelspath allows for an offline installation of Cloudify
from predownloaded Cloudify dependency wheels. Note that if wheels are found
within the default wheels directory, they will be used instead of performing
an online installation.
A --nosudo flag can be supplied (If not on Windows) so that prerequisites can
be installed on machines/containers without the sudo execuable
(must be run by root user). Sudo for relevant prerequisites is on by default.
By default, the script assumes that the Python executable is in the
path and is called 'Python' on Linux and 'c:\python27\python.exe on Windows.
The Python path can be overriden by using the --pythonpath flag.
The script will attempt to install all necessary requirements including
python-dev and gcc (for Fabric on Linux), pycrypto (for Fabric on Windows),
pip and virtualenv depending on the OS and Distro you're running on.
Please refer to Cloudify's documentation at http://getcloudify.org for
additional information.'''

QUIET = False
VERBOSE = False
PIP_URL = 'https://bootstrap.pypa.io/get-pip.py'
# http://www.voidspace.org.uk/python/modules.shtml#pycrypto
PYCR64_URL = 'http://www.voidspace.org.uk/downloads/pycrypto26/pycrypto-2.6.win-amd64-py2.7.exe'  # NOQA
PYCR32_URL = 'http://www.voidspace.org.uk/downloads/pycrypto26/pycrypto-2.6.win32-py2.7.exe'  # NOQA

WHEELS_LOOKUP_PATHS = [
    'wheelhouse',
    'cfy/wheelhouse'
]


def prn(what):
    if QUIET:
        return
    print(what)


def run(cmd, sudo=False):
    """This will execute a command either sudo-ically or not.
    """
    cmd = 'sudo {0}'.format(cmd) if sudo else cmd
    if VERBOSE:
        prn('Executing: {0}...'.format(cmd))
    proc = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # while the process is still running, print output
    while proc.poll() is None:
        stdout_line = proc.stdout.readline()
        if VERBOSE and len(stdout_line) > 0:
            prn('STDOUT: {0}'.format(stdout_line))
    stderr = proc.stderr.read()
    if len(stderr) > 0:
        prn('STDERR: {0}'.format(stderr))
    return proc


def make_virtualenv(virtualenv_dir, python_path=False):
    """This will create a virtualenv. If no `python_path` is supplied,
    will assume that `python` is in path. This default assumption is provided
    with the argument parser.
    """
    prn('Creating Virtualenv {0}...'.format(virtualenv_dir))
    result = run('virtualenv -p {0} {1}'.format(python_path, virtualenv_dir))
    if not result.returncode == 0:
        sys.exit('Could not create virtualenv: {0}'.format(virtualenv_dir))


def install_module(module, version=False, pre=False, virtualenv_path=False,
                   wheelspath=False):
    """This will install a module.
    Can specify a specific version.
    Can specify a prerelease.
    Can specify a virtualenv to install in.
    Can specify a local wheelspath to use for offline installation.

    In a Windows envrinoment, a virtualenv bin dir would be declared under
    'VIRTUALENV\\scripts\\'.
    """
    prn('Installing {0}...'.format(module))
    if version:
        module = '{0}=={1}'.format(module, version)
    pip_cmd = 'pip install {0}'.format(module)
    if wheelspath:
        pip_cmd = '{0} --use-wheel --no-index --find-links={1}'.format(
            pip_cmd, wheelspath)
    if pre:
        pip_cmd = '{0} --pre'.format(pip_cmd)
    if virtualenv_path:
        pip_cmd = '{0}{1}{2}'.format(
            virtualenv_path, ENV_BIN_RELATIVE_PATH, pip_cmd)
    if IS_VIRTUALENV and not virtualenv_path:
        prn('Installing within current virtualenv: {0}'.format(IS_VIRTUALENV))
    # sudo will be used only when not installing into a virtualenv and sudo
    # is enabled
    result = run(pip_cmd, sudo=True) \
        if (not IS_VIRTUALENV and not virtualenv_path) \
        and SUDO else run(pip_cmd)
    if not result.returncode == 0:
        sys.exit('Could not install module: {0}'.format(module))


def download_file(url, destination):
    prn('Downloading {0} to {1}'.format(url, destination))
    f = urllib.URLopener()
    f.retrieve(url, destination)


def get_os_props():
    distro_info = platform.linux_distribution()
    os = platform.system()
    distro = distro_info[0]
    release = distro_info[2]
    return os, distro, release


class CloudifyInstaller():
    def __init__(self, args):
        self.args = args

    def install(self):
        """Installation Logic
        --force argument forces installation of all prerequisites
        """
        # TODO: check if there are any darwin dependencies to handle
        if self.args.force or self.args.installpip:
            self.install_pip()
        if self.args.virtualenv and (
                self.args.force or self.args.installvirtualenv):
            self.install_virtualenv()
        if OS == 'linux' and (self.args.force or self.args.installpythondev):
                self.install_pythondev()
        if self.args.virtualenv:
            if not os.path.isfile(
                    self.args.virtualenv + ENV_BIN_RELATIVE_PATH +
                    ('activate.exe' if OS == 'windows' else 'activate')):
                make_virtualenv(self.args.virtualenv, self.args.pythonpath)
        if OS == 'windows' and (self.args.force or self.args.installpycrypto):
            self.install_pycrypto(self.args.virtualenv)
        if self.args.forceonline or not os.path.isdir(self.args.wheelspath):
            install_module('cloudify', self.args.version, self.args.pre,
                           self.args.virtualenv)
        else:
            WHEELS_LOOKUP_PATHS.append(self.args.wheelspath)
            for wheelspath in WHEELS_LOOKUP_PATHS:
                if os.path.isdir(wheelspath):
                    install_module('cloudify', pre=True,
                                   virtualenv_path=self.args.virtualenv,
                                   wheelspath=wheelspath)
                    return

    def install_virtualenv(self):
        # TODO: use `install_module` function instead.
        prn('Installing virtualenv...')
        cmd = 'pip install virtualenv'
        result = run(cmd, sudo=True) if SUDO else run(cmd)
        if not result.returncode == 0:
            sys.exit('Could not install Virtualenv.')

    def install_pip(self):
        prn('Installing pip...')
        # TODO: check below to see if pip already exists
        # import distutils
        # if not distutils.spawn.find_executable('pip'):
        download_file(PIP_URL, 'get-pip.py')
        cmd = '{0} get-pip.py'.format(self.args.pythonpath)
        result = run(cmd, sudo=True) if SUDO else run(cmd)
        if not result.returncode == 0:
            sys.exit('Could not install pip')

    def install_pythondev(self):
        prn('Installing python-dev...')
        if DISTRO in ('ubuntu', 'debian'):
            cmd = 'apt-get install -y gcc python-dev'
        elif DISTRO in ('centos', 'redhat'):
            cmd = 'yum -y install gcc python-devel'
        elif os.path.isfile('/etc/arch-release'):
            # Arch doesn't require a python-dev package.
            # It's already supplied with Python.
            cmd = 'pacman -S gcc --noconfirm'
        elif os == 'darwin':
            prn('python-dev package not required on Darwin.')
        run(cmd, sudo=True) if SUDO else run(cmd)

    # Windows only
    def install_pycrypto(self, venv):
        """This will install PyCrypto to be used by Fabric.
        PyCrypto isn't compiled with Fabric on Windows by default thus it needs
        to be provided explicitly.
        It will attempt to install the 32 or 64 bit version according to the
        Python version installed.
        """
        prn('Installing PyCrypto {0}bit...'.format('32' if IS_PYX32 else '64'))
        cmd = 'easy_install {0}'.format(PYCR32_URL if IS_PYX32 else PYCR64_URL)
        if venv:
            cmd = '{0}\\{1}'.format(os.path.join(venv, 'scripts'), cmd)
        run(cmd)


def parse_args():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    default_group = parser.add_mutually_exclusive_group()
    version_group = parser.add_mutually_exclusive_group()
    online_group = parser.add_mutually_exclusive_group()
    default_group.add_argument('-v', '--verbose', action='store_true')
    default_group.add_argument('-q', '--quiet', action='store_true')
    parser.add_argument(
        '-f', '--force', action='store_true',
        help='Force install any requirements (USE WITH CARE!).')
    parser.add_argument(
        '--virtualenv', type=str,
        help='Path to a Virtualenv to install Cloudify in')
    version_group.add_argument(
        '--version', type=str,
        help='Attempt to install a specific version of Cloudify')
    version_group.add_argument(
        '--pre', action='store_true',
        help='Attempt to install the latest Cloudify Milestone')
    online_group.add_argument(
        '--forceonline', action='store_true',
        help='Even if wheels are found locally, install from PyPI.')
    online_group.add_argument(
        '--wheelspath', type=str, default='wheelhouse',
        help='Path to wheels (defaults to "<cwd>/wheelhouse").')
    if OS == 'windows':
        parser.add_argument(
            '--pythonpath', type=str, default='c:/python27/python.exe',
            help='Python path to use (defaults to "python").')
    else:
        parser.add_argument(
            '--nosudo', action='store_true',
            help='Do not use sudo for prerequisites.')
        parser.add_argument(
            '--pythonpath', type=str, default='python',
            help='Python path to use (defaults to "python").')
    parser.add_argument(
        '--installpip', action='store_true',
        help='Attempt to install pip')
    parser.add_argument(
        '--installvirtualenv', action='store_true',
        help='Attempt to install Virtualenv')
    if OS == 'linux':
        parser.add_argument(
            '--installpythondev', action='store_true',
            help='Attempt to install Python Developers Package')
    if OS == 'windows':
        parser.add_argument(
            '--installpycrypto', action='store_true',
            help='Attempt to install PyCrypto')
    return parser.parse_args()

if __name__ == '__main__':
    os_props = get_os_props()
    OS = os_props[0].lower() if os_props[0] else 'Unknown'
    DISTRO = os_props[1].lower() if os_props[1] else 'Unknown'
    RELEASE = os_props[2].lower() if os_props[2] else 'Unknown'
    # check 32/64bit to choose the correct PyCrypto installation (windows only)
    IS_PYX32 = True if struct.calcsize("P") == 4 else False
    args = parse_args()
    if args.quiet:
        QUIET = True
    elif args.verbose:
        VERBOSE = True
    # if OS is windows, we want to make sure sudo will not be used
    if hasattr(args, 'nosudo'):
        SUDO = False if args.nosudo or OS == 'windows' else True
    else:
        SUDO = False
    # are we running within a virtualenv when executing the script?
    IS_VIRTUALENV = os.environ.get('VIRTUAL_ENV')
    ENV_BIN_RELATIVE_PATH = '\\scripts\\' if OS == 'windows' else '/bin/'
    if VERBOSE:
        prn('Identified OS: {0}'.format(OS))
        prn('Identified Distribution: {0}'.format(DISTRO))
        prn('Identified Release: {0}'.format(RELEASE))
    if OS in ('windows', 'linux', 'darwin'):
        installer = CloudifyInstaller(args)
        installer.install()
    else:
        sys.exit('OS {0} not supported.'.format(OS))
