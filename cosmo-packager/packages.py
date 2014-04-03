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

from definitions import *

PACKAGES = {
    "cloudify3": {
        "name": "cloudify3",
        "version": "3.0.0",
        "depends": [
            'cloudify3-components'
        ],
        "package_path": "/cloudify",
        "sources_path": CODE_PACKAGES_PATH,
        "src_package_type": "dir",
        "dst_package_type": "deb",
        "bootstrap_script_in_pkg": "{0}/cloudify3-bootstrap.sh".format(PACKAGER_SCRIPTS_PATH),
        "bootstrap_template": "cloudify3-bootstrap.template",
        "bootstrap_log": "/var/log/cloudify3-bootstrap.log",
        "overwrite": False,
        "config_templates": {
            "__params_celery": {
                "defaults_path": "/etc/default/celeryd-cloudify.management",
                "init_path": "/etc/init.d/celeryd-cloudify.management",
                "run_dir": "{0}/celery".format(VIRTUALENVS_PATH),
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
        "package_path": "/cloudify",
        "sources_path": COMPONENT_PACKAGES_PATH,
        "src_package_type": "dir",
        "dst_package_type": "deb",
        "bootstrap_script_in_pkg": "{0}/cloudify3-components-bootstrap.sh".format(PACKAGER_SCRIPTS_PATH),
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
                "template": "{0}/nginx/default.conf.template".format(PACKAGER_CONFIG_PATH),
                "output_file": "default.conf",
                "config_dir": "config/nginx",
                "dst_dir": "/etc/nginx/conf.d",
            },
            "__params_nginx": {
                "kibana_run_dir": "/opt/kibana3",
                "kibana_port": "3000",
                "rest_port": "80",
                "file_server_port": "53229",
                "file_server_dir": "{0}/manager/resources".format(VIRTUALENVS_PATH),
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
                "templates": "{0}/riemann".format(PACKAGER_CONFIG_PATH),
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
        "version": "3.0.0",
        "source_url": "https://github.com/cloudify-cosmo/cloudify-manager/archive/develop.tar.gz",
        "depends": [
            'ruby2.1'
        ],
        "package_path": "{0}/manager/".format(CODE_PACKAGES_PATH),
        "sources_path": "{0}/manager".format(VIRTUALENVS_PATH),
        "modules": [
            '{0}/manager/cloudify-manager-develop/rest-service/'.format(VIRTUALENVS_PATH),
            '{0}/manager/cloudify-manager-develop/plugins/agent-installer/'.format(VIRTUALENVS_PATH),
            '{0}/manager/cloudify-manager-develop/plugins/plugin-installer/'.format(VIRTUALENVS_PATH),
        ],
        "resources_path": "{0}/manager/cloudify-manager-develop/resources/rest-service/cloudify/".format(VIRTUALENVS_PATH),
        "file_server_dir": "{0}/manager/resources".format(VIRTUALENVS_PATH),
        "src_package_type": "dir",
        "dst_package_type": "deb",
        "bootstrap_script": "{0}/manager-bootstrap.sh".format(PACKAGER_SCRIPTS_PATH),
        "bootstrap_template": "manager-bootstrap.template",
        "bootstrap_params": {
            "resources_dir_src": "cosmo-manager-*/orchestrator/src/main/resources/cloudify/",
            "resources_dir_dst": "filesrv",
            "alias_file_src": "cosmo-manager-*/orchestrator/src/main/resources/org/CloudifySource/cosmo/dsl/alias-mappings.yaml",
            "alias_file_dst": "filesrv/cloudify",
        },
        "config_templates": {
            "#__template_file_init_gunicorn": {
                "template": "{0}/manager/init/manager.conf.template".format(PACKAGER_CONFIG_PATH),
                "output_file": "manager.conf",
                "config_dir": "config/init",
                "dst_dir": "/etc/init",
            },
            "#__template_file_init_workflow": {
                "template": "{0}/manager/init/workflow.conf.template".format(PACKAGER_CONFIG_PATH),
                "output_file": "manager.conf",
                "config_dir": "config/init",
                "dst_dir": "/etc/init",
            },
            "__params_init": {
                "rest_server_path": "{0}/manager/cloudify-manager-develop/rest-service/manager_rest/".format(VIRTUALENVS_PATH),
                "gunicorn_user": "root",
                "gunicorn_conf_path": "{0}/manager/config/conf/guni.conf".format(VIRTUALENVS_PATH),
                "unicorn_user": "root",
                "ruby_path": "{0}/ruby".format(VIRTUALENVS_PATH),
                "workflow_service_path": "{0}/manager/cloudify-manager-develop/workflow-service/".format(VIRTUALENVS_PATH),
                "workflow_service_logs_path": "/var/log/cosmo/blueprints",
            },
            "__template_file_conf": {
                "template": "{0}/manager/conf/guni.conf.template".format(PACKAGER_CONFIG_PATH),
                "output_file": "guni.conf",
                "config_dir": "config/conf",
                # "dst_dir": "/opt/manager/config/conf",
            },
            "__params_conf": {
                "file_server_dir": "{0}/manager/resources".format(VIRTUALENVS_PATH),
            },
            "__template_dir_init": {
                "templates": "{0}/manager/init".format(PACKAGER_CONFIG_PATH),
                "config_dir": "config/init",
                "dst_dir": "/etc/init",
            },
        }
    },
    "celery": {
        "name": "celery",
        "version": "0.0.1",
        "source_url": "https://github.com/cloudify-cosmo/cloudify-manager/archive/develop.tar.gz",
        "package_path": "{0}/celery/".format(CODE_PACKAGES_PATH),
        "sources_path": "{0}/celery/cloudify.management__worker/env".format(VIRTUALENVS_PATH),
        "modules": ['billiard==2.7.3.28', 'celery==3.0.24', 'bernhard', 'pika',
                    '{0}/manager/cloudify-manager-develop/plugins/agent-installer/'.format(VIRTUALENVS_PATH),
                    '{0}/manager/cloudify-manager-develop/plugins/plugin-installer/'.format(VIRTUALENVS_PATH),
                    'https://github.com/cloudify-cosmo/cloudify-plugins-common/archive/develop.tar.gz',
        ],
        "src_package_type": "dir",
        "dst_package_type": "deb",
        "bootstrap_script": "{0}/celery-bootstrap.sh".format(PACKAGER_SCRIPTS_PATH),
        "bootstrap_template": "celery-bootstrap.template",
        "config_templates": {
            "__template_file_init": {
                "template": "{0}/celery/init/celeryd-cloudify.management.template".format(PACKAGER_CONFIG_PATH),
                "output_file": "celeryd-cloudify.management",
                "config_dir": "config/init",
                "dst_dir": "/etc/init.d",
            },
            "__params_init": {
                "defaults_file": "/etc/default/celeryd-cloudify.management",
                "base_dir": "/opt/celery",
            },
            "__template_file_conf": {
                "template": "{0}/celery/conf/celeryd-cloudify.management.template".format(PACKAGER_CONFIG_PATH),
                "output_file": "celeryd-cloudify.management",
                "config_dir": "config/conf",
                "dst_dir": "/etc/default",
            },
            "__params_conf": {
                "work_dir": "{0}/celery/cloudify.management__worker/work".format(VIRTUALENVS_PATH),
                "base": "/opt/celery",
                "rest_port": "8100",
                "file_server_port": "53229",
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
        "package_path": "{0}/cosmo-ui/".format(CODE_PACKAGES_PATH),
        "sources_path": "{0}/cosmo-ui".format(PACKAGES_PATH),
        "src_package_type": "dir",
        "dst_package_type": "deb",
        "bootstrap_script": "{0}/cosmo-ui-bootstrap.sh".format(PACKAGER_SCRIPTS_PATH),
        "bootstrap_template": "cosmo-ui-bootstrap.template",
        "config_templates": {
            "__template_file_init": {
                "template": "{0}/cosmo-ui/init/cosmo-ui.conf.template".format(PACKAGER_CONFIG_PATH),
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
    "linux-agent": {
        "name": "linux-agent",
        "version": "3.0.0",
        "source_url": "https://github.com/cloudify-cosmo/cloudify-manager/archive/develop.tar.gz",
        "package_path": "{0}/linux-agent".format(AGENT_PACKAGES_PATH),
        "sources_path": "/linux-agent/env",
        "modules": ['billiard==2.7.3.28', 'celery==3.0.24', 'bernhard', 'pika',
                    '{0}/manager/cloudify-manager-develop/plugins/agent-installer/'.format(VIRTUALENVS_PATH),
                    '{0}/manager/cloudify-manager-develop/plugins/plugin-installer/'.format(VIRTUALENVS_PATH),
                    'https://github.com/cloudify-cosmo/cloudify-plugins-common/archive/develop.tar.gz',
        ],
        "src_package_type": "dir",
        "dst_package_type": "tar.gz",
    },
    "ubuntu-agent": {
        "name": "ubuntu-agent",
        "version": "3.0.0",
        "package_path": "{0}/Ubuntu-agent/".format(AGENT_PACKAGES_PATH),
        "sources_path": "/agents/linux-agent",  # .format(AGENT_PACKAGES_PATH),
        "src_package_type": "dir",
        "dst_package_type": "deb",
        "bootstrap_script": "{0}/agent-ubuntu-bootstrap.sh".format(PACKAGER_SCRIPTS_PATH),
        "bootstrap_template": "agent-ubuntu-bootstrap.template",
        "bootstrap_params": {
            "file_server_path": "{0}/manager/resources".format(VIRTUALENVS_PATH),
            "dst_agent_location": "packages/agents",
            "dst_template_location": "packages/templates",
        },
        # TODO: CREATE INIT AND DEFAULTS FILES FROM TEMPLATES!
        "config_templates": {
            "__config_dir": {
                "files": "{0}/linux-agent".format(PACKAGER_CONFIG_PATH),
                "config_dir": "config",
                "dst_dir": "{0}/manager/resources/packages/agents/templates/".format(VIRTUALENVS_PATH),
            },
        },
    },
    "logstash": {
        "name": "logstash",
        "version": "1.3.2",
        "source_url": "https://download.elasticsearch.org/logstash/logstash/logstash-1.3.2-flatjar.jar",
        "depends": [
            'openjdk-7-jdk'
        ],
        "package_path": "{0}/logstash/".format(COMPONENT_PACKAGES_PATH),
        "sources_path": "{0}/logstash".format(PACKAGES_PATH),
        "src_package_type": "dir",
        "dst_package_type": "debs",
        "bootstrap_script": "{0}/logstash-bootstrap.sh".format(PACKAGER_SCRIPTS_PATH),
        "bootstrap_template": "logstash-bootstrap.template",
        "config_templates": {
            "__template_file_init": {
                "template": "{0}/logstash/init/logstash.conf.template".format(PACKAGER_CONFIG_PATH),
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
                "template": "{0}/logstash/conf/logstash.conf.template".format(PACKAGER_CONFIG_PATH),
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
        "package_path": "{0}/elasticsearch/".format(COMPONENT_PACKAGES_PATH),
        "sources_path": "{0}/elasticsearch".format(PACKAGES_PATH),
        "src_package_type": "dir",
        "dst_package_type": "deb",
        "bootstrap_script": "{0}/elasticsearch-bootstrap.sh".format(PACKAGER_SCRIPTS_PATH),
        "bootstrap_template": "elasticsearch-bootstrap.template",
        "config_templates": {
            "__template_file_init": {
                "template": "{0}/elasticsearch/init/elasticsearch.conf.template".format(PACKAGER_CONFIG_PATH),
                "output_file": "elasticsearch.conf",
                "config_dir": "config/init",
                "dst_dir": "/etc/init",
            },
            "__params_init": {
                "run_dir": "/opt/elasticsearch",
                "user": "root",
            },
            "__template_file_conf": {
                "template": "{0}/elasticsearch/init/elasticsearch.conf.template".format(PACKAGER_CONFIG_PATH),
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
        "package_path": "{0}/kibana3/".format(COMPONENT_PACKAGES_PATH),
        "sources_path": "{0}/kibana3".format(PACKAGES_PATH),
        "src_package_type": "dir",
        "dst_package_type": "deb",
        "bootstrap_script": "{0}/kibana-bootstrap.sh".format(PACKAGER_SCRIPTS_PATH),
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
        "key_file": "{0}/nginx/nginx_signing.key".format(PACKAGES_PATH),
        "package_path": "{0}/nginx/".format(COMPONENT_PACKAGES_PATH),
        "sources_path": "{0}/nginx".format(PACKAGES_PATH),
        "dst_package_type": "deb",
    },
    "rabbitmq-server": {
        "name": "rabbitmq-server",
        "version": "0.0.1",
        "source_repo": "http://www.rabbitmq.com/debian/ testing main",
        "source_key": "http://www.rabbitmq.com/rabbitmq-signing-key-public.asc",
        "key_file": "{0}/rabbitmq-server/rabbitmq-signing-key-public.asc".format(PACKAGES_PATH),
        "reqs": [
            "rabbitmq-server",
            "erlang-nox"
        ],
        "package_path": "{0}/rabbitmq-server/".format(COMPONENT_PACKAGES_PATH),
        "sources_path": "{0}/rabbitmq-server".format(PACKAGES_PATH),
        "dst_package_type": "deb"
    },
    "riemann": {
        "name": "riemann",
        "version": "0.2.2",
        "source_url": "http://aphyr.com/riemann/riemann_0.2.2_all.deb",
        "depends": [
            'openjdk-7-jdk'
        ],
        "package_path": "{0}/riemann/".format(COMPONENT_PACKAGES_PATH),
        "sources_path": "{0}/riemann".format(PACKAGES_PATH),
        "dst_package_type": "deb"
    },
    "nodejs": {
        "name": "nodejs",
        "version": "0.0.1",
        "reqs": [
            "nodejs"
        ],
        "source_ppa": "ppa:chris-lea/node.js",
        "package_path": "{0}/nodejs/".format(COMPONENT_PACKAGES_PATH),
        "sources_path": "{0}/nodejs".format(PACKAGES_PATH),
        "dst_package_type": "deb",
        "prereqs": ['python-software-properties', 'g++', 'make', 'python']
    },
    "openjdk-7-jdk": {
        "name": "openjdk-7-jdk",
        "version": "0.0.1",
        "reqs": [
            "openjdk-7-jdk"
        ],
        "package_path": "{0}/openjdk-7-jdk/".format(COMPONENT_PACKAGES_PATH),
        "sources_path": "{0}/openjdk-7-jdk".format(PACKAGES_PATH),
        "dst_package_type": "deb",
    },
    "virtualenv": {
        "name": "virtualenv",
        "version": "1.11.4",
        "package_path": "{0}/virtualenv/".format(COMPONENT_PACKAGES_PATH),
        "sources_path": "{0}/virtualenv".format(PACKAGES_PATH),
        "modules": ['virtualenv==1.11.4'],
        "src_package_type": "dir",
        "dst_package_type": "deb",
        "bootstrap_script": "{0}/virtualenv-bootstrap.sh".format(PACKAGER_SCRIPTS_PATH),
        "bootstrap_template": "virtualenv-bootstrap.template"
    },
    "graphite": {
        "name": "graphite",
        "version": "0.9.12",
        "package_path": "{0}/graphite/".format(COMPONENT_PACKAGES_PATH),
        "sources_path": "{0}/graphite".format(VIRTUALENVS_PATH),
        "modules": [
            'carbon==0.9.10',
            'whisper==0.9.12',
            'graphite-web==0.9.12'
        ],
        "src_package_type": "dir",
        "dst_package_type": "deb",
        "bootstrap_script": "{0}/graphite-bootstrap.sh".format(PACKAGER_SCRIPTS_PATH),
        "bootstrap_template": "graphite-bootstrap.template"
    },
    "curl": {
        "name": "curl",
        "version": "0.0.1",
        "reqs": [
            "curl",
            "libcurl3",
        ],
        "package_path": "{0}/curl/".format(COMPONENT_PACKAGES_PATH),
        "sources_path": "{0}/curl".format(PACKAGES_PATH),
        "dst_package_type": "deb",
    },
    "make": {
        "name": "make",
        "version": "0.0.1",
        "reqs": [
            "make"
        ],
        "package_path": "{0}/make/".format(COMPONENT_PACKAGES_PATH),
        "sources_path": "{0}/make".format(PACKAGES_PATH),
        "dst_package_type": "deb",
    },
    "ruby": {
        "name": "ruby2.1",
        "version": "2.1.0",
        "depends": [
            'make'
        ],
        # "source_url": "http://cache.ruby-lang.org/pub/ruby/2.1/ruby-2.1.0.tar.gz",
        "package_path": "{0}/ruby/".format(COMPONENT_PACKAGES_PATH),
        "sources_path": "{0}/ruby".format(VIRTUALENVS_PATH),
        "src_package_type": "dir",
        "dst_package_type": "deb",
        # "bootstrap_script": "%s/ruby-bootstrap.sh" % PACKAGER_SCRIPTS_PATH,
        # "bootstrap_template": "ruby-bootstrap.template",
        "ruby_build_dir": "/opt/ruby-build"
    },
    "workflow-gems": {
        "name": "workflow-gems",
        "version": "0.0.1",
        "source_url": "https://github.com/cloudify-cosmo/cloudify-manager/archive/develop.tar.gz",
        "depends": [
            'ruby2.1'
        ],
        "gemfile_location": "{0}/workflow-gems/cloudify-manager-develop/workflow-service/Gemfile".format(PACKAGES_PATH),
        "gemfile_base_dir": "{0}/workflow-gems/cloudify-manager-develop".format(PACKAGES_PATH),
        "package_path": "{0}/workflow-gems/".format(COMPONENT_PACKAGES_PATH),
        "sources_path": "{0}/workflow-gems".format(PACKAGES_PATH),
        "src_package_type": "dir",
        "dst_package_type": "deb",
        "reqs": [
            'make'
        ],
        "bootstrap_script": "{0}/workflow-gems-bootstrap.sh".format(PACKAGER_SCRIPTS_PATH),
        "bootstrap_template": "workflow-gems-bootstrap.template"
    },
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
    #     "package_path": "%s/gcc/" % COMPONENT_PACKAGES_PATH,
    #     "sources_path": "%s/gcc" % PACKAGES_PATH
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
    #     "package_path": "{0}/zlib/".format(COMPONENT_PACKAGES_PATH),
    #     "sources_path": "{0}/zlib".format(PACKAGES_PATH),
    #     "src_package_type": "dir",
    #     "dst_package_type": "deb",
    #     "bootstrap_script": "{0}/zlib-bootstrap.sh".format(PACKAGER_SCRIPTS_PATH),
    #     "bootstrap_template": "zlib-bootstrap.template"
    # },
}
