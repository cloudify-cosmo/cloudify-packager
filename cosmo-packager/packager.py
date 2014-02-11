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
#    * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    * See the License for the specific language governing permissions and
#    * limitations under the License.

#!/usr/bin/env python

import logging
import logging.config

import os
run_env = os.environ['RUN_ENV']
config = __import__(run_env)

from fabric.api import *  # NOQA
import sys
import re
from time import sleep
from templgen import template_formatter, make_file

# __all__ = ['list']

try:
    logging.config.dictConfig(config.PACKAGER_LOGGER)
    lgr = logging.getLogger('packager')
except ValueError:
    sys.exit('could not initiate logger. try sudo...')


def loc_ret(command, retries=3, sleeper=3, capture=False):
    """
    runs a fab local() with retries
    """

    for execution in range(retries):
        lgr.debug('running command: %s' % command)
        try:
            r = local(command, capture)
            lgr.debug('ran command: %s' % command)
            return r
        except:
            lgr.warning('failed to run command: %s -retrying (%s/%s)' % (command, execution, retries))
            sleep(sleeper)
    lgr.error('failed to run command: %s even after %s retries' % (command, execution))
    return r


def delete_pip_build_root():

    rmdir('/tmp/pip_buid_root/')


def check_if_package_is_installed(package):

    lgr.debug('checking if %s is installed' % package)
    try:
        loc_ret('sudo dpkg -s %s' % package)
        lgr.debug('%s is installed' % package)
        return True
    except:
        lgr.error('%s is not installed' % package)
        return False


def create_bootstrap_script(component, template_file, script_file):
    """
    creates a script file from a template file
    """
    formatted_text = template_formatter(
        config.PACKAGER_TEMPLATE_DIR, template_file, component)
    make_file(script_file, formatted_text)


def get_package_configuration(component):
    """
    retrieves a package's configuration from config.PACKAGES
    """

    lgr.debug('retrieving configuration for %s' % component)
    try:
        package_config = config.PACKAGES[component]
        lgr.debug('%s config retrieved successfully' % component)
        return package_config
    except KeyError:
        lgr.error('package configuration for %s was not found, terminating...' % component)
        sys.exit()


def pack(src_type, dst_type, name, src_path, dst_path, version, bootstrap_script=False, depends=False):
    """
    uses fpm (https://github.com/jordansissel/fpm/wiki)
    to create packages with/without bootstrap scripts
    """

    lgr.debug('packing %s' % name)
    if is_dir(src_path):
        with lcd(dst_path):
            if bootstrap_script and not depends:
                x = loc_ret('sudo fpm -s %s -t %s --after-install %s -n %s -v %s -f %s' % (
                    src_type, dst_type, bootstrap_script, name, version, src_path))
            elif bootstrap_script and depends:
                lgr.debug('dependencies are: %s' % ", ".join(depends))
                dep_str = "-d " + " -d ".join(depends)
                x = loc_ret('sudo fpm -s %s -t %s --after-install %s %s -n %s -v %s -f %s' % (
                    src_type, dst_type, bootstrap_script, dep_str, name, version, src_path))
            else:
                x = loc_ret('sudo fpm -s %s -t %s -n %s -v %s -f %s' % (
                    src_type, dst_type, name, version, src_path))
            if x.succeeded:
                lgr.debug('successfully packed %s:%s' % (name, version))
            else:
                lgr.error('unsuccessfully packed %s:%s' % (name, version))
    else:
        lgr.error('package dir %s does\'nt exist, termintating...' % src_path)
        sys.exit()


def make_package_dirs(pkg_dir, tmp_dir):
    """
    creates directory for managing packages
    """

    lgr.debug('creating package directories')
    mkdir('%s/archives' % tmp_dir)
    mkdir(pkg_dir)


def get_ruby_gem(gem, dir):
    """
    downloads a ruby gem
    """

    lgr.debug('downloading gem %s' % gem)
    try:
        x = loc_ret('sudo /home/vagrant/.rvm/rubies/ruby-2.1.0/bin/gem install --no-ri --no-rdoc --install-dir %s %s' % (dir, gem))
    except:
        x = loc_ret('sudo /usr/local/rvm/rubies/ruby-2.1.0/bin/gem install --no-ri --no-rdoc --install-dir %s %s' % (dir, gem))
    if x.succeeded:
        lgr.debug('successfully downloaded ruby gem %s to %s' % (gem, dir))
    else:
        lgr.error('unsuccessfully downloaded ruby gem %s' % gem)


