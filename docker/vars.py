VARS = {
    "maintainer": {
        "name": "adaml",
        "email": "adaml@gigaspaces.com"
    },
    "image": {
        "repository": "ubuntu",
        "tag": "12.04"
    },
    "rabbitmq": {
        "service_name": "rabbitmq-server",
        "reqs": [
            "curl",
            "logrotate",
            "erlang-nox",
        ],
        "package_url": "http://www.rabbitmq.com/releases/rabbitmq-server/v3.2.4/rabbitmq-server_3.2.4-1_all.deb",
        "package_dest": "/opt/tmp/rabbitmq/rabbitmq-server.deb",
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
        "package_url": "http://aphyr.com/riemann/riemann_0.2.6_all.deb",
        "package_dest": "/opt/tmp/riemann/riemann.deb",
        "langohr_url": "https://s3-eu-west-1.amazonaws.com/gigaspaces-repository-eu/langohr/2.11.0/langohr.jar",
        "langohr_dest": "/usr/lib/riemann/langohr.jar",
        "ports": [],
    },
    "python": {
        "package_url": "https://bootstrap.pypa.io/get-pip.py",
        "virtualenv_version": "1.11.4"
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
        "package_dest": "/opt/tmp/logstash/logstash.jar",
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
        ],
        "package_url": "https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-1.0.1.tar.gz",
        "package_dest": "/opt/tmp/elasticsearch/elasticsearch.tar.gz",
        "ports": [],
    },
    "kibana": {
        "service_name": "kibana",
        "package_url": "https://download.elasticsearch.org/kibana/kibana/kibana-3.0.0milestone4.tar.gz",
        "package_dest": "/opt/tmp/kibana.tar.gz",
    },
    "influxdb": {
        "package_url": "http://s3.amazonaws.com/influxdb/influxdb_0.8.0_amd64.deb",
        "package_dest": "/opt/tmp/influxdb.deb",
        "ports": [],
    },
    "celery": {
        "package_url": "https://codeload.github.com/cloudify-cosmo/cloudify-manager/tar.gz/master",
        "package_dest": "/opt/tmp/celery/manager.tar.gz",
        "untar_dest": "/opt/celery/cloudify.management__worker/env",
        "cloudify_rest_client_url": "https://github.com/cloudify-cosmo/cloudify-rest-client/archive/master.tar.gz",
        "plugins_common_url": "https://github.com/cloudify-cosmo/cloudify-plugins-common/archive/master.tar.gz",
        "ports": [],
    }
}