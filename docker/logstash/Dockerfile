FROM docker_javabase:latest
MAINTAINER Gigaspaces, cosmo-admin@gigaspaces.com

COPY LOGSTASH_NOTICE.txt /root/LOGSTASH_NOTICE.txt

ENV LOGSTASH_VERSION=1.4.2 \
    DOCKER_ENV=True \
    LOGSTASH_SERVICE_DIR=/etc/service/logstash
ENV LOGSTASH_CONF_FILE=${LOGSTASH_SERVICE_DIR}/logstash.conf

COPY logstash.conf /tmp/logstash.conf

RUN apt-get update && \
    mkdir -p ${LOGSTASH_SERVICE_DIR}/logs && \
    mv /tmp/logstash.conf ${LOGSTASH_SERVICE_DIR} && \
    apt-get install -y curl && \
    # TODO: update logstash to latest version
    curl https://download.elasticsearch.org/logstash/logstash/logstash-${LOGSTASH_VERSION}.tar.gz --create-dirs -o /opt/tmp/logstash.tar.gz && \
    tar -C ${LOGSTASH_SERVICE_DIR}/ -xzvf /opt/tmp/logstash.tar.gz --strip-components=1 && \
    rm -rf /var/lib/apt/lists; rm /opt/tmp/*; apt-get purge curl -y; apt-get autoremove -y

VOLUME /etc/service/logstash/logs
EXPOSE 9999

# TODO: make sure logs are persistent
# TODO: check whether we need --verbose or --debug
# To run manually:
# docker run -it --link docker_elasticsearch_1:elasticsearch --link docker_rabbitmq_1:rabbitmq docker_logstash /bin/bash
CMD ${LOGSTASH_SERVICE_DIR}/bin/logstash -f ${LOGSTASH_CONF_FILE} -l ${LOGSTASH_SERVICE_DIR}/logs/logstash.log --verbose