FROM debian:jessie
MAINTAINER Gigaspaces, cosmo-admin@gigaspaces.com

# Used by 'cfy status' impl to determine if running in container.
ENV DOCKER_ENV True
# LICENSE
COPY NOTICE.txt /root/NOTICE.txt

# ------------------------------------------------------------------------------------------------------------------------------------------ #
# INSTALL - RABBITMQ, DependsOn: ~
# ------------------------------------------------------------------------------------------------------------------------------------------ #
ENV RABBITMQ_SERVICE_NAME rabbitmq-server
ENV RABBITMQ_SERVICE_DIR /etc/service/$RABBITMQ_SERVICE_NAME
ENV RABBITMQ_RUN_FILE $RABBITMQ_SERVICE_DIR/run

RUN apt-get update && \
    # installing rabbitmq dependencies
    apt-get install -y curl logrotate erlang-nox && \
    # installing rabbitmq-server and setting its properties
    apt-get -y install rabbitmq-server && \
    rabbitmq-plugins enable rabbitmq_management && \
    rabbitmq-plugins enable rabbitmq_tracing && \
    # cleanup
    # remove curl
    apt-get remove curl -y && \
    apt-get autoremove -y

EXPOSE 5672 15672 4369

CMD rabbitmq-server


# ALT IMPLEMENTATION
# https://github.com/mikaelhg/docker-rabbitmq/blob/master/Dockerfile