def pip(module, dir):
    """
    pip installs a module
    """

    lgr.debug('installing module %s' % module)
    x = loc_ret('sudo %s/pip --default-timeout=45 install %s' % (dir, module))
    if x.succeeded:
        lgr.debug('successfully installed python module %s to %s' % (module, dir))
    else:
        lgr.error('unsuccessfully installed python module %s' % module)


def get_python_module(module, dir):
    """
    downloads a python module
    """

    lgr.debug('downloading module %s' % module)
    x = loc_ret('''sudo /usr/local/bin/pip install --no-install --no-use-wheel --process-dependency-links --download "%s/" %s''' % (dir, module))
    if x.succeeded:
        lgr.debug('successfully downloaded python module %s to %s' % (module, dir))
    else:
        lgr.error('unsuccessfully downloaded python module %s' % module)


def check_module_installed(name):
    """
    checks to see that a module is installed
    """

    lgr.debug('checking to see that %s is installed' % name)
    x = loc_ret('pip freeze', capture=True)
    if re.search(r'%s' % name, x.stdout):
        lgr.debug('module %s is installed' % name)
        return True
    else:
        lgr.debug('module %s is not installed' % name)
        return False


def venv(root_dir, name=False):
    """
    creates a virtualenv
    """

    lgr.debug('creating virtualenv in %s' % (root_dir))
    if check_module_installed('virtualenv'):
        #with lcd(root_dir):
        x = loc_ret('virtualenv %s' % root_dir)
        if x.succeeded:
            lgr.debug('successfully created virtualenv in %s' % (root_dir))
        else:
            lgr.error('unsuccessfully created virtualenv in %s' % (root_dir))
    else:
        lgr.error('virtualenv is not installed. terminating')
        sys.exit()


def wget(url, dir=False, file=False):
    """
    wgets a url to a destination directory or file
    """

    lgr.debug('downloading %s to %s' % (url, dir))
    try:
        if file:
            x = loc_ret('sudo wget %s -O %s' % (url, file))
        elif dir:
            x = loc_ret('sudo wget %s -P %s' % (url, dir))
        elif dir and file:
            lgr.warning('please specify either a directory or file to download to, not both')
            sys.exit()
        else:
            lgr.warning('please specify at least one of target dir or file. you\'re downloading to the current directory')
            x = loc_ret('sudo wget %s' % url)
        if x.succeeded:
            if file:
                lgr.debug('successfully downloaded %s to %s' % (url, file))
            elif dir:
                lgr.debug('successfully downloaded %s to %s' % (url, dir))
            elif not dir and not file:
                lgr.debug('successfully downloaded %s to local directory' % url)
        else:
            if file:
                lgr.error('unsuccessfully downloaded %s to %s' % (url, file))
            elif dir:
                lgr.error('unsuccessfully downloaded %s to %s' % (url, dir))
            elif not dir and not file:
                lgr.debug('unsuccessfully downloaded %s to local directory' % url)
    except:
        lgr.error('failed downloading %s' % url)


def rmdir(dir):
    """
    deletes a directory
    """

    lgr.debug('removing directory %s' % dir)
    x = loc_ret('sudo rm -rf %s' % dir)
    if x.succeeded:
        lgr.debug('successfully removed directory %s' % dir)
    else:
        lgr.error('unsuccessfully removed directory %s' % dir)


def rm(file):
    """
    deletes a file or a set of files
    """

    lgr.debug('removing files %s' % file)
    try:
        loc_ret('sudo rm %s' % file)
        lgr.debug('successfully removed file %s' % file)
    except:
        lgr.error('unsuccessfully removed file %s' % file)


def mkdir(dir):
    """
    creates (recursively) a directory
    """

    lgr.debug('creating directory %s' % dir)
    x = loc_ret('sudo mkdir -p %s' % dir)
    if x.succeeded:
        lgr.debug('successfully created directory %s' % dir)
    else:
        lgr.error('unsuccessfully created directory %s' % dir)


def cp(src, dst, recurse=True):
    """
    copies (recuresively or not) files or directories
    """

    lgr.debug('copying %s to %s' % (src, dst))
    if recurse:
        x = loc_ret('sudo cp -R %s %s' % (src, dst))
    else:
        x = loc_ret('sudo cp %s %s' % (src, dst))
    if x.succeeded:
        lgr.debug('successfully copied %s to %s' % (src, dst))
    else:
        lgr.error('unsuccessfully copied %s to %s' % (src, dst))


