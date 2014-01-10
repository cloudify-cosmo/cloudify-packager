PACKAGER_SCRIPTS_DIR = "/cosmo-packager/cosmo-packager/package-scripts"
PACKAGER_CONF_DIR = "/cosmo-packager/cosmo-packager/package-configuration"
PACKAGES_DIR = "/packages"
PACKAGES_BOOTSTRAP_DIR = "/cosmo-bootstrap"

PACKAGES = {
    "logstash": {
        "name": "logstash",
        "version": "1.3.2",
        "source_url": "https://download.elasticsearch.org/logstash/logstash/logstash-1.3.2-flatjar.jar",
        "bootstrap_dir": "%s/logstash" % PACKAGES_BOOTSTRAP_DIR,
        "package_dir": "%s/logstash" % PACKAGES_DIR
    },
    "elasticsearch": {
        "name": "elasticsearch",
        "version": "0.90.9",
        "source_url": "https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-0.90.9.tar.gz",
        "bootstrap_dir": "%s/elasticsearch" % PACKAGES_BOOTSTRAP_DIR,
        "package_dir": "%s/elasticsearch" % PACKAGES_DIR
    },
    "jruby": {
        "name": "jruby",
        "version": "1.7.3",
        "source_url": "http://jruby.org.s3.amazonaws.com/downloads/1.7.3/jruby-bin-1.7.3.tar.gz",
        "bootstrap_dir": "%s/jruby" % PACKAGES_BOOTSTRAP_DIR,
        "package_dir": "%s/jruby" % PACKAGES_DIR
    },
    "nginx": {
        "name": "nginx",
        "version": "1.5.8",
        "source_url": "http://nginx.org/packages/mainline/ubuntu/ precise nginx",
        "source_key": "http://nginx.org/keys/nginx_signing.key",
        "key_file": "nginx_signing.key",
        "bootstrap_dir": "%s/nginx" % PACKAGES_BOOTSTRAP_DIR,
        "package_dir": "%s/nginx" % PACKAGES_DIR
    },
    "rabbitmq-server": {
        "name": "rabbitmq-server",
        "version": "",
        "source_url": "http://www.rabbitmq.com/debian/ testing main",
        "source_key": "http://www.rabbitmq.com/rabbitmq-signing-key-public.asc",
        "key_file": "rabbitmq-signing-key-public.asc",
        'erlang': "erlang-nox",
        "bootstrap_dir": "%s/rabbitmq-server" % PACKAGES_BOOTSTRAP_DIR,
        "package_dir": "%s/rabbitmq-server" % PACKAGES_DIR
    },
    "riemann": {
        "name": "riemann",
        "version": "0.2.2",
        "source_url": "http://aphyr.com/riemann/riemann_0.2.2_all.deb",
        "bootstrap_dir": "%s/riemann" % PACKAGES_BOOTSTRAP_DIR,
        "package_dir": "%s/riemann" % PACKAGES_DIR
    },
    "nodejs": {
        "name": "nodejs",
        "version": "",
        "source_url": "ppa:chris-lea/node.js",
        "bootstrap_dir": "%s/nodejs" % PACKAGES_BOOTSTRAP_DIR,
        "package_dir": "%s/nodejs" % PACKAGES_DIR,
        "prereqs": ['python-software-properties', 'g++', 'make', 'python']
    },
    "openjdk-7-jdk": {
        "name": "openjdk-7-jdk",
        "version": "",
        "bootstrap_dir": "%s/openjdk-7-jdk" % PACKAGES_BOOTSTRAP_DIR,
        "package_dir": "%s/openjdk-7-jdk" % PACKAGES_DIR
    },
    "dsl-parser-modules": {
        "name": "dsl-parser-modlues",
        "version": "",
        "bootstrap_dir": "%s/dsl-parser-modules" % PACKAGES_BOOTSTRAP_DIR,
        "package_dir": "%s/dsl-parser-modules" % PACKAGES_DIR,
        "modules": ['pyyaml', 'jsonschema']
    },
    "manager-rest-modules": {
        "name": "manager-rest-modlues",
        "version": "",
        "bootstrap_dir": "%s/manager-rest-modules" % PACKAGES_BOOTSTRAP_DIR,
        "package_dir": "%s/manager-rest-modules" % PACKAGES_DIR,
        "modules": ['Flask', 'flask-restful', 'flask-restful-swagger', 'requests', 'bernhard']
    },
    "celery-modules": {
        "name": "celery-modlues",
        "version": "",
        "bootstrap_dir": "%s/celery-modules" % PACKAGES_BOOTSTRAP_DIR,
        "package_dir": "%s/celery-modules" % PACKAGES_DIR,
        "modules": ['billiard==2.7.3.28', 'celery==3.0.24', 'bernhard']
    },
    "workflow-gems": {
        "name": "workflow-gems",
        "version": "",
        "bootstrap_dir": "%s/workflow-gems" % PACKAGES_BOOTSTRAP_DIR,
        "package_dir": "%s/workflow-gems" % PACKAGES_DIR,
        "gems": ['rufus-scheduler -v 2.0.24', 'sinatra -v 1.4.4', 'ruby_parser -v 3.1', 'ruby_parser -v 2.3', 'ruote -v 2.3.0.2', 'rest-client -v 1.6.7']
    }
}


PACKAGER_LOGGER = {
    "version": 1,
    "formatters": {
        "file": {
            "format": "%(asctime)s %(levelname)s - %(message)s"
        },
        "console": {
            "format": "%(asctime)s %(levelname)s - %(message)s"
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
            "formatter": "console"
        }
    },
    "loggers": {
        "packager": {
            "level": "DEBUG",
            "handlers": ["file", "console"]
        }
    }
}
