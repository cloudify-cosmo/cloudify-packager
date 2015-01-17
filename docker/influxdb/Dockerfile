FROM debian:jessie
MAINTAINER Gigaspaces, cosmo-admin@gigaspaces.com

COPY NOTICE.txt /root/NOTICE.txt
COPY utils.sh /opt/tmp/utils.sh

# Used by 'cfy status' impl to determine if running in container.
ENV VERSION=0.8.8 \
    DOCKER_ENV=True \
    INFLUXDB_SERVICE_DIR=/opt/influxdb
ENV INFLUXDB_CONFIG_FILE=${INFLUXDB_SERVICE_DIR}/shared/config.toml

RUN apt-get update && \
    apt-get install -y curl && \
    curl http://s3.amazonaws.com/influxdb/influxdb_${VERSION}_amd64.deb --create-dirs -o /opt/tmp/influxdb.deb && \
    dpkg -i /opt/tmp/influxdb.deb && \
    # starting influxdb as daemon to create cloudify db
    /bin/bash -c 'source /opt/tmp/utils.sh && \
    /usr/bin/influxdb-daemon -config=${INFLUXDB_CONFIG_FILE} && \
    wait_for_port 8086' && \
    curl -s "http://localhost:8086/db?u=root&p=root" -d "{\"name\": \"cloudify\"}" && \
    rm -rf /var/lib/apt/lists; rm /opt/tmp/*; apt-get remove curl -y; apt-get autoremove -y

VOLUME ${INFLUXDB_SERVICE_DIR}/shared/data

EXPOSE 8086 8083

CMD /usr/bin/influxdb -config=${INFLUXDB_CONFIG_FILE}