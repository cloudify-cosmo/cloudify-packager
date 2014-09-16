FROM ubuntu:12.04
MAINTAINER adaml, adaml@gigaspaces.com
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# CONTAINER - BASE
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# add all init and config files
ADD conf/ /opt/tmp/
ADD init/ /opt/tmp/
# add utility functions
ADD utils/ /opt/tmp/

# allow rc policies
RUN sed -i 's/101/0/g' /usr/sbin/policy-rc.d

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

# ------------------------------------------------------------------------------------------------------------------------------------------ #
# CONTAINER - RABBITMQ, DependsOn: ~
# ------------------------------------------------------------------------------------------------------------------------------------------ #
RUN apt-get install -y erlang-nox && \
    curl http://www.rabbitmq.com/releases/rabbitmq-server/v3.2.4/rabbitmq-server_3.2.4-1_all.deb --create-dirs -o /opt/tmp/rabbitmq/rabbitmq-server.deb && \
    dpkg -i /opt/tmp/rabbitmq/rabbitmq-server.deb
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
RUN curl http://aphyr.com/riemann/riemann_0.2.6_all.deb --create-dirs -o /opt/tmp/riemann/riemann.deb && \
    dpkg -i /opt/tmp/riemann/riemann.deb && \
    curl https://s3-eu-west-1.amazonaws.com/gigaspaces-repository-eu/langohr/2.11.0/langohr.jar --create-dirs -o /usr/lib/riemann/langohr.jar && \
    chmod 644 /usr/lib/riemann/langohr.jar
    # APPLY RIEMANN INIT FILE
    # START RIEMANN
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# CONTAINER - PYTHON and VIRTUALENV DependsOn: ~
# ------------------------------------------------------------------------------------------------------------------------------------------ #
RUN curl --silent --show-error --retry 5 https://bootstrap.pypa.io/get-pip.py | python && \
    pip install virtualenv==1.11.4
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# CONTAINER - NODEJS DependsOn: ~
# ------------------------------------------------------------------------------------------------------------------------------------------ #
RUN add-apt-repository -y ppa:chris-lea/node.js && \
	apt-get update && \
    apt-get install -y nodejs
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# CONTAINER - LOGSTASH DependsOn: ~
# ------------------------------------------------------------------------------------------------------------------------------------------ #
RUN curl https://download.elasticsearch.org/logstash/logstash/logstash-1.3.2-flatjar.jar --create-dirs -o /opt/tmp/logstash/logstash.jar

##### ENV #####
ENV LOGSTASH_JAR_NAME $(basename /opt/tmp/logstash/logstash.jar)
ENV LOGSTASH_SERVICE_NAME logstash
ENV LOGSTASH_SERVICE_DIR /opt/$LOGSTASH_SERVICE_NAME/
# temp init and config files
ENV TMP_CONF_FILE /opt/tmp/conf/$LOGSTASH_SERVICE_NAME.conf
ENV TMP_INIT_FILE /opt/tmp/init/$LOGSTASH_SERVICE_NAME.conf
##### ENV #####

# inject required env vars to init script
RUN sed -i '1s/^/LOGSTASH_JAR_PATH='$LOGSTASH_SERVICE_DIR$LOGSTASH_JAR_NAME' \n/' $TMP_INIT_FILE
RUN sed -i '1s/^/LOGSTASH_CONF_PATH='/etc/$LOGSTASH_SERVICE_NAME.conf' \n/' $TMP_INIT_FILE

# create service dir
RUN /bin/bash -c 'source /opt/tmp/bootstrap_utils.sh' && \
    mkdir -p $LOGSTASH_SERVICE_DIR && \
    check_dir "$LOGSTASH_SERVICE_DIR"

# place jar in service dir
RUN /bin/bash -c 'source /opt/tmp/bootstrap_utils.sh' && \
    mv /opt/tmp/logstash/logstash.jar $LOGSTASH_SERVICE_DIR && \
    check_file "$LOGSTASH_SERVICE_DIR$LOGSTASH_JAR_NAME"
# place init script in local init dir
RUN /bin/bash -c 'source /opt/tmp/bootstrap_utils.sh' && \
    mv $TMP_INIT_FILE /etc/init/ && \
    check_file "/etc/init/$LOGSTASH_SERVICE_NAME.conf"
# place conf script in conf dir
RUN /bin/bash -c 'source /opt/tmp/bootstrap_utils.sh' && \
    mv $TMP_INIT_FILE /etc/ && \
    check_file "/etc/$LOGSTASH_SERVICE_NAME.conf"

# start logstash
RUN /bin/bash -c 'source /opt/tmp/bootstrap_utils.sh' && \
    start $LOGSTASH_SERVICE_NAME && \
    check_upstart $LOGSTASH_SERVICE_NAME

# ------------------------------------------------------------------------------------------------------------------------------------------ #
# CONTAINER - ELASTICSEARCH
# ------------------------------------------------------------------------------------------------------------------------------------------ #
RUN curl https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-1.0.1.tar.gz --create-dirs -o /opt/tmp/elasticsearch/elasticsearch.tar.gz && \
    tar -C /opt/ -xvf /opt/tmp/elasticsearch/elasticsearch.tar.gz && \
    ln -sf /opt/elasticsearch-* /opt/elasticsearch
    # ADD ELASTICSEARCH INIT FILE
    # START ELASTISEARCH
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# CONTAINER - KIBANA
# ------------------------------------------------------------------------------------------------------------------------------------------ #
RUN curl https://download.elasticsearch.org/kibana/kibana/kibana-3.0.0milestone4.tar.gz --create-dirs -o /opt/tmp/kibana.tar.gz && \
    tar -C /opt/ -xzvf /opt/tmp/kibana.tar.gz && \
    ln -sf /opt/kibana-* /opt/kibana
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# CONTAINER - INFLUXDB
# ------------------------------------------------------------------------------------------------------------------------------------------ #
RUN curl http://s3.amazonaws.com/influxdb/influxdb_0.8.0_amd64.deb --create-dirs -o /opt/tmp/influxdb.deb && \
    dpkg -i /opt/tmp/influxdb.deb && \
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
RUN curl https://codeload.github.com/cloudify-cosmo/cloudify-manager/tar.gz/master --create-dirs -o /opt/tmp/celery/manager.tar.gz && \
    mkdir -p /opt/celery/cloudify.management__worker/env && \
    tar -C /opt/celery/cloudify.management__worker/env -xzvf /opt/tmp/celery/manager.tar.gz && \
    virtualenv /opt/celery/cloudify.management__worker/env && \
    /opt/celery/cloudify.management__worker/env/bin/pip install https://github.com/cloudify-cosmo/cloudify-rest-client/archive/master.tar.gz && \
    /opt/celery/cloudify.management__worker/env/bin/pip install https://github.com/cloudify-cosmo/cloudify-plugins-common/archive/master.tar.gz && \
    /opt/celery/cloudify.management__worker/env/bin/pip install /opt/celery/cloudify.management__worker/env/cloudify-manager-master/plugins/agent-installer/ && \
    /opt/celery/cloudify.management__worker/env/bin/pip install /opt/celery/cloudify.management__worker/env/cloudify-manager-master/plugins/plugin-installer/ && \
    /opt/celery/cloudify.management__worker/env/bin/pip install /opt/celery/cloudify.management__worker/env/cloudify-manager-master/plugins/riemann-controller/ && \
    /opt/celery/cloudify.management__worker/env/bin/pip install /opt/celery/cloudify.management__worker/env/cloudify-manager-master/workflows/