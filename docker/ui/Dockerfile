FROM debian:jessie
MAINTAINER Gigaspaces, cosmo-admin@gigaspaces.com

COPY NOTICE.txt /root/NOTICE.txt

# Used by 'cfy status' impl to determine if running in container.
ENV DOCKER_ENV=True \
    WEBUI_SERVICE_DIR=/etc/service/cloudify-ui
ENV WEBUI_RUN_FILE $WEBUI_SERVICE_DIR/run
ENV WEBUI_VIRTUAL_ENV_DIR $WEBUI_SERVICE_DIR/env
##### ENV #####
COPY ui/ $WEBUI_SERVICE_DIR/

RUN apt-get update && \
    echo '\n# Node.js\nexport PATH="node_modules/.bin:$PATH"' >> /root/.bashrc && \
    # downloading cloudify-webui package and extracting webui and grafana tar.gz
    curl http://gigaspaces-repository-eu.s3.amazonaws.com/org/cloudify3/3.2.0/m2-RELEASE/cloudify-ui_3.2.0-m2-b171_amd64.deb --create-dirs -o /opt/tmp/cloudify-webui/cloudify-webui.deb && \
    dpkg-deb -x /opt/tmp/cloudify-webui/cloudify-webui.deb /opt/tmp/cloudify-webui/ && \
    mkdir -p $WEBUI_SERVICE_DIR/cosmo-ui && \
    tar -xvf /opt/tmp/cloudify-webui/packages/cloudify-ui/cosmo-ui* -C $WEBUI_SERVICE_DIR/cosmo-ui --strip-components=1 && \
    mkdir -p $WEBUI_SERVICE_DIR/grafana && \
    tar -xvf /opt/tmp/cloudify-webui/packages/cloudify-ui/grafana* -C $WEBUI_SERVICE_DIR/grafana --strip-components=1 && \
    cp /opt/tmp/cloudify-webui/packages/cloudify-ui/config/grafana/config.js $WEBUI_SERVICE_DIR/grafana/ && \
    rm -rf /opt/tmp/cloudify-webui/cloudify-webui.deb && \
    chmod +x $WEBUI_RUN_FILE && \
    cd /etc/service/cloudify-ui/cosmo-ui && \
    npm update

EXPOSE 9100

CMD cd /etc/service/cloudify-ui/cosmo-ui/ && node cosmoui.js localhost