#!/usr/bin/env python

"""cosmo-packager"""

__author__ = 'nirc'

from fabric.api import *

import os
import sys

import config
import logging
import logging.config

# __all__ = ['list']

logging.config.dictConfig(config.PACKAGER_LOGGER)
lgr = logging.getLogger('packager')


def pack(src_type, dst_type, name, files_path, version, bootstrap_script=False):

    lgr.debug('packing %s' % name)
    if bootstrap_script:
        local('sudo fpm -s %s -t %s --after-install %s -n %s -v %s -f %s' % (src_type, dst_type, bootstrap_script, name, version, files_path))
    else:
        local('sudo fpm -s %s -t %s -n %s -v %s -f %s' % (src_type, dst_type, name, version, files_path))


def make_package_dirs(bootstrap_dir, pkg_dir):

    mkdir(bootstrap_dir)
    mkdir('%s/archives' % pkg_dir)


def wget(url, dir=False):

    lgr.debug('downloading %s to %s' % (url, dir))
    if dir:
        local('sudo wget %s -P %s' % (url, dir))
    else:
        local('sudo wget %s' % url)


def mkdir(dir):

    lgr.debug('creating directory %s' % dir)
    local('sudo mkdir -p %s' % dir)


def cp(src, dst, recurse=True):

    lgr.debug('copying %s to %s' % (src, dst))
    if recurse:
        local('sudo cp -R %s %s' % (src, dst))
    else:
        local('sudo cp %s %s' % (src, dst))


def apt_download(pkg, dir):

    lgr.debug('downloading %s to %s' % (pkg, dir))
    local('sudo apt-get -y install %s -d -o=dir::cache=%s' % (pkg, dir))


def add_key(key_file):

    lgr.debug('adding key %s' % key_file)
    local('sudo apt-key add %s' % key_file)


def apt_update():

    lgr.debug('updating local apt repo')
    local('sudo apt-get update')


def apt_get(list):

    for package in list:
        lgr.debug('installing %s')
        local ('sudo apt-get -y install %s' % package)


def get_gem(gem, dir):

    lgr.debug('downloading gem %s' % gem)
    local('sudo gem install --no-ri --no-rdoc --install-dir %s %s' % (dir, gem))


def get_module(module, dir):

    lgr.debug('downloading module %s' % module)
    local('sudo /usr/local/bin/pip install --no-install --no-use-wheel --download "%s/" %s' % (dir, module))


def run_script(package_name, action, arg_s=''):
    """
    runs a a shell scripts after checking for its dependencies
    """

    # if check_prereqs(package_name, action):
    SCRIPT_PATH = '%s/%s-%s.sh' % (config.PACKAGER_SCRIPTS_DIR, package_name, action)

    try:
        with open(SCRIPT_PATH):
            lgr.debug('%s package: %s' % (action, package_name))
            lgr.debug('running %s %s' % (SCRIPT_PATH, arg_s))
            local('%s %s' % (SCRIPT_PATH, arg_s))
    except IOError:
        lgr.error('Oh Dear... the script %s does not exist' % SCRIPT_PATH)
        sys.exit()
    # else:
        # lgr.error('script prereqs not fulfilled. exiting')
        # sys.exit()


def check_if_dir_exists(package_name):

    is_dir = os.path.isdir("%s/%s" % (config.PACKAGES_DIR, package_name))
    return is_dir


def check_prereqs(package_name, action):

    if action == 'pkg':
        if check_if_dir_exists(package_name):
            lgr.debug('package directory exists. \
                continuing with packing process')
            return True
        else:
            lgr.error('package directory does not exist. \
                get the package and try again')
            return False
    elif action == 'get':
        return True
    elif action == 'remove':
        return True
    elif action == 'bootstrap':
        if not package_name == 'cosmo':
            if check_if_dir_exists(package_name):
                lgr.debug('%s package directory exists. \
                    continuing with packing process' % package_name)
                return True
            else:
                lgr.error('%s package directory does not exist. \
                    get the package and try again' % package_name)
                return False
        else:
            return True


def main():

    lgr.debug('VALIDATED!')


if __name__ == '__main__':
    main()
