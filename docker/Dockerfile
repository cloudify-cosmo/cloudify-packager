FROM phusion/baseimage:0.9.15
MAINTAINER adaml, adaml@gigaspaces.com
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# INSTALL - BASE
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# add utility functions
ADD utils/ /opt/tmp/utils/
# Used by 'cfy status' impl to determine if running in container.
ENV DOCKER_ENV True

RUN apt-get update
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# INSTALL - RABBITMQ, DependsOn: ~
# ------------------------------------------------------------------------------------------------------------------------------------------ #
##### ENV #####
ENV RABBITMQ_SERVICE_NAME rabbitmq-server
ENV RABBITMQ_SERVICE_DIR /etc/service/$RABBITMQ_SERVICE_NAME
ENV RABBITMQ_RUN_FILE $RABBITMQ_SERVICE_DIR/run
##### ENV #####
# add run scripts and configuration
ADD rabbitmq/ $RABBITMQ_SERVICE_DIR/

RUN echo installing rabbitmq dependencies && \
    apt-get install -y  curl logrotate erlang-nox && \
    \
    echo installing rabbitmq-server and setting its properties && \
    apt-get -y install rabbitmq-server && \
    rabbitmq-plugins enable rabbitmq_management && \
    rabbitmq-plugins enable rabbitmq_tracing && \
    \
    echo granting exec permissions && \
    chmod +x $RABBITMQ_RUN_FILE

# ------------------------------------------------------------------------------------------------------------------------------------------ #
# INSTALL - RIEMANN
# ------------------------------------------------------------------------------------------------------------------------------------------ #
##### ENV #####
ENV RIEMANN_SERVICE_NAME riemann
ENV RIEMANN_SERVICE_DIR /etc/service/$RIEMANN_SERVICE_NAME
ENV RIEMANN_RUN_FILE $RIEMANN_SERVICE_DIR/run
ENV MANAGER_CONFIG_PATH $RIEMANN_SERVICE_DIR/manager.config
##### ENV #####
# add run scripts and configuration
ADD riemann/ $RIEMANN_SERVICE_DIR/

RUN echo installing riemann dependencies && \
    apt-get install -y  curl openjdk-7-jdk && \
    \
    echo downloading jar to service dir and setting permissions on langohr jar && \
    curl https://s3-eu-west-1.amazonaws.com/gigaspaces-repository-eu/langohr/2.11.0/langohr.jar --create-dirs -o $RIEMANN_SERVICE_DIR/langohr.jar && \
    chmod 644 $RIEMANN_SERVICE_DIR/langohr.jar && \
    \
    echo downloading and installing riemann deb && \
    curl http://aphyr.com/riemann/riemann_0.2.6_all.deb --create-dirs -o /opt/tmp/riemann/riemann.deb && \
    dpkg -i /opt/tmp/riemann/riemann.deb && \
    rm -rf /opt/tmp/riemann/riemann.deb && \
    \
    echo download riemann config && \
    curl -o $MANAGER_CONFIG_PATH https://raw.githubusercontent.com/cloudify-cosmo/cloudify-manager/3.1/plugins/riemann-controller/riemann_controller/resources/manager.config

# inject required env vars to run script
RUN sed -i '1s|^|RIEMANN_JAR_PATH='$RIEMANN_SERVICE_DIR'/langohr.jar \n|' $RIEMANN_RUN_FILE && \
    sed -i '1s|^|MANAGER_CONFIG_PATH='$MANAGER_CONFIG_PATH' \n|' $RIEMANN_RUN_FILE && \
    sed -i '1s|^|#!/bin/bash \n|' $RIEMANN_RUN_FILE && \
    chmod +x $RIEMANN_RUN_FILE

# riemann persistence path
VOLUME /etc/service/riemann
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# INSTALL - LOGSTASH
# ------------------------------------------------------------------------------------------------------------------------------------------ #
##### ENV #####
ENV LOGSTASH_SERVICE_NAME logstash
ENV LOGSTASH_SERVICE_DIR /etc/service/$LOGSTASH_SERVICE_NAME
# logstash exec file
ENV LOGSTASH_RUN_FILE $LOGSTASH_SERVICE_DIR/run
# logstash conf file
ENV LOGSTASH_CONF_FILE $LOGSTASH_SERVICE_DIR/config.conf
##### ENV #####
# add run scripts and configuration
ADD logstash/ $LOGSTASH_SERVICE_DIR/

