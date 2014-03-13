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
import config
# run_env = os.environ['RUN_ENV']
# config = __import__(run_env)

import os
from fabric.api import *  # NOQA
import sys
import re
from time import sleep
from templgen import template_formatter, make_file

# __all__ = ['list']

try:
    d = os.path.dirname(config.LOGGER['handlers']['file']['filename'])
    if not os.path.exists(d):
        os.makedirs(d)
    logging.config.dictConfig(config.LOGGER)
    lgr = logging.getLogger('main')
    lgr.setLevel(logging.INFO)
except ValueError:
    sys.exit('could not initialize logger.'
             ' verify your logger config'
             ' and permissions to write to {0}'
             .format(config.LOGGER['handlers']['file']['filename']))


def _run_locally_with_retries(command, sudo=False, retries=5,
                              sleeper=3, capture=False):
    """
    runs a fab local() with retries
    """
    def _execute():
        for execution in range(retries):
            try:
                if sudo:
                    r = local('sudo {0}'.format(command, capture))
                else:
                    r = local(command, capture)
                # lgr.debug('ran command: {0}'.format(command))
                return r
            except:
                lgr.warning('failed to run command: {0} -retrying ({1}/{2})'
                            .format(command, execution, retries))
                sleep(sleeper)
        lgr.error('failed to run command: {0} even after {1} retries'
                  .format(command, execution))
        sys.exit(1)

    # lgr.info('running command: {0}'.format(command))
    if config.VERBOSE:
        return _execute()
    else:
        with hide('running'):
            return _execute()


def do(command, sudo=False):
    """
    runs a command
    """

    _run_locally_with_retries(command)


def delete_pip_build_root():
    """
    DEPRACATED
    """

    rmdir('/tmp/pip_buid_root/')


def check_if_package_is_installed(package):
    """
    checks if a package is installed
    """

    lgr.debug('checking if {0} is installed'.format(package))
    try:
        _run_locally_with_retries('sudo dpkg -s {0}'.format(package))
        lgr.debug('{0} is installed'.format(package))
        return True
    except:
        lgr.error('{0} is not installed'.format(package))
        return False


def create_bootstrap_script(component, template_file, script_file):
    """
    creates a script file from a template file
    """

    lgr.debug('creating bootstrap script...')
    formatted_text = template_formatter(
        config.PACKAGER_TEMPLATE_DIR, template_file, component)
    make_file(script_file, formatted_text)


def generate_configs(component):
    """
    generates configuration files from templates
    """

    for key, value in component['config_templates'].iteritems():
        if key.startswith('__template'):
            config_dir = value['config_dir']  # .split('_')[0]
            template_dir = '/'.join(value['template_file'].split('/')[:-1])
            template_file = value['template_file'].split('/')[-1]
            output_file = value['output_file'] \
                if 'output_file' in value \
                else '.'.join(template_file.split('.')[:-1])
            output_path = '{0}/{1}/{2}'.format(
                component['package_dir'], config_dir, output_file)

            print '!!!!!!!!!!!config_dir: {0}'.format(config_dir)
            print '!!!!!!!!!!!template_dir: {0}'.format(template_dir)
            print '!!!!!!!!!!!template_file: {0}'.format(template_file)
            print '!!!!!!!!!!!output_file: {0}'.format(output_file)
            print '!!!!!!!!!!!output_path: {0}'.format(output_path)

            mkdir('{0}/{1}'.format(
                component['package_dir'], config_dir))
            generate_from_template(component,
                                   output_path,
                                   template_file,
                                   template_dir)


def generate_from_template(component, output_file, template_file,
                           template_dir=config.PACKAGER_TEMPLATE_DIR):
    """
    generates configuration files from templates
    """

    lgr.debug('generating config file...')
    formatted_text = template_formatter(
        template_dir, template_file, component)
    make_file(output_file, formatted_text)


