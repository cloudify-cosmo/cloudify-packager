FROM phusion/baseimage:0.9.15
MAINTAINER Cloudify, cosmo-admin@gigaspaces.com
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# INSTALL - BASE
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# add utility functions
ADD ../utils/ /opt/tmp/utils/
ADD NOTICE.txt /root/license
# Used by 'cfy status' impl to determine if running in container.
ENV DOCKER_ENV True

RUN apt-get update
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# INSTALL - NGINX
# ------------------------------------------------------------------------------------------------------------------------------------------ #
##### ENV #####
# set nginx service name
ENV NGINX_SERVICE_NAME nginx
ENV NGINX_SERVICE_DIR /etc/service/$NGINX_SERVICE_NAME
# nginx default conf file path
ENV NGINX_CONF_FILE /etc/nginx/nginx.conf
ENV NGINX_RUN_FILE $NGINX_SERVICE_DIR/run
ENV NGINX_LOGS_DIR $NGINX_SERVICE_DIR/logs
##### ENV #####
# add run scripts and configuration
ADD nginx/ $NGINX_SERVICE_DIR

RUN echo adding nginx repositories to sources.list file and update repo && \
    echo ['deb http://nginx.org/packages/mainline/ubuntu/ precise nginx', 'deb-src http://nginx.org/packages/mainline/ubuntu/ precise nginx'] | tr -d "'["| tr ',]' '\n' >> /etc/apt/sources.list && \
    apt-get update && \
    \
    echo installing nginx dependencies && \
    apt-get install -y  curl && \
    \
    echo download and add signing key && \
    curl http://nginx.org/keys/nginx_signing.key --create-dirs -o /opt/tmp/nginx/nginx_signing.key && \
    apt-key add /opt/tmp/nginx/nginx_signing.key && \
    \
    echo installing nginx && \
    apt-get install -y --force-yes $NGINX_SERVICE_NAME

# turn-off daemon execution, set logging dir and default.conf location in conf file
RUN echo "daemon off;" >> $NGINX_CONF_FILE && \
    sed -i "s%/var/log/nginx/error.log warn%$NGINX_SERVICE_DIR/logs/error.log warn%g" $NGINX_CONF_FILE && \
    sed -i "s%/var/run/nginx.pid%$NGINX_SERVICE_DIR/logs/nginx.pid%g" $NGINX_CONF_FILE && \
    sed -i "s%/etc/nginx/conf.d/\*.conf%$NGINX_SERVICE_DIR/default.conf%g" $NGINX_CONF_FILE && \
    mkdir -p $NGINX_LOGS_DIR && \
    \
    echo setting config path in run file && \
    sed -i '1s|^|NGINX_CONF_FILE='$NGINX_CONF_FILE' \n|' $NGINX_RUN_FILE && \
    sed -i '1s|^|#!/bin/bash \n|' $NGINX_RUN_FILE && \
    chmod +x $NGINX_RUN_FILE