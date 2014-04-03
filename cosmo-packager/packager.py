#!/usr/bin/env python
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

import logging
import logging.config

import config
import definitions
import packages

import os
from fabric.api import *  # NOQA
import sys
import re
from time import sleep
from jinja2 import Environment, FileSystemLoader

# __all__ = ['list']


def init_logger():
    """
    Initialize a logger to be used throughout the packager

    :param config:
    """
    log_dir = os.path.dirname(config.LOGGER['handlers']['file']['filename'])
    if os.path.isfile(log_dir):
        sys.exit('file {0} exists - log directory cannot be created '
                 'there. please remove the file and try again.'
                 .format(log_dir))
    try:
        logfile = config.LOGGER['handlers']['file']['filename']
        d = os.path.dirname(logfile)
        if not os.path.exists(d):
            os.makedirs(d)
        logging.config.dictConfig(config.LOGGER)
        lgr = logging.getLogger('user')
        if not config.VERBOSE:
            lgr.setLevel(logging.INFO)
        else:
            lgr.setLevel(logging.DEBUG)
        return lgr
    except ValueError:
        sys.exit('could not initialize logger.'
                 ' verify your logger config'
                 ' and permissions to write to {0}'
                 .format(logfile))

lgr = init_logger()


def handle(func):
    """
    handles errors triggered by fabric
    """
    def execution_handler(*args, **kwargs):
        response = func(*args, **kwargs)
        return True and lgr.debug('successfully ran command!') \
            if response.succeeded \
            else False and lgr.error('failed - {0} ({1})'.format(
                response.stderr, response.return_code))
    return execution_handler


def get_package_configuration(component):
    """
    retrieves a package's configuration from packages.PACKAGES
    """
    lgr.debug('retrieving configuration for {0}'.format(component))
    try:
        package_config = packages.PACKAGES[component]
        lgr.debug('{0} config retrieved successfully'.format(component))
        return package_config
    except KeyError:
        lgr.error('package configuration for'
                  ' {0} was not found, terminating...'.format(component))
        sys.exit(1)


def get(package=False, version=False, source_repo=False, source_ppa=False,
        source_key=False, source_url=False, key_file=False, reqs=False,
        dst_path=False, name=False, package_path=False, modules=False,
        gems=False, overwrite=True):
    """
    retrieves resources for packaging
    """

    # TODO: source_url should become source_urls list
    # define params for packaging
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
    dst_path = package['sources_path'] \
        if not dst_path else dst_path
    name = package['name'] \
        if not name else name
    package_path = package['package_path'] \
        if not package_path else package_path
    modules = package['modules'] \
        if not modules else modules
    gems = pakcage['gems'] \
        if not gems else gems
    overwrite = package['overwrite'] \
        if not overwrite else overwrite

    f_handler = FileAndDirectoryHandler()
    apt_handler = AptHandler()
    dl_handler = DownloadsHandler()
    py_handler = PythonHandler()
    ruby_handler = RubyHandler()
    # should the source dir be removed before retrieving package contents?
    if overwrite:
        lgr.info('overwrite enabled. removing directory before retrieval')
        f_handler.rmdir(dst_path)
    else:
        if os.path.isdir(dst_path):
            lgr.error('the destination directory for this package already '
                      'exists and overwrite is disabled.')
    # create the directories required for package creation...
    # TODO: remove make_package_paths and create the relevant dirs manually.
    f_handler.mkdir(package_path + '/archives')
    f_handler.mkdir(dst_path)
    # if there's a source repo to add... add it.
    # TODO: SEND LIST OF REPOS WITh MARKS
    if source_repo:
        apt_handler.add_src_repo(source_repo, 'deb')
    # if there's a source ppa to add... add it?
    if source_ppa:
        apt_handler.add_ppa_repo(source_ppa)
    # get a key for the repo if it's required..
    if source_key:
        dl_handler.wget(source_key, dst_path)
    # retrieve the source for the package
    if source_url:
        wget(
            source_url,
            dst_path)
    # add the repo key
    if key_file:
        apt_handler.add_key(key_file)
        apt_handler.apt_update()
    # apt download any other requirements if they exist
    if reqs:
        apt_handler.apt_download_reqs(reqs, dst_path)
    # download relevant python modules...
    if modules:
        for module in modules:
            py_handler.get_python_module(module, dst_path)
    # download relevant ruby gems...
    if gems:
        for gem in gems:
            ruby_handler.get_ruby_gem(gem, dst_path)


