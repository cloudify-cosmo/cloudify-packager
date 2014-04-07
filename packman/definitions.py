# flake8: NOQA

# packager base definitions (REQUIRED)
PACKAGER_SCRIPTS_PATH = "package-scripts"  # directory for bootstrap/download/removal/package scripts - if applicable
PACKAGER_CONFIG_PATH = "package-configuration"  # package configurations directory
PACKAGER_TEMPLATE_PATH = "package-templates"  # directory which contains configuration for all modules

# packager base config params (REQUIRED)
PARAM_NAME = 'name'  # 'string' representing the package's name
PARAM_AUTO_GET = 'auto_get'  # bool representing whether the package is automatically retrieved by packman or if there's an external logic for retrieving it
PARAM_AUTO_PACK = 'auto_pack'  # bool representing whether the package is automatically packaged by packman or if there's an external logic for packaging it
PARAM_VERSION = 'version'  # 'string' representing the package's version
PARAM_DEPENDS = 'depends'  # [list] of the dependencies of the package
PARAM_REQUIRES = 'reqs'  # [list] of the requirements to download
PARAM_PACKAGE_PATH = 'package_path'  # 'string' representing the destination path to be used in the packaging process
PARAM_SOURCES_PATH = 'sources_path'  # 'string' representing the source path to which files will be downloaded
PARAM_SOURCE_PACKAGE_TYPE = 'src_package_type'  # 'string' representing the source type of the package (as supported by fpm)
PARAM_DESTINATION_PACKAGE_TYPE = 'dst_package_type'  # 'string' representing the destination type of the package (as supported by fpm)
PARAM_BOOTSTRAP_SCRIPT_IN_PACKAGE_PATH = 'bootstrap_script_in_pkg'  # 'string' representing a bootstrap script path to be appended to a tar (copied into)
PARAM_BOOTSTRAP_SCRIPT_PATH = 'bootstrap_script'  # 'string' representing a path to which the bootstrap script (generated from the template) will be written
PARAM_BOOTSTRAP_TEMPLATE_PATH = 'bootstrap_template'  # 'string' representing a bootstrap script path to be appended to a deb or rpm (appended)
PARAM_OVERWRITE_OUTPUT_PACKAGE = 'overwrite_package'  # bool representing whether to overwrite a destination package by default
PARAM_OVERWRITE_SOURCES = 'overwrite_sources'  # bool representing whether to overwrite sources when retrieving package sources
PARAM_CONFIG_TEMPLATE_CONFIG = 'config_templates'  # {dict} of configuration files and templates
PARAM_MODULES = 'modules'  # [list] of python modules to install into a virtualenv
PARAM_GEMS = 'gems'  # [list] of ruby gems to download
PARAM_SOURCE_URLS = 'source_urls'  # 'string' representing the sources to download # TOOD: REPLACE WIT [LIST]!
PARAM_SOURCE_REPO = 'source_repo'  # 'string' representing an apt-repository to add to /etc/apt/sources.list
PARAM_SOURCE_PPA = 'source_ppa'  # 'string' representing a ppa repository to add
PARAM_SOURCE_KEY = 'source_key'  # 'string' representing an apt-key to download
PARAM_KEY_FILE_PATH = 'key_file'  # 'string' representing an apt-get to deploy
PARAM_PREREQS = 'prereqs'  # [list] of prerequirements to install from apt before retrieving the sources or packgaging

# packager config config params (REQUIRED)
PARAM_CONFIG_TEMPLATE_DIR = '__tepmlate_dir'
PARAM_CONFIG_TEMPLATE_FILE = '__tepmlate_file'
PARAM_CONFIG_CONFIG_DIR = '__config_dir'
PARAM_CONFIG_CONFIG_FILE = '__config_file'
PARAM_CONFIG_TEMPALTES_FILE_TEMPLATE_FILE = 'template'
PARAM_CONFIG_TEMPALTES_FILE_OUTPUT_FILE = 'output_file'
PARAM_CONFIG_TEMPALTES_FILE_CONFIG_DIR = 'config_dir'
PARAM_CONFIG_TEMPALTES_DIR_TEMPLATES_PATH = 'templates'
PARAM_CONFIG_TEMPALTES_DIR_CONFIG_DIR = 'config_dir'
PARAM_CONFIG_FILES_CONFIGS_PATH = 'files'
PARAM_CONFIG_FILES_CONFIGS_PATH = 'config_dir'

# user configuration (OPTIONAL)
ENV = "develop"  # github branch to use
# PACKAGER_BASE = "/vagrant"  # base packager repo dir
PACKAGES_PATH = "/packages"  # temporary directory to which items are downloaded and packages are created.
VIRTUALENVS_PATH = "/opt"  # directory for cosmo modules and virtual environments
AGENT_VIRTUALENVS_PATH = "/env"  # final directory to put the created packages in.
COMPONENT_PACKAGES_PATH = "/cloudify3-components"  # where to put 3rd party components packages
CODE_PACKAGES_PATH = "/cloudify3"  # where to put code packages
AGENT_PACKAGES_PATH = "/agents"  # where to put agent packages
