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
        "ports": ["5672"],
    },
    "riemann": {
        "service_name": "riemann",
        "reqs": [
            "curl",
            "openjdk-7-jdk"
        ],
        "package_url": "https://aphyr.com/riemann/riemann_0.2.6_all.deb",
        "langohr_url": "https://s3-eu-west-1.amazonaws.com/gigaspaces-repository-eu/langohr/2.11.0/langohr.jar",
        "config_url": "https://raw.githubusercontent.com/cloudify-cosmo/cloudify-manager/3.3m5/plugins/riemann-controller/riemann_controller/resources/manager.config",
        "ports": ["5555"],
        "persistence_path": ["/etc/service/riemann"],
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
        "persistence_path": ["/etc/service/elasticsearch/data", "/etc/service/elasticsearch/logs"],
    },
    "influxdb": {
        "service_name": "influxdb",
        "reqs": [
            "curl",
        ],
        "package_url": "http://s3.amazonaws.com/influxdb/influxdb_0.8.0_amd64.deb",
        "ports": ["8086"],
        "persistence_path": ["/opt/influxdb/shared/data"],
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
        "source_key": "http://nginx.org/keys/nginx_signing.key",
        "ports": ["9200", "53229"],
    },
    "celery": {
        "service_name": "celeryd-cloudify-management",
        "reqs": [
            "curl",
            "python-dev",
            "libxslt-dev",
            "libxml2-dev",
            "git",
            "g++",
            "wget",
            "sudo"
        ],
        "python_install_requires": [
            "celery==3.1.17",
            "pyzmq==14.3.1"
        ],
        "modules": {
                "cloudify_rest_client": "git+git://github.com/cloudify-cosmo/cloudify-rest-client.git@3.3m5",
                "cloudify_plugins_common": "git+git://github.com/cloudify-cosmo/cloudify-plugins-common.git@3.3m5",
                "cloudify_script_plugin": "git+git://github.com/cloudify-cosmo/cloudify-script-plugin.git@1.3m5",
                "cloudify_diamond_plugin": "git+git://github.com/cloudify-cosmo/cloudify-diamond-plugin.git@1.3m5",
                "cloudify_agent": "git+git://github.com/cloudify-cosmo/cloudify-agent.git@3.3m5",
                "cloudify_manager": "-b 3.3m5 https://github.com/cloudify-cosmo/cloudify-manager.git",
            },
        "workers_autoscale": "5,2",
        "ports": [],
        "persistence_path": ["/root", "/etc/init.d", "/etc/default"],
    },
    "manager": {
        "service_name": "manager",
        "reqs": [
            "git",
            "python2.7"
        ],
        "modules": {
            # all these modules are only installed so we could eventually use plugin installation code
            # from cloudify-agent
            "cloudify_rest_client": "git+git://github.com/cloudify-cosmo/cloudify-rest-client.git@3.3m5",
            "cloudify_plugins_common": "git+git://github.com/cloudify-cosmo/cloudify-plugins-common.git@3.3m5",
            "cloudify_script_plugin": "git+git://github.com/cloudify-cosmo/cloudify-script-plugin.git@1.3m5",
            "cloudify_diamond_plugin": "git+git://github.com/cloudify-cosmo/cloudify-diamond-plugin.git@1.3m5",
            "cloudify_agent": "git+git://github.com/cloudify-cosmo/cloudify-agent.git@3.3m5",

            "cloudify_amqp_influxdb": "git+git://github.com/cloudify-cosmo/cloudify-amqp-influxdb.git@3.3m5",
            "cloudify_dsl_parser": "git+git://github.com/cloudify-cosmo/cloudify-dsl-parser.git@3.3m5",
            "flask_securest": "git+git://github.com/cloudify-cosmo/flask-securest.git@0.6",
            "cloudify_manager": "-b 3.3m5 https://github.com/cloudify-cosmo/cloudify-manager.git",
        },
        "ports": ["8100", "8101"],
        "persistence_path": ["/opt/manager/resources", "/var/log/cloudify"],
    },
    "webui": {
        "service_name": "cloudify-ui",
        "reqs": [
            "curl",
            "g++",
            "python2.7",
            "make"
        ],
        "nodejs_latest_url": "http://nodejs.org/dist/v0.10.25/node-v0.10.25.tar.gz",
        "ui_package_url": "http://gigaspaces-repository-eu.s3.amazonaws.com/org/cloudify3/3.3.0/m5-RELEASE/cloudify-ui_3.3.0-m5-b275_amd64.deb",
        "ports": ["80"],
    }
}
