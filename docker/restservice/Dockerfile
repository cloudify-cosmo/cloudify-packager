FROM debian:jessie
MAINTAINER Gigaspaces, cosmo-admin@gigaspaces.com

COPY NOTICE.txt /root/NOTICE.txt

# Used by 'cfy status' impl to determine if running in container.
ENV DOCKER_ENV=True \
    MANAGER_SERVICE_DIR=/opt/manager
ENV MANAGER_VIRTUAL_ENV_DIR=$MANAGER_SERVICE_DIR/env \
    SERVER_FILES_DIR=$MANAGER_SERVICE_DIR/cloudify-manager*/rest-service/manager_rest \
    REST_CONFIG_PATH=/etc/service/rest-service/guni.conf
# ENV AMQPFLUX_RUN_FILE /etc/service/amqp-influx/run
# ENV REST_RUN_FILE /etc/service/rest-service/run

# add run scripts and configuration
# COPY amqp_influx/ /etc/service/amqp-influx/
# COPY restservice/ /etc/service/rest-service/

WORKDIR /opt/manager/

RUN apt-get update && \
    apt-get install -y curl git python2.7 python-dev && \
    curl --silent --show-error --retry 5 https://bootstrap.pypa.io/get-pip.py | python && \
    pip install virtualenv && \
    virtualenv $MANAGER_VIRTUAL_ENV_DIR && \
    $MANAGER_VIRTUAL_ENV_DIR/bin/pip install git+git://github.com/cloudify-cosmo/cloudify-amqp-influxdb.git@master && \
    $MANAGER_VIRTUAL_ENV_DIR/bin/pip install git+git://github.com/cloudify-cosmo/cloudify-dsl-parser.git@master && \
    git clone -b master https://github.com/cloudify-cosmo/cloudify-manager.git && \
    cd cloudify-manager/rest-service && \
    $MANAGER_VIRTUAL_ENV_DIR/bin/pip install . && \
    cd ../../ && \
    # # injecting required params to run script
    # sed -i '1s|^|MANAGER_VIRTUALENV_DIR='$MANAGER_VIRTUAL_ENV_DIR' \n|' $AMQPFLUX_RUN_FILE && \
    # sed -i '1s|^|MANAGER_VIRTUALENV_DIR='$MANAGER_VIRTUAL_ENV_DIR' \n|' $REST_RUN_FILE && \
    # sed -i '1s|^|MANAGER_REST_CONFIG_PATH='$REST_CONFIG_PATH' \n|' $REST_RUN_FILE && \
    # sed -i '1s|^|SERVER_FILES_DIR='$SERVER_FILES_DIR' \n|' $REST_RUN_FILE && \
    # sed -i '1s|^|#!/bin/bash \n|' $REST_RUN_FILE && \
    # sed -i '1s|^|#!/bin/bash \n|' $AMQPFLUX_RUN_FILE && \
    # creating logs folder
    mkdir -p /var/log/cloudify && \
    # copying rest-service resources to resource folder
    cp -r /opt/manager/cloudify-manager/resources/rest-service/. /opt/manager/resources && \
    rm -rf cloudify-manager

EXPOSE 8100

WORKDIR $SERVER_FILES_DIR
CMD $MANAGER_VIRTUALENV_DIR/bin/gunicorn  -w $(($(nproc)*2+1)) -b 0.0.0.0:8100 --timeout 300 server:app --log-file /var/log/cloudify/gunicorn.log --access-logfile /var/log/cloudify/gunicorn-access.log
