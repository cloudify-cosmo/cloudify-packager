FROM docker_javabase:latest
MAINTAINER Gigaspaces, cosmo-admin@gigaspaces.com

COPY ELASTICSEARCH_NOTICE.txt /root/ELASTICSEARCH_NOTICE.txt
COPY scripts/* /opt/scripts/

# Used by 'cfy status' impl to determine if running in container.
ENV ELASTICSEARCH_VERSION=1.4.3 \
    DOCKER_ENV=True \
    ELASTICSEARCH_SERVICE_DIR=/opt/elasticsearch \
    ES_JAVA_OPTS="-Xmx1024m -Xms1024m"

RUN apt-get update && \
    apt-get install -y curl && \
    curl --fail https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-${ELASTICSEARCH_VERSION}.tar.gz -o /tmp/elasticsearch.tar.gz && \
    mkdir -p ${ELASTICSEARCH_SERVICE_DIR} && \
    tar -C ${ELASTICSEARCH_SERVICE_DIR}/ -xvf /tmp/elasticsearch.tar.gz --strip-components=1 && \
    # start elasticsearch as daemon for configuration purposes.
    ${ELASTICSEARCH_SERVICE_DIR}/bin/elasticsearch -d && \
    chmod +x /opt/scripts/wait_for_port && sleep 3 && /opt/scripts/wait_for_port 9200 && \
    chmod +x /opt/scripts/configure_es && sleep 3 && /opt/scripts/configure_es && \
    rm -rf /var/lib/apt/lists && \
    rm -rf /tmp/* && \
    apt-get purge curl -y && \
    apt-get autoremove -y


VOLUME ${ELASTICSEARCH_SERVICE_DIR}/data
VOLUME ${ELASTICSEARCH_SERVICE_DIR}/logs

EXPOSE 9200

CMD ${ELASTICSEARCH_SERVICE_DIR}/bin/elasticsearch