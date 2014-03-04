# flake8: NOQA
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

# WORKING ENVIRONMENT
ENV = "develop"
# base packager repo dir
PACKAGER_BASE = "/vagrant/cosmo-packager"
# directory for bootstrap/download/removal/package scripts - if applicable
PACKAGER_SCRIPTS_DIR = "/vagrant/cosmo-packager/package-scripts"
# package configurations directory
PACKAGER_CONF_DIR = "/vagrant/cosmo-packager/package-configuration"
# directory which contains configuration for all modules
PACKAGER_TEMPLATE_DIR = "/vagrant/cosmo-packager/package-templates"
# temporary directory to which items are downloaded and packages are created.
PACKAGES_DIR = "/packages"
# final directory to put the created packages in.
COMPONENTS_BOOTSTRAP_DIR = "/cloudify3-components"
CODE_BOOTSTRAP_DIR = "/cloudify3"
AGENTS_BOOTSTRAP_DIR = "/agents"
# directory for cosmo modules and virtual environments
VIRTUALENVS_DIR = "/opt"
# specific package configuration
PACKAGES = {
    "cloudify3": {
        "name": "cloudify3",
        "version": "3.0.0",
        "depends": [
            'cloudify3-components'
        ],
        "bootstrap_dir": "/cloudify",
        "package_dir": "%s" % CODE_BOOTSTRAP_DIR,
        "conf_dir": "%s" % PACKAGER_CONF_DIR,
        "src_package_type": "dir",
        "dst_package_type": "deb",
        "bootstrap_script_internal": "%s/cloudify3-bootstrap.sh" % PACKAGER_SCRIPTS_DIR,
        "bootstrap_template": "cloudify3-bootstrap.template",
        "bootstrap_log": "/var/log/cloudify3-bootstrap.log",
        "req_free_mem": "10000",
        "req_free_disk": "5",
        "req_cpu_cores": "1",
        "req_arch": "x86_64",
        "req_os": "precise"
    },
    "cloudify3-components": {
        "name": "cloudify3-components",
        "version": "3.0.0",
        "bootstrap_dir": "/cloudify",
        "package_dir": "%s" % COMPONENTS_BOOTSTRAP_DIR,
        "conf_dir": "%s" % PACKAGER_CONF_DIR,
        "src_package_type": "dir",
        "dst_package_type": "deb",
        "bootstrap_script_internal": "%s/cloudify3-components-bootstrap.sh" % PACKAGER_SCRIPTS_DIR,
        "bootstrap_template": "cloudify3-components-bootstrap.template",
        "bootstrap_log": "/var/log/cloudify3-bootstrap.log",
        "req_free_mem": "10000",
        "req_free_disk": "5",
        "req_cpu_cores": "1",
        "req_arch": "x86_64",
        "req_os": "precise"
    },
    "logstash": {
        "name": "logstash",
        "version": "1.3.2",
        "source_url": "https://download.elasticsearch.org/logstash/logstash/logstash-1.3.2-flatjar.jar",
        "depends": [
            'openjdk-7-jdk'
        ],
        "bootstrap_dir": "%s/logstash/" % COMPONENTS_BOOTSTRAP_DIR,
        "package_dir": "%s/logstash" % PACKAGES_DIR,
        "conf_dir": "%s/logstash" % PACKAGER_CONF_DIR,
        "src_package_type": "dir",
        "dst_package_type": "deb",
        "bootstrap_script": "%s/logstash-bootstrap.sh" % PACKAGER_SCRIPTS_DIR,
        "bootstrap_template": "logstash-bootstrap.template"
    },
    "elasticsearch": {
        "name": "elasticsearch",
        "version": "0.90.9",
        "source_url": "https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-0.90.9.tar.gz",
        "depends": [
            'openjdk-7-jdk'
        ],
        "bootstrap_dir": "%s/elasticsearch/" % COMPONENTS_BOOTSTRAP_DIR,
        "package_dir": "%s/elasticsearch" % PACKAGES_DIR,
        "conf_dir": "%s/elasticsearch" % PACKAGER_CONF_DIR,
        "src_package_type": "dir",
        "dst_package_type": "deb",
        "bootstrap_script": "%s/elasticsearch-bootstrap.sh" % PACKAGER_SCRIPTS_DIR,
        "bootstrap_template": "elasticsearch-bootstrap.template"
    },
    "kibana3": {
        "name": "kibana3",
        "version": "3.0.0milestone4",
        "source_url": "https://download.elasticsearch.org/kibana/kibana/kibana-3.0.0milestone4.tar.gz",
        "depends": [
            'openjdk-7-jdk',
            'logstash',
            'elasticsearch'
        ],
        "bootstrap_dir": "%s/kibana3/" % COMPONENTS_BOOTSTRAP_DIR,
        "package_dir": "%s/kibana3" % PACKAGES_DIR,
        "src_package_type": "dir",
        "dst_package_type": "deb",
        "bootstrap_script": "%s/kibana-bootstrap.sh" % PACKAGER_SCRIPTS_DIR,
        "bootstrap_template": "kibana-bootstrap.template"
    },
    "nginx": {
        "name": "nginx",
        "version": "1.5.8",
        "reqs": [
            "nginx"
        ],
        "source_repo": "http://nginx.org/packages/mainline/ubuntu/ precise nginx",
        "source_key": "http://nginx.org/keys/nginx_signing.key",
        "key_file": "%s/nginx/nginx_signing.key" % PACKAGES_DIR,
        "bootstrap_dir": "%s/nginx/" % COMPONENTS_BOOTSTRAP_DIR,
        "package_dir": "%s/nginx" % PACKAGES_DIR,
        "dst_package_type": "deb",
        "conf_dir": "%s/nginx" % PACKAGER_CONF_DIR
    },
    "rabbitmq-server": {
        "name": "rabbitmq-server",
        "version": "0.0.1",
        "source_repo": "http://www.rabbitmq.com/debian/ testing main",
        "source_key": "http://www.rabbitmq.com/rabbitmq-signing-key-public.asc",
        "key_file": "%s/rabbitmq-server/rabbitmq-signing-key-public.asc" % PACKAGES_DIR,
        "reqs": [
            "rabbitmq-server",
            "erlang-nox"
        ],
        "bootstrap_dir": "%s/rabbitmq-server/" % COMPONENTS_BOOTSTRAP_DIR,
        "package_dir": "%s/rabbitmq-server" % PACKAGES_DIR,
        "dst_package_type": "deb"
    },
    "riemann": {
        "name": "riemann",
        "version": "0.2.2",
        "source_url": "http://aphyr.com/riemann/riemann_0.2.2_all.deb",
        "depends": [
            'openjdk-7-jdk'
        ],
        "bootstrap_dir": "%s/riemann/" % COMPONENTS_BOOTSTRAP_DIR,
        "package_dir": "%s/riemann" % PACKAGES_DIR,
        "conf_dir": "%s/riemann" % PACKAGER_CONF_DIR,
        "dst_package_type": "deb"
    },
    "nodejs": {
        "name": "nodejs",
        "version": "0.0.1",
        "reqs": [
            "nodejs"
        ],
        "source_ppa": "ppa:chris-lea/node.js",
        "bootstrap_dir": "%s/nodejs/" % COMPONENTS_BOOTSTRAP_DIR,
        "package_dir": "%s/nodejs" % PACKAGES_DIR,
        "dst_package_type": "deb",
        "prereqs": ['python-software-properties', 'g++', 'make', 'python']
    },
    "openjdk-7-jdk": {
        "name": "openjdk-7-jdk",
        "version": "0.0.1",
        "reqs": [
            "openjdk-7-jdk"
        ],
        "bootstrap_dir": "%s/openjdk-7-jdk/" % COMPONENTS_BOOTSTRAP_DIR,
        "package_dir": "%s/openjdk-7-jdk" % PACKAGES_DIR,
        "dst_package_type": "deb",
    },
    "virtualenv": {
        "name": "virtualenv",
        "version": "1.10.1",
        "bootstrap_dir": "%s/virtualenv/" % COMPONENTS_BOOTSTRAP_DIR,
        "package_dir": "%s/virtualenv" % PACKAGES_DIR,
        "modules": ['virtualenv==1.10.1'],
        "src_package_type": "dir",
        "dst_package_type": "deb",
        "bootstrap_script": "%s/virtualenv-bootstrap.sh" % PACKAGER_SCRIPTS_DIR,
        "bootstrap_template": "virtualenv-bootstrap.template"
    },
    "graphite": {
        "name": "graphite",
        "version": "0.9.12",
        "bootstrap_dir": "%s/graphite/" % COMPONENTS_BOOTSTRAP_DIR,
        "package_dir": "%s/graphite" % VIRTUALENVS_DIR,
        "modules": [
            'carbon==0.9.10',
            'whisper==0.9.12',
            'graphite-web==0.9.12'
        ],
        "src_package_type": "dir",
        "dst_package_type": "deb",
        "bootstrap_script": "%s/graphite-bootstrap.sh" % PACKAGER_SCRIPTS_DIR,
        "bootstrap_template": "graphite-bootstrap.template"
    },
    "manager": {
        "name": "manager",
        "version": "0.0.1",
        "source_url": "https://github.com/CloudifySource/cosmo-manager/archive/develop.tar.gz",
        "depends": [
            'ruby2.1'
        ],
        "bootstrap_dir": "%s/manager/" % CODE_BOOTSTRAP_DIR,
        "package_dir": "%s/manager" % VIRTUALENVS_DIR,
        "conf_dir": "%s/manager" % PACKAGER_CONF_DIR,
        "modules": ['%s/manager/cosmo-manager-develop/manager-rest/' % VIRTUALENVS_DIR],
        "src_package_type": "dir",
        "dst_package_type": "deb",
        "bootstrap_script": "%s/manager-bootstrap.sh" % PACKAGER_SCRIPTS_DIR,
        "bootstrap_template": "manager-bootstrap.template"
    },
    "celery": {
        "name": "celery",
        "version": "0.0.1",
        "bootstrap_dir": "%s/celery/" % CODE_BOOTSTRAP_DIR,
        "package_dir": "%s/celery/cloudify.management__worker/env" % VIRTUALENVS_DIR,
        "conf_dir": "%s/celery" % PACKAGER_CONF_DIR,
        "modules": ['billiard==2.7.3.28', 'celery==3.0.24', 'bernhard', 'pika',
                    'https://github.com/CloudifySource/cosmo-plugin-agent-installer/archive/develop.tar.gz',
                    'https://github.com/CloudifySource/cosmo-plugin-openstack-provisioner/archive/develop.tar.gz',
                    'https://github.com/CloudifySource/cosmo-plugin-plugin-installer/archive/develop.tar.gz',
                    'https://github.com/CloudifySource/cosmo-plugin-riemann-configurer/archive/develop.tar.gz',
                    'https://github.com/CloudifySource/cosmo-plugin-kv-store/archive/develop.tar.gz',
                    'https://github.com/CloudifySource/cosmo-celery-common/archive/develop.tar.gz'
        ],
        "src_package_type": "dir",
        "dst_package_type": "deb",
        "bootstrap_script": "%s/celery-bootstrap.sh" % PACKAGER_SCRIPTS_DIR,
        "bootstrap_template": "celery-bootstrap.template"
    },
    "gcc": {
        "name": "gcc",
        "version": "0.0.1",
        "reqs": [
            "libc6",
            "libc-bin",
            "zlib1g-dev",
            "libmpc2",
            "libgomp1",
            "binutils",
            "cpp",
            "gcc-4.6",
            "gcc-multilib",
            "make",
            "manpages-dev",
            "autoconf",
            "automake1.9",
            "libtool",
            "flex",
            "bison",
            "gdb",
            "gcc-doc",
            "libc6-dev",
            "libc-dev",
            "gcc"
        ],
        "bootstrap_dir": "%s/gcc/" % COMPONENTS_BOOTSTRAP_DIR,
        "package_dir": "%s/gcc" % PACKAGES_DIR
    },
    "curl": {
        "name": "curl",
        "version": "0.0.1",
        "reqs": [
            "curl"
        ],
        "bootstrap_dir": "%s/curl/" % COMPONENTS_BOOTSTRAP_DIR,
        "package_dir": "%s/curl" % PACKAGES_DIR,
        "dst_package_type": "deb",
    },
    "make": {
        "name": "make",
        "version": "0.0.1",
        "reqs": [
            "make"
        ],
        "bootstrap_dir": "%s/make/" % COMPONENTS_BOOTSTRAP_DIR,
        "package_dir": "%s/make" % PACKAGES_DIR,
        "dst_package_type": "deb",
    },
    "zlib": {
        "name": "zlib",
        "version": "1.2.8",
        "depends": [
            'make',
            'gcc'
        ],
        "source_url": "http://zlib.net/zlib-1.2.8.tar.gz",
        "version": "0.0.1",
        "bootstrap_dir": "%s/zlib/" % COMPONENTS_BOOTSTRAP_DIR,
        "package_dir": "%s/zlib" % PACKAGES_DIR,
        "src_package_type": "dir",
        "dst_package_type": "deb",
        "bootstrap_script": "%s/zlib-bootstrap.sh" % PACKAGER_SCRIPTS_DIR,
        "bootstrap_template": "zlib-bootstrap.template"        
    },
    "ruby": {
        "name": "ruby2.1",
        "version": "2.1.0",
        "depends": [
            'make'
        ],
        # "source_url": "http://cache.ruby-lang.org/pub/ruby/2.1/ruby-2.1.0.tar.gz",
        "bootstrap_dir": "%s/ruby/" % COMPONENTS_BOOTSTRAP_DIR,
        "package_dir": "%s/ruby" % VIRTUALENVS_DIR,
        "src_package_type": "dir",
        "dst_package_type": "deb",
        # "bootstrap_script": "%s/ruby-bootstrap.sh" % PACKAGER_SCRIPTS_DIR,
        # "bootstrap_template": "ruby-bootstrap.template",
        "ruby_build_dir": "/opt/ruby-build"
    },
    "workflow-gems": {
        "name": "workflow-gems",
        "version": "0.0.1",
        "depends": [
            'ruby2.1'
        ],
        "gemfile_source_url": "https://github.com/CloudifySource/cosmo-manager/archive/develop.tar.gz",
        "gemfile_location": "%s/workflow-gems/cosmo-manager-develop/workflow-service/Gemfile" % PACKAGES_DIR,
        "gemfile_base_dir": "%s/workflow-gems/cosmo-manager-develop" % PACKAGES_DIR,
        "bootstrap_dir": "%s/workflow-gems/" % COMPONENTS_BOOTSTRAP_DIR,
        "package_dir": "%s/workflow-gems" % PACKAGES_DIR,
        "src_package_type": "dir",
        "dst_package_type": "deb",
        "reqs": ['make'],
        "bootstrap_script": "%s/workflow-gems-bootstrap.sh" % PACKAGER_SCRIPTS_DIR,
        "bootstrap_template": "workflow-gems-bootstrap.template"
    },
    "cosmo-ui": {
        "name": "cosmo-ui",
        "version": "1.0.0",
        "source_url": "http://builds.gsdev.info/cosmo-ui/1.0.0/cosmo-ui-1.0.0-latest.tgz",
        "depends": [
            'nodejs'
        ],
        "bootstrap_dir": "%s/cosmo-ui/" % CODE_BOOTSTRAP_DIR,
        "package_dir": "%s/cosmo-ui" % PACKAGES_DIR,
        "conf_dir": "%s/cosmo-ui" % PACKAGER_CONF_DIR,
        "src_package_type": "dir",
        "dst_package_type": "deb",
        "bootstrap_script": "%s/cosmo-ui-bootstrap.sh" % PACKAGER_SCRIPTS_DIR,
        "bootstrap_template": "cosmo-ui-bootstrap.template"
    },
    "agent-ubuntu": {
        "name": "agent-ubuntu",
        "version": "0.0.1",
        "bootstrap_dir": "%s/agent-ubuntu/" % AGENTS_BOOTSTRAP_DIR,
        "package_dir": "%s/agent-ubuntu/cloudify.management__worker/env" % VIRTUALENVS_DIR,
        "conf_dir": "%s/agent-ubuntu" % PACKAGER_CONF_DIR,
        "modules": ['billiard==2.7.3.28', 'celery==3.0.24', 'bernhard',
                    'https://github.com/CloudifySource/cosmo-plugin-agent-installer/archive/develop.tar.gz',
                    'https://github.com/CloudifySource/cosmo-plugin-plugin-installer/archive/develop.tar.gz',
                    'https://github.com/CloudifySource/cosmo-plugin-kv-store/archive/develop.tar.gz',
                    'https://github.com/CloudifySource/cosmo-celery-common/archive/develop.tar.gz'
        ],
        "src_package_type": "dir",
        "dst_package_type": "tar",
        "bootstrap_script_internal": "%s/agent-ubuntu-bootstrap.sh" % PACKAGER_SCRIPTS_DIR,
        "bootstrap_template": "agent-ubuntu-bootstrap.template"
    }
}
# logger configuration
LOGGER = {
    "version": 1,
    "formatters": {
        "file": {
            "format": "%(asctime)s %(levelname)s - %(message)s"
        },
        "console": {
            "format": "########## %(message)s"
        }
    },
    "handlers": {
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "file",
            "level": "DEBUG",
            "filename": "/var/log/packager/packager.log",
            "maxBytes": "5000000",
            "backupCount": "20"
        },
        "console": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "formatter": "console"
        }
    },
    "loggers": {
        "main": {
            "handlers": ["file", "console"]
        }
    }
}
# event broker config (if applicable)
RABBITMQ_HOST = '10.0.0.3'
# RABBITMQ_HOST = 'installcosmo.gsdev.info'
# queue name for packager events
RABBITMQ_QUEUE = 'hello'
# routing key..
RABBITMQ_ROUTING_KEY = 'packager'
# broker exchange
RABBITMQ_EXCHANGE = ''