RUN echo installing logstash dependencies && \
    apt-get install -y  curl openjdk-7-jdk && \
    \
    echo download jar file && \
    curl https://download.elasticsearch.org/logstash/logstash/logstash-1.3.2-flatjar.jar --create-dirs -o $LOGSTASH_SERVICE_DIR/logstash.jar

# inject required env vars to run script
RUN sed -i '1s|^|LOGSTASH_JAR_PATH='$LOGSTASH_SERVICE_DIR/logstash.jar' \n|' $LOGSTASH_RUN_FILE && \
    sed -i '1s|^|LOGSTASH_CONF_PATH='$LOGSTASH_CONF_FILE' \n|' $LOGSTASH_RUN_FILE && \
    sed -i '1s|^|#!/bin/bash \n|' $LOGSTASH_RUN_FILE && \
    chmod +x $LOGSTASH_RUN_FILE

# ------------------------------------------------------------------------------------------------------------------------------------------ #
# INSTALL - ELASTICSEARCH
# ------------------------------------------------------------------------------------------------------------------------------------------ #
##### ENV #####
ENV ELASTICSEARCH_SERVICE_NAME elasticsearch
ENV ELASTICSEARCH_SERVICE_DIR /etc/service/$ELASTICSEARCH_SERVICE_NAME
##### ENV #####
# add run scripts and configuration
ADD elasticsearch/ $ELASTICSEARCH_SERVICE_DIR/


RUN echo  installing elasticsearch dependencies && \
    apt-get install -y  curl openjdk-7-jdk && \
    \
    echo download elasticsearch binaries && \
    curl https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-1.0.1.tar.gz --create-dirs -o /opt/tmp/elasticsearch/elasticsearch.tar.gz && \
    \
    echo extracting binaries to service dir && \
    mkdir -p $ELASTICSEARCH_SERVICE_DIR && \
    tar -C $ELASTICSEARCH_SERVICE_DIR/ -xvf /opt/tmp/elasticsearch/elasticsearch.tar.gz --strip-components=1 && \
    rm -rf /opt/tmp/elasticsearch/elasticsearch.tar.gz

# start elasticsearch as daemon for configuration purposes.
# todo(adaml): move config to run script
# config includes setting elasticsearch indexes.
RUN /bin/bash -c 'source /opt/tmp/utils/bootstrap_utils.sh && \
    $ELASTICSEARCH_SERVICE_DIR/bin/elasticsearch -d && \
    wait_for_port 9200' && \
    echo "deleting events index if exists..." && \
    curl --retry 5 --retry-delay 3 -XDELETE http://localhost:9200/cloudify_events/ && \
    echo "creating events index..." && \
    curl --retry 5 --retry-delay 3 -XPUT http://localhost:9200/cloudify_events -d '{"settings": {"analysis": {"analyzer": {"default": {"tokenizer": "whitespace"}}}}}' && \
    echo "deleting index if exists..." && \
    curl --retry 5 --retry-delay 3 -XDELETE http://localhost:9200/cloudify_storage && \
    echo "creating index..." && \
    curl --retry 5 --retry-delay 3 -XPUT http://localhost:9200/cloudify_storage -d '{"settings": {"analysis": {"analyzer": {"default": {"tokenizer": "whitespace"}}}}}' && \
    echo "creating blueprint mapping..." && \
    curl --retry 5 --retry-delay 3 -XPUT http://localhost:9200/cloudify_storage/blueprint/_mapping -d '{"blueprint": {"properties": {"plan": {"enabled": false}}}}' && \
    echo "creating deployment mapping..." && \
    curl --retry 5 --retry-delay 3 -XPUT http://localhost:9200/cloudify_storage/deployment/_mapping -d '{"deployment": {"properties": {"workflows": {"enabled": false}, "inputs": {"enabled": false}, "policy_type": {"enabled": false}, "policy_triggers": {"enabled": false}, "groups": {"enabled": false}, "outputs": {"enabled": false}}}}' && \
    echo "creating node mapping..." && \
    curl --retry 5 --retry-delay 3 -XPUT http://localhost:9200/cloudify_storage/node/_mapping -d '{ "node": { "_id": { "path": "id" }, "properties": { "types": { "type": "string", "index_name": "type" }, "properties": { "enabled": false } } } }' && \
    echo "creating node-instance mapping..." && \
    curl --retry 5 --retry-delay 3 -XPUT http://localhost:9200/cloudify_storage/node_instance/_mapping -d '{ "node_instance": { "_id": { "path": "id" }, "properties": { "runtime_properties": { "enabled": false } } } }' && \
    echo "printing mappings..." && \
    curl --retry 5 --retry-delay 3 -XGET http://localhost:9200/cloudify_storage/_mapping?pretty=1 && \
    \
    echo granting run permissions to run file && \
    chmod +x $ELASTICSEARCH_SERVICE_DIR/run

