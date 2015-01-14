FROM debian:jessie
MAINTAINER Gigaspaces, cosmo-admin@gigaspaces.com

COPY NOTICE.txt /root/NOTICE.txt

# Used by 'cfy status' impl to determine if running in container.
ENV VERSION=1.3.2 \
    DOCKER_ENV=True \
    LOGSTASH_SERVICE_DIR=/etc/service/logstash
ENV LOGSTASH_CONF_FILE=${LOGSTASH_SERVICE_DIR}/logstash.conf \
    LOGSTASH_JAR_PATH=${LOGSTASH_SERVICE_DIR}/logstash.jar \
    JAVA_HOME=/etc/java

COPY logstash.conf /tmp/logstash.conf

RUN apt-get update && \
    mkdir -p ${LOGSTASH_SERVICE_DIR} && \
    mv /tmp/logstash.conf ${LOGSTASH_SERVICE_DIR} && \
    apt-get install -y curl && \
    curl https://dl.dropboxusercontent.com/u/407576/jre-7-linux-x64.tar.gz --create-dirs -o /opt/tmp/java.tar.gz && \
    mkdir ${JAVA_HOME} && tar -xzvf /opt/tmp/java.tar.gz -C ${JAVA_HOME} --strip=1 && \
    # TODO: update logstash to latest version
    curl https://download.elasticsearch.org/logstash/logstash/logstash-${VERSION}-flatjar.jar --create-dirs -o ${LOGSTASH_SERVICE_DIR}/logstash.jar && \
    rm -rf /var/lib/apt/lists; rm /opt/tmp/*; apt-get remove curl -y; apt-get autoremove -y

EXPOSE 9999

CMD sed -i "s|ELASTICSEARCH_ADDR|$ELASTICSEARCH_PORT_9200_TCP_ADDR|g" $LOGSTASH_CONF_FILE && \
    sed -i "s|RABBITMQ_ADDR|$RABBITMQ_PORT_5672_TCP_ADDR|g" $LOGSTASH_CONF_FILE && \
    # sed -i "s|INFLUXDB_ADDR|$INFLUXDB_PORT_8086_TCP_ADDR|g" $LOGSTASH_CONF_FILE && \
    ${JAVA_HOME}/bin/java -jar ${LOGSTASH_JAR_PATH} agent -f $LOGSTASH_CONF_FILE
# ONELINER FOR TESTING
# sed -i "s|ELASTICSEARCH_ADDR|$ELASTICSEARCH_PORT_9200_TCP_ADDR|g" $LOGSTASH_CONF_FILE && sed -i "s|RABBITMQ_ADDR|$RABBITMQ_PORT_5672_TCP_ADDR|g" $LOGSTASH_CONF_FILE && /etc/java/bin/java -jar ${LOGSTASH_JAR_PATH} agent -f $LOGSTASH_CONF_FILE