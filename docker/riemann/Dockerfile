FROM debian:jessie
MAINTAINER Gigaspaces, cosmo-admin@gigaspaces.com

COPY NOTICE.txt /root/NOTICE.txt

# Used by 'cfy status' impl to determine if running in container.
ENV VERSION=0.2.6 \
    DOCKER_ENV=True \
    RIEMANN_SERVICE_DIR=/etc/service/riemann
ENV MANAGER_CONFIG_PATH=${RIEMANN_SERVICE_DIR}/manager.config \
    EXTRA_CLASSPATH=${RIEMANN_SERVICE_DIR}/langohr.jar \
    JAVA_HOME=/etc/java \
    PATH=$PATH:/etc/java/bin

COPY manager.config /tmp/manager.config

RUN apt-get update && \
    mkdir -p ${RIEMANN_SERVICE_DIR} && \
    mv /tmp/manager.config ${RIEMANN_SERVICE_DIR} && \
    apt-get install -y curl && \
    curl https://dl.dropboxusercontent.com/u/407576/jre-7-linux-x64.tar.gz --create-dirs -o /opt/tmp/java.tar.gz && \
    mkdir ${JAVA_HOME} && tar -xzvf /opt/tmp/java.tar.gz -C ${JAVA_HOME} --strip=1 && \
    curl https://s3-eu-west-1.amazonaws.com/gigaspaces-repository-eu/langohr/2.11.0/langohr.jar --create-dirs -o ${RIEMANN_SERVICE_DIR}/langohr.jar && \
    chmod 644 ${RIEMANN_SERVICE_DIR}/langohr.jar && \
    curl https://aphyr.com/riemann/riemann_${VERSION}_all.deb --create-dirs -o /opt/tmp/riemann.deb && \
    dpkg -i /opt/tmp/riemann.deb && \
    # download riemann config
    # curl -o ${MANAGER_CONFIG_PATH} https://raw.githubusercontent.com/cloudify-cosmo/cloudify-manager/master/plugins/riemann-controller/riemann_controller/resources/manager.config && \
    rm -rf /var/lib/apt/lists; rm /opt/tmp/*; apt-get remove curl -y; apt-get autoremove -y

VOLUME ${RIEMANN_SERVICE_DIR}

EXPOSE 5556 5555

CMD /usr/bin/riemann -a ${MANAGER_CONFIG_PATH}
