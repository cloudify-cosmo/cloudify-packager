FROM docker_pythonbase
MAINTAINER Gigaspaces, cosmo-admin@gigaspaces.com

COPY NOTICE.txt /root/NOTICE.txt

# Used by 'cfy status' impl to determine if running in container.
ENV VERSION=master \
    MANAGER_VERSION=CFY-1838-separate-services-container-to-service-specific-containers \
    DOCKER_ENV=True \
    MANAGER_SERVICE_DIR=/opt/manager
ENV MANAGER_VIRTUALENV_DIR=${MANAGER_SERVICE_DIR}/env \
    MANAGER_REST_CONFIG_PATH=${MANAGER_SERVICE_DIR}/guni.conf

# add run scripts and configuration
COPY guni.conf /tmp/guni.conf

WORKDIR ${MANAGER_SERVICE_DIR}

RUN apt-get update && \
    apt-get install -y curl gcc python-dev && \
    mkdir -p ${MANAGER_SERVICE_DIR} && \
    mkdir -p /var/log/cloudify && \
    mv /tmp/guni.conf ${MANAGER_SERVICE_DIR} && \
    virtualenv ${MANAGER_VIRTUALENV_DIR} && \
    ${MANAGER_VIRTUALENV_DIR}/bin/pip install https://github.com/cloudify-cosmo/cloudify-dsl-parser/archive/${VERSION}.zip && \
    curl --silent -L -o /tmp/cloudify-manager/manager.tar.gz --create-dirs https://github.com/cloudify-cosmo/cloudify-manager/archive/${MANAGER_VERSION}.tar.gz && \
    tar -xzf /tmp/cloudify-manager/manager.tar.gz --strip-components=1 -C /tmp/cloudify-manager/ && \
    ${MANAGER_VIRTUALENV_DIR}/bin/pip install /tmp/cloudify-manager/rest-service && \
    # copying rest-service resources to resource folder
    cp -r /tmp/cloudify-manager/resources/rest-service/* /opt/manager/resources && \
    rm -rf /var/lib/apt/lists /tmp/* && \
    apt-get purge -y curl gcc python-dev && \
    apt-get autoremove -y

VOLUME /opt/manager/resources/blueprints
VOLUME /opt/manager/resources/uploaded-blueprints

EXPOSE 8100

CMD echo "fileserver   $(/sbin/ip route|awk '/default/ { print $3 }')" >> /etc/hosts && \
    echo "elasticsearch   $(/sbin/ip route|awk '/default/ { print $3 }')" >> /etc/hosts && \
    ${MANAGER_VIRTUALENV_DIR}/bin/gunicorn  -w $(($(nproc)*2+1)) -b 0.0.0.0:8100 --timeout 300 manager_rest.server:app --log-file /var/log/cloudify/gunicorn.log --access-logfile /var/log/cloudify/gunicorn-access.log
