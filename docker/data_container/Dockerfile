FROM phusion/baseimage:0.9.15
MAINTAINER adaml, adaml@gigaspaces.com

ADD utils/ /opt/tmp/utils/

RUN apt-get update
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
    curl https://aphyr.com/riemann/riemann_0.2.6_all.deb --create-dirs -o /opt/tmp/riemann/riemann.deb && \
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
# INSTALL - ELASTICSEARCH
# ------------------------------------------------------------------------------------------------------------------------------------------ #
##### ENV #####
ENV ELASTICSEARCH_SERVICE_NAME elasticsearch
ENV ELASTICSEARCH_SERVICE_DIR /etc/service/$ELASTICSEARCH_SERVICE_NAME
##### ENV #####

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
    curl --retry 5 --retry-delay 3 -XGET http://localhost:9200/cloudify_storage/_mapping?pretty=1

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
    curl -s "http://localhost:8086/db?u=root&p=root" -d "{\"name\": \"cloudify\"}"

#influxdb persistence path
VOLUME /opt/influxdb/shared/data
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# Rest-Service persistence path
# ------------------------------------------------------------------------------------------------------------------------------------------ #
RUN echo creating logs folder && \
    mkdir -p /var/log/cloudify

VOLUME /var/log/cloudify
