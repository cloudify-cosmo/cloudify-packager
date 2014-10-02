FROM ubuntu:12.04
MAINTAINER adaml, adaml@gigaspaces.com
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# CONTAINER - BASE
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# add utility functions
ADD utils/ /opt/tmp/utils/

RUN apt-get update
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# CONTAINER - RABBITMQ, DependsOn: ~
# ------------------------------------------------------------------------------------------------------------------------------------------ #
##### ENV #####
ENV RABBITMQ_SERVICE_NAME rabbitmq-server
ENV RABBITMQ_SERVICE_DIR /opt/$RABBITMQ_SERVICE_NAME
#ENV RABBITMQ_RUN_FILE $RABBITMQ_SERVICE_DIR/run.sh
##### ENV #####
# add run scripts and configuration
ADD rabbitmq/ $RABBITMQ_SERVICE_DIR/

# install dependencies.
RUN apt-get install -y $(echo ['curl', 'logrotate', 'erlang-nox'] | tr -d "',[]")
# download rabbit package
RUN curl http://www.rabbitmq.com/releases/rabbitmq-server/v3.2.4/rabbitmq-server_3.2.4-1_all.deb --create-dirs -o /opt/tmp/rabbitmq/rabbitmq-server.deb

# install and run rabbitmq-server
RUN dpkg -i /opt/tmp/rabbitmq/rabbitmq-server.deb && \
    rabbitmq-plugins enable rabbitmq_management && \
    rabbitmq-plugins enable rabbitmq_tracing

# grant exec permissions
RUN chmod 0755 $RABBITMQ_RUN_FILE

# start rabbitmq
CMD /opt/rabbitmq-server/run.sh
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# CONTAINER - RIEMANN, DependsOn: langohr
# ------------------------------------------------------------------------------------------------------------------------------------------ #
##### ENV #####
ENV RIEMANN_SERVICE_NAME riemann
ENV RIEMANN_SERVICE_DIR /opt/$RIEMANN_SERVICE_NAME
ENV RIEMANN_RUN_FILE $RIEMANN_SERVICE_DIR/run.sh
ENV MANAGER_CONFIG_PATH $RIEMANN_SERVICE_DIR/manager.config
##### ENV #####
# add run scripts and configuration
ADD riemann/ $RIEMANN_SERVICE_DIR/

# install dependencies.
RUN apt-get install -y $(echo ['curl', 'openjdk-7-jdk'] | tr -d "',[]")
# download to service dir and set permissions on langohr jar.
RUN curl https://s3-eu-west-1.amazonaws.com/gigaspaces-repository-eu/langohr/2.11.0/langohr.jar --create-dirs -o $RIEMANN_SERVICE_DIR/langohr.jar && \
    chmod 644 $RIEMANN_SERVICE_DIR/langohr.jar
# download riemann deb
RUN curl http://aphyr.com/riemann/riemann_0.2.6_all.deb --create-dirs -o /opt/tmp/riemann/riemann.deb
# download riemann config
RUN curl -o $MANAGER_CONFIG_PATH https://raw.githubusercontent.com/cloudify-cosmo/cloudify-manager/master/plugins/riemann-controller/riemann_controller/resources/manager.config

# inject required env vars to run script
RUN sed -i '1s|^|RIEMANN_JAR_PATH='$RIEMANN_SERVICE_DIR'/langohr.jar \n|' $RIEMANN_RUN_FILE && \
    sed -i '1s|^|MANAGER_CONFIG_PATH='$MANAGER_CONFIG_PATH' \n|' $RIEMANN_RUN_FILE

# install riemann
RUN dpkg -i /opt/tmp/riemann/riemann.deb

# grant exec permissions
RUN chmod 0755 /opt/$RIEMANN_SERVICE_NAME/run.sh

CMD /opt/riemann/run.sh

