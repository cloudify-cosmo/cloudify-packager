FROM ubuntu:12.04
MAINTAINER adaml, adaml@gigaspaces.com
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# CONTAINER - BASE
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# add all init and config files
ADD conf/ /opt/tmp/conf/
ADD init/ /opt/tmp/init/
# add utility functions
ADD utils/ /opt/tmp/utils/

# allow rc policies
RUN sed -i 's/101/0/g' /usr/sbin/policy-rc.d

# update local cache
RUN apt-get update
# install 3rd party components
#RUN apt-get install -y \
#    python-dev \
#    make \
#    curl \
#    openjdk-7-jdk \
#    python-software-properties \
#    g++ \
#    logrotate \
#    vim \
#    mlocate

# ------------------------------------------------------------------------------------------------------------------------------------------ #
# CONTAINER - RABBITMQ, DependsOn: ~
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# install dependencies.
RUN apt-get install -y $(echo ['curl', 'logrotate', 'erlang-nox'] | tr -d "',[]")
# download rabbit package
RUN curl http://www.rabbitmq.com/releases/rabbitmq-server/v3.2.4/rabbitmq-server_3.2.4-1_all.deb --create-dirs -o /opt/tmp/rabbitmq/rabbitmq-server.deb

ENV RABBITMQ_SERVICE_NAME rabbitmq-server
ENV RABBITMQ_INIT_FILE /opt/tmp/init/$RABBITMQ_SERVICE_NAME.conf

# place init script in local init dir
RUN /bin/bash -c 'source /opt/tmp/utils/bootstrap_utils.sh && \
    mv $RABBITMQ_INIT_FILE /etc/init/ && \
    check_file "/etc/init/$RABBITMQ_SERVICE_NAME.conf"'

# install and run rabbitmq-server
RUN dpkg -i /opt/tmp/rabbitmq/rabbitmq-server.deb && \
    rabbitmq-plugins enable rabbitmq_management && \
    rabbitmq-plugins enable rabbitmq_tracing && \
    invoke-rc.d $RABBITMQ_SERVICE_NAME stop && \
    invoke-rc.d $RABBITMQ_SERVICE_NAME start && \
    rabbitmqctl trace_on
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# CONTAINER - RIEMANN, DependsOn: langohr
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# install dependencies.
RUN apt-get install -y $(echo ['curl', 'openjdk-7-jdk'] | tr -d "',[]")
# download and set permissions on langohr jar.
RUN curl https://s3-eu-west-1.amazonaws.com/gigaspaces-repository-eu/langohr/2.11.0/langohr.jar --create-dirs -o /usr/lib/riemann/langohr.jar && \
    chmod 644 /usr/lib/riemann/langohr.jar
# download riemann deb
RUN curl http://aphyr.com/riemann/riemann_0.2.6_all.deb --create-dirs -o /opt/tmp/riemann/riemann.deb

##### ENV #####
ENV RIEMANN_SERVICE_NAME riemann
# riemann init file
ENV RIEMANN_INIT_FILE /opt/tmp/init/$RIEMANN_SERVICE_NAME.conf
ENV RIEMANN_SERVICE_DIR /opt/$RIEMANN_SERVICE_NAME/
##### ENV #####

# inject required env vars to init script
RUN sed -i '1s|^|RIEMANN_JAR_PATH='$RIEMANN_SERVICE_DIR$(basename /usr/lib/riemann/langohr.jar)' \n|' $RIEMANN_INIT_FILE
# todo(adaml): inject init script the proper config path according to riemann-controller plugin path

# place jar in service dir
RUN /bin/bash -c 'source /opt/tmp/utils/bootstrap_utils.sh && \
# place init script in local init dir
RUN /bin/bash -c 'source /opt/tmp/utils/bootstrap_utils.sh && \
    mv $RIEMANN_INIT_FILE /etc/init/ && \
    check_file "/etc/init/$RIEMANN_SERVICE_NAME.conf"'

    mv /usr/lib/riemann/langohr.jar $RIEMANN_SERVICE_DIR && \
    check_file "$RIEMANN_SERVICE_DIR$(basename /usr/lib/riemann/langohr.jar)"'
# install riemann
RUN dpkg -i /opt/tmp/riemann/riemann.deb

# todo(adaml): start riemann

# ------------------------------------------------------------------------------------------------------------------------------------------ #
# CONTAINER - NODEJS DependsOn: ~
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# install dependencies.
#RUN apt-get install -y $(echo [] | tr -d "',[]")
# download and install
RUN add-apt-repository -y ppa:chris-lea/node.js && \
	apt-get update && \
    apt-get install -y nodejs
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# CONTAINER - LOGSTASH DependsOn: ~
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# install dependencies.
RUN apt-get install -y $(echo ['curl', 'openjdk-7-jdk'] | tr -d "',[]")
# download jar file
RUN curl https://download.elasticsearch.org/logstash/logstash/logstash-1.3.2-flatjar.jar --create-dirs -o /opt/tmp/logstash/logstash.jar

##### ENV #####
ENV LOGSTASH_SERVICE_NAME logstash
ENV LOGSTASH_SERVICE_DIR /opt/$LOGSTASH_SERVICE_NAME/
# logstash init file
ENV LOGSTASH_INIT_FILE /opt/tmp/init/$LOGSTASH_SERVICE_NAME.conf
# logstash conf file
ENV LOGSTASH_CONF_FILE /opt/tmp/conf/$LOGSTASH_SERVICE_NAME.conf
##### ENV #####