def apt_download(pkg, dir):
    """
    uses apt to download package debs from ubuntu's repo
    """

    apt_purge(pkg)
    lgr.debug('downloading %s to %s' % (pkg, dir))
    x = loc_ret('sudo apt-get -y install %s -d -o=dir::cache=%s' % (pkg, dir))
    if x.succeeded:
        lgr.debug('successfully downloaded %s to %s' % (pkg, dir))
    else:
        lgr.error('unsuccessfully downloaded %s to %s' % (pkg, dir))


def add_key(key_file):
    """
    adds a key to the local repo
    """

    lgr.debug('adding key %s' % key_file)
    x = loc_ret('sudo apt-key add %s' % key_file)
    if x.succeeded:
        lgr.debug('successfully added key %s' % key_file)
    else:
        lgr.error('unsuccessfully added key %s' % key_file)


def apt_update():
    """
    runs apt-get update
    """

    lgr.debug('updating local apt repo')
    x = loc_ret('sudo apt-get update')
    if x.succeeded:
        lgr.debug('successfully ran apt-get update')
    else:
        lgr.error('unsuccessfully ran apt-get update')


def apt_get(list):
    """
    apt-get installs a package
    """

    for package in list:
        lgr.debug('installing %s' % package)
        x = loc_ret('sudo apt-get -y install %s' % package)
        if x.succeeded:
            lgr.debug('successfully installed %s' % package)
        else:
            lgr.error('unsuccessfully installed %s' % package)


def mvn(file):
    """
    build a jar
    """

    lgr.debug('building from %s' % file)
    x = loc_ret('mvn clean package -DskipTests -Pall -f %s' % file)
    if x.succeeded:
        lgr.debug('successfully built from %s' % file)
    else:
        lgr.error('unsuccessfully built from %s' % file)


def find_in_dir(dir, pattern):

    lgr.debug('looking for %s in %s' % (pattern, dir))
    x = loc_ret('find %s -iname "%s" -exec echo {} \;' % (dir, pattern), capture=True)
    if x.succeeded:
        return x.stdout
        lgr.debug('successfully found %s in %s' % (pattern, dir))
    else:
        lgr.error('unsuccessfully found %s in %s' % (pattern, dir))


def tar(chdir, output_file, input):
    """
    tars an input file or directory
    """

    lgr.debug('tar-ing %s' % output_file)
    x = loc_ret('sudo tar -C %s -czvf %s %s' % (chdir, output_file, input))
    if x.succeeded:
        lgr.debug('successfully tar-ed %s' % output_file)
    else:
        lgr.error('unsuccessfully tar-ed %s' % output_file)


def untar(chdir, input_file):
    """
    untars a dir
    """

    lgr.debug('tar-ing %s' % input_file)
    x = loc_ret('sudo tar -C %s -xzvf %s' % (chdir, input_file))
    if x.succeeded:
        lgr.debug('successfully untar-ed %s' % input_file)
    else:
        lgr.error('unsuccessfully untar-ed %s' % input_file)


def apt_purge(package):
    """
    completely purges a package from the local repo
    """

    x = loc_ret('sudo apt-get -y purge %s' % package)
    if x.succeeded:
        lgr.debug('successfully purged %s' % package)
    else:
        lgr.error('unsuccessfully purged %s' % package)


def run_script(package_name, action, arg_s=''):
    """
    runs a a shell scripts with optional arguments
    """

    SCRIPT_PATH = '%s/%s-%s.sh' % (config.PACKAGER_SCRIPTS_DIR, package_name, action)

    try:
        with open(SCRIPT_PATH):
            lgr.debug('%s package: %s' % (action, package_name))
            lgr.debug('running %s %s' % (SCRIPT_PATH, arg_s))
            loc_ret('%s %s' % (SCRIPT_PATH, arg_s))
    except IOError:
        lgr.error('Oh Dear... the script %s does not exist' % SCRIPT_PATH)
        sys.exit()


def is_dir(dir):
    """
    checks if a directory exists
    """

    lgr.debug('checking if %s exists' % dir)
    if os.path.isdir(dir):
        lgr.debug('%s exists' % dir)
        return True
    else:
        lgr.debug('%s does not exist' % dir)
        return False


def main():

    lgr.debug('VALIDATED!')


if __name__ == '__main__':
    main()