# ------------------------------------------------------------------------------------------------------------------------------------------ #
# CONTAINER - NODEJS DependsOn: ~
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# install dependencies.
#RUN apt-get install -y $(echo [] | tr -d "',[]")
# download and install
#RUN add-apt-repository -y ppa:chris-lea/node.js && \
#	apt-get update && \
#    apt-get install -y nodejs
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# CONTAINER - LOGSTASH DependsOn: ~
# ------------------------------------------------------------------------------------------------------------------------------------------ #
##### ENV #####
ENV LOGSTASH_SERVICE_NAME logstash
ENV LOGSTASH_SERVICE_DIR /opt/$LOGSTASH_SERVICE_NAME
# logstash exec file
ENV LOGSTASH_RUN_FILE $LOGSTASH_SERVICE_DIR/run.sh
# logstash conf file
ENV LOGSTASH_CONF_FILE $LOGSTASH_SERVICE_DIR/config.conf
##### ENV #####
# add run scripts and configuration
ADD logstash/ $LOGSTASH_SERVICE_DIR/

# install dependencies.
RUN apt-get install -y $(echo ['curl', 'openjdk-7-jdk'] | tr -d "',[]")
# download jar file
RUN curl https://download.elasticsearch.org/logstash/logstash/logstash-1.3.2-flatjar.jar --create-dirs -o $LOGSTASH_SERVICE_DIR/logstash.jar

# inject required env vars to run script
RUN sed -i '1s|^|LOGSTASH_JAR_PATH='$LOGSTASH_SERVICE_DIR/logstash.jar' \n|' $LOGSTASH_RUN_FILE && \
    sed -i '1s|^|LOGSTASH_CONF_PATH='$LOGSTASH_CONF_FILE' \n|' $LOGSTASH_RUN_FILE

# grant exec permissions
RUN chmod 0755 /opt/logstash/run.sh

# start logstash
CMD /opt/logstash/run.sh

EXPOSE 9999
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# CONTAINER - ELASTICSEARCH
# ------------------------------------------------------------------------------------------------------------------------------------------ #
##### ENV #####
ENV ELASTICSEARCH_SERVICE_NAME elasticsearch
ENV ELASTICSEARCH_SERVICE_DIR /opt/$ELASTICSEARCH_SERVICE_NAME
##### ENV #####
# add run scripts and configuration
ADD elasticsearch/ $ELASTICSEARCH_SERVICE_DIR/

# install dependencies
RUN apt-get install -y $(echo ['curl', 'openjdk-7-jdk'] | tr -d "',[]")
# download binaries
RUN curl https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-1.0.1.tar.gz --create-dirs -o /opt/tmp/elasticsearch/elasticsearch.tar.gz

# create service dir todo(adaml): this command is not necessary
RUN /bin/bash -c 'source /opt/tmp/utils/bootstrap_utils.sh && \
    mkdir -p $ELASTICSEARCH_SERVICE_DIR/ && \
    check_dir "$ELASTICSEARCH_SERVICE_DIR/"'

# extract binaries to service dir
RUN tar -C $ELASTICSEARCH_SERVICE_DIR/ -xvf /opt/tmp/elasticsearch/elasticsearch.tar.gz --strip-components=1

# start elasticsearch as daemon for configuration purposes.
# todo(adaml): move config to run script
# config includes setting elasticsearch indexes.
RUN /bin/bash -c 'source /opt/tmp/utils/bootstrap_utils.sh && \
    $ELASTICSEARCH_SERVICE_DIR/bin/elasticsearch -d && \
    wait_for_port 9200' && \
    curl --retry 5 --retry-delay 3 -XDELETE http://localhost:9200/cloudify_storage && \
    curl --retry 5 --retry-delay 3 -XPUT http://localhost:9200/cloudify_storage -d '{"settings": {"analysis": {"analyzer": {"default": {"tokenizer": "whitespace"}}}}}' && \
    curl --retry 5 --retry-delay 3 -XPUT http://localhost:9200/cloudify_storage/blueprint/_mapping -d '{"blueprint": {"properties": {"plan": {"enabled": false}}}}' && \
    curl --retry 5 --retry-delay 3 -XPUT http://localhost:9200/cloudify_storage/deployment/_mapping -d '{"deployment": {"properties": {"plan": {"enabled": false}, "workflows": {"enabled": false}}}}' && \
    curl --retry 5 --retry-delay 3 -XPUT http://localhost:9200/cloudify_storage/node/_mapping -d '{ "node": { "_id": { "path": "id" }, "properties": { "types": { "type": "string", "index_name": "type" }, "properties": { "enabled": false } } } }' && \
    curl --retry 5 --retry-delay 3 -XPUT http://localhost:9200/cloudify_storage/node_instance/_mapping -d '{ "node_instance": { "_id": { "path": "id" }, "properties": { "runtime_properties": { "enabled": false } } } }' && \
    curl --retry 5 --retry-delay 3 -XGET http://localhost:9200/cloudify_storage/_mapping?pretty=1