# inject required env vars to init script
RUN sed -i '1s|^|LOGSTASH_JAR_PATH='$LOGSTASH_SERVICE_DIR$(basename /opt/tmp/logstash/logstash.jar)' \n|' $LOGSTASH_INIT_FILE
RUN sed -i '1s|^|LOGSTASH_CONF_PATH='/etc/$LOGSTASH_SERVICE_NAME.conf' \n|' $LOGSTASH_INIT_FILE

# create service dir
RUN /bin/bash -c 'source /opt/tmp/utils/bootstrap_utils.sh && \
    mkdir -p $LOGSTASH_SERVICE_DIR && \
    check_dir "$LOGSTASH_SERVICE_DIR"'

# place jar in service dir
RUN /bin/bash -c 'source /opt/tmp/utils/bootstrap_utils.sh && \
    mv /opt/tmp/logstash/logstash.jar $LOGSTASH_SERVICE_DIR && \
    check_file "$LOGSTASH_SERVICE_DIR$(basename /opt/tmp/logstash/logstash.jar)"'
# place init script in local init dir
RUN /bin/bash -c 'source /opt/tmp/utils/bootstrap_utils.sh && \
    mv $LOGSTASH_INIT_FILE /etc/init/ && \
    check_file "/etc/init/$LOGSTASH_SERVICE_NAME.conf"'
# place conf script in conf dir
RUN /bin/bash -c 'source /opt/tmp/utils/bootstrap_utils.sh && \
    mv $LOGSTASH_CONF_FILE /etc/ && \
    check_file "/etc/$LOGSTASH_SERVICE_NAME.conf"'

# start logstash
RUN /bin/bash -c 'source /opt/tmp/utils/bootstrap_utils.sh && \
    start $LOGSTASH_SERVICE_NAME && \
    check_upstart $LOGSTASH_SERVICE_NAME'

# ------------------------------------------------------------------------------------------------------------------------------------------ #
# CONTAINER - ELASTICSEARCH
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# install dependencies
RUN apt-get install -y $(echo ['curl'] | tr -d "',[]")
# download binaries
RUN curl https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-1.0.1.tar.gz --create-dirs -o /opt/tmp/elasticsearch/elasticsearch.tar.gz

##### ENV #####
ENV ELASTICSEARCH_SERVICE_NAME elasticsearch
ENV ELASTICSEARCH_SERVICE_DIR /opt/$ELASTICSEARCH_SERVICE_NAME/

# elasticsearch init file
ENV ELASTICSEARCH_INIT_FILE /opt/tmp/init/$ELASTICSEARCH_SERVICE_NAME.conf
##### ENV #####

# inject required env vars to init script
RUN sed -i '1s|^|ELASTICSEARCH_SERVICE_DIR='$ELASTICSEARCH_SERVICE_DIR' \n|' $ELASTICSEARCH_INIT_FILE

# create service dir
RUN /bin/bash -c 'source /opt/tmp/utils/bootstrap_utils.sh && \
    mkdir -p $ELASTICSEARCH_SERVICE_DIR && \
    check_dir "$ELASTICSEARCH_SERVICE_DIR"'

# extract binaries to service dir
RUN tar -C $ELASTICSEARCH_SERVICE_DIR -xvf /opt/tmp/elasticsearch/elasticsearch.tar.gz

# place init script in local init dir
# config file is generated
RUN /bin/bash -c 'source /opt/tmp/utils/bootstrap_utils.sh && \
    mv $ELASTICSEARCH_INIT_FILE /etc/init/ && \
    check_file "/etc/init/$ELASTICSEARCH_SERVICE_NAME.conf"'

# start elasticsearch
RUN /bin/bash -c 'source /opt/tmp/utils/bootstrap_utils.sh && \
    start $ELASTICSEARCH_SERVICE_NAME && \
    check_upstart $ELASTICSEARCH_SERVICE_NAME'

# ------------------------------------------------------------------------------------------------------------------------------------------ #
# CONTAINER - INFLUXDB
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# install dependencies
RUN apt-get install -y $(echo ['curl'] | tr -d "',[]")
# download binaries
RUN curl http://s3.amazonaws.com/influxdb/influxdb_0.8.0_amd64.deb --create-dirs -o /opt/tmp/influxdb.deb
##### ENV #####
ENV INFLUXDB_SERVICE_NAME influxdb
##### ENV #####

# install influxdb
RUN dpkg -i /opt/tmp/influxdb.deb

#start influxdb
RUN /etc/init.d/$INFLUXDB_SERVICE_NAME start
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# CONTAINER - NGINX
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# add nginx repositories to sources.list file and update repo
RUN echo ['2i deb http://nginx.org/packages/mainline/ubuntu/ precise nginx', '2i deb-src http://nginx.org/packages/mainline/ubuntu/ precise nginx'] | tr -d "'["| tr ',]' '\n' >> /etc/apt/sources.list && \
    apt-get update
# install dependencies
RUN apt-get install -y $(echo ['curl', 'openjdk-7-jdk'] | tr -d "',[]")

ENV NGINX_SERVICE_NAME nginx

# download and add signing key
RUN curl http://nginx.org/keys/nginx_signing.key --create-dirs -o /opt/tmp/nginx/nginx_signing.key && \
    apt-key add /opt/tmp/nginx/nginx_signing.key

# install nginx
RUN apt-get install -y $NGINX_SERVICE_NAME

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