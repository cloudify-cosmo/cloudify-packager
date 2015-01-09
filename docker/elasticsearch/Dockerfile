FROM debian:jessie
MAINTAINER Gigaspaces, cosmo-admin@gigaspaces.com
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# INSTALL - BASE
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# add utility functions
COPY utils.sh /opt/tmp/utils/utils.sh
COPY NOTICE.txt /root/NOTICE.txt
# Used by 'cfy status' impl to determine if running in container.
ENV DOCKER_ENV True

# ------------------------------------------------------------------------------------------------------------------------------------------ #
# INSTALL - ELASTICSEARCH
# ------------------------------------------------------------------------------------------------------------------------------------------ #
##### ENV #####
ENV ELASTICSEARCH_SERVICE_NAME=elasticsearch
ENV ELASTICSEARCH_SERVICE_DIR=/etc/service/$ELASTICSEARCH_SERVICE_NAME \
    ES_JAVA_OPTS="-Xmx1024m -Xms1024m" \
    JAVA_HOME=/etc/java/

# add run scripts and configuration
COPY elasticsearch/ $ELASTICSEARCH_SERVICE_DIR/


RUN apt-get update && \
    # installing elasticsearch dependencies
    apt-get install -y curl && \
    curl https://dl.dropboxusercontent.com/u/407576/jre-7-linux-x64.tar.gz --create-dirs -o /opt/tmp/java/java.tar.gz && \
    mkdir /etc/java && \
    tar -xzvf /opt/tmp/java/java.tar.gz -C /etc/java --strip=1 && \
    rm /opt/tmp/java/java.tar.gz && \
    # download elasticsearch binaries
    curl https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-1.0.1.tar.gz --create-dirs -o /opt/tmp/elasticsearch/elasticsearch.tar.gz && \
    # extracting binaries to service dir
    mkdir -p $ELASTICSEARCH_SERVICE_DIR && \
    tar -C $ELASTICSEARCH_SERVICE_DIR/ -xvf /opt/tmp/elasticsearch/elasticsearch.tar.gz --strip-components=1 && \
    rm -rf /opt/tmp/elasticsearch/elasticsearch.tar.gz && \
    # start elasticsearch as daemon for configuration purposes.
    # todo(adaml): move config to run script
    # config includes setting elasticsearch indexes.
    /bin/bash -c 'source /opt/tmp/utils/utils.sh && \
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
    curl --retry 5 --retry-delay 3 -XPUT http://localhost:9200/cloudify_storage/node/_mapping -d '{ "node": { "_id": { "path": "id" }, "properties": { "types": { "type": "string", "index_name": "type" }, "properties": { "enabled": false }, "operations": { "enabled": false } } } }' && \
    echo "creating node-instance mapping..." && \
    curl --retry 5 --retry-delay 3 -XPUT http://localhost:9200/cloudify_storage/node_instance/_mapping -d '{ "node_instance": { "_id": { "path": "id" }, "properties": { "runtime_properties": { "enabled": false } } } }' && \
    echo "printing mappings..." && \
    curl --retry 5 --retry-delay 3 -XGET http://localhost:9200/cloudify_storage/_mapping?pretty=1 && \
    # cleanup
    rm -rf /var/lib/apt/lists
    # remove curl
    apt-get remove curl -y && \
    apt-get autoremove -y

# elasticsearch persistence paths
# VOLUME /etc/service/elasticsearch/data
# VOLUME /etc/service/elasticsearch/logs

EXPOSE 9200

CMD /etc/service/elasticsearch/bin/elasticsearch