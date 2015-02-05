FROM phusion/baseimage
MAINTAINER Gigaspaces, cosmo-admin@gigaspaces.com

###
# Nginx
###
ENV DOCKER_ENV=True \
    NGINX_SERVICE_DIR=/etc/service/nginx \
    NGINX_SERVER_CONF_FILE=/etc/service/nginx/default.conf \
    NGINX_FILESERVER_DIR=/fileserver

COPY nginx/run /etc/service/nginx/run

RUN mkdir -p ${NGINX_SERVICE_DIR} && \
    mkdir -p ${NGINX_FILESERVER_DIR} && \
    echo "deb http://nginx.org/packages/ubuntu/ trusty nginx" >> /etc/apt/sources.list.d/nginx.list && \
    apt-key adv --fetch-keys http://nginx.org/keys/nginx_signing.key && \
    apt-get update && \
    apt-get install -y nginx && \
    chmod +x /etc/service/nginx/run && \
    rm -rf /var/lib/apt/lists && \
    apt-get autoremove -y

COPY nginx/default.conf /etc/nginx/conf.d/
VOLUME ${NGINX_FILESERVER_DIR}
EXPOSE 80 53229

###
# UI
###
ENV DOCKER_ENV=True \
    NODEJS_VERSION=0.10.35 \
    WEBUI_VERSION=3.1.1 \
    NODEJS_HOME=/opt/nodejs \
    WEBUI_HOME=/opt/cloudify-ui

COPY webui/run /etc/service/cloudify-ui/run

RUN apt-get update && \
    apt-get install curl -y && \
    chmod +x /etc/service/cloudify-ui/run && \
    mkdir -p ${NODEJS_HOME} && \
    mkdir -p /var/log/cloudify-ui && touch /var/log/cloudify-ui/cloudify-ui.log && \
    mkdir -p ${WEBUI_HOME}/grafana && \
    curl --silent http://nodejs.org/dist/v${NODEJS_VERSION}/node-v${NODEJS_VERSION}-linux-x64.tar.gz -o /tmp/nodejs.tar.gz && \
    tar -xzvf /tmp/nodejs.tar.gz -C ${NODEJS_HOME} --strip-components=1 && \
    curl --silent http://gigaspaces-repository-eu.s3.amazonaws.com/org/cloudify3/${WEBUI_VERSION}/ga-RELEASE/cloudify-ui_${WEBUI_VERSION}-ga-b87_amd64.deb -o /tmp/cloudify-webui.deb && \
    dpkg-deb -x /tmp/cloudify-webui.deb /tmp/cloudify-webui/ && \
    tar -xzvf /tmp/cloudify-webui/packages/cloudify-ui/cosmo-ui* -C ${WEBUI_HOME} --strip-components=1 && \
    tar -xzvf /tmp/cloudify-webui/packages/cloudify-ui/grafana* -C ${WEBUI_HOME}/grafana --strip-components=1 && \
    cp /tmp/cloudify-webui/packages/cloudify-ui/config/grafana/config.js ${WEBUI_HOME}/grafana/ && \
    # current workaround for missing dependency
    ${NODEJS_HOME}/bin/npm install --prefix ${WEBUI_HOME} request && \
    rm -rf /var/lib/apt/lists && \
    rm -rf /tmp/* && \
    apt-get purge -y curl && \
    apt-get autoremove -y

###
# REST
###
ENV DOCKER_ENV=True \
    DSL_VERSION=master \
    MANAGER_VERSION=CFY-1838-separate-services-container-to-service-specific-containers \
    MANAGER_HOME_DIR=/opt/manager
ENV MANAGER_VIRTUALENV_DIR=${MANAGER_HOME_DIR}/env \
    MANAGER_REST_CONFIG_PATH=${MANAGER_HOME_DIR}/guni.conf

# add run scripts and configuration
COPY restservice/guni.conf /tmp/guni.conf
COPY restservice/run /etc/service/restservice/run

RUN apt-get update && \
    apt-get install -y curl gcc python-dev && \
    chmod +x /etc/service/restservice/run && \
    curl --silent --show-error --retry 5 https://bootstrap.pypa.io/get-pip.py | python && \
    pip install virtualenv && \
    mkdir -p ${MANAGER_HOME_DIR} && \
    mkdir -p /var/log/cloudify && \
    mv /tmp/guni.conf ${MANAGER_HOME_DIR} && \
    virtualenv ${MANAGER_VIRTUALENV_DIR} && \
    ${MANAGER_VIRTUALENV_DIR}/bin/pip install https://github.com/cloudify-cosmo/cloudify-dsl-parser/archive/${DSL_VERSION}.zip && \
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


CMD /sbin/my_init