#elasticsearch persistence paths
VOLUME /etc/service/elasticsearch/data
VOLUME /etc/service/elasticsearch/logs
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# INSTALL - INFLUXDB
# ------------------------------------------------------------------------------------------------------------------------------------------ #
##### ENV #####
ENV INFLUXDB_SERVICE_NAME influxdb
# default influxdb config path
ENV INFLUXDB_CONFIG_FILE /opt/influxdb/shared/config.toml
ENV INFLUXDB_RUN_FILE /etc/service/$INFLUXDB_SERVICE_NAME/run
##### ENV #####
# add run scripts and configuration
ADD influxdb/ /etc/service/$INFLUXDB_SERVICE_NAME/

RUN echo installing influxdb dependencies && \
    apt-get install -y  curl && \
    \
    echo downloading influxdb binaries && \
    curl http://s3.amazonaws.com/influxdb/influxdb_0.8.0_amd64.deb --create-dirs -o /opt/tmp/influxdb/influxdb.deb && \
    \
    echo installing influxdb && \
    dpkg -i /opt/tmp/influxdb/influxdb.deb && \
    rm -rf /opt/tmp/influxdb/influxdb.deb

RUN echo starting influxdb as daemon to create cloudify db && \
    /bin/bash -c 'source /opt/tmp/utils/bootstrap_utils.sh && \
    /usr/bin/influxdb-daemon -config=$INFLUXDB_CONFIG_FILE && \
    wait_for_port 8086' && \
    curl -s "http://localhost:8086/db?u=root&p=root" -d "{\"name\": \"cloudify\"}" && \
    rm -rf /opt/influxdb/shared/data/raft

# set config path in run file
RUN sed -i '1s|^|INFLUXDB_CONFIG_FILE='$INFLUXDB_CONFIG_FILE' \n|' $INFLUXDB_RUN_FILE && \
    sed -i '1s|^|#!/bin/bash \n|' $INFLUXDB_RUN_FILE && \
    chmod +x $INFLUXDB_RUN_FILE

#influxdb persistence path
VOLUME /opt/influxdb/shared/data
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# INSTALL - NGINX
# ------------------------------------------------------------------------------------------------------------------------------------------ #
##### ENV #####
# set nginx service name
ENV NGINX_SERVICE_NAME nginx
ENV NGINX_SERVICE_DIR /etc/service/$NGINX_SERVICE_NAME
# nginx default conf file path
ENV NGINX_CONF_FILE /etc/nginx/nginx.conf
ENV NGINX_RUN_FILE $NGINX_SERVICE_DIR/run
ENV NGINX_LOGS_DIR $NGINX_SERVICE_DIR/logs
##### ENV #####
# add run scripts and configuration
ADD nginx/ $NGINX_SERVICE_DIR

RUN echo adding nginx repositories to sources.list file and update repo && \
    echo ['deb http://nginx.org/packages/mainline/ubuntu/ precise nginx', 'deb-src http://nginx.org/packages/mainline/ubuntu/ precise nginx'] | tr -d "'["| tr ',]' '\n' >> /etc/apt/sources.list && \
    apt-get update && \
    \
    echo installing nginx dependencies && \
    apt-get install -y  curl && \
    \
    echo download and add signing key && \
    curl http://nginx.org/keys/nginx_signing.key --create-dirs -o /opt/tmp/nginx/nginx_signing.key && \
    apt-key add /opt/tmp/nginx/nginx_signing.key && \
    \
    echo installing nginx && \
    apt-get install -y --force-yes $NGINX_SERVICE_NAME

