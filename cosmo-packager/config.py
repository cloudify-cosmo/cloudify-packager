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
        "package_dir": CODE_BOOTSTRAP_DIR,
        "conf_dir": PACKAGER_CONF_DIR,
        "src_package_type": "dir",
        "dst_package_type": "deb",
        "bootstrap_script_in_pkg": "{0}/cloudify3-bootstrap.sh".format(PACKAGER_SCRIPTS_DIR),
        "bootstrap_template": "cloudify3-bootstrap.template",
        "bootstrap_log": "/var/log/cloudify3-bootstrap.log",
        "overwrite": False,
        "config_templates": {
            "__params_celery": {
                "defaults_path": "/etc/default/celeryd-cloudify.management",
                "init_path": "/etc/init.d/celeryd-cloudify.management",
                "run_dir": "{0}/celery".format(VIRTUALENVS_DIR),
            },
            "__params_manager": {
                "port": "8100",
            },
            "__params_workflow": {
                "port": "8101",
            },
            "__params_ui": {
                "port": "9001",
            },
        }
    },
    "cloudify3-components": {
        "name": "cloudify3-components",
        "version": "3.0.0",
        "bootstrap_dir": "/cloudify",
        "package_dir": COMPONENTS_BOOTSTRAP_DIR,
        "conf_dir": PACKAGER_CONF_DIR,
        "src_package_type": "dir",
        "dst_package_type": "deb",
        "bootstrap_script_in_pkg": "{0}/cloudify3-components-bootstrap.sh".format(PACKAGER_SCRIPTS_DIR),
        "bootstrap_template": "cloudify3-components-bootstrap.template",
        "bootstrap_log": "/var/log/cloudify3-bootstrap.log",
        "overwrite": False,
        "bootstrap_params": {
            "req_free_mem": "10000",
            "req_free_disk": "5",
            "req_cpu_cores": "1",
            "req_arch": "x86_64",
            "req_os": "precise",
        },
        "config_templates": {
            "__template_file_nginx": {
                "template": "{0}/nginx/default.conf.template".format(PACKAGER_CONF_DIR),
                "output_file": "default.conf",
                "config_dir": "config/nginx",
                "dst_dir": "/etc/nginx/conf.d",
            },
            "__params_nginx": {
                "kibana_run_dir": "/opt/kibana3",
                "kibana_port": "3000",
                "rest_port": "80",
                "file_server_port": "53229",
                "file_server_dir": "{0}/manager/resources".format(VIRTUALENVS_DIR),
            },
            "__params_rabbitmq": {
                "port": "5672"
            },
            "__params_logstash": {
                "port": "9999"
            },
            "__params_elasticsearch": {
                "port": "9200"
            },
            "__template_dir_riemann": {
                "templates": "{0}/riemann".format(PACKAGER_CONF_DIR),
                "config_dir": "config/riemann",
                "dst_dir": "/etc/riemann",
            },
            "__params_riemann": {
                "ws_port": "5556",
                "tcp_port": "5555",
            },
            "__params_ruby": {
                "run_dir": "/opt/ruby",
            },
        }
    },
    "manager": {
        "name": "manager",
        "version": "0.0.1",
        "source_url": "https://github.com/CloudifySource/cosmo-manager/archive/develop.tar.gz",
        "depends": [
            'ruby2.1'
        ],
        "bootstrap_dir": "{0}/manager/".format(CODE_BOOTSTRAP_DIR),
        "package_dir": "{0}/manager".format(VIRTUALENVS_DIR),
        # "conf_dir": "{0}/manager".format(PACKAGER_CONF_DIR),
        "modules": ['{0}/manager/cosmo-manager-develop/manager-rest/'.format(VIRTUALENVS_DIR)],
        "resources_dir": "{0}/manager/cosmo-manager-develop/orchestrator/".format(VIRTUALENVS_DIR),
        "file_server_dir": "{0}/manager/resources".format(VIRTUALENVS_DIR),
        "src_package_type": "dir",
        "dst_package_type": "deb",
        "bootstrap_script": "{0}/manager-bootstrap.sh".format(PACKAGER_SCRIPTS_DIR),
        "bootstrap_template": "manager-bootstrap.template",
        "bootstrap_params": {
            "resources_dir_src": "cosmo-manager-*/orchestrator/src/main/resources/cloudify/",
            "resources_dir_dst": "filesrv",
            "alias_file_src": "cosmo-manager-*/orchestrator/src/main/resources/org/cloudifysource/cosmo/dsl/alias-mappings.yaml",
            "alias_file_dst": "filesrv/cloudify",
        },
        "config_templates": {
            "#__template_file_init_gunicorn": {
                "template": "{0}/manager/init/manager.conf.template".format(PACKAGER_CONF_DIR),
                "output_file": "manager.conf",
                "config_dir": "config/init",
                "dst_dir": "/etc/init",
            },
            "#__template_file_init_workflow": {
                "template": "{0}/manager/init/workflow.conf.template".format(PACKAGER_CONF_DIR),
                "output_file": "manager.conf",
                "config_dir": "config/init",
                "dst_dir": "/etc/init",
            },
            "__params_init": {
                "rest_server_path": "{0}/manager/cosmo-manager-develop/manager-rest/manager_rest/".format(VIRTUALENVS_DIR),
                "gunicorn_user": "root",
                "gunicorn_conf_path": "{0}/manager/config/conf/guni.conf".format(VIRTUALENVS_DIR),
                "unicorn_user": "root",
                "ruby_path": "{0}/ruby".format(VIRTUALENVS_DIR),
                "workflow_service_path": "{0}/manager/cosmo-manager-develop/workflow-service/".format(VIRTUALENVS_DIR),
                "workflow_service_logs_path": "/var/log/cosmo/blueprints",
            },
            "__template_file_conf": {
                "template": "{0}/manager/conf/guni.conf.template".format(PACKAGER_CONF_DIR),
                "output_file": "guni.conf",
                "config_dir": "config/conf",
                # "dst_dir": "/opt/manager/config/conf",
            },
            "__params_conf": {
                "file_server_dir": "{0}/manager/resources".format(VIRTUALENVS_DIR),
            },
            "__template_dir_init": {
                "templates": "{0}/manager/init".format(PACKAGER_CONF_DIR),
                "config_dir": "config/init",
                "dst_dir": "/etc/init",
            },
        }
    },
    "celery": {
        "name": "celery",
        "version": "0.0.1",
        "bootstrap_dir": "{0}/celery/".format(CODE_BOOTSTRAP_DIR),
        "package_dir": "{0}/celery/cloudify.management__worker/env".format(VIRTUALENVS_DIR),
        # "conf_dir": "{0}/celery".format(PACKAGER_CONF_DIR),
        "modules": ['billiard==2.7.3.28', 'celery==3.0.24', 'bernhard', 'pika',
                    'https://github.com/CloudifySource/cosmo-plugin-agent-installer/archive/develop.tar.gz',
                    'https://github.com/CloudifySource/cosmo-plugin-plugin-installer/archive/develop.tar.gz',
                    'https://github.com/CloudifySource/cosmo-plugin-kv-store/archive/develop.tar.gz',
                    'https://github.com/CloudifySource/cosmo-celery-common/archive/develop.tar.gz',
        ],
        "src_package_type": "dir",
        "dst_package_type": "deb",
        "bootstrap_script": "{0}/celery-bootstrap.sh".format(PACKAGER_SCRIPTS_DIR),
        "bootstrap_template": "celery-bootstrap.template",
        "config_templates": {
            "__template_file_init": {
                "template": "{0}/celery/init/celeryd-cloudify.management.template".format(PACKAGER_CONF_DIR),
                "output_file": "celeryd-cloudify.management",
                "config_dir": "config/init",
                "dst_dir": "/etc/init.d",
            },
            "__params_init": {
                "defaults_file": "/etc/default/celeryd-cloudify.management",
                "base_dir": "/opt/celery",
            },
            "__template_file_conf": {
                "template": "{0}/celery/conf/celeryd-cloudify.management.template".format(PACKAGER_CONF_DIR),
                "output_file": "celeryd-cloudify.management",
                "config_dir": "config/conf",
                "dst_dir": "/etc/default",
            },
            "__params_conf": {
                "work_dir": "{0}/celery/cloudify.management__worker/work".format(VIRTUALENVS_DIR),
                "base": "/opt/celery",
                "rest_port": "8100",
            }
        }
    },
    "cosmo-ui": {
        "name": "cosmo-ui",
        "version": "1.0.0",
        "source_url": "http://builds.gsdev.info/cosmo-ui/1.0.0/cosmo-ui-1.0.0-latest.tgz",
        "depends": [
            'nodejs'
        ],
        "bootstrap_dir": "{0}/cosmo-ui/".format(CODE_BOOTSTRAP_DIR),
        "package_dir": "{0}/cosmo-ui".format(PACKAGES_DIR),
        # "conf_dir": "{0}/cosmo-ui".format(PACKAGER_CONF_DIR),
        "src_package_type": "dir",
        "dst_package_type": "deb",
        "bootstrap_script": "{0}/cosmo-ui-bootstrap.sh".format(PACKAGER_SCRIPTS_DIR),
        "bootstrap_template": "cosmo-ui-bootstrap.template",
        "config_templates": {
            "__template_file_init": {
                "template": "{0}/cosmo-ui/init/cosmo-ui.conf.template".format(PACKAGER_CONF_DIR),
                "output_file": "cosmo-ui.conf",
                "config_dir": "config/init",
                "dst_dir": "/etc/init",
            },
            "__params_init": {
                "log_file": "/var/log/cosmo-ui/cosmo-ui.log",
                "user": "root",
                "run_dir": "/opt/cosmo-ui",
            }
        }
    },
    "logstash": {
        "name": "logstash",
        "version": "1.3.2",
        "source_url": "https://download.elasticsearch.org/logstash/logstash/logstash-1.3.2-flatjar.jar",
        "depends": [
            'openjdk-7-jdk'
        ],
        "bootstrap_dir": "{0}/logstash/".format(COMPONENTS_BOOTSTRAP_DIR),
        "package_dir": "{0}/logstash".format(PACKAGES_DIR),
        "conf_dir": "{0}/logstash".format(PACKAGER_CONF_DIR),
        "src_package_type": "dir",
        "dst_package_type": "deb",
        "bootstrap_script": "{0}/logstash-bootstrap.sh".format(PACKAGER_SCRIPTS_DIR),
        "bootstrap_template": "logstash-bootstrap.template",
        "config_templates": {
            "__template_file_init": {
                "template": "{0}/logstash/init/logstash.conf.template".format(PACKAGER_CONF_DIR),
                "output_file": "logstash.conf",
                "config_dir": "config/init",
                "dst_dir": "/etc/init",
            },
            "__params_init": {
                "jar": "logstash.jar",
                "log_file": "/var/log/logstash.out",
                "conf_path": "/etc/logstash.conf",
                "run_dir": "/opt/logstash",
                "user": "root",
            },
            "__template_file_conf": {
                "template": "{0}/logstash/conf/logstash.conf.template".format(PACKAGER_CONF_DIR),
                "output_file": "logstash.conf",
                "config_dir": "config/conf",
                "dst_dir": "/etc",
            },
            "__params_conf": {
                "events_queue": "cloudify-events",
                "logs_queue": "cloudify-logs",
                "test_tcp_port": "9999",
                "events_index": "cloudify_events",
            }
        }
    },
    "elasticsearch": {
        "name": "elasticsearch",
        "version": "1.0.1",
        "source_url": "https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-1.0.1.tar.gz",
        "depends": [
            'openjdk-7-jdk'
        ],
        "bootstrap_dir": "{0}/elasticsearch/".format(COMPONENTS_BOOTSTRAP_DIR),
        "package_dir": "{0}/elasticsearch".format(PACKAGES_DIR),
        "conf_dir": "{0}/elasticsearch".format(PACKAGER_CONF_DIR),
        "src_package_type": "dir",
        "dst_package_type": "deb",
        "bootstrap_script": "{0}/elasticsearch-bootstrap.sh".format(PACKAGER_SCRIPTS_DIR),
        "bootstrap_template": "elasticsearch-bootstrap.template",
        "config_templates": {
            "__template_file_init": {
                "template": "{0}/elasticsearch/init/elasticsearch.conf.template".format(PACKAGER_CONF_DIR),
                "output_file": "elasticsearch.conf",
                "config_dir": "config/init",
                "dst_dir": "/etc/init",
            },
            "__params_init": {
                "run_dir": "/opt/elasticsearch",
                "user": "root",
            },
            "__template_file_conf": {
                "template": "{0}/elasticsearch/init/elasticsearch.conf.template".format(PACKAGER_CONF_DIR),
                "output_file": "elasticsearch.conf",
                "config_dir": "config/conf",
                "dst_dir": "/etc/init",
            },
            "__params_conf": {
            }
        }
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
        "bootstrap_dir": "{0}/kibana3/".format(COMPONENTS_BOOTSTRAP_DIR),
        "package_dir": "{0}/kibana3".format(PACKAGES_DIR),
        "src_package_type": "dir",
        "dst_package_type": "deb",
        "bootstrap_script": "{0}/kibana-bootstrap.sh".format(PACKAGER_SCRIPTS_DIR),
        "bootstrap_template": "kibana-bootstrap.template",
    },
    "nginx": {
        "name": "nginx",
        "version": "1.5.8",
        "reqs": [
            "nginx"
        ],
        "source_repo": "http://nginx.org/packages/mainline/ubuntu/ precise nginx",
        "source_key": "http://nginx.org/keys/nginx_signing.key",
        "key_file": "{0}/nginx/nginx_signing.key".format(PACKAGES_DIR),
        "bootstrap_dir": "{0}/nginx/".format(COMPONENTS_BOOTSTRAP_DIR),
        "package_dir": "{0}/nginx".format(PACKAGES_DIR),
        "dst_package_type": "deb",
        "conf_dir": "{0}/nginx".format(PACKAGER_CONF_DIR),
    },
    "rabbitmq-server": {
        "name": "rabbitmq-server",
        "version": "0.0.1",
        "source_repo": "http://www.rabbitmq.com/debian/ testing main",
        "source_key": "http://www.rabbitmq.com/rabbitmq-signing-key-public.asc",
        "key_file": "{0}/rabbitmq-server/rabbitmq-signing-key-public.asc".format(PACKAGES_DIR),
        "reqs": [
            "rabbitmq-server",
            "erlang-nox"
        ],
        "bootstrap_dir": "{0}/rabbitmq-server/".format(COMPONENTS_BOOTSTRAP_DIR),
        "package_dir": "{0}/rabbitmq-server".format(PACKAGES_DIR),
        "dst_package_type": "deb"
    },
    "riemann": {
        "name": "riemann",
        "version": "0.2.2",
        "source_url": "http://aphyr.com/riemann/riemann_0.2.2_all.deb",
        "depends": [
            'openjdk-7-jdk'
        ],
        "bootstrap_dir": "{0}/riemann/".format(COMPONENTS_BOOTSTRAP_DIR),
        "package_dir": "{0}/riemann".format(PACKAGES_DIR),
        "conf_dir": "{0}/riemann".format(PACKAGER_CONF_DIR),
        "dst_package_type": "deb"
    },
    "nodejs": {
        "name": "nodejs",
        "version": "0.0.1",
        "reqs": [
            "nodejs"
        ],
        "source_ppa": "ppa:chris-lea/node.js",
        "bootstrap_dir": "{0}/nodejs/".format(COMPONENTS_BOOTSTRAP_DIR),
        "package_dir": "{0}/nodejs".format(PACKAGES_DIR),
        "dst_package_type": "deb",
        "prereqs": ['python-software-properties', 'g++', 'make', 'python']
    },
    "openjdk-7-jdk": {
        "name": "openjdk-7-jdk",
        "version": "0.0.1",
        "reqs": [
            "openjdk-7-jdk"
        ],
        "bootstrap_dir": "{0}/openjdk-7-jdk/".format(COMPONENTS_BOOTSTRAP_DIR),
        "package_dir": "{0}/openjdk-7-jdk".format(PACKAGES_DIR),
        "dst_package_type": "deb",
    },
    "virtualenv": {
        "name": "virtualenv",
        "version": "1.10.1",
        "bootstrap_dir": "{0}/virtualenv/".format(COMPONENTS_BOOTSTRAP_DIR),
        "package_dir": "{0}/virtualenv".format(PACKAGES_DIR),
        "modules": ['virtualenv==1.10.1'],
        "src_package_type": "dir",
        "dst_package_type": "deb",
        "bootstrap_script": "{0}/virtualenv-bootstrap.sh".format(PACKAGER_SCRIPTS_DIR),
        "bootstrap_template": "virtualenv-bootstrap.template"
    },
    "graphite": {
        "name": "graphite",
        "version": "0.9.12",
        "bootstrap_dir": "{0}/graphite/".format(COMPONENTS_BOOTSTRAP_DIR),
        "package_dir": "{0}/graphite".format(VIRTUALENVS_DIR),
        "modules": [
            'carbon==0.9.10',
            'whisper==0.9.12',
            'graphite-web==0.9.12'
        ],
        "src_package_type": "dir",
        "dst_package_type": "deb",
        "bootstrap_script": "{0}/graphite-bootstrap.sh".format(PACKAGER_SCRIPTS_DIR),
        "bootstrap_template": "graphite-bootstrap.template"
    },
    "curl": {
        "name": "curl",
        "version": "0.0.1",
        "reqs": [
            "curl",
            "libcurl3",
        ],
        "bootstrap_dir": "{0}/curl/".format(COMPONENTS_BOOTSTRAP_DIR),
        "package_dir": "{0}/curl".format(PACKAGES_DIR),
        "dst_package_type": "deb",
    },
    "make": {
        "name": "make",
        "version": "0.0.1",
        "reqs": [
            "make"
        ],
        "bootstrap_dir": "{0}/make/".format(COMPONENTS_BOOTSTRAP_DIR),
        "package_dir": "{0}/make".format(PACKAGES_DIR),
        "dst_package_type": "deb",
    },

    "ruby": {
        "name": "ruby2.1",
        "version": "2.1.0",
        "depends": [
            'make'
        ],
        # "source_url": "http://cache.ruby-lang.org/pub/ruby/2.1/ruby-2.1.0.tar.gz",
        "bootstrap_dir": "{0}/ruby/".format(COMPONENTS_BOOTSTRAP_DIR),
        "package_dir": "{0}/ruby".format(VIRTUALENVS_DIR),
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
        "gemfile_location": "{0}/workflow-gems/cosmo-manager-develop/workflow-service/Gemfile".format(PACKAGES_DIR),
        "gemfile_base_dir": "{0}/workflow-gems/cosmo-manager-develop".format(PACKAGES_DIR),
        "bootstrap_dir": "{0}/workflow-gems/".format(COMPONENTS_BOOTSTRAP_DIR),
        "package_dir": "{0}/workflow-gems".format(PACKAGES_DIR),
        "src_package_type": "dir",
        "dst_package_type": "deb",
        "reqs": [
            'make'
        ],
        "bootstrap_script": "{0}/workflow-gems-bootstrap.sh".format(PACKAGER_SCRIPTS_DIR),
        "bootstrap_template": "workflow-gems-bootstrap.template"
    },
    "agent-ubuntu": {
        "name": "agent-Ubuntu",
        "version": "3.0.0",
        "bootstrap_dir": "{0}/agent-Ubuntu/".format(AGENTS_BOOTSTRAP_DIR),
        "package_dir": "{0}/agent-Ubuntu/cloudify.management__worker/env".format(VIRTUALENVS_DIR),
        # "conf_dir": "{0}/agent-ubuntu".format(PACKAGER_CONF_DIR),
        "modules": ['billiard==2.7.3.28', 'celery==3.0.24', 'bernhard',
                    'https://github.com/CloudifySource/cosmo-plugin-agent-installer/archive/develop.tar.gz',
                    'https://github.com/CloudifySource/cosmo-plugin-plugin-installer/archive/develop.tar.gz',
                    'https://github.com/CloudifySource/cosmo-celery-common/archive/develop.tar.gz'
        ],
        "package_location": "/packages/agents/Ubuntu/Ubuntu-agent.tar.gz",
        "src_package_type": "dir",
        "dst_package_type": "tar",
        "config_templates": {
            "__template_file_init": {
                "template": "{0}/agent-ubuntu/init/celeryd-cloudify.agent.template".format(PACKAGER_CONF_DIR),
                "output_file": "celeryd-cloudify.agent",
                "config_dir": "config/init",
                "dst_dir": "/etc/init.d",
            },
            "__template_file_conf": {
                "template": "{0}/agent-ubuntu/conf/celeryd-cloudify.agent.template".format(PACKAGER_CONF_DIR),
                "output_file": "celeryd-cloudify.agent",
                "config_dir": "config/conf",
                "dst_dir": "/etc/default",
            },
            "__params_celery": {
                "defaults_path": "/etc/default/celeryd-cloudify.management",
                "init_path": "/etc/init.d/celeryd-cloudify.management",
                "run_dir": "{0}/celery".format(VIRTUALENVS_DIR),
            },
        }
        # "bootstrap_script_in_pkg": "{0}/agent-ubuntu-bootstrap.sh".format(PACKAGER_SCRIPTS_DIR),
        # "bootstrap_template": "agent-ubuntu-bootstrap.template"
    },
    "cli-ubuntu": {
        "name": "cli-ubuntu",
        "version": "0.0.1",
        "bootstrap_dir": "{0}/cli-ubuntu/".format(CODE_BOOTSTRAP_DIR),
        "package_dir": "{0}/cli-ubuntu".format(VIRTUALENVS_DIR),
        "modules": [
            'https://github.com/CloudifySource/cosmo-cli/archive/develop.zip'
        ],
        "src_package_type": "dir",
        "dst_package_type": "deb",
    }
        # "gcc": {
    #     "name": "gcc",
    #     "version": "0.0.1",
    #     "reqs": [
    #         "libc6",
    #         "libc-bin",
    #         "zlib1g-dev",
    #         "libmpc2",
    #         "libgomp1",
    #         "binutils",
    #         "cpp",
    #         "gcc-4.6",
    #         "gcc-multilib",
    #         "make",
    #         "manpages-dev",
    #         "autoconf",
    #         "automake1.9",
    #         "libtool",
    #         "flex",
    #         "bison",
    #         "gdb",
    #         "gcc-doc",
    #         "libc6-dev",
    #         "libc-dev",
    #         "gcc"
    #     ],
    #     "bootstrap_dir": "%s/gcc/" % COMPONENTS_BOOTSTRAP_DIR,
    #     "package_dir": "%s/gcc" % PACKAGES_DIR
    # },
        # "zlib": {
    #     "name": "zlib",
    #     "version": "1.2.8",
    #     "depends": [
    #         'make',
    #         'gcc'
    #     ],
    #     "source_url": "http://zlib.net/zlib-1.2.8.tar.gz",
    #     "version": "0.0.1",
    #     "bootstrap_dir": "{0}/zlib/".format(COMPONENTS_BOOTSTRAP_DIR),
    #     "package_dir": "{0}/zlib".format(PACKAGES_DIR),
    #     "src_package_type": "dir",
    #     "dst_package_type": "deb",
    #     "bootstrap_script": "{0}/zlib-bootstrap.sh".format(PACKAGER_SCRIPTS_DIR),
    #     "bootstrap_template": "zlib-bootstrap.template"        
    # },
}
# logger configuration
VERBOSE = False
LOGGER = {
    "version": 1,
    "formatters": {
        "file": {
            "format": "%(asctime)s %(levelname)s - %(message)s"
        },
        "console": {
            "format": "### %(message)s"
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
