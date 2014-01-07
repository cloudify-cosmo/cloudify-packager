#!/usr/bin/env python

__author__ = 'nirc'

from fabric.api import *
from fabric.contrib.files import exists
from fabric.context_managers import cd

import config
import logging
import logging.config

# __all__ = ['list']

logging.config.dictConfig(config.PACKAGER_LOGGER)
lgr = logging.getLogger('packager')


def create_package(package_name):
    """
    creates packages
    """

    lgr.debug('creating package: %s' % package_name)
    local('echo $PATH')
    return 0


def get_package(package_name):
    """
    downloads packages
    """

    lgr.debug('creating package: %s' % package_name)
    return 0


def delete_package(package_name):
    """
    deletes packages
    """

    lgr.debug('creating package: %s' % package_name)
    return 0


def main():

    lgr.debug('check run')


if __name__ == '__main__':
    main()
