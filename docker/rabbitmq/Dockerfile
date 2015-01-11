FROM debian:jessie
MAINTAINER Gigaspaces, cosmo-admin@gigaspaces.com

COPY NOTICE.txt /root/NOTICE.txt

# Used by 'cfy status' impl to determine if running in container.
ENV DOCKER_ENV=True
    RABBITMQ_SERVICE_NAME=rabbitmq-server
ENV RABBITMQ_SERVICE_DIR=/etc/service/$RABBITMQ_SERVICE_NAME
ENV RABBITMQ_RUN_FILE= $RABBITMQ_SERVICE_DIR/run

RUN apt-get update && \
    apt-get install -y logrotate erlang-nox && \
    apt-get -y install rabbitmq-server && \
    rabbitmq-plugins enable rabbitmq_management && \
    rabbitmq-plugins enable rabbitmq_tracing && \
    # enable guest user to access cluster not on localhost
    echo "[{rabbit, [{loopback_users, []}]}]." > /etc/rabbitmq/rabbitmq.config
    # cleanup
    rm -rf /var/lib/apt/lists && apt-get remove curl -y && apt-get autoremove -y

EXPOSE 5672 15672 4369

CMD rabbitmq-server