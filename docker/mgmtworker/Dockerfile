FROM debian:jessie
MAINTAINER Gigaspaces, cosmo-admin@gigaspaces.com

COPY NOTICE.txt /root/NOTICE.txt

# Used by 'cfy status' impl to determine if running in container.
ENV VERSION=3.1 \
    DOCKER_ENV=True \
    CELERY_SERVICE_DIR=/etc/service/mgmtworker
ENV CELERY_RUN_FILE=${CELERY_SERVICE_DIR}/run \
    CELERY_VIRTUALENV_DIR=${CELERY_SERVICE_DIR}/env \
    CELERY_LOG_DIR=${CELERY_SERVICE_DIR}/logs

# add run scripts and configuration
COPY run /tmp/run

RUN apt-get update && \
    mkdir -p ${CELERY_SERVICE_DIR} && \
    mv /tmp/run ${CELERY_SERVICE_DIR} && \
    apt-get install -y curl python2.7 git g++ python-dev && \
    curl --silent --show-error --retry 5 https://bootstrap.pypa.io/get-pip.py | python && \
    pip install virtualenv && \
    virtualenv ${CELERY_VIRTUALENV_DIR} && \
    ${CELERY_VIRTUALENV_DIR}/bin/pip install celery==3.0.24 && \
    ${CELERY_VIRTUALENV_DIR}/bin/pip install git+git://github.com/cloudify-cosmo/cloudify-rest-client.git@${VERSION} && \
    ${CELERY_VIRTUALENV_DIR}/bin/pip install git+git://github.com/cloudify-cosmo/cloudify-plugins-common.git@${VERSION} && \
    ${CELERY_VIRTUALENV_DIR}/bin/pip install git+git://github.com/cloudify-cosmo/cloudify-script-plugin.git@${VERSION} && \
    cd ${CELERY_SERVICE_DIR} && \
    git clone -b ${VERSION} https://github.com/cloudify-cosmo/cloudify-manager.git && \
    ${CELERY_VIRTUALENV_DIR}/bin/pip install cloudify-manager/plugins/plugin-installer && \
    ${CELERY_VIRTUALENV_DIR}/bin/pip install cloudify-manager/plugins/agent-installer && \
    ${CELERY_VIRTUALENV_DIR}/bin/pip install cloudify-manager/plugins/riemann-controller && \
    ${CELERY_VIRTUALENV_DIR}/bin/pip install cloudify-manager/workflows && \
    # inject required params to run script and create logs dir
    sed -i '1s|^|CELERY_HOME_DIR='${CELERY_SERVICE_DIR}' \n|' ${CELERY_RUN_FILE} && \
    sed -i '1s|^|CELERY_LOG_DIR='${CELERY_LOG_DIR}' \n|' ${CELERY_RUN_FILE} && \
    sed -i '1s|^|#!/bin/bash \n|' ${CELERY_RUN_FILE} && \
    mkdir -p ${CELERY_LOG_DIR} && \
    chmod +x ${CELERY_RUN_FILE} && \
    # rm -rf /var/lib/apt/lists; apt-get remove curl git python-dev g++ -y; apt-get autoremove -y

CMD /etc/service/mgmtworker/run