FROM {{ image.repository }}:{{ image.tag }}
MAINTAINER {{ maintainer.name }}, {{ maintainer.email }}
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# CONTAINER - BASE
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# update local cache
RUN apt-get update
# install 3rd party components
RUN apt-get install -y \
    python-dev \
    make \
    curl \
    openjdk-7-jdk \
    python-software-properties \
    g++ \
    logrotate \
    vim \
    mlocate

# allow rc policies
RUN sed -i 's/101/0/g' /usr/sbin/policy-rc.d

# base directory where all services will be installed.
RUN BASE_DIR=/opt/
# upstart init folder
RUN INIT_DIR=/etc/init

# add all init and config files
# ADD <src> <dest>
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# CONTAINER - RABBITMQ, DependsOn: ~
# ------------------------------------------------------------------------------------------------------------------------------------------ #
RUN apt-get install -y erlang-nox && \
    curl {{ rabbitmq.package_url }} --create-dirs -o {{ rabbitmq.package_dest }} && \
    dpkg -i {{ rabbitmq.package_dest }}
    # APPLY INIT SCRIPT
	# cp ${PKG_DIR}/{ config_templates.__template_file_rabbitmq.config_dir }/* { config_templates.__template_file_rabbitmq.dst_dir } >> ${BOOTSTRAP_LOG} 2>&1
    rabbitmq-plugins enable rabbitmq_management
    rabbitmq-plugins enable rabbitmq_tracing
    /usr/sbin/rabbitmqctl stop
    start rabbitmq-server
    rabbitmqctl trace_on
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# CONTAINER - RIEMANN, DependsOn: langohr
# ------------------------------------------------------------------------------------------------------------------------------------------ #
RUN curl {{ riemann.package_url }} --create-dirs -o {{ riemann.package_dest }} && \
    dpkg -i {{ riemann.package_dest }} && \
    curl {{ riemann.langohr_url }} --create-dirs -o {{ riemann.langohr_dest }} && \
    chmod 644 {{ riemann.langohr_dest }}
    # APPLY RIEMANN INIT FILE
    # START RIEMANN
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# CONTAINER - PYTHON and VIRTUALENV DependsOn: ~
# ------------------------------------------------------------------------------------------------------------------------------------------ #
RUN curl --silent --show-error --retry 5 {{ python.package_url }} | python && \
    pip install virtualenv=={{ python.virtualenv_version }}
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# CONTAINER - NODEJS DependsOn: ~
# ------------------------------------------------------------------------------------------------------------------------------------------ #
RUN add-apt-repository -y {{ nodejs.repo_name }} && \
	apt-get update && \
    apt-get install -y nodejs
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# CONTAINER - LOGSTASH DependsOn: ~
# ------------------------------------------------------------------------------------------------------------------------------------------ #
RUN curl {{ logstash.package_url }} --create-dirs -o {{ logstash.package_dest }}
# Set env vars.
RUN LOGSTASH_INIT_FILE={{ logstash.init_file }}
RUN LOGSTASH_CONF_FILE={{ logstash.conf_file }}
RUN LOGSTASH_HOME_DIR=${BASE_DIR} {{ logstash.install_dir_name }}
    # ADD LOGSTASH CONFIG
    # APPLY LOGSTASH INIT FILE
    # START LOGSTASH
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# CONTAINER - ELASTICSEARCH
# ------------------------------------------------------------------------------------------------------------------------------------------ #
RUN curl {{ elasticsearch.package_url }} --create-dirs -o {{ elasticsearch.package_dest }} && \
    tar -C {{ elasticsearch.untar_dest }} -xvf {{ elasticsearch.package_dest }} && \
    ln -sf {{ elasticsearch.untar_dest }}elasticsearch-* {{ elasticsearch.sim_link }}
    # ADD ELASTICSEARCH INIT FILE
    # START ELASTISEARCH
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# CONTAINER - KIBANA
# ------------------------------------------------------------------------------------------------------------------------------------------ #
RUN curl {{ kibana.package_url }} --create-dirs -o {{ kibana.package_dest }} && \
    tar -C {{ kibana.untar_dest }} -xzvf {{ kibana.package_dest }} && \
    ln -sf {{ kibana.untar_dest }}kibana-* {{ kibana.sim_link }}
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# CONTAINER - INFLUXDB
# ------------------------------------------------------------------------------------------------------------------------------------------ #
RUN curl {{ influxdb.package_url }} --create-dirs -o {{ influxdb.package_dest }} && \
    dpkg -i {{ influxdb.package_dest }} && \
    /etc/init.d/influxdb start
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# CONTAINER - NGINX
# ------------------------------------------------------------------------------------------------------------------------------------------ #
RUN sed -i "2i deb http://nginx.org/packages/mainline/ubuntu/ precise nginx" /etc/apt/sources.list && \
    sed -i "2i deb-src http://nginx.org/packages/mainline/ubuntu/ precise nginx" /etc/apt/sources.list && \
    curl http://nginx.org/keys/nginx_signing.key --create-dirs -o /opt/tmp/nginx/nginx_signing.key && \
    apt-key add /opt/tmp/nginx/nginx_signing.key && \
    apt-get update && \
    apt-get install -y nginx
    # APPLY NGINX CONFIG
    # START NGINX
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# CONTAINER - CELERY
# ------------------------------------------------------------------------------------------------------------------------------------------ #
RUN curl {{ celery.package_url }} --create-dirs -o {{ celery.package_dest }} && \
    mkdir -p {{ celery.untar_dest }} && \
    tar -C {{ celery.untar_dest }} -xzvf {{ celery.package_dest }} && \
    virtualenv {{ celery.untar_dest }} && \
    {{ celery.untar_dest }}/bin/pip install {{ celery.cloudify_rest_client_url }} && \
    {{ celery.untar_dest }}/bin/pip install {{ celery.plugins_common_url }} && \
    {{ celery.untar_dest }}/bin/pip install {{ celery.untar_dest }}/cloudify-manager-master/plugins/agent-installer/ && \
    {{ celery.untar_dest }}/bin/pip install {{ celery.untar_dest }}/cloudify-manager-master/plugins/plugin-installer/ && \
    {{ celery.untar_dest }}/bin/pip install {{ celery.untar_dest }}/cloudify-manager-master/plugins/riemann-controller/ && \
    {{ celery.untar_dest }}/bin/pip install {{ celery.untar_dest }}/cloudify-manager-master/workflows/