# turn-off daemon execution, set logging dir and default.conf location in conf file
RUN echo "daemon off;" >> $NGINX_CONF_FILE && \
    sed -i "s%/var/log/nginx/error.log warn%$NGINX_SERVICE_DIR/logs/error.log warn%g" $NGINX_CONF_FILE && \
    sed -i "s%/var/run/nginx.pid%$NGINX_SERVICE_DIR/logs/nginx.pid%g" $NGINX_CONF_FILE && \
    sed -i "s%/etc/nginx/conf.d/\*.conf%$NGINX_SERVICE_DIR/default.conf%g" $NGINX_CONF_FILE && \
    mkdir -p $NGINX_LOGS_DIR && \
    \
    echo setting config path in run file && \
    sed -i '1s|^|NGINX_CONF_FILE='$NGINX_CONF_FILE' \n|' $NGINX_RUN_FILE && \
    sed -i '1s|^|#!/bin/bash \n|' $NGINX_RUN_FILE && \
    chmod +x $NGINX_RUN_FILE

# ------------------------------------------------------------------------------------------------------------------------------------------ #
# INSTALL - CELERY
# ------------------------------------------------------------------------------------------------------------------------------------------ #
##### ENV #####
ENV CELERY_SERVICE_NAME celeryd-cloudify-management
ENV CELERY_SERVICE_DIR /etc/service/$CELERY_SERVICE_NAME
ENV CELERY_RUN_FILE $CELERY_SERVICE_DIR/run
ENV CELERY_VIRTUAL_ENV_DIR $CELERY_SERVICE_DIR/env
ENV CELERY_LOG_DIR $CELERY_SERVICE_DIR/logs
##### ENV #####
# add run scripts and configuration
ADD celery/ $CELERY_SERVICE_DIR/

RUN echo installing celery dependencies && \
    apt-get install -y  curl python-dev git g++ wget sudo && \
    \
    echo installing pip && \
    curl --silent --show-error --retry 5 https://bootstrap.pypa.io/get-pip.py | python && \
    \
    echo installing virtualenv and creating one && \
    pip install virtualenv && \
    virtualenv $CELERY_VIRTUAL_ENV_DIR && \
    \
    echo installing celery python requirements in virtualenv && \
    $CELERY_VIRTUAL_ENV_DIR/bin/pip install $(echo ['celery==3.0.24', 'pyzmq==14.3.1'] | tr -d "',[]")

############################## install cloudify core components ##############################
WORKDIR /etc/service/celeryd-cloudify-management/

RUN $CELERY_VIRTUAL_ENV_DIR/bin/pip install git+git://github.com/cloudify-cosmo/cloudify-rest-client.git@3.1 && \
    $CELERY_VIRTUAL_ENV_DIR/bin/pip install git+git://github.com/cloudify-cosmo/cloudify-plugins-common.git@3.1 && \
    $CELERY_VIRTUAL_ENV_DIR/bin/pip install git+git://github.com/cloudify-cosmo/cloudify-script-plugin.git@3.1 && \
    /bin/bash -c 'git clone -b 3.1 https://github.com/cloudify-cosmo/cloudify-manager.git && \
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

# inject required params to run script and create logs dir
RUN sed -i '1s|^|CELERY_HOME_DIR='$CELERY_SERVICE_DIR' \n|' $CELERY_RUN_FILE && \
    sed -i '1s|^|CELERY_LOG_DIR='$CELERY_LOG_DIR' \n|' $CELERY_RUN_FILE && \
    sed -i '1s|^|#!/bin/bash \n|' $CELERY_RUN_FILE && \
    mkdir -p $CELERY_LOG_DIR && \
    chmod +x $CELERY_RUN_FILE

# ------------------------------------------------------------------------------------------------------------------------------------------ #
# INSTALL - MANAGER
# ------------------------------------------------------------------------------------------------------------------------------------------ #
##### ENV #####
ENV MANAGER_SERVICE_NAME manager
ENV MANAGER_SERVICES_DIR /opt/$MANAGER_SERVICE_NAME
ENV MANAGER_VIRTUAL_ENV_DIR $MANAGER_SERVICES_DIR/env
ENV SERVER_FILES_DIR $MANAGER_SERVICES_DIR/cloudify-manager*/rest-service/manager_rest

ENV AMQPFLUX_RUN_FILE /etc/service/amqp-influx/run
ENV REST_RUN_FILE /etc/service/rest-service/run

ENV REST_CONFIG_PATH /etc/service/rest-service/guni.conf
##### ENV #####
# add run scripts and configuration
ADD manager/ $MANAGER_SERVICES_DIR/
ADD amqp_influx/ /etc/service/amqp-influx/
ADD rest_service/ /etc/service/rest-service/

WORKDIR /opt/manager/

