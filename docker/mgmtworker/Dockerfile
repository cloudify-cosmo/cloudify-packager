FROM debian:jessie
MAINTAINER Gigaspaces, cosmo-admin@gigaspaces.com

# Used by 'cfy status' impl to determine if running in container.
ENV DOCKER_ENV True
# LICENSE
COPY NOTICE.txt /root/NOTICE.txt

# ------------------------------------------------------------------------------------------------------------------------------------------ #
# INSTALL - MGMTWORKER
# ------------------------------------------------------------------------------------------------------------------------------------------ #
ENV CELERY_SERVICE_DIR=/etc/service/mgmtworker
ENV CELERY_RUN_FILE=$CELERY_SERVICE_DIR/run && \
    CELERY_VIRTUAL_ENV_DIR=$CELERY_SERVICE_DIR/env && \
    CELERY_LOG_DIR=$CELERY_SERVICE_DIR/logs

# add run scripts and configuration
COPY mgmtworker/run /tmp/run

RUN apt-get update && \
    mkdir -p $CELERY_SERVICE_DIR && \
    mv /tmp/run $CELERY_SERVICE_DIR && \
    # installing celery dependencies
    apt-get install -y curl python2.7 git g++ python-dev && \
    # installing pip
    curl --silent --show-error --retry 5 https://bootstrap.pypa.io/get-pip.py | python && \
    # installing virtualenv and creating one
    pip install virtualenv && \
    virtualenv $CELERY_VIRTUAL_ENV_DIR && \
    # installing celery python requirements in virtualenv1
    $CELERY_VIRTUAL_ENV_DIR/bin/pip install celery==3.0.24 && \
    $CELERY_VIRTUAL_ENV_DIR/bin/pip install git+git://github.com/cloudify-cosmo/cloudify-rest-client.git@master && \
    $CELERY_VIRTUAL_ENV_DIR/bin/pip install git+git://github.com/cloudify-cosmo/cloudify-plugins-common.git@master && \
    $CELERY_VIRTUAL_ENV_DIR/bin/pip install git+git://github.com/cloudify-cosmo/cloudify-script-plugin.git@master && \
    cd $CELERY_SERVICE_DIR && \
    /bin/bash -c 'git clone -b master https://github.com/cloudify-cosmo/cloudify-manager.git && \
    pushd cloudify-manager/plugins/plugin-installer && \
    $CELERY_VIRTUAL_ENV_DIR/bin/pip install . && \
    popd && \
    pushd cloudify-manager/plugins/agent-installer && \
    $CELERY_VIRTUAL_ENV_DIR/bin/pip install . && \
    popd && \
    pushd cloudify-manager/plugins/windows-agent-installer && \
    $CELERY_VIRTUAL_ENV_DIR/bin/pip install . && \
    popd && \
    pushd cloudify-manager/plugins/riemann-controller && \
    $CELERY_VIRTUAL_ENV_DIR/bin/pip install . && \
    popd && \
    pushd cloudify-manager/workflows && \
    $CELERY_VIRTUAL_ENV_DIR/bin/pip install .' && \
    # inject required params to run script and create logs dir
    sed -i '1s|^|CELERY_HOME_DIR='$CELERY_SERVICE_DIR' \n|' $CELERY_RUN_FILE && \
    sed -i '1s|^|CELERY_LOG_DIR='$CELERY_LOG_DIR' \n|' $CELERY_RUN_FILE && \
    sed -i '1s|^|#!/bin/bash \n|' $CELERY_RUN_FILE && \
    mkdir -p $CELERY_LOG_DIR && \
    chmod +x $CELERY_RUN_FILE

CMD /etc/service/mgmtworker/run