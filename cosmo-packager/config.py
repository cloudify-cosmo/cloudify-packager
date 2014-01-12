PACKAGER_SCRIPTS_DIR = "/cosmo-packager/cosmo-packager/package-scripts" # directory for bootstrap/download/removal/package scripts - if applicable
PACKAGER_CONF_DIR = "/cosmo-packager/cosmo-packager/package-configuration" # package configurations directory
PACKAGES_DIR = "/packages" # temporary directory to which items are downloaded and packages are created.
PACKAGES_BOOTSTRAP_DIR = "/cosmo-bootstrap" # final directory to put the created packages in.

PACKAGES = {
    "logstash": {
        "name": "logstash",
        "version": "1.3.2",
        "source_url": "https://download.elasticsearch.org/logstash/logstash/logstash-1.3.2-flatjar.jar",
        "bootstrap_dir": "%s/logstash/" % PACKAGES_BOOTSTRAP_DIR,
        "package_dir": "%s/logstash" % PACKAGES_DIR,
        "src_package_type": "dir",
        "dst_package_type": "deb",
        "bootstrap_script": "%s/logstash-bootstrap.sh" % PACKAGER_SCRIPTS_DIR
    },
    "elasticsearch": {
        "name": "elasticsearch",
        "version": "0.90.9",
        "source_url": "https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-0.90.9.tar.gz",
        "bootstrap_dir": "%s/elasticsearch/" % PACKAGES_BOOTSTRAP_DIR,
        "package_dir": "%s/elasticsearch" % PACKAGES_DIR,
        "src_package_type": "dir",
        "dst_package_type": "deb",
        "bootstrap_script": "%s/elasticsearch-bootstrap.sh" % PACKAGER_SCRIPTS_DIR
    },
    "jruby": {
        "name": "jruby",
        "version": "1.7.3",
        "source_url": "http://jruby.org.s3.amazonaws.com/downloads/1.7.3/jruby-bin-1.7.3.tar.gz",
        "bootstrap_dir": "%s/jruby/" % PACKAGES_BOOTSTRAP_DIR,
        "package_dir": "%s/jruby" % PACKAGES_DIR,
        "src_package_type": "dir",
        "dst_package_type": "deb",
        "bootstrap_script": "%s/jruby-bootstrap.sh" % PACKAGER_SCRIPTS_DIR
    },
    "nginx": {
        "name": "nginx",
        "version": "1.5.8",
        "source_url": "http://nginx.org/packages/mainline/ubuntu/ precise nginx",
        "source_key": "http://nginx.org/keys/nginx_signing.key",
        "key_file": "nginx_signing.key",
        "bootstrap_dir": "%s/nginx/" % PACKAGES_BOOTSTRAP_DIR,
        "package_dir": "%s/nginx" % PACKAGES_DIR
    },
    "rabbitmq-server": {
        "name": "rabbitmq-server",
        "version": "",
        "source_url": "http://www.rabbitmq.com/debian/ testing main",
        "source_key": "http://www.rabbitmq.com/rabbitmq-signing-key-public.asc",
        "key_file": "rabbitmq-signing-key-public.asc",
        'erlang': "erlang-nox",
        "bootstrap_dir": "%s/rabbitmq-server/" % PACKAGES_BOOTSTRAP_DIR,
        "package_dir": "%s/rabbitmq-server" % PACKAGES_DIR
    },
    "riemann": {
        "name": "riemann",
        "version": "0.2.2",
        "source_url": "http://aphyr.com/riemann/riemann_0.2.2_all.deb",
        "bootstrap_dir": "%s/riemann/" % PACKAGES_BOOTSTRAP_DIR,
        "package_dir": "%s/riemann" % PACKAGES_DIR
    },
    "nodejs": {
        "name": "nodejs",
        "version": "",
        "source_url": "ppa:chris-lea/node.js",
        "bootstrap_dir": "%s/nodejs/" % PACKAGES_BOOTSTRAP_DIR,
        "package_dir": "%s/nodejs" % PACKAGES_DIR,
        "prereqs": ['python-software-properties', 'g++', 'make', 'python']
    },
    "openjdk-7-jdk": {
        "name": "openjdk-7-jdk",
        "version": "",
        "bootstrap_dir": "%s/openjdk-7-jdk/" % PACKAGES_BOOTSTRAP_DIR,
        "package_dir": "%s/openjdk-7-jdk" % PACKAGES_DIR
    },
    "dsl-parser-modules": {
        "name": "dsl-parser-modlues",
        "version": "",
        "bootstrap_dir": "%s/dsl-parser-modules/" % PACKAGES_BOOTSTRAP_DIR,
        "package_dir": "%s/dsl-parser-modules" % PACKAGES_DIR,
        "modules": ['pyyaml', 'jsonschema'],
        "src_package_type": "dir",
        "dst_package_type": "deb",
        "bootstrap_script": "%s/dsl-parser-modules-bootstrap.sh" % PACKAGER_SCRIPTS_DIR
    },
    "manager-rest-modules": {
        "name": "manager-rest-modlues",
        "version": "",
        "bootstrap_dir": "%s/manager-rest-modules/" % PACKAGES_BOOTSTRAP_DIR,
        "package_dir": "%s/manager-rest-modules" % PACKAGES_DIR,
        "modules": ['Flask', 'flask-restful', 'flask-restful-swagger', 'requests', 'bernhard'],
        "src_package_type": "dir",
        "dst_package_type": "deb",
        "bootstrap_script": "%s/manager-rest-modules-bootstrap.sh" % PACKAGER_SCRIPTS_DIR
    },
    "celery-modules": {
        "name": "celery-modlues",
        "version": "",
        "bootstrap_dir": "%s/celery-modules/" % PACKAGES_BOOTSTRAP_DIR,
        "package_dir": "%s/celery-modules" % PACKAGES_DIR,
        "modules": ['billiard==2.7.3.28', 'celery==3.0.24', 'bernhard'],
        "src_package_type": "dir",
        "dst_package_type": "deb",
        "bootstrap_script": "%s/celery-modules-bootstrap.sh" % PACKAGER_SCRIPTS_DIR
    },
    "workflow-gems": {
        "name": "workflow-gems",
        "version": "",
        "bootstrap_dir": "%s/workflow-gems/" % PACKAGES_BOOTSTRAP_DIR,
        "package_dir": "%s/workflow-gems" % PACKAGES_DIR,
        "gems": ['rufus-scheduler -v 2.0.24', 'sinatra -v 1.4.4', 'ruby_parser -v 3.1', 'ruby_parser -v 2.3', 'ruote -v 2.3.0.2'],
        "_gems": ['rufus-scheduler -v 2.0.24', 'sinatra -v 1.4.4', 'ruby_parser -v 3.1', 'ruby_parser -v 2.3', 'ruote -v 2.3.0.2', 'rest-client -v 1.6.7'],
        "src_package_type": "dir",
        "dst_package_type": "deb",
        "bootstrap_script": "%s/workflow-gems-bootstrap.sh" % PACKAGER_SCRIPTS_DIR
    },
    "cosmo-dsl-parser": {
        "name": "cosmo-dsl-parser",
        "version": "0.0.1",
        "source_url": "https://github.com/CloudifySource/cosmo-plugin-dsl-parser/archive/develop.zip",
        "bootstrap_dir": "%s/cosmo-dsl-parser/" % PACKAGES_BOOTSTRAP_DIR,
        "package_dir": "%s/cosmo-dsl-parser" % PACKAGES_DIR,
        "src_package_type": "dir",
        "dst_package_type": "deb",
        "bootstrap_script": "%s/cosmo-dsl-parser-bootstrap.sh" % PACKAGER_SCRIPTS_DIR
    },
    "cosmo-manager": {
        "name": "cosmo-manager",
        "version": "0.0.1",
        "source_url": "https://github.com/CloudifySource/cosmo-manager/archive/develop.zip",
        "bootstrap_dir": "%s/cosmo-manager/" % PACKAGES_BOOTSTRAP_DIR,
        "package_dir": "%s/cosmo-manager" % PACKAGES_DIR,
        "src_package_type": "dir",
        "dst_package_type": "deb",
        "bootstrap_script": "%s/cosmo-manager-bootstrap.sh" % PACKAGER_SCRIPTS_DIR
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