def pack(package=False, src_type=False, dst_type=False, name=False,
         src_path=False, dst_path=False, version=False, package_path=False,
         bootstrap_script=False, bootstrap_template=False, depends=False,
         bootstrap_script_in_pkg=False, config_templates=False,
         overwrite=True, config_dir=False):
    """
    uses fpm (https://github.com/jordansissel/fpm/wiki)
    to create packages
    logic documentation is in-line
    """

    # get the cwd since fpm will later change it.
    cwd = os.getcwd()

    # define params for packaging
    bootstrap_template = package[definitions.PARAM_BOOTSTRAP_TEMPLATE_PATH] \
        if definitions.PARAM_BOOTSTRAP_TEMPLATE_PATH in package \
        else bootstrap_template
    bootstrap_script = package[definitions.PARAM_BOOTSTRAP_SCRIPT_PATH] \
        if definitions.PARAM_BOOTSTRAP_SCRIPT_PATH in package \
        else bootstrap_script
    bootstrap_script_in_pkg = cwd + '/' + \
        package[definitions.PARAM_BOOTSTRAP_SCRIPT_IN_PACKAGE_PATH] \
        if definitions.PARAM_BOOTSTRAP_SCRIPT_IN_PACKAGE_PATH in package \
        else bootstrap_script_in_pkg
    src_type = package[definitions.PARAM_SOURCE_PACKAGE_TYPE] \
        if definitions.PARAM_SOURCE_PACKAGE_TYPE in package \
        else src_type
    dst_type = package[definitions.PARAM_DESTINATION_PACKAGE_TYPE] \
        if definitions.PARAM_DESTINATION_PACKAGE_TYPE in package \
        else dst_type
    name = package[definitions.PARAM_NAME] \
        if definitions.PARAM_NAME in package \
        else name
    src_path = package[definitions.PARAM_SOURCES_PATH] \
        if definitions.PARAM_SOURCES_PATH in package else src_path
    # TODO: JEEZ... this archives thing is dumb...
    # replace it with a normal destination path
    dst_path = '{0}/archives'.format(package[definitions.PARAM_SOURCES_PATH]) \
        if not dst_path \
        else dst_path
    version = package[definitions.PARAM_VERSION] \
        if definitions.PARAM_VERSION in package \
        else version
    package_path = package[definitions.PARAM_PACKAGE_PATH] \
        if definitions.PARAM_PACKAGE_PATH in package \
        else package_path
    depends = package[definitions.PARAM_DEPENDS] \
        if definitions.PARAM_DEPENDS in package \
        else depends
    config_templates = package[definitions.PARAM_CONFIG_TEMPLATE_CONFIG] \
        if definitions.PARAM_CONFIG_TEMPLATE_CONFIG in package \
        else config_templates
    overwrite = package[definitions.PARAM_OVERWRITE_OUTPUT_PACKAGE] \
        if definitions.PARAM_OVERWRITE_OUTPUT_PACKAGE in package \
        else overwrite

    f_handler = FileAndDirectoryHandler()
    tmp_handler = TemplateHandler()

    # can't use src_path == dst_path for the package... duh!
    if src_path == dst_path:
        lgr.error('source and destination paths must'
                  ' be different to avoid conflicts!')
    lgr.info('cleaning up before packaging...')

    # should the packaging process overwrite the previous packages?
    if overwrite:
        lgr.info('overwrite enabled. removing directory before packaging')
        f_handler.rmdir(package_path)
    # if the package is ...
    if src_type:
        f_handler.rmdir(dst_path)
        f_handler.mkdir(dst_path)

    lgr.info('generating package scripts and config files...')
    # if there are configuration templates to generate configs from...
    if config_templates:
        tmp_handler.generate_configs(package, f_handler)
    # if bootstrap scripts are required, generate them.
    if bootstrap_script or bootstrap_script_in_pkg:
        # TODO: handle cases where a bootstrap script is not a template.
        # bootstrap_script - a bootstrap script to be attached to the package
        # bootstrap_script_in_pkg - same but for putting inside the package
        if bootstrap_template and bootstrap_script:
            tmp_handler.create_bootstrap_script(package, bootstrap_template,
                                                bootstrap_script)
        if bootstrap_template and bootstrap_script_in_pkg:
            tmp_handler.create_bootstrap_script(package, bootstrap_template,
                                                bootstrap_script_in_pkg)
            # if it's in_pkg, grant it exec permissions and copy it to the
            # package's path.
            if bootstrap_script_in_pkg:
                lgr.debug('granting execution permissions')
                do('chmod +x {0}'.format(bootstrap_script_in_pkg))
                lgr.debug('copying bootstrap script to package directory')
                f_handler.cp(bootstrap_script_in_pkg, src_path)
    lgr.info('packing up component...')
    # if a package needs to be created (not just files copied)...
    if src_type:
        lgr.info('packing {0}'.format(name))
        # if the source dir for the package exists
        if f_handler.is_dir(src_path):
            # change the path to the destination path, since fpm doesn't accept
            # (for now) a dst dir, but rather creates the package in the cwd.
            with lcd(dst_path):
                # these will handle the different packages cases based on
                # the requirement. for instance, if a bootstrap script exists,
                # and there are dependencies for the package, run fpm with
                # the relevant flags.
                if bootstrap_script_in_pkg and dst_type == "tar":
                    do(
                        'sudo fpm -s {0} -t {1} -n {2} -v {3} -f {4}'
                        .format(src_type, "tar", name, version, src_path))
                elif bootstrap_script and not depends:
                    do(
                        'sudo fpm -s {0} -t {1} --after-install {2} -n {3}'
                        ' -v {4} -f {5}'
                        .format(src_type, dst_type, os.getcwd() + '/'
                                + bootstrap_script, name, version, src_path))
                elif bootstrap_script and depends:
                    lgr.debug('package dependencies are: {0}'.format(", "
                              .join(depends)))
                    dep_str = "-d " + " -d ".join(depends)
                    do(
                        'sudo fpm -s {0} -t {1} --after-install {2} {3} -n {4}'
                        ' -v {5} -f {6}'
                        .format(src_type, dst_type, os.getcwd() + '/'
                                + bootstrap_script, dep_str,
                                name, version, src_path))
                # else just create a package with default flags...
                else:
                    if dst_type.startswith("tar"):
                        do(
                            'sudo fpm -s {0} -t {1} -n {2} -v {3} -f {4}'
                            .format(src_type, "tar", name, version, src_path))
                    else:
                        do(
                            'sudo fpm -s {0} -t {1} -n {2} -v {3} -f {4}'
                            .format(src_type, dst_type, name,
                                    version, src_path))
                    if dst_type == "tar.gz":
                        do('sudo gzip {0}*'.format(name))
                # and check if the packaging process succeeded.
                # TODO: actually test the package itself.
        # apparently, the src for creation the package doesn't exist...
        # what can you do?
        else:
            lgr.error('package dir {0} does\'nt exist, termintating...'
                      .format(src_path))
            # maybe bluntly exit since this is all irrelevant??
            sys.exit(1)

    # make sure the final destination for the package exists..
    if not f_handler.is_dir(package_path):
        f_handler.mkdir(package_path)
    lgr.info("isolating archives...")
    # and then copy the final package over..
    f_handler.cp('{0}/*.{1}'.format(dst_path, dst_type), package_path)