def get_package_configuration(component):
    """
    retrieves a package's configuration from config.PACKAGES
    """

    lgr.debug('retrieving configuration for {0}'.format(component))
    try:
        package_config = config.PACKAGES[component]
        lgr.debug('{0} config retrieved successfully'.format(component))
        return package_config
    except KeyError:
        lgr.error('package configuration for'
                  ' {0} was not found, terminating...'.format(component))
        sys.exit()


def get(package=False, version=False, source_repo=False, source_ppa=False,
        source_key=False, source_url=False, key_file=False, reqs=False,
        dst_path=False, name=False, bootstrap_dir=False, modules=False,
        gems=False, overwrite=True):
    """
    retrieves resources for packaging
    """

    version = package['version'] \
        if not version else version
    source_repo = package['source_repo'] \
        if not source_repo else source_repo
    source_ppa = package['source_ppa'] \
        if not source_ppa else source_ppa
    source_key = package['source_key'] \
        if not source_key else source_key
    source_url = package['source_url'] \
        if not source_url else source_url
    key_file = package['key_file'] \
        if not key_file else key_file
    reqs = package['reqs'] \
        if not reqs else reqs
    dst_path = package['package_dir'] \
        if not dst_path else dst_path
    name = package['name'] \
        if not name else name
    bootstrap_dir = package['bootstrap_dir'] \
        if not bootstrap_dir else bootstrap_dir
    conf_dir = package['conf_dir'] \
        if not conf_dir else conf_dir
    modules = package['modules'] \
        if not modules else modules
    gems = pakcage['gems'] \
        if not gems else gems
    overwrite = package['overwrite'] \
        if not overwrite else overwrite

    if overwrite:
        lgr.info('overwrite enabled. removing directory before retrieval')
        rmdir(dst_path)
    else:
        if os.path.isdir(dst_path):
            lgr.error('the destination directory for thie package already '
                      'exists and overwrite is disabled.')
    make_package_dirs(
        bootstrap_dir,
        dst_path)
    if conf_dir:
        cp(conf_dir, dst_path)
    if source_repo:
        add_src_repo(source_repo, 'deb')  # TODO: SEND LIST OF REPOS WITh MARKS
    if source_ppa:
        add_ppa_repo(source_ppa)
    if source_key:
        wget(source_key, dst_path)
    if source_url:
        wget(
            source_url,
            dst_path)
    if key_file:
        add_key(key_file)
        apt_update()
    if reqs:
        apt_download_reqs(reqs, dst_path)
    if modules:
        for module in modules:
            get_python_module(module, dst_path)
    if gems:
        for gem in gems:
            get_ruby_gem(gem, dst_path)


