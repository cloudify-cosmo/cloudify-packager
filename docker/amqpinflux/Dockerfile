FROM docker_pythonbase
MAINTAINER Gigaspaces, cosmo-admin@gigaspaces.com

COPY NOTICE.txt /root/NOTICE.txt

ENV VERSION=master \
    DOCKER_ENV=True \
    AMQP_HOST=rabbitmq
    INFLUXDB_HOST=influxdb
    SERVICE_DIR=/opt/amqpinflux \
    VIRTUALENV_DIR=${SERVICE_DIR}/env

RUN mkdir -p ${SERVICE_DIR} && \
    virtualenv ${VIRTUALENV_DIR} && \
    ${VIRTUALENV_DIR}/bin/pip install https://github.com/cloudify-cosmo/cloudify-amqp-influxdb/archive/${VERSION}.zip

CMD ${VIRTUALENV_DIR}/bin/python ${VIRTUALENV_DIR}/bin/cloudify-amqp-influxdb \
    --amqp-exchange cloudify-monitoring \
    --amqp-routing-key '*' \
    --amqp-hostname ${AMQP_HOST} \
    --influx-database cloudify \
    --influx-hostname ${INFLUXDB_HOST}