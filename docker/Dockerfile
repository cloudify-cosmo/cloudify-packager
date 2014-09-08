FROM ubuntu:12.04
MAINTAINER nir0s, nirc@gigaspaces.com

# CONTAINER - BASE
# update local cache
RUN apt-get update
# install 3rd party components
RUN apt-get install -y \
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

# CONTAINER - RABBITMQ
COPY
RUN apt-get install -y erlang-nox && \
    curl http://www.rabbitmq.com/releases/rabbitmq-server/v3.2.4/rabbitmq-server_3.2.4-1_all.deb --create-dirs -o /opt/tmp/rabbitmq/rabbitmq-server.deb && \
    dpkg -i /opt/tmp/rabbitmq/rabbitmq-server.deb
    # APPLY INIT SCRIPT
    # cp ${PKG_DIR}/{{ config_templates.__template_file_rabbitmq.config_dir }}/* {{ config_templates.__template_file_rabbitmq.dst_dir }} >> ${BOOTSTRAP_LOG} 2>&1
    rabbitmq-plugins enable rabbitmq_management
    rabbitmq-plugins enable rabbitmq_tracing
    /usr/sbin/rabbitmqctl stop
    start rabbitmq-server
    rabbitmqctl trace_on

# CONTAINER - RIEMANN
RUN curl http://aphyr.com/riemann/riemann_0.2.6_all.deb --create-dirs -o /opt/tmp/riemann/riemann.deb && \
    dpkg -i /opt/tmp/riemann/riemann.deb && \
    curl https://s3-eu-west-1.amazonaws.com/gigaspaces-repository-eu/langohr/2.11.0/langohr.jar --create-dirs -o /usr/lib/riemann/langohr.jar && \
    chmod 644 /usr/lib/riemann/langohr.jar
    # APPLY RIEMANN INIT FILE
    # START RIEMANN

# CONTAINER - PYTHON
RUN curl --silent --show-error --retry 5 https://bootstrap.pypa.io/get-pip.py | python && \
    pip install virtualenv==1.11.4

# CONTAINER - NODEJS
RUN add-apt-repository -y ppa:chris-lea/node.js && \
    apt-get install -y nodejs

# CONTAINER - LOGSTASH
# RUN curl https://download.elasticsearch.org/logstash/logstash/logstash-1.4.2.tar.gz --create-dirs -o /opt/tmp/logstash/logstash.jar
RUN curl https://download.elasticsearch.org/logstash/logstash/logstash-1.3.2-flatjar.jar --create-dirs -o /opt/tmp/logstash/logstash.jar && \
    # ADD LOGSTASH CONFIG
    # APPLY LOGSTASH INIT FILE
    # START LOGSTASH

# CONTAINER - ELASTICSEARCH
RUN curl https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-1.0.1.tar.gz --create-dirs -o /opt/tmp/elasticsearch/elasticsearch.tar.gz && \
    tar -C /opt/ -xvf /opt/tmp/elasticsearch/elasticsearch.tar.gz && \
    ln -sf /opt/elasticsearch-* /opt/elasticsearch
    # ADD ELASTICSEARCH INIT FILE
    # START ELASTISEARCH

# CONTAINER - KIBANA
RUN curl https://download.elasticsearch.org/kibana/kibana/kibana-3.0.0milestone4.tar.gz --create-dirs -o /opt/tmp/kibana.tar.gz
    tar -C /opt/ -xzvf /opt/tmp/kibana.tar.gz && \
    ln -sf /opt/kibana-* /opt/kibana

# CONTAINER - INFLUXDB
RUN curl http://s3.amazonaws.com/influxdb/influxdb_0.8.0_amd64.deb --create-dirs -o /opt/tmp/influxdb.deb && \
    dpkg -i /opt/tmp/influxdb.deb
    /etc/init.d/influxdb start

# CONTAINER - GRAFANA
RUN curl http://grafanarel.s3.amazonaws.com/grafana-1.7.0.tar.gz --create-dirs -o /opt/tmp/grafana.tar.gz && \
    tar -C /opt/ -xzvf /opt/tmp/grafana.tar.gz && \
    ln -sf /opt/grafana-* /opt/grafana

# CONTAINER - NGINX
RUN sed -i "2i deb http://nginx.org/packages/mainline/ubuntu/ precise nginx" /etc/apt/sources.list && \
    sed -i "2i deb-src http://nginx.org/packages/mainline/ubuntu/ precise nginx" /etc/apt/sources.list && \
    curl http://nginx.org/keys/nginx_signing.key --create-dirs -o /opt/tmp/nginx/nginx_signing.key && \
    apt-key add /opt/tmp/nginx/nginx_signing.key && \
    apt-get update && \
    apt-get install -y nginx
    # APPLY NGINX CONFIG
    # START NGINX

# CONTAINER - CELERY
RUN curl https://github.com/cloudify-cosmo/cloudify-manager/archive/master.tar.gz --create-dirs -o /opt/tmp/celery/manager.tar.gz && \
    tar -C /opt/celery/cloudify.management__worker/env -xzvf /opt/tmp/celery/manager.tar.gz
    virtualenv /opt/celery/cloudify.management__worker/env && \
    /opt/celery/cloudify.management__worker/env/bin/pip install https://github.com/cloudify-cosmo/cloudify-rest-client/archive/master.tar.gz && \
    /opt/celery/cloudify.management__worker/env/bin/pip install https://github.com/cloudify-cosmo/cloudify-plugins-common/archive/master.tar.gz && \
    /opt/celery/cloudify.management__worker/env/bin/pip install /opt/celery/cloudify.management__worker/env/cloudify-manager-master/plugins/agent-installer/ && \
    /opt/celery/cloudify.management__worker/env/bin/pip install /opt/celery/cloudify.management__worker/env/cloudify-manager-master/plugins/plugin-installer/ && \
    /opt/celery/cloudify.management__worker/env/bin/pip install /opt/celery/cloudify.management__worker/env/cloudify-manager-master/plugins/riemann-controller/ && \
    /opt/celery/cloudify.management__worker/env/bin/pip install /opt/celery/cloudify.management__worker/env/cloudify-manager-master/workflows/


# CONTAINER - MANAGER
RUN curl https://github.com/cloudify-cosmo/cloudify-manager/archive/master.tar.gz --create-dirs -o /opt/tmp/manager/manager.tar.gz && \
    tar -C /opt/manager -xzvf /opt/tmp/manager/manager.tar.gz && \
    virtualenv /opt/manager && \
    /opt/manager/bin/pip install https://github.com/cloudify-cosmo/cloudify-dsl-parser/archive/master.tar.gz && \
    /opt/manager/bin/pip install https://github.com/cloudify-cosmo/cloudify-plugins-common/archive/master.tar.gz && \
    /opt/manager/cloudify-manager-master/rest-service/