# grant exec permissions
RUN chmod 0755 $ELASTICSEARCH_SERVICE_DIR/run.sh

# start elasticsearch as non-daemon
CMD ["ES_JAVA_OPTS=-Xmx1024m -Xms1024m; /opt/elasticsearch/run.sh"]

# expose elasticsearch port
EXPOSE 9200

# ------------------------------------------------------------------------------------------------------------------------------------------ #
# CONTAINER - INFLUXDB
# ------------------------------------------------------------------------------------------------------------------------------------------ #
##### ENV #####
ENV INFLUXDB_SERVICE_NAME influxdb
# default influxdb config path
ENV INFLUXDB_CONFIG_FILE /opt/influxdb/shared/config.toml
ENV INFLUXDB_RUN_FILE /opt/$INFLUXDB_SERVICE_NAME/run.sh
##### ENV #####
# add run scripts and configuration
ADD influxdb/ /opt/$INFLUXDB_SERVICE_NAME/

# install dependencies
RUN apt-get install -y $(echo ['curl'] | tr -d "',[]")
# download binaries
RUN curl http://s3.amazonaws.com/influxdb/influxdb_0.8.0_amd64.deb --create-dirs -o /opt/tmp/influxdb/influxdb.deb

# install influxdb
RUN dpkg -i /opt/tmp/influxdb/influxdb.deb

# start influxdb as daemon and create cloudify db
RUN /bin/bash -c 'source /opt/tmp/utils/bootstrap_utils.sh && \
    /usr/bin/influxdb-daemon -config=$INFLUXDB_CONFIG_FILE && \
    wait_for_port 8086' && \
    curl -s "http://localhost:8086/db?u=root&p=root" -d "{\"name\": \"cloudify\"}"

# set config path in run file
RUN sed -i '1s|^|INFLUXDB_CONFIG_FILE='$INFLUXDB_CONFIG_FILE' \n|' $INFLUXDB_RUN_FILE

# grant exec permissions
RUN chmod 0755 /opt/influxdb/run.sh

# run the service as non-daemon
CMD /opt/influxdb/run.sh

# expose api port
EXPOSE 8086
# expose admin port
EXPOSE 8083
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# CONTAINER - NGINX
# ------------------------------------------------------------------------------------------------------------------------------------------ #
##### ENV #####
# set nginx service name
ENV NGINX_SERVICE_NAME nginx
ENV NGINX_SERVICE_DIR /opt/$NGINX_SERVICE_NAME

# nginx default conf file path
ENV NGINX_CONF_FILE /etc/nginx/nginx.conf
ENV NGINX_RUN_FILE $NGINX_SERVICE_DIR/run.sh
ENV NGINX_LOGS_DIR $NGINX_SERVICE_DIR/logs
##### ENV #####
# add run scripts and configuration
ADD nginx/ $NGINX_SERVICE_DIR

# add nginx repositories to sources.list file and update repo
RUN echo ['deb http://nginx.org/packages/mainline/ubuntu/ precise nginx', 'deb-src http://nginx.org/packages/mainline/ubuntu/ precise nginx'] | tr -d "'["| tr ',]' '\n' >> /etc/apt/sources.list && \
    apt-get update