def pack(package=False, src_type=False, dst_type=False, name=False,
         src_path=False, dst_path=False, version=False, bootstrap_dir=False,
         bootstrap_script=False, bootstrap_template=False, depends=False,
         bootstrap_script_in_pkg=False, config_templates=False):
    """
    uses fpm (https://github.com/jordansissel/fpm/wiki)
    to create packages
    """

    bootstrap_template = package['bootstrap_template'] \
        if 'bootstrap_template' in package else bootstrap_template
    bootstrap_script = package['bootstrap_script'] \
        if 'bootstrap_script' in package else bootstrap_script
    src_type = package['src_package_type'] \
        if 'src_package_type' in package else src_type
    dst_type = package['dst_package_type'] \
        if 'dst_package_type' in package else dst_type
    name = package['name'] \
        if 'name' in package else name
    src_path = package['package_dir'] \
        if 'package_dir' in package else src_path
    dst_path = '{0}/archives'.format(package['package_dir']) \
        if not dst_path else dst_path
    version = package['version'] \
        if 'version' in package else version
    bootstrap_dir = package['bootstrap_dir'] \
        if 'bootstrap_dir' in package else bootstrap_dir
    bootstrap_script = package['bootstrap_script'] \
        if 'bootstrap_script' in package else bootstrap_script
    bootstrap_script_in_pkg = package['bootstrap_script_in_pkg'] \
        if 'bootstrap_script_in_pkg' in package else bootstrap_script_in_pkg
    depends = package['depends'] \
        if 'depends' in package else depends
    config_templates = package['config_templates'] \
        if 'config_templates' in package else config_templates

    if src_path == dst_path:
        lgr.error('source and destination paths must'
                  ' be different to avoid conflics!')
    lgr.info('cleaning up before packaging...')
    rmdir(bootstrap_dir)
    if src_type:
        rmdir(dst_path)
        mkdir(dst_path)

    lgr.info('generating package scripts and config files...')
    if config_templates:
        generate_configs(package)
    if bootstrap_script or bootstrap_script_in_pkg:
        if bootstrap_template and bootstrap_script:
            create_bootstrap_script(package, bootstrap_template,
                                    bootstrap_script)
        if bootstrap_template and bootstrap_script_in_pkg:
            create_bootstrap_script(package, bootstrap_template,
                                    bootstrap_script_in_pkg)
            if bootstrap_script_in_pkg:
                lgr.debug('granting execution permissions')
                do('chmod +x {0}'.format(bootstrap_script_in_pkg))
                lgr.debug('copying bootstrap script to package directory')
                cp(bootstrap_script_in_pkg, src_path)
    lgr.info('packing up component...')
    if src_type:
        lgr.info('packing {0}'.format(name))
        if is_dir(src_path):
            with lcd(dst_path):
                if bootstrap_script_in_pkg and dst_type == "tar":
                    x = _run_locally_with_retries(
                        'sudo fpm -s {0} -t {1} -n {2} -v {3} -f {4}'
                        .format(src_type, dst_type, name, version, src_path))
                elif bootstrap_script and not depends:
                    x = _run_locally_with_retries(
                        'sudo fpm -s {0} -t {1} --after-install {2} -n {3}'
                        ' -v {4} -f {5}'
                        .format(src_type, dst_type, bootstrap_script,
                                name, version, src_path))
                elif bootstrap_script and depends:
                    lgr.debug('package dependencies are: {0}'.format(", "
                              .join(depends)))
                    dep_str = "-d " + " -d ".join(depends)
                    x = _run_locally_with_retries(
                        'sudo fpm -s {0} -t {1} --after-install {2} {3} -n {4}'
                        ' -v {5} -f {6}'
                        .format(src_type, dst_type, bootstrap_script, dep_str,
                                name, version, src_path))
                else:
                    x = _run_locally_with_retries(
                        'sudo fpm -s {0} -t {1} -n {2} -v {3} -f {4}'
                        .format(src_type, dst_type, name, version, src_path))
                if x.succeeded:
                    lgr.info('successfully packed {0}:{1}'
                             .format(name, version))
                else:
                    lgr.error('unsuccessfully packed {0}:{1}'
                              .format(name, version))
        else:
            lgr.error('package dir {0} does\'nt exist, termintating...'
                      .format(src_path))
            sys.exit(1)

    if not is_dir(bootstrap_dir):
        mkdir(bootstrap_dir)
    lgr.info("isolating archives...")
    cp('{0}/*.{1}'.format(dst_path, dst_type), bootstrap_dir)


def make_package_dirs(pkg_dir, tmp_dir):
    """
    creates directories for managing packages
    """

    lgr.debug('creating package directories')
    mkdir('%s/archives' % tmp_dir)
    mkdir(pkg_dir)


