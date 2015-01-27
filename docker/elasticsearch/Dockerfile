FROM thinkops/light-jre:latest
MAINTAINER Gigaspaces, cosmo-admin@gigaspaces.com

COPY NOTICE.txt /root/NOTICE.txt
COPY scripts/* /opt/scripts/

# Used by 'cfy status' impl to determine if running in container.
ENV VERSION=1.4.2 \
    DOCKER_ENV=True \
    ELASTICSEARCH_SERVICE_DIR=/etc/service/elasticsearch \
    ES_JAVA_OPTS="-Xmx1024m -Xms1024m"

RUN apt-get update && \
    apt-get install -y curl && \
    curl https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-${VERSION}.tar.gz --create-dirs -o /opt/tmp/elasticsearch.tar.gz && \
    mkdir -p ${ELASTICSEARCH_SERVICE_DIR} && \
    tar -C ${ELASTICSEARCH_SERVICE_DIR}/ -xvf /opt/tmp/elasticsearch.tar.gz --strip-components=1 && \
    # start elasticsearch as daemon for configuration purposes.
    ${ELASTICSEARCH_SERVICE_DIR}/bin/elasticsearch -d && \
    chmod +x /opt/scripts/wait_for_port && sleep 3 && /opt/scripts/wait_for_port 9200 && \
    chmod +x /opt/scripts/configure_es && sleep 3 && /opt/scripts/configure_es && \
    rm -rf /var/lib/apt/lists; rm /opt/tmp/*; apt-get remove curl -y; apt-get autoremove -y


VOLUME ${ELASTICSEARCH_SERVICE_DIR}/data
VOLUME ${ELASTICSEARCH_SERVICE_DIR}/logs

EXPOSE 9200

CMD ${ELASTICSEARCH_SERVICE_DIR}/bin/elasticsearch