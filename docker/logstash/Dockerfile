FROM docker_javabase:latest
MAINTAINER Gigaspaces, cosmo-admin@gigaspaces.com

COPY LOGSTASH_NOTICE.txt /root/LOGSTASH_NOTICE.txt

ENV LOGSTASH_VERSION=1.4.2 \
    DOCKER_ENV=True \
    LOGSTASH_HOME_DIR=/opt/logstash \
    LOGSTASH_LOG_DIR=/var/log/logstash


RUN apt-get update && \
    mkdir -p ${LOGSTASH_LOG_DIR} && \
    mkdir -p ${LOGSTASH_HOME_DIR} && \
    apt-get install -y curl && \
    curl --fail --silent --location https://download.elasticsearch.org/logstash/logstash/logstash-${LOGSTASH_VERSION}.tar.gz -o /tmp/logstash.tar.gz && \
    tar -C ${LOGSTASH_HOME_DIR} -xzvf /tmp/logstash.tar.gz --strip-components=1 && \
    rm -rf /var/lib/apt/lists && \
    rm /tmp/* && \
    apt-get purge curl -y && \
    apt-get autoremove -y

COPY logstash.conf ${LOGSTASH_HOME_DIR}/logstash.conf

VOLUME ${LOGSTASH_LOG_DIR}
EXPOSE 9999

CMD ${LOGSTASH_HOME_DIR}/bin/logstash -f ${LOGSTASH_HOME_DIR}/logstash.conf -l ${LOGSTASH_LOG_DIR}/logstash.log --verbose