def get_ruby_gem(gem, dir):
    """
    downloads a ruby gem
    """

    lgr.debug('downloading gem {0}'.format(gem))
    try:
        x = _run_locally_with_retries(
            'sudo /home/vagrant/.rvm/rubies/ruby-2.1.0/bin/gem install'
            ' --no-ri --no-rdoc --install-dir {0} {1}'.format(dir, gem))
    except:
        x = _run_locally_with_retries(
            'sudo /usr/local/rvm/rubies/ruby-2.1.0/bin/gem install'
            ' --no-ri --no-rdoc --install-dir {0} {1}'.format(dir, gem))
    if x.succeeded:
        lgr.debug('successfully downloaded ruby gem {0} to {1}'
                  .format(gem, dir))
    else:
        lgr.error('unsuccessfully downloaded ruby gem {0}'.format(gem))


def pip(module, dir):
    """
    pip installs a module
    """

    lgr.debug('installing module {0}'.format(module))
    x = _run_locally_with_retries(
        'sudo {0}/pip --default-timeout=45 install {1}'.format(dir, module))
    if x.succeeded:
        lgr.debug('successfully installed python module {0} to {1}'
                  .format(module, dir))
    else:
        lgr.error('unsuccessfully installed python module {0}'.format(module))


def get_python_module(module, dir):
    """
    downloads a python module
    """

    lgr.debug('downloading module {0}'.format(module))
    x = _run_locally_with_retries(
        'sudo /usr/local/bin/pip install --no-use-wheel \
        --process-dependency-links --download "{0}/" {1}'
        .format(dir, module))
    if x.succeeded:
        lgr.debug('successfully downloaded python module {0} to {1}'
                  .format(module, dir))
    else:
        lgr.error('unsuccessfully downloaded python module {0}'
                  .format(module))


def check_module_installed(name):
    """
    checks to see that a module is installed
    """

    lgr.debug('checking to see that {0} is installed'.format(name))
    x = _run_locally_with_retries('pip freeze', capture=True)
    if re.search(r'{0}'.format(name), x.stdout):
        lgr.debug('module {0} is installed'.format(name))
        return True
    else:
        lgr.debug('module {0} is not installed'.format(name))
        return False


def venv(root_dir, name=False):
    """
    creates a virtualenv
    """

    lgr.debug('creating virtualenv in {0}'.format(root_dir))
    if check_module_installed('virtualenv'):
        #with lcd(root_dir):
        x = _run_locally_with_retries('virtualenv {0}'
                                      .format(root_dir))
        if x.succeeded:
            lgr.debug('successfully created virtualenv in {0}'
                      .format(root_dir))
        else:
            lgr.error('unsuccessfully created virtualenv in {0}'
                      .format(root_dir))
    else:
        lgr.error('virtualenv is not installed. terminating')
        sys.exit()


def wget(url, dir=False, file=False):
    """
    wgets a url to a destination directory or file
    """

    lgr.debug('downloading {0} to {1}'.format(url, dir))
    try:
        if file:
            x = _run_locally_with_retries('sudo wget {0} -O {1}'
                                          .format(url, file))
        elif dir:
            x = _run_locally_with_retries('sudo wget {0} -P {1}'
                                          .format(url, dir))
        elif dir and file:
            lgr.warning('please specify either a directory'
                        ' or file to download to, not both')
            sys.exit()
        else:
            lgr.warning('please specify at least one of target dir or file.')
            sys.exit()
        if x.succeeded:
            if file:
                lgr.debug('successfully downloaded {0} to {1}'
                          .format(url, file))
            elif dir:
                lgr.debug('successfully downloaded {0} to {1}'
                          .format(url, dir))
            elif not dir and not file:
                lgr.debug('successfully downloaded {0} to local directory'
                          .format(url))
        else:
            if file:
                lgr.error('unsuccessfully downloaded {0} to {1}'
                          .format(url, file))
            elif dir:
                lgr.error('unsuccessfully downloaded {0} to {1}'
                          .format(url, dir))
            elif not dir and not file:
                lgr.debug('unsuccessfully downloaded {0} to local directory'
                          .format(url))
    except:
        lgr.error('failed downloading {0}'.format(url))


