FROM debian:jessie
MAINTAINER Gigaspaces, cosmo-admin@gigaspaces.com

COPY NOTICE.txt /root/NOTICE.txt

# Used by 'cfy status' impl to determine if running in container.
ENV DOCKER_ENV=True
    LOGSTASH_SERVICE_NAME=logstash
ENV LOGSTASH_SERVICE_DIR=/etc/service/$LOGSTASH_SERVICE_NAME
ENV LOGSTASH_CONF_FILE=$LOGSTASH_SERVICE_DIR/logstash.conf \
    LOGSTASH_JAR_PATH=$LOGSTASH_SERVICE_DIR/logstash.jar \
    JAVA_HOME=/etc/java

COPY logstash.conf /tmp/logstash.conf

RUN apt-get update && \
    mkdir -p $LOGSTASH_SERVICE_DIR && \
    mv /tmp/logstash.conf $LOGSTASH_SERVICE_DIR && \
    apt-get install -y curl && \
    curl https://dl.dropboxusercontent.com/u/407576/jre-7-linux-x64.tar.gz --create-dirs -o /opt/tmp/java/java.tar.gz && \
    mkdir /etc/java && \
    tar -xzvf /opt/tmp/java/java.tar.gz -C /etc/java --strip=1 && \
    rm /opt/tmp/java/java.tar.gz && \
    curl https://download.elasticsearch.org/logstash/logstash/logstash-1.3.2-flatjar.jar --create-dirs -o $LOGSTASH_SERVICE_DIR/logstash.jar
    # cleanup
    rm -rf /var/lib/apt/lists && apt-get remove curl -y && apt-get autoremove -y

EXPOSE 9999

CMD sed -i "s|ELASTICSEARCH_ADDR|$ELASTICSEARCH_PORT_9200_TCP_ADDR|g" $LOGSTASH_CONF_FILE && \
    sed -i "s|RABBITMQ_ADDR|$RABBITMQ_PORT_5672_TCP_ADDR|g" $LOGSTASH_CONF_FILE && \
    /etc/java/bin/java -jar $LOGSTASH_JAR_PATH agent -f $LOGSTASH_CONF_FILE
# ONELINER FOR TESTING
# sed -i "s|ELASTICSEARCH_ADDR|$ELASTICSEARCH_PORT_9200_TCP_ADDR|g" $LOGSTASH_CONF_FILE && sed -i "s|RABBITMQ_ADDR|$RABBITMQ_PORT_5672_TCP_ADDR|g" $LOGSTASH_CONF_FILE && /etc/java/bin/java -jar $LOGSTASH_JAR_PATH agent -f $LOGSTASH_CONF_FILE