def do(command, sudo=False, retries=5,
       some=3, capture=False):
    """
    runs a fab local() with retries
    """
    def _execute():
        for execution in range(retries):
            try:
                if sudo:
                    local('sudo {0}'.format(command, capture))
                else:
                    local(command, capture)
                lgr.debug('successfully executed: ' + command)
                return
            except:
                lgr.warning('failed to run command: {0} -retrying ({1}/{2})'
                            .format(command, execution + 1, retries))
                sleep(some)
        lgr.error('failed to run command: {0} even after {1} retries'
                  .format(command, execution))
        sys.exit(1)

    # lgr.info('running command: {0}'.format(command))
    if config.VERBOSE:
        return _execute()
    else:
        with hide('running'):
            return _execute()


class PythonHandler():
    def pip(self, module, dir):
        """
        pip installs a module
        """
        lgr.debug('installing module {0}'.format(module))
        do('sudo {0}/pip --default-timeout=45 install {1}'
           ' --process-dependency-links'.format(dir, module))

    def get_python_module(self, module, dir):
        """
        downloads a python module
        """
        lgr.debug('downloading module {0}'.format(module))
        do('sudo /usr/local/bin/pip install --no-use-wheel \
           --process-dependency-links --download "{0}/" {1}'
           .format(dir, module))

    def check_module_installed(self, name):
        """
        checks to see that a module is installed
        """
        lgr.debug('checking to see that {0} is installed'.format(name))
        x = do('pip freeze', capture=True)
        if re.search(r'{0}'.format(name), x.stdout):
            lgr.debug('module {0} is installed'.format(name))
            return True
        else:
            lgr.debug('module {0} is not installed'.format(name))
            return False

    def venv(self, root_dir, name=False):
        """
        creates a virtualenv
        """
        lgr.debug('creating virtualenv in {0}'.format(root_dir))
        if self.check_module_installed('virtualenv'):
            do('virtualenv {0}'.format(root_dir))
        else:
            lgr.error('virtualenv is not installed. terminating')
            sys.exit()