def rmdir(dir):
    """
    deletes a directory
    """

    lgr.debug('removing directory {0}'.format(dir))
    try:
        if os.path.isdir(dir):
            _run_locally_with_retries('sudo rm -rf {0}'.format(dir))
        lgr.debug('successfully removed directory {0}'.format(dir))
    except:
        lgr.error('unsuccessfully removed directory {0}'.format(dir))


def rm(file):
    """
    deletes a file or a set of files
    """

    lgr.info('removing files {0}'.format(file))
    try:
        if os.path.isfile(file):
            _run_locally_with_retries('sudo rm {0}'.format(file))
        lgr.info('successfully removed file {0}'.format(file))
    except:
        lgr.error('unsuccessfully removed file {0}'.format(file))


def mkdir(dir):
    """
    creates (recursively) a directory
    """

    lgr.debug('creating directory {0}'.format(dir))
    if not os.path.isdir(dir):
        x = _run_locally_with_retries('sudo mkdir -p {0}'.format(dir))
        if x.succeeded:
            lgr.debug('successfully created directory {0}'.format(dir))
        else:
            lgr.error('unsuccessfully created directory {0}'.format(dir))
    else:
        lgr.debug('directory already exists, skipping.')


def cp(src, dst, recurse=True):
    """
    copies (recuresively or not) files or directories
    """

    lgr.debug('copying {0} to {1}'.format(src, dst))
    if recurse:
        x = _run_locally_with_retries('sudo cp -R {0} {1}'.format(src, dst))
    else:
        x = _run_locally_with_retries('sudo cp {0} {1}'.format(src, dst))
    if x.succeeded:
        lgr.debug('successfully copied {0} to {1}'.format(src, dst))
    else:
        lgr.error('unsuccessfully copied {0} to {1}'.format(src, dst))


def dpkg_name(dir):
    """
    renames deb files to converntional names
    """

    lgr.debug('renaming deb files...')
    _run_locally_with_retries('dpkg-name {0}/*.deb'.format(dir))


def apt_download_reqs(req_list, package_dir):

    for req in req_list:
        apt_download(req, package_dir)


def apt_autoremove(pkg):
    """
    autoremoves package dependencies
    """

    lgr.debug('removing unnecessary dependencies...')
    _run_locally_with_retries('sudo apt-get -y autoremove {0}'.formaT(pkg))


def apt_download(pkg, dir):
    """
    uses apt to download package debs from ubuntu's repo
    """

    lgr.debug('downloading {0} to {1}'.format(pkg, dir))
    x = _run_locally_with_retries(
        'sudo apt-get -y install {0} -d -o=dir::cache={1}'.format(pkg, dir))
    if x.succeeded:
        lgr.debug('successfully downloaded {0} to {1}'.format(pkg, dir))
    else:
        lgr.error('unsuccessfully downloaded {0} to {1}'.format(pkg, dir))


def add_src_repo(url, mark):

    lgr.debug('adding source repository {0} mark {1}'.format(url, mark))
    x = _run_locally_with_retries('sudo sed -i "2i {0} {1}" '
                                  '/etc/apt/sources.list'
                                  .format(mark, url))
    if x.succeeded:
        lgr.debug('successfully added repo {0}'.format(url))
    else:
        lgr.error('unsuccessfully added repo {0}'.format(url))


def add_ppa_repo(url):

    lgr.debug('adding ppa repository {0}'.format(url))
    x = _run_locally_with_retries('add-apt-repository -y {0}'.format(url))
    if x.succeeded:
        lgr.debug('successfully added repo {0}'.format(url))
    else:
        lgr.error('unsuccessfully added repo {0}'.format(url))


def add_key(key_file):
    """
    adds a key to the local repo
    """

    lgr.debug('adding key {0}'.format(key_file))
    x = _run_locally_with_retries('sudo apt-key add {0}'.format(key_file))
    if x.succeeded:
        lgr.debug('successfully added key {0}'.format(key_file))
    else:
        lgr.error('unsuccessfully added key {0}'.format(key_file))


