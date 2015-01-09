FROM debian:jessie
MAINTAINER Gigaspaces, cosmo-admin@gigaspaces.com
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# INSTALL - BASE
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# add utility functions
COPY utils.sh /opt/tmp/utils/utils.sh
COPY NOTICE.txt /root/NOTICE.txt
# Used by 'cfy status' impl to determine if running in container.
ENV DOCKER_ENV True

# ------------------------------------------------------------------------------------------------------------------------------------------ #
# INSTALL - INFLUXDB
# ------------------------------------------------------------------------------------------------------------------------------------------ #
##### ENV #####
ENV INFLUXDB_SERVICE_NAME=influxdb \
    INFLUXDB_CONFIG_FILE=/opt/influxdb/shared/config.toml
ENV INFLUXDB_RUN_FILE=/etc/service/$INFLUXDB_SERVICE_NAME/run

RUN apt-get update && \
    # installing influxdb dependencies
    apt-get install -y curl && \
    # downloading influxdb binaries
    curl http://s3.amazonaws.com/influxdb/influxdb_0.8.0_amd64.deb --create-dirs -o /opt/tmp/influxdb/influxdb.deb && \
    # installing influxdb
    dpkg -i /opt/tmp/influxdb/influxdb.deb && \
    rm -rf /opt/tmp/influxdb/influxdb.deb && \
    # starting influxdb as daemon to create cloudify db && \
    /bin/bash -c 'source /opt/tmp/utils/utils.sh && \
    /usr/bin/influxdb-daemon -config=$INFLUXDB_CONFIG_FILE && \
    wait_for_port 8086' && \
    curl -s "http://localhost:8086/db?u=root&p=root" -d "{\"name\": \"cloudify\"}"

# influxdb persistence path
# VOLUME /opt/influxdb/shared/data

EXPOSE 8086 8083

CMD /usr/bin/influxdb -config=$INFLUXDB_CONFIG_FILE