RUN echo install dependencies && \
    apt-get install -y  git python2.7 && \
    \
    echo installing pip && \
    curl --silent --show-error --retry 5 https://bootstrap.pypa.io/get-pip.py | python && \
    \
    echo install virtualenv and create one && \
    pip install virtualenv && \
    virtualenv $MANAGER_VIRTUAL_ENV_DIR && \
    \
    echo installing amqpinflux && \
    $MANAGER_VIRTUAL_ENV_DIR/bin/pip install git+git://github.com/cloudify-cosmo/cloudify-amqp-influxdb.git@3.1 && \
    $MANAGER_VIRTUAL_ENV_DIR/bin/pip install git+git://github.com/cloudify-cosmo/cloudify-dsl-parser.git@3.1 && \
    \
    echo installing rest-service && \
    /bin/bash -c 'git clone -b 3.1 https://github.com/cloudify-cosmo/cloudify-manager.git && \
    pushd cloudify-manager/rest-service && \
    $MANAGER_VIRTUAL_ENV_DIR/bin/pip install .' && \
    \
    echo injecting required params to run script && \
    sed -i '1s|^|MANAGER_VIRTUALENV_DIR='$MANAGER_VIRTUAL_ENV_DIR' \n|' $AMQPFLUX_RUN_FILE && \
    sed -i '1s|^|MANAGER_VIRTUALENV_DIR='$MANAGER_VIRTUAL_ENV_DIR' \n|' $REST_RUN_FILE && \
    sed -i '1s|^|MANAGER_REST_CONFIG_PATH='$REST_CONFIG_PATH' \n|' $REST_RUN_FILE && \
    sed -i '1s|^|SERVER_FILES_DIR='$SERVER_FILES_DIR' \n|' $REST_RUN_FILE && \
    sed -i '1s|^|#!/bin/bash \n|' $REST_RUN_FILE && \
    sed -i '1s|^|#!/bin/bash \n|' $AMQPFLUX_RUN_FILE && \
    \
    echo creating logs folder && \
    mkdir -p /var/log/cloudify && \
    \
    echo granting run permissions to run file && \
    chmod +x $AMQPFLUX_RUN_FILE && \
    chmod +x $REST_RUN_FILE