# install dependencies
RUN apt-get install -y $(echo ['curl'] | tr -d "',[]")

# download and add signing key
RUN curl http://nginx.org/keys/nginx_signing.key --create-dirs -o /opt/tmp/nginx/nginx_signing.key && \
    apt-key add /opt/tmp/nginx/nginx_signing.key

# install nginx
RUN apt-get install -y --force-yes $NGINX_SERVICE_NAME

# place config file in config path
# todo: do we need this config file?
RUN /bin/bash -c 'source /opt/tmp/utils/bootstrap_utils.sh && \
    mv /opt/nginx/default.conf /etc/nginx/conf.d && \
    check_file "/etc/nginx/conf.d/default.conf"'

# turn-off daemon execution and set logging dir in conf file
RUN echo "daemon off;" >> $NGINX_CONF_FILE && \
    sed -i "s%/var/log/nginx/error.log warn%$NGINX_SERVICE_DIR/logs/error.log warn%g" $NGINX_CONF_FILE && \
    sed -i "s%/var/run/nginx.pid%$NGINX_SERVICE_DIR/logs/nginx.pid%g" /etc/nginx/nginx.conf && \
    mkdir $NGINX_LOGS_DIR

# set config path in run file
RUN sed -i '1s|^|NGINX_CONF_FILE='$NGINX_CONF_FILE' \n|' $NGINX_RUN_FILE

# grant exec permissions
RUN chmod 0755 $NGINX_RUN_FILE

# run the service as non-daemon
CMD /opt/nginx/run.sh

# Expose ports.
EXPOSE 80

# ------------------------------------------------------------------------------------------------------------------------------------------ #
# CONTAINER - CELERY
# ------------------------------------------------------------------------------------------------------------------------------------------ #
##### ENV #####
ENV CELERY_SERVICE_NAME celery
ENV CELERY_SERVICE_DIR /opt/$CELERY_SERVICE_NAME
ENV CELERY_RUN_FILE $CELERY_SERVICE_DIR/run.sh
ENV CELERY_VIRTUAL_ENV_DIR $CELERY_SERVICE_DIR/env
ENV CELERY_LOG_DIR $CELERY_SERVICE_DIR/logs
##### ENV #####
# add run scripts and configuration
ADD celery/ $CELERY_SERVICE_DIR/

# install dependencies.
RUN apt-get install -y $(echo ['curl', 'python-dev', 'git', 'g++'] | tr -d "',[]")
# install pip
RUN curl --silent --show-error --retry 5 https://bootstrap.pypa.io/get-pip.py | python

# install virtualenv and create one
RUN pip install virtualenv==1.11.4 && \
    virtualenv $MANAGER_VIRTUAL_ENV_DIR

# create celery log dir
RUN mkdir $CELERY_LOG_DIR

# install requirements
RUN $CELERY_VIRTUAL_ENV_DIR/bin/pip install $(echo ['celery==3.0.24', 'pyzmq==14.3.1'] | tr -d "',[]")

############################## install cloudify core components ##############################
WORKDIR /opt/celery/

RUN $CELERY_VIRTUAL_ENV_DIR/bin/pip install git+git://github.com/cloudify-cosmo/cloudify-rest-client.git@master && \
    $CELERY_VIRTUAL_ENV_DIR/bin/pip install git+git://github.com/cloudify-cosmo/cloudify-plugins-common.git@master && \
    $CELERY_VIRTUAL_ENV_DIR/bin/pip install git+git://github.com/cloudify-cosmo/cloudify-script-plugin.git@master