def apt_update():
    """
    runs apt-get update
    """

    lgr.debug('updating local apt repo')
    x = _run_locally_with_retries('sudo apt-get update')
    if x.succeeded:
        lgr.debug('successfully ran apt-get update')
    else:
        lgr.error('unsuccessfully ran apt-get update')


def apt_get(list):
    """
    apt-get installs a package
    """

    for package in list:
        lgr.debug('installing {0}'.format(package))
        x = _run_locally_with_retries('sudo apt-get -y install {0}'
                                      .format(package))
        if x.succeeded:
            lgr.debug('successfully installed {0}'.format(package))
        else:
            lgr.error('unsuccessfully installed {0}'.format(package))


def mvn(file):
    """
    build a jar
    """

    lgr.debug('building from {0}'.format(file))
    x = _run_locally_with_retries(
        'mvn clean package -DskipTests -Pall -f {0}'.format(file))
    if x.succeeded:
        lgr.debug('successfully built from {0}'.format(file))
    else:
        lgr.error('unsuccessfully built from {0}'.format(file))


def find_in_dir(dir, pattern):

    lgr.debug('looking for {0} in {1}'.format(pattern, dir))
    x = _run_locally_with_retries(
        'find {0} -iname "{1}" -exec echo {} \;'
        .format(dir, pattern), capture=True)
    if x.succeeded:
        return x.stdout
        lgr.debug('successfully found {0} in {1}'.format(pattern, dir))
    else:
        lgr.error('unsuccessfully found {0} in {1}'.format(pattern, dir))


def tar(chdir, output_file, input):
    """
    tars an input file or directory
    """

    lgr.debug('tar-ing {0}'.format(output_file))
    x = _run_locally_with_retries(
        'sudo tar -C {0} -czvf {1} {2}'.format(chdir, output_file, input))
    if x.succeeded:
        lgr.debug('successfully tar-ed {0}'.format(output_file))
    else:
        lgr.error('unsuccessfully tar-ed {0}'.format(output_file))


def untar(chdir, input_file):
    """
    untars a dir
    """

    lgr.debug('tar-ing {0}'.format(input_file))
    x = _run_locally_with_retries(
        'sudo tar -C {0} -xzvf {1}'.format(chdir, input_file))
    if x.succeeded:
        lgr.debug('successfully untar-ed {0}'.format(input_file))
    else:
        lgr.error('unsuccessfully untar-ed {0}'.format(input_file))


def apt_purge(package):
    """
    completely purges a package from the local repo
    """

    x = _run_locally_with_retries('sudo apt-get -y purge {0}'.format(package))
    if x.succeeded:
        lgr.debug('successfully purged {0}'.format(package))
    else:
        lgr.error('unsuccessfully purged {0}'.format(package))


def run_script(package_name, action, arg_s=''):
    """
    runs a a shell scripts with optional arguments
    """

    SCRIPT_PATH = '{0}/{1}-{2}.sh'.format(
        config.PACKAGER_SCRIPTS_DIR, package_name, action)

    try:
        with open(SCRIPT_PATH):
            lgr.debug('{0} package: {1}'.format(action, package_name))
            lgr.debug('running {0} {1}'.format(SCRIPT_PATH, arg_s))
            _run_locally_with_retries('{0} {1}'.format(SCRIPT_PATH, arg_s))
    except IOError:
        lgr.error('Oh Dear... the script {0} does not exist'
                  .format(SCRIPT_PATH))
        sys.exit()


def is_dir(dir):
    """
    checks if a directory exists
    """

    lgr.debug('checking if {0} exists'.format(dir))
    if os.path.isdir(dir):
        lgr.debug('{0} exists'.format(dir))
        return True
    else:
        lgr.debug('{0} does not exist'.format(dir))
        return False


def main():

    lgr.debug('VALIDATED!')


if __name__ == '__main__':
    main()
