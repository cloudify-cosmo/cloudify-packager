FROM debian:jessie
MAINTAINER Gigaspaces, cosmo-admin@gigaspaces.com

# COPY NOTICE.txt /root/NOTICE.txt

# Used by 'cfy status' impl to determine if running in container.
ENV VERSION=4.0.0-beta3 \
    DOCKER_ENV=True \
    KIBANA_SERVICE_DIR=/etc/service/kibana \
    JAVA_HOME=/etc/java/

RUN apt-get update && \
    apt-get install -y curl && \
    curl https://dl.dropboxusercontent.com/u/407576/jre-7-linux-x64.tar.gz --create-dirs -o /opt/tmp/java.tar.gz && \
    mkdir ${JAVA_HOME} && tar -xzvf /opt/tmp/java.tar.gz -C ${JAVA_HOME} --strip=1 && \
    curl https://download.elasticsearch.org/kibana/kibana/kibana-${VERSION}.tar.gz --create-dirs -o /opt/tmp/kibana.tar.gz && \
    mkdir -p ${KIBANA_SERVICE_DIR} && \
    tar -C ${KIBANA_SERVICE_DIR}/ -xvf /opt/tmp/kibana.tar.gz --strip-components=1 && \
    rm -rf /var/lib/apt/lists; rm /opt/tmp/*; apt-get remove curl -y; apt-get autoremove -y

EXPOSE 5601

CMD sed -i "s|localhost|$ELASTICSEARCH_PORT_9200_TCP_ADDR|g" /etc/service/kibana/config/kibana.yml && \
    /etc/service/kibana/bin/kibana