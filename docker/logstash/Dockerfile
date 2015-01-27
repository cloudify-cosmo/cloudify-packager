FROM thinkops/light-jre:latest
MAINTAINER Gigaspaces, cosmo-admin@gigaspaces.com

COPY NOTICE.txt /root/NOTICE.txt

ENV VERSION=1.3.2 \
    DOCKER_ENV=True \
    LOGSTASH_SERVICE_DIR=/etc/service/logstash
ENV LOGSTASH_CONF_FILE=${LOGSTASH_SERVICE_DIR}/logstash.conf \
    LOGSTASH_JAR_PATH=${LOGSTASH_SERVICE_DIR}/logstash.jar

COPY logstash.conf /tmp/logstash.conf

RUN apt-get update && \
    mkdir -p ${LOGSTASH_SERVICE_DIR}/logs && \
    mv /tmp/logstash.conf ${LOGSTASH_SERVICE_DIR} && \
    apt-get install -y curl && \
    # TODO: update logstash to latest version
    curl https://download.elasticsearch.org/logstash/logstash/logstash-${VERSION}-flatjar.jar --create-dirs -o ${LOGSTASH_SERVICE_DIR}/logstash.jar && \
    rm -rf /var/lib/apt/lists; rm /opt/tmp/*; apt-get remove curl -y; apt-get autoremove -y

EXPOSE 9999

# TODO: make sure logs are persistent
# TODO: check whether we need --verbose or --debug
# To run manually:
# docker run -it --link docker_elasticsearch_1:elasticsearch --link docker_rabbitmq_1:rabbitmq docker_logstash /bin/bash
CMD ${JAVA_HOME}/bin/java -jar ${LOGSTASH_JAR_PATH} agent -f ${LOGSTASH_CONF_FILE} -l /etc/service/logstash/logs/logstash.log --verbose