# create resources folder and copy all required resources
RUN curl http://gigaspaces-repository-eu.s3.amazonaws.com/org/cloudify3/3.1.0/ga-RELEASE/cloudify-ubuntu-precise-agent_3.1.0-ga-b85_amd64.deb --create-dirs -o /opt/tmp/manager/ubuntu_agent.deb && \
    dpkg-deb -x /opt/tmp/manager/ubuntu_agent.deb /opt/tmp/manager && \
    mkdir -p /opt/manager/resources/packages/scripts && mv /opt/tmp/manager/agents/Ubuntu*/config/Ubuntu-agent-disable-requiretty.sh /opt/manager/resources/packages/scripts && \
    mkdir -p /opt/manager/resources/packages/templates && mv /opt/tmp/manager/agents/Ubuntu*/config/Ubuntu-celeryd-cloudify.conf.template /opt/manager/resources/packages/templates && \
    mkdir -p /opt/manager/resources/packages/templates && mv /opt/tmp/manager/agents/Ubuntu*/config/Ubuntu-celeryd-cloudify.init.template /opt/manager/resources/packages/templates && \
    mkdir -p /opt/manager/resources/packages/agents && mv /opt/tmp/manager/agents/Ubuntu*/Ubuntu-precise-agent.tar.gz /opt/manager/resources/packages/agents/Ubuntu-precise-agent.tar.gz && \
    rm -rf /opt/tmp/manager/ubuntu_agent.deb && \
    echo compiling ubuntu 14.04 trusty agent && \
    /bin/bash -c 'virtualenv temp_env && source temp_env/bin/activate && \
    pip install https://github.com/cloudify-cosmo/cloudify-agent-packager/archive/master.tar.gz && \
    cfy-ap -f -c my_config.yaml -v' && \
    curl http://gigaspaces-repository-eu.s3.amazonaws.com/org/cloudify3/3.1.0/ga-RELEASE/cloudify-centos-final-agent_3.1.0-ga-b85_amd64.deb --create-dirs -o /opt/tmp/manager/centos_agent.deb && \
    dpkg-deb -x /opt/tmp/manager/centos_agent.deb /opt/tmp/manager && \
    mkdir -p /opt/manager/resources/packages/scripts && mv /opt/tmp/manager/agents/centos*/config/centos-agent-disable-requiretty.sh /opt/manager/resources/packages/scripts && \
    mkdir -p /opt/manager/resources/packages/templates && mv /opt/tmp/manager/agents/centos*/config/centos-celeryd-cloudify.conf.template /opt/manager/resources/packages/templates && \
    mkdir -p /opt/manager/resources/packages/templates && mv /opt/tmp/manager/agents/centos*/config/centos-celeryd-cloudify.init.template /opt/manager/resources/packages/templates && \
    mkdir -p /opt/manager/resources/packages/agents && mv /opt/tmp/manager/agents/centos*/centos-Final-agent.tar.gz /opt/manager/resources/packages/agents && \
    rm -rf /opt/tmp/manager/centos_agent.deb && \
    curl http://gigaspaces-repository-eu.s3.amazonaws.com/org/cloudify3/3.1.0/ga-RELEASE/cloudify-windows-agent_3.1.0-ga-b85_amd64.deb --create-dirs -o /opt/tmp/manager/windows_agent.deb && \
    dpkg-deb -x /opt/tmp/manager/windows_agent.deb /opt/tmp/manager && \
    mkdir -p /opt/manager/resources/packages/agents && mv /opt/tmp/manager/agents/windows*/Cloudify.exe /opt/manager/resources/packages/agents/CloudifyWindowsAgent.exe && \
    cp -r /opt/manager/cloudify-manager/resources/rest-service/* /opt/manager/resources && \
    rm -rf /opt/tmp/manager/windows_agent.deb

# ------------------------------------------------------------------------------------------------------------------------------------------ #
# INSTALL - WEB-UI
# ------------------------------------------------------------------------------------------------------------------------------------------ #
##### ENV #####
ENV WEBUI_SERVICE_NAME cloudify-ui
ENV WEBUI_SERVICE_DIR /etc/service/$WEBUI_SERVICE_NAME
ENV WEBUI_RUN_FILE $WEBUI_SERVICE_DIR/run
ENV WEBUI_VIRTUAL_ENV_DIR $WEBUI_SERVICE_DIR/env
##### ENV #####
ADD cloudify-ui/ $WEBUI_SERVICE_DIR/

RUN echo installing web-ui dependencies && \
    apt-get install -y  curl g++ python2.7 make && \
    \
    echo installing nodejs from source && \
    cd /tmp && \
    curl http://nodejs.org/dist/node-latest.tar.gz -o /tmp/node-latest.tar.gz && \
    tar xvzf node-latest.tar.gz && \
    rm -f node-latest.tar.gz && \
    cd node-v* && \
    ./configure && \
    CXX="g++ -Wno-unused-local-typedefs" make && \
    CXX="g++ -Wno-unused-local-typedefs" make install && \
    cd /tmp && \
    rm -rf /tmp/node-v* && \
    echo '\n# Node.js\nexport PATH="node_modules/.bin:$PATH"' >> /root/.bashrc && \
    \
    echo downloading cloudify-webui package and extracting webui and grafana tar.gz && \
    curl http://gigaspaces-repository-eu.s3.amazonaws.com/org/cloudify3/3.1.1/ga-RELEASE/cloudify-ui_3.1.1-ga-b87_amd64.deb --create-dirs -o /opt/tmp/cloudify-webui/cloudify-webui.deb && \
    dpkg-deb -x /opt/tmp/cloudify-webui/cloudify-webui.deb /opt/tmp/cloudify-webui/ && \
    mkdir -p $WEBUI_SERVICE_DIR/cosmo-ui && \
    tar -xvf /opt/tmp/cloudify-webui/packages/cloudify-ui/cosmo-ui* -C $WEBUI_SERVICE_DIR/cosmo-ui --strip-components=1 && \
    mkdir -p $WEBUI_SERVICE_DIR/grafana && \
    tar -xvf /opt/tmp/cloudify-webui/packages/cloudify-ui/grafana* -C $WEBUI_SERVICE_DIR/grafana --strip-components=1 && \
    cp /opt/tmp/cloudify-webui/packages/cloudify-ui/config/grafana/config.js $WEBUI_SERVICE_DIR/grafana/ && \
    rm -rf /opt/tmp/cloudify-webui/cloudify-webui.deb && \
    chmod +x $WEBUI_RUN_FILE
#RUN apt-get -y install nodejs npm