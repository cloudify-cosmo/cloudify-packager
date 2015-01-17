FROM debian:jessie
MAINTAINER Gigaspaces, cosmo-admin@gigaspaces.com

COPY NOTICE.txt /root/NOTICE.txt

# Used by 'cfy status' impl to determine if running in container.
ENV VERSION=0.10.35 \
    DOCKER_ENV=True \
    NODEJS_HOME=/etc/nodejs \
    WEBUI_SERVICE_DIR=/etc/service/cloudify-ui \
    WEBUI_LOGS_DIR=/var/log/cloudify-ui
# ENV PATH=PATH:/etc/nodejs/bin

RUN apt-get update && \
    apt-get install curl git bzip2 -y && \
    mkdir -p ${NODEJS_HOME} && \
    mkdir -p ${WEBUI_LOGS_DIR} && touch ${WEBUI_LOGS_DIR}/cloudify-ui.log && \
    mkdir -p ${WEBUI_SERVICE_DIR}/ui && \
    mkdir -p ${WEBUI_SERVICE_DIR}/grafana && \
    curl http://nodejs.org/dist/v0.10.35/node-v${VERSION}-linux-x64.tar.gz  --create-dirs -o /opt/tmp/nodejs.tar.gz && \
    tar -xzvf /opt/tmp/nodejs.tar.gz -C ${NODEJS_HOME} --strip-components=1 && \
    curl http://gigaspaces-repository-eu.s3.amazonaws.com/org/cloudify3/3.1.1/ga-RELEASE/cloudify-ui_3.1.1-ga-b87_amd64.deb --create-dirs -o /opt/tmp/cloudify-webui.deb && \
    dpkg-deb -x /opt/tmp/cloudify-webui.deb /opt/tmp/cloudify-webui/ && \
    tar -xzvf /opt/tmp/cloudify-webui/packages/cloudify-ui/cosmo-ui* -C ${WEBUI_SERVICE_DIR} --strip-components=1 && \
    tar -xzvf /opt/tmp/cloudify-webui/packages/cloudify-ui/grafana* -C ${WEBUI_SERVICE_DIR}/grafana --strip-components=1 && \
    cp /opt/tmp/cloudify-webui/packages/cloudify-ui/config/grafana/config.js $WEBUI_SERVICE_DIR/grafana/ && \
    cd ${WEBUI_SERVICE_DIR} && ${NODEJS_HOME}/bin/npm install -d && \
    rm -rf /var/lib/apt/lists; rm /opt/tmp/*; apt-get remove curl git bzip2 -y; apt-get autoremove -y

EXPOSE 9001

CMD cd /etc/service/cloudify-ui && ${NODEJS_HOME}/bin/node cosmoui.js 0.0.0.0