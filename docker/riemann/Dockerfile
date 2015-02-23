FROM docker_javabase:latest
MAINTAINER Gigaspaces, cosmo-admin@gigaspaces.com

COPY RIEMANN_NOTICE.txt /root/RIEMANN_NOTICE.txt

ENV RIEMANN_VERSION=0.2.6 \
    DOCKER_ENV=True \
    RIEMANN_SERVICE_DIR=/etc/service/riemann \
    PATH=$PATH:/opt/java/bin \
    # this is the host name, as seen in /etc/hosts, for the restservice container`
    # Riemann's config reads this env var to direct calls to the rest service.
    MANAGEMENT_IP='frontend' \
    RABBITMQ_HOST='rabbitmq'
ENV RIEMANN_CONFIG_PATH=${RIEMANN_SERVICE_DIR}/manager.config \
    RIEMANN_LOG_PATH=${RIEMANN_SERVICE_DIR}/logs/riemann.log \
    EXTRA_CLASSPATH=${RIEMANN_SERVICE_DIR}/langohr.jar

RUN apt-get update && \
    mkdir -p ${RIEMANN_SERVICE_DIR}/logs && \
    apt-get install -y curl && \
    curl --fail https://s3-eu-west-1.amazonaws.com/gigaspaces-repository-eu/langohr/2.11.0/langohr.jar --create-dirs -o ${RIEMANN_SERVICE_DIR}/langohr.jar && \
    chmod 644 ${RIEMANN_SERVICE_DIR}/langohr.jar && \
    curl --fail https://aphyr.com/riemann/riemann_${RIEMANN_VERSION}_all.deb --create-dirs -o /tmp/riemann.deb && \
    dpkg -i /tmp/riemann.deb && \
    # TODO: use this instead of the one below it
    # curl -o ${RIEMANN_CONFIG_PATH} https://raw.githubusercontent.com/cloudify-cosmo/cloudify-manager/master/plugins/riemann-controller/riemann_controller/resources/manager.config && \
    curl --fail -o ${RIEMANN_CONFIG_PATH} https://raw.githubusercontent.com/cloudify-cosmo/cloudify-manager/CFY-2173-configure-riemann-for-external-hosts/plugins/riemann-controller/riemann_controller/resources/manager.config && \
    rm -rf /var/lib/apt/lists && \
    rm /tmp/* && \
    apt-get purge curl -y && \
    apt-get autoremove -y

VOLUME ${RIEMANN_SERVICE_DIR}

CMD /usr/bin/riemann -a ${RIEMANN_CONFIG_PATH}
