FROM debian:jessie
MAINTAINER Gigaspaces, cosmo-admin@gigaspaces.com
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# INSTALL - BASE
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# add utility functions
COPY utils/ /opt/tmp/utils/
COPY NOTICE.txt /root/NOTICE.txt
# Used by 'cfy status' impl to determine if running in container.
ENV DOCKER_ENV True

# ------------------------------------------------------------------------------------------------------------------------------------------ #
# INSTALL - RIEMANN
# ------------------------------------------------------------------------------------------------------------------------------------------ #
##### ENV #####
ENV RIEMANN_SERVICE_NAME=riemann
ENV RIEMANN_SERVICE_DIR=/etc/service/$RIEMANN_SERVICE_NAME
ENV RIEMANN_RUN_FILE=$RIEMANN_SERVICE_DIR/run \
    MANAGER_CONFIG_PATH=$RIEMANN_SERVICE_DIR/manager.config \
    EXTRA_CLASSPATH=$RIEMANN_SERVICE_DIR/langohr.jar

# add run scripts and configuration
COPY riemann/ $RIEMANN_SERVICE_DIR/

RUN apt-get update && \
    # installing riemann dependencies
    apt-get install -y curl && \
    curl https://dl.dropboxusercontent.com/u/407576/jre-7-linux-x64.tar.gz --create-dirs -o /opt/tmp/java/java.tar.gz && \
    mkdir /etc/java && \
    tar -xzvf /opt/tmp/java/java.tar.gz -C /etc/java --strip=1 && \
    rm /opt/tmp/java/java.tar.gz && \
    # downloading jar to service dir and setting permissions on langohr jar
    curl https://s3-eu-west-1.amazonaws.com/gigaspaces-repository-eu/langohr/2.11.0/langohr.jar --create-dirs -o $RIEMANN_SERVICE_DIR/langohr.jar && \
    chmod 644 $RIEMANN_SERVICE_DIR/langohr.jar && \
    # downloading and installing riemann deb
    curl https://aphyr.com/riemann/riemann_0.2.6_all.deb --create-dirs -o /opt/tmp/riemann/riemann.deb && \
    dpkg -i /opt/tmp/riemann/riemann.deb && \
    rm -rf /opt/tmp/riemann/riemann.deb && \
    # download riemann config
    curl -o $MANAGER_CONFIG_PATH https://raw.githubusercontent.com/cloudify-cosmo/cloudify-manager/master/plugins/riemann-controller/riemann_controller/resources/manager.config
    # sed -i "s|RABBITMQ_ADDR|$RABBITMQ_PORT_5672_TCP_ADDR|g" $MANAGER_CONFIG_PATH

# riemann persistence path
# VOLUME /etc/service/riemann

EXPOSE 5556
EXPOSE 5555

# run riemann service
CMD /usr/bin/riemann -a $MANAGER_CONFIG_PATH