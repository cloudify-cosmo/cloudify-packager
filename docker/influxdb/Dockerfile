FROM debian:jessie
MAINTAINER Gigaspaces, cosmo-admin@gigaspaces.com

COPY INFLUXDB_NOTICE.txt /root/INFLUXDB_NOTICE.txt
COPY scripts/* /opt/scripts/

ENV INFLUXDB_VERSION=0.8.8 \
    DOCKER_ENV=True \
    INFLUXDB_SERVICE_DIR=/opt/influxdb
ENV INFLUXDB_CONFIG_FILE=${INFLUXDB_SERVICE_DIR}/shared/config.toml

RUN apt-get update && \
    apt-get install -y curl && \
    curl http://s3.amazonaws.com/influxdb/influxdb_${INFLUXDB_VERSION}_amd64.deb --create-dirs -o /opt/tmp/influxdb.deb && \
    dpkg -i /opt/tmp/influxdb.deb && \
    # starting influxdb as daemon to create cloudify db
    /usr/bin/influxdb-daemon -config=${INFLUXDB_CONFIG_FILE} && \
    chmod +x /opt/scripts/wait_for_port && sleep 3 && /opt/scripts/wait_for_port 8086 && \
    curl -s "http://localhost:8086/db?u=root&p=root" -d "{\"name\": \"cloudify\"}" && \
    rm -rf /var/lib/apt/lists; rm /opt/tmp/*; apt-get purge curl -y; apt-get autoremove -y

VOLUME ${INFLUXDB_SERVICE_DIR}/shared/data

EXPOSE 8086 8083

CMD /usr/bin/influxdb -config=${INFLUXDB_CONFIG_FILE}