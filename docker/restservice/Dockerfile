FROM debian:jessie
MAINTAINER Gigaspaces, cosmo-admin@gigaspaces.com

COPY NOTICE.txt /root/NOTICE.txt

# Used by 'cfy status' impl to determine if running in container.
ENV DOCKER_ENV=True \
    MANAGER_SERVICE_DIR=/opt/manager
ENV MANAGER_VIRTUAL_ENV_DIR=$MANAGER_SERVICE_DIR/env \
    SERVER_FILES_DIR=$MANAGER_SERVICE_DIR/cloudify-manager*/rest-service/manager_rest
    REST_CONFIG_PATH=/etc/service/rest-service/guni.conf
ENV AMQPFLUX_RUN_FILE /etc/service/amqp-influx/run
ENV REST_RUN_FILE /etc/service/rest-service/run

##### ENV #####
# add run scripts and configuration
COPY amqp_influx/ /etc/service/amqp-influx/
COPY restservice/ /etc/service/rest-service/

WORKDIR /opt/manager/

RUN apt-get update && \
    apt-get install -y {% for dep in manager.reqs %} {{ dep }}{% endfor %} && \
    # installing pip
    curl --silent --show-error --retry 5 https://bootstrap.pypa.io/get-pip.py | python && \
    # install virtualenv and create one
    pip install virtualenv && \
    virtualenv $MANAGER_VIRTUAL_ENV_DIR && \
    # installing amqpinflux
    $MANAGER_VIRTUAL_ENV_DIR/bin/pip install {{ manager.modules.cloudify_amqp_influxdb }} && \
    $MANAGER_VIRTUAL_ENV_DIR/bin/pip install {{ manager.modules.cloudify_dsl_parser }} && \
    # installing rest-service
    /bin/bash -c 'git clone {{ manager.modules.cloudify_manager }} && \
    cd cloudify-manager/rest-service && \
    $MANAGER_VIRTUAL_ENV_DIR/bin/pip install .' && \
    cd ../../ && \
    rm -rf cloudify-manager && \
    # injecting required params to run script
    sed -i '1s|^|MANAGER_VIRTUALENV_DIR='$MANAGER_VIRTUAL_ENV_DIR' \n|' $AMQPFLUX_RUN_FILE && \
    sed -i '1s|^|MANAGER_VIRTUALENV_DIR='$MANAGER_VIRTUAL_ENV_DIR' \n|' $REST_RUN_FILE && \
    sed -i '1s|^|MANAGER_REST_CONFIG_PATH='$REST_CONFIG_PATH' \n|' $REST_RUN_FILE && \
    sed -i '1s|^|SERVER_FILES_DIR='$SERVER_FILES_DIR' \n|' $REST_RUN_FILE && \
    sed -i '1s|^|#!/bin/bash \n|' $REST_RUN_FILE && \
    sed -i '1s|^|#!/bin/bash \n|' $AMQPFLUX_RUN_FILE && \
    # creating logs folder
    mkdir -p /var/log/cloudify && \
    # copying rest-service resources to resource folder
    cp -r /opt/manager/cloudify-manager/resources/rest-service/. /opt/manager/resources && \
    # granting run permissions to run file
    chmod +x $AMQPFLUX_RUN_FILE && \
    chmod +x $REST_RUN_FILE
    # cleanup
    # remove curl
    apt-get remove git -y && \
    apt-get autoremove -y

EXPOSE 8100