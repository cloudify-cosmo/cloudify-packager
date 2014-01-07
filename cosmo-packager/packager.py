#!/usr/bin/env python

"""cosmo-packager"""

__author__ = 'nirc'

from fabric.api import *
from fabric.contrib.files import exists
from fabric.context_managers import cd

import os
import sys

import config
import logging
import logging.config

# __all__ = ['list']

logging.config.dictConfig(config.PACKAGER_LOGGER)
lgr = logging.getLogger('packager')


def run_script(package_name, action):
    """
    runs a a shell scripts after checking for its dependencies
    """

    if check_prereqs(package_name, action):
        SCRIPT_PATH = '%s/%s-%s.sh' % (config.PACKAGER_SCRIPTS_DIR, package_name, action)

        try:
            with open(SCRIPT_PATH):
                lgr.debug('%s package: %s' % (action, package_name))
                local(SCRIPT_PATH)
        except IOError:
            lgr.error('Oh Dear... the script %s does not exist' % SCRIPT_PATH)
        return 0
    else:
        lgr.error('script prereqs not fulfilled. exiting')
        sys.exit()


def check_if_dir_exists(package_name):

    is_dir = os.path.isdir("%s/%s" % (config.PACKAGES_DIR, package_name))
    return is_dir


def check_prereqs(package_name, action):

    if action == 'pkg':
        if check_if_dir_exists(package_name):
            lgr.debug('package directory exists. continuing with packing process')
            return True
        else:
            lgr.error('package directory does not exist. get the package and try again')
            return False
    elif action == 'get':
        return True
    elif action == 'remove':
        return True
    elif action == 'bootstrap':
        if check_if_dir_exists(package_name):
            lgr.debug('package directory exists. continuing with packing process')
            return True
        else:
            lgr.error('package directory does not exist. get the package and try again')
            return False


def main():

    lgr.debug('VALIDATED!')


if __name__ == '__main__':
    main()
