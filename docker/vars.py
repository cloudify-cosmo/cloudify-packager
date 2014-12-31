VARS = {
    "maintainer": {
        "name": "adaml",
        "email": "adaml@gigaspaces.com"
    },
    "image": {
        "repository": "phusion/baseimage",
        "tag": "0.9.15"
    },
    "rabbitmq": {
        "service_name": "rabbitmq-server",
        "reqs": [
            "curl",
            "logrotate",
            "erlang-nox",
        ],
        "ports": [
            "8080",
        ],
    },
    "riemann": {
        "service_name": "riemann",
        "reqs": [
            "curl",
            "openjdk-7-jdk"
        ],
        "package_url": "https://aphyr.com/riemann/riemann_0.2.6_all.deb",
        "langohr_url": "https://s3-eu-west-1.amazonaws.com/gigaspaces-repository-eu/langohr/2.11.0/langohr.jar",
        "config_url": "https://raw.githubusercontent.com/cloudify-cosmo/cloudify-manager/master/plugins/riemann-controller/riemann_controller/resources/manager.config",
        "ports": [],
    },
    "nodejs": {
        "reqs": [
        ],
        "repo_name": "ppa:chris-lea/node.js"
    },
    "logstash": {
        "service_name": "logstash",
        "reqs": [
            "curl",
            "openjdk-7-jdk"
        ],
        "package_url": "https://download.elasticsearch.org/logstash/logstash/logstash-1.3.2-flatjar.jar",
        "init_file": {
            "log_file": "/var/log/logstash.out",
        },
        "conf_file": {
            "conf_file_path": "/opt/tmp/conf/logstash.conf",
            "logs_queue": "cloudify-logs",
            "events_queue": "cloudify-events",
            "events_index": "cloudify_events",
            "test_tcp_port": "9999",
        },
        "params": {

        },
        "ports": [],
    },
    "elasticsearch": {
        "service_name": "elasticsearch",
        "reqs": [
            "curl",
            "openjdk-7-jdk",
        ],
        "elasticsearch_tar_url": "https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-1.0.1.tar.gz",
        "ports": ["9200"],
        "min_mem": "1024m",
        "max_mem": "1024m",
    },
    "influxdb": {
        "service_name": "influxdb",
        "reqs": [
            "curl",
        ],
        "package_url": "http://s3.amazonaws.com/influxdb/influxdb_0.8.0_amd64.deb",
        "ports": ["8086"],
    },
    "nginx": {
        "service_name": "nginx",
        "reqs": [
            "curl",
        ],
        "source_repos": [
            "deb http://nginx.org/packages/mainline/ubuntu/ precise nginx",
            "deb-src http://nginx.org/packages/mainline/ubuntu/ precise nginx",
        ],
        "params": {
            "file_server_port": "53229",
        },
        "source_key": "http://nginx.org/keys/nginx_signing.key",
        "ports": ["9200"],
    },
    "celery": {
        "service_name": "celeryd-cloudify-management",
        "reqs": [
            "curl",
            "python-dev",
            "git",
            "g++",
            "wget",
            "sudo"
        ],
        "python_install_requires": [
            "celery==3.0.24",
            "pyzmq==14.3.1"
        ],
        "modules": {
                "cloudify_rest_client": "git+git://github.com/cloudify-cosmo/cloudify-rest-client.git@master",
                "cloudify_plugins_common": "git+git://github.com/cloudify-cosmo/cloudify-plugins-common.git@master",
                "cloudify_script_plugin": "git+git://github.com/cloudify-cosmo/cloudify-script-plugin.git@master",
                "cloudify_manager": "-b master https://github.com/cloudify-cosmo/cloudify-manager.git",
            },
        "workers_autoscale": "5,2",
        "ports": [],
    },
    "manager": {
        "service_name": "manager",
        "reqs": [
            "git",
            "python2.7"
        ],
        "modules": {
            "cloudify_amqp_influxdb": "git+git://github.com/cloudify-cosmo/cloudify-amqp-influxdb.git@master",
            "cloudify_dsl_parser": "git+git://github.com/cloudify-cosmo/cloudify-dsl-parser.git@master",
            "cloudify_manager": "-b master https://github.com/cloudify-cosmo/cloudify-manager.git",
        },
        "agents": {
          "ubuntu_agent_url": "http://gigaspaces-repository-eu.s3.amazonaws.com/org/cloudify3/3.2.0/m1-RELEASE/cloudify-ubuntu-agent_3.2.0-m1-b170_amd64.deb",
          "centos_agent_url": "http://gigaspaces-repository-eu.s3.amazonaws.com/org/cloudify3/3.2.0/m1-RELEASE/cloudify-centos-final-agent_3.2.0-m1-b170_amd64.deb",
          "windows_agent_url": "http://gigaspaces-repository-eu.s3.amazonaws.com/org/cloudify3/3.2.0/m1-RELEASE/cloudify-windows-agent_3.2.0-m1-b170_amd64.deb",
        },
        "manager_rest_port": "8100",
        },
    "webui": {
        "service_name": "cloudify-ui",
        "reqs": [
            "curl",
            "g++",
            "python2.7",
            "make"
        ],
        "nodejs_latest_url": "http://nodejs.org/dist/node-latest.tar.gz",
        "ui_package_url": "http://gigaspaces-repository-eu.s3.amazonaws.com/org/cloudify3/3.2.0/m1-RELEASE/cloudify-ui_3.2.0-m1-b170_amd64.deb",
    }
}