FROM debian:jessie
MAINTAINER Gigaspaces, cosmo-admin@gigaspaces.com

COPY NOTICE.txt /root/NOTICE.txt

# Used by 'cfy status' impl to determine if running in container.
ENV VERSION=master \
    DOCKER_ENV=True \
    MANAGER_SERVICE_DIR=/opt/manager
ENV MANAGER_VIRTUALENV_DIR=${MANAGER_SERVICE_DIR}/env \
    MANAGER_REST_CONFIG_PATH=${MANAGER_SERVICE_DIR}/guni.conf

# add run scripts and configuration
COPY guni.conf /tmp/guni.conf

WORKDIR ${MANAGER_SERVICE_DIR}

RUN apt-get update && \
    mkdir -p ${MANAGER_SERVICE_DIR} && \
    mv /tmp/guni.conf ${MANAGER_SERVICE_DIR} && \
    apt-get install -y curl git python2.7 python-dev && \
    curl --silent --show-error --retry 5 https://bootstrap.pypa.io/get-pip.py | python && \
    pip install virtualenv && \
    virtualenv ${MANAGER_VIRTUALENV_DIR} && \
    ${MANAGER_VIRTUALENV_DIR}/bin/pip install git+git://github.com/cloudify-cosmo/cloudify-dsl-parser.git@${VERSION} && \
    git clone -b ${VERSION} https://github.com/cloudify-cosmo/cloudify-manager.git && \
    cd cloudify-manager/rest-service && \
    ${MANAGER_VIRTUALENV_DIR}/bin/pip install . && \
    cd ../../ && \
    mkdir -p /var/log/cloudify && \
    # copying rest-service resources to resource folder
    cp -r /opt/manager/cloudify-manager/resources/rest-service/. /opt/manager/resources && \
    rm -rf cloudify-manager && \
    rm -rf /var/lib/apt/lists; apt-get remove curl git python-dev -y; apt-get autoremove -y

EXPOSE 8100

CMD ${MANAGER_VIRTUALENV_DIR}/bin/gunicorn  -w $(($(nproc)*2+1)) -b 0.0.0.0:8100 --timeout 300 manager_rest.server:app --log-file /var/log/cloudify/gunicorn.log --access-logfile /var/log/cloudify/gunicorn-access.log
