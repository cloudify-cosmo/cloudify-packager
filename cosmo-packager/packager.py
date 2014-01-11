#!/usr/bin/env python

from fabric.api import *
import config

import logging
import logging.config

import os
import sys

# __all__ = ['list']

logging.config.dictConfig(config.PACKAGER_LOGGER)
lgr = logging.getLogger('packager')


def get_package_configuration(component):

    lgr.debug('retrieving configuration for %s' % component)
    try:
        package_config = config.PACKAGES[component]
        lgr.debug('%s config retrieved successfully' % component)
        return package_config
    except KeyError:
        lgr.error('package configuration for %s was not found, terminating...' % component)
        sys.exit()


def pack(src_type, dst_type, name, src_path, version, bootstrap_script=False):

    lgr.debug('packing %s' % name)
    if is_dir(package['package_dir']):
        with lcd('%s/archives/' % package['package_dir']):
            if bootstrap_script:
                x = local('sudo fpm -s %s -t %s --after-install %s -n %s -v %s -f %s' % (src_type, dst_type, bootstrap_script, name, version, src_path))
            else:
                x = local('sudo fpm -s %s -t %s -n %s -v %s -f -p %s %s' % (src_type, dst_type, name, version, src_path))
            if x.succeeded:
                lgr.debug('successfully packed %s:%s' % (name, version))
            else:
                lgr.error('unsuccessfully packed %s:%s' % (name, version))
    else:
        lgr.error('package dir %s does\'nt exist, termintating...' % package['package_dir'])
        sys.exit()


def make_package_dirs(bootstrap_dir, pkg_dir):

    lgr.debug('creating package directories')
    mkdir(bootstrap_dir)
    mkdir('%s/archives' % pkg_dir)


def wget(url, dir):

    lgr.debug('downloading %s to %s' % (url, dir))
    try:
        x = local('sudo wget %s -P %s' % (url, dir))
        if x.succeeded:
            lgr.debug('successfully downloaded %s to %s' % (url, dir))
        else:
            lgr.error('unsuccessfully downloaded %s to %s' % (url, dir))
    except:
        lgr.error('failed downloading %s' % url)


def rmdir(dir):

    lgr.debug('removing directory %s' % dir)
    x = local('sudo rm -rf %s' % dir)
    if x.succeeded:
        lgr.debug('successfully removed directory %s' % dir)
    else:
        lgr.error('unsuccessfully removed directory %s' % dir)


def mkdir(dir):

    lgr.debug('creating directory %s' % dir)
    x = local('sudo mkdir -p %s' % dir)
    if x.succeeded:
        lgr.debug('successfully created directory %s' % dir)
    else:
        lgr.error('unsuccessfully created directory %s' % dir)


def cp(src, dst, recurse=True):

    lgr.debug('copying %s to %s' % (src, dst))
    if recurse:
        x = local('sudo cp -R %s %s' % (src, dst))
    else:
        x = local('sudo cp %s %s' % (src, dst))
    if x.succeeded:
        lgr.debug('successfully copied %s to %s' % (src, dst))
    else:
        lgr.error('unsuccessfully copied %s to %s' % (src, dst))


def apt_download(pkg, dir):

    lgr.debug('downloading %s to %s' % (pkg, dir))
    x = local('sudo apt-get -y install %s -d -o=dir::cache=%s' % (pkg, dir))
    if x.succeeded:
        lgr.debug('successfully downloaded %s to %s' % (pkg, dst))
    else:
        lgr.error('unsuccessfully downloaded %s to %s' % (pkg, dst))

def add_key(key_file):

    lgr.debug('adding key %s' % key_file)
    x = local('sudo apt-key add %s' % key_file)
    if x.succeeded:
        lgr.debug('successfully added key %s' % key_file)
    else:
        lgr.error('unsuccessfully added key %s' % key_file)


def apt_update():

    lgr.debug('updating local apt repo')
    x = local('sudo apt-get update')
    if x.succeeded:
        lgr.debug('successfully ran apt-get update')
    else:
        lgr.error('unsuccessfully ran apt-get update')


def apt_get(list):

    for package in list:
        lgr.debug('installing %s')
        x = local ('sudo apt-get -y install %s' % package)
        if x.succeeded:
            lgr.debug('successfully installed %s' % package)
        else:
            lgr.error('unsuccessfully installed %s' % package)


def get_ruby_gem(gem, dir):

    lgr.debug('downloading gem %s' % gem)
    x = local('sudo gem install --no-ri --no-rdoc --install-dir %s %s' % (dir, gem))
    if x.succeeded:
        lgr.debug('successfully downloaded ruby gem %s to %s' % (gem, dir))
    else:
        lgr.error('unsuccessfully downloaded ruby gem %s' % gem)


def get_python_module(module, dir):

    lgr.debug('downloading module %s' % module)
    x = local('sudo /usr/local/bin/pip install --no-install --no-use-wheel --download "%s/" %s' % (dir, module))
    if x.succeeded:
        lgr.debug('successfully downloaded python module %s to %s' % (gem, dir))
    else:
        lgr.error('unsuccessfully downloaded python module %s' % gem)


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


def is_dir(dir):

    lgr.debug('checking if %s exists' % dir)
    if os.path.isdir(dir):
        lgr.debug('%s exists' % dir)
        return True
    else:
        lgr.debug('%s does not exist' % dir)
        return False


def check_prereqs(package_name, action):

    if action == 'pkg':
        if is_dir(package_name):
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
            if is_dir(package_name):
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