RUN /bin/bash -c 'git clone -b master https://github.com/cloudify-cosmo/cloudify-manager.git && \
    pushd cloudify-manager/plugins/plugin-installer && \
    $CELERY_VIRTUAL_ENV_DIR/bin/pip install . && \
    popd && \
    pushd cloudify-manager/plugins/agent-installer && \
    $CELERY_VIRTUAL_ENV_DIR/bin/pip install . && \
    popd && \
    pushd cloudify-manager/plugins/windows-agent-installer && \
    $CELERY_VIRTUAL_ENV_DIR/bin/pip install . && \
    popd && \
    pushd cloudify-manager/plugins/riemann-controller && \
    $CELERY_VIRTUAL_ENV_DIR/bin/pip install . && \
    popd && \
    pushd cloudify-manager/workflows && \
    $CELERY_VIRTUAL_ENV_DIR/bin/pip install .'

# inject required params to run script
RUN sed -i '1s|^|CELERY_HOME_DIR='$CELERY_SERVICE_DIR' \n|' $CELERY_RUN_FILE && \
    sed -i '1s|^|CELERY_LOG_DIR='$CELERY_LOG_DIR' \n|' $CELERY_RUN_FILE

# grant exec permissions
RUN chmod 0755 $CELERY_SERVICE_DIR/run.sh

# run the service as non-daemon
CMD /opt/celery/run.sh

# ------------------------------------------------------------------------------------------------------------------------------------------ #
# CONTAINER - MANAGER
# ------------------------------------------------------------------------------------------------------------------------------------------ #
##### ENV #####
ENV MANAGER_SERVICE_NAME manager
ENV MANAGER_SERVICES_DIR /opt/$MANAGER_SERVICE_NAME
ENV MANAGER_VIRTUAL_ENV_DIR $MANAGER_SERVICES_DIR/env
ENV SERVER_FILES_DIR $MANAGER_SERVICES_DIR/cloudify-manager/rest-service/manager_rest

ENV AMQPFLUX_RUN_FILE $MANAGER_SERVICES_DIR/run_amqpflux.sh
ENV MANAGER_RUN_FILE $MANAGER_SERVICES_DIR/run_manager.sh

ENV MANAGER_REST_CONFIG_PATH $MANAGER_SERVICES_DIR/guni.conf
##### ENV #####
# add run scripts and configuration
ADD manager/ $MANAGER_SERVICES_DIR/

#install dependencies
RUN apt-get install -y $(echo ['git'] | tr -d "',[]")

# inject required params to run script
RUN sed -i '1s|^|MANAGER_VIRTUALENV_DIR='$MANAGER_VIRTUAL_ENV_DIR' \n|' $AMQPFLUX_RUN_FILE && \
    sed -i '1s|^|MANAGER_VIRTUALENV_DIR='$MANAGER_VIRTUAL_ENV_DIR' \n|' $MANAGER_RUN_FILE && \
    sed -i '1s|^|MANAGER_REST_CONFIG_PATH='$MANAGER_REST_CONFIG_PATH' \n|' $MANAGER_RUN_FILE && \
    sed -i '1s|^|SERVER_FILES_DIR='$SERVER_FILES_DIR' \n|' $MANAGER_RUN_FILE

# install pip
RUN curl --silent --show-error --retry 5 https://bootstrap.pypa.io/get-pip.py | python
# install virtualenv and create one
RUN pip install virtualenv==1.11.4 && \
    virtualenv $MANAGER_VIRTUAL_ENV_DIR

WORKDIR /opt/manager/

# install amqpinflux
RUN $MANAGER_VIRTUAL_ENV_DIR/bin/pip install git+git://github.com/cloudify-cosmo/cloudify-amqp-influxdb.git@master && \
    $MANAGER_VIRTUAL_ENV_DIR/bin/pip install git+git://github.com/cloudify-cosmo/cloudify-dsl-parser.git@master
# install rest-service
RUN /bin/bash -c 'git clone -b master https://github.com/cloudify-cosmo/cloudify-manager.git && \
    pushd cloudify-manager/rest-service && \
    $MANAGER_VIRTUAL_ENV_DIR/bin/pip install .'

# grant exec permissions for amqpflux and for rest-service
RUN chmod 0755 $AMQPFLUX_RUN_FILE && \
    chmod 0755 $MANAGER_RUN_FILE