class FileAndDirectoryHandler():
    def find_in_dir(self, dir, pattern):
        """
        finds a string/file pattern in a dir
        """
        lgr.debug('looking for {0} in {1}'.format(pattern, dir))
        x = do('find {0} -iname "{1}" -exec echo {} \;'
               .format(dir, pattern), capture=True)
        return x.stdout if x.succeeded else None

    def is_dir(self, dir):
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

    def mkdir(self, dir):
        """
        creates (recursively) a directory
        """
        lgr.debug('creating directory {0}'.format(dir))
        if not os.path.isdir(dir):
            do('sudo mkdir -p {0}'.format(dir))
        else:
            lgr.debug('directory already exists, skipping.')

    def rmdir(self, dir):
        """
        deletes a directory
        """
        lgr.debug('attempting to remove directory {0}'.format(dir))
        print dir
        if os.path.isdir(dir):
            do('sudo rm -rf {0}'.format(dir))
        else:
            lgr.warning('dir doesn\'t exist')

    def rm(self, file):
        """
        deletes a file or a set of files
        """
        lgr.info('removing files {0}'.format(file))
        if os.path.isfile(file):
            do('sudo rm {0}'.format(file))
        else:
            lgr.warning('file(s) do(es)n\'t exist')

    def cp(self, src, dst, recurse=True):
        """
        copies (recuresively or not) files or directories
        """
        lgr.debug('copying {0} to {1}'.format(src, dst))
        if recurse:
            do('sudo cp -R {0} {1}'.format(src, dst))
        else:
            do('sudo cp {0} {1}'.format(src, dst))

    # TODO: depracate this useless thing...
    def make_package_paths(self, pkg_dir, tmp_dir):
        """
        DEPRACATED!
        creates directories for managing packages
        """
        # this is stupid... remove it soon...
        lgr.debug('creating package directories')
        self.mkdir('%s/archives' % tmp_dir)
        self.mkdir(pkg_dir)

    def tar(self, chdir, output_file, input):
        """
        tars an input file or directory
        """
        lgr.debug('tar-ing {0}'.format(output_file))
        do('sudo tar -C {0} -czvf {1} {2}'.format(chdir, output_file,
                                                  input))

    def untar(self, chdir, input_file):
        """
        untars a dir
        """
        lgr.debug('tar-ing {0}'.format(input_file))
        do('sudo tar -C {0} -xzvf {1}'.format(chdir, input_file))


class RubyHandler():
    # TODO: remove static paths for ruby installations..
    def get_ruby_gem(self, gem, dir):
        """
        downloads a ruby gem
        """
        lgr.debug('downloading gem {0}'.format(gem))
        try:
            do('sudo /home/vagrant/.rvm/rubies/ruby-2.1.0/bin/gem install'
               ' --no-ri --no-rdoc --install-dir {0} {1}'.format(dir, gem))
        except:
            do('sudo /usr/local/rvm/rubies/ruby-2.1.0/bin/gem install'
               ' --no-ri --no-rdoc --install-dir {0} {1}'.format(dir, gem))


class AptHandler():
    def dpkg_name(self, dir):
        """
        renames deb files to conventional names
        """

        lgr.debug('renaming deb files...')
        do('dpkg-name {0}/*.deb'.format(dir))

    # NOTE: THIS IS CURRENTLY BROKEN (it should dig a bit deeper)
    def check_if_package_is_installed(self, package):
        """
        checks if a package is installed
        """

        lgr.debug('checking if {0} is installed'.format(package))
        try:
            do('sudo dpkg -s {0}'.format(package))
            lgr.debug('{0} is installed'.format(package))
            return True
        except:
            lgr.error('{0} is not installed'.format(package))
            return False

    def apt_download_reqs(self, req_list, sources_path):

        for req in req_list:
            self.apt_download(req, sources_path)

    def apt_autoremove(self, pkg):
        """
        autoremoves package dependencies
        """
        lgr.debug('removing unnecessary dependencies...')
        do('sudo apt-get -y autoremove {0}'.formaT(pkg))

    def apt_download(self, pkg, dir):
        """
        uses apt to download package debs from ubuntu's repo
        """
        lgr.debug('downloading {0} to {1}'.format(pkg, dir))
        do('sudo apt-get -y install {0} -d -o=dir::cache={1}'.format(pkg, dir))

    def add_src_repo(self, url, mark):
        """
        adds a source repo to the apt repo
        """
        lgr.debug('adding source repository {0} mark {1}'.format(url, mark))
        do('sudo sed -i "2i {0} {1}" /etc/apt/sources.list'.format(mark, url))

    def add_ppa_repo(self, url):
        """
        adds a ppa repo to the apt repo
        """
        lgr.debug('adding ppa repository {0}'.format(url))
        do('add-apt-repository -y {0}'.format(url))

    def add_key(self, key_file):
        """
        adds a key to the local repo
        """
        lgr.debug('adding key {0}'.format(key_file))
        do('sudo apt-key add {0}'.format(key_file))

    @staticmethod
    def apt_update():
        """
        runs apt-get update
        """
        lgr.debug('updating local apt repo')
        do('sudo apt-get update')

    def apt_get(self, list):
        """
        apt-get installs a package
        """
        for package in list:
            lgr.debug('installing {0}'.format(package))
            do('sudo apt-get -y install {0}'.format(package))

    def apt_purge(self, package):
        """
        completely purges a package from the local repo
        """
        lgr.debug('attemping to purge {0}'.format(package))
        do('sudo apt-get -y purge {0}'.format(package))


class DownloadsHandler():
    def wget(self, url, dir=False, file=False):
        """
        wgets a url to a destination directory or file
        """
        lgr.debug('downloading {0} to {1}'.format(url, dir))
        try:
            if file:
                x = do('sudo wget {0} -O {1}'.format(url, file))
            elif dir:
                x = do('sudo wget {0} -P {1}'.format(url, dir))
            elif dir and file:
                lgr.warning('please specify either a directory'
                            ' or file to download to, not both')
                sys.exit()
            else:
                lgr.warning('please specify at least one of dir or file.')
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
                    lgr.debug('failed to download {0} to local directory'
                              .format(url))
        except:
            lgr.error('failed downloading {0}'.format(url))


class TemplateHandler():
    # TODO: replace this with generated from template..
    def create_bootstrap_script(self, component, template_file, script_file):
        """
        creates a script file from a template file
        """
        lgr.debug('creating bootstrap script...')
        formatted_text = self.template_formatter(
            definitions.PACKAGER_TEMPLATE_PATH, template_file, component)
        self.make_file(script_file, formatted_text)

    def generate_configs(self, component, f_handler):
        """
        generates configuration files from templates
        """
        # iterate over the config_templates dict in the package's config
        for key, value in component['config_templates'].iteritems():
            # we'll make some assumptions regarding the structure of the config
            # placement. spliting and joining to make up the positions.

            # and find something to mark that you should generate a template
            # from a file
            if key.startswith('__template_file'):
                # where should config reside within the package?
                config_dir = value['config_dir']  # .split('_')[0]
                # where is the template dir?
                template_dir = '/'.join(value['template']
                                        .split('/')[:-1])
                # where is the template file?
                template_file = value['template'].split('/')[-1]
                # the output file's name is...
                output_file = value['output_file'] \
                    if 'output_file' in value \
                    else '.'.join(template_file.split('.')[:-1])
                # and its path is...
                output_path = '{0}/{1}/{2}'.format(
                    component['sources_path'], config_dir, output_file)
                # create the directory to put the config in after it's
                # generated
                f_handler.mkdir('{0}/{1}'.format(
                    component['sources_path'], config_dir))
                # and then generate the config file. WOOHOO!
                self.generate_from_template(component,
                                            output_path,
                                            template_file,
                                            template_dir)
            # or generate templates from a dir, where the difference
            # would be that the name of the output files will correspond
            # to the names of the template files (removing .template)
            elif key.startswith('__template_dir'):
                config_dir = value['config_dir']  # .split('_')[0]
                template_dir = value['templates']
                # iterate over the files in the dir...
                # and just perform the same steps as above..
                for subdir, dirs, files in os.walk(template_dir):
                    for file in files:
                        template_file = file
                        output_file = '.'.join(template_file.split('.')[:-1])
                        output_path = '{0}/{1}/{2}'.format(
                            component['sources_path'], config_dir, output_file)

                        f_handler.mkdir('{0}/{1}'.format(
                            component['sources_path'], config_dir))
                        self.generate_from_template(component,
                                                    output_path,
                                                    template_file,
                                                    template_dir)
            elif key.startswith('__config_dir'):
                config_dir = value['config_dir']
                files_dir = value['files']
                f_handler.mkdir('{0}/{1}'.format(
                    component['sources_path'], config_dir))
                f_handler.cp(files_dir + '/*', component['sources_path'] + '/'
                             + config_dir)

    def generate_from_template(self, component, output_file, template_file,
                               templates=definitions.PACKAGER_TEMPLATE_PATH):
        """
        generates configuration files from templates using jinja2
        http://jinja.pocoo.org/docs/
        """
        lgr.debug('generating config file...')
        formatted_text = self.template_formatter(
            templates, template_file, component)
        self.make_file(output_file, formatted_text)

    def template_formatter(self, template_dir, template_file, var_dict):
        """
        receives a template and returns a formatted version of it
        according to a provided variable dictionary
        """
        env = Environment(loader=FileSystemLoader(template_dir))
        template = env.get_template(template_file)

        lgr.debug('generating template from {0}/{1}'.format(
                  template_dir, template_file))
        return(template.render(var_dict))

    def make_file(self, output_file, content):
        """
        creates a file from content
        """
        if config.PRINT_TEMPLATES:
            lgr.debug('creating file: {0} with content: \n{1}'.format(
                      output_file, content))
        with open('{0}'.format(output_file), 'w+') as f:
            f.write(content)


def main():

    lgr.debug('running in main...')
    # f = FileAndDirectoryHandler()


if __name__ == '__main__':
    main()
