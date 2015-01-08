FROM {{ image.repository }}:{{ image.tag }}
MAINTAINER {{ maintainer.name }}, {{ maintainer.email }}
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# INSTALL - BASE
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# add utility functions
COPY utils/ /opt/tmp/utils/
COPY NOTICE.txt /root/NOTICE.txt
# Used by 'cfy status' impl to determine if running in container.
ENV DOCKER_ENV True

# ------------------------------------------------------------------------------------------------------------------------------------------ #
# INSTALL - UI
# ------------------------------------------------------------------------------------------------------------------------------------------ #
##### ENV #####
ENV WEBUI_SERVICE_NAME {{ webui.service_name }}
ENV WEBUI_SERVICE_DIR /etc/service/$WEBUI_SERVICE_NAME
ENV WEBUI_RUN_FILE $WEBUI_SERVICE_DIR/run
ENV WEBUI_VIRTUAL_ENV_DIR $WEBUI_SERVICE_DIR/env
##### ENV #####
COPY ui/ $WEBUI_SERVICE_DIR/
http://nodejs.org/dist/v0.10.35/node-v0.10.35-linux-x64.tar.gz
RUN apt-get update && \
    # installing web-ui dependencies
    apt-get install -y {% for dep in webui.reqs %} {{ dep }}{% endfor %} && \
    # installing nodejs from source
    cd /tmp && \
    curl {{ webui.nodejs_latest_url }} -o /tmp/node-latest.tar.gz && \
    tar xvzf node-latest.tar.gz && \
    rm -f node-latest.tar.gz && \
    cd node-v* && \
    ./configure && \
    CXX="g++ -Wno-unused-local-typedefs" make && \
    CXX="g++ -Wno-unused-local-typedefs" make install && \
    cd /tmp && \
    rm -rf /tmp/node-v* && \
    echo '\n# Node.js\nexport PATH="node_modules/.bin:$PATH"' >> /root/.bashrc && \
    # downloading cloudify-webui package and extracting webui and grafana tar.gz
    curl {{ webui.ui_package_url }} --create-dirs -o /opt/tmp/cloudify-webui/cloudify-webui.deb && \
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
FROM {{ image.repository }}:{{ image.tag }}
MAINTAINER {{ maintainer.name }}, {{ maintainer.email }}
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# INSTALL - BASE
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# add utility functions
COPY utils/ /opt/tmp/utils/
COPY NOTICE.txt /root/NOTICE.txt
# Used by 'cfy status' impl to determine if running in container.
ENV DOCKER_ENV True

# ------------------------------------------------------------------------------------------------------------------------------------------ #
# INSTALL - UI
# ------------------------------------------------------------------------------------------------------------------------------------------ #
##### ENV #####
ENV WEBUI_SERVICE_NAME {{ webui.service_name }}
ENV WEBUI_SERVICE_DIR /etc/service/$WEBUI_SERVICE_NAME
ENV WEBUI_RUN_FILE $WEBUI_SERVICE_DIR/run
ENV WEBUI_VIRTUAL_ENV_DIR $WEBUI_SERVICE_DIR/env
##### ENV #####
COPY ui/ $WEBUI_SERVICE_DIR/

RUN apt-get update && \
    # installing web-ui dependencies
    apt-get install -y {% for dep in webui.reqs %} {{ dep }}{% endfor %} && \
    # installing nodejs from source
    http://nodejs.org/dist/v0.10.35/node-v0.10.35-linux-x64.tar.gz
    cd /tmp && \
    curl {{ webui.nodejs_latest_url }} -o /tmp/node-latest.tar.gz && \
    tar xvzf node-latest.tar.gz && \
    rm -f node-latest.tar.gz && \
    cd node-v* && \
    ./configure && \
    CXX="g++ -Wno-unused-local-typedefs" make && \
    CXX="g++ -Wno-unused-local-typedefs" make install && \
    cd /tmp && \
    rm -rf /tmp/node-v* && \
    echo '\n# Node.js\nexport PATH="node_modules/.bin:$PATH"' >> /root/.bashrc && \
    # downloading cloudify-webui package and extracting webui and grafana tar.gz
    curl {{ webui.ui_package_url }} --create-dirs -o /opt/tmp/cloudify-webui/cloudify-webui.deb && \
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
