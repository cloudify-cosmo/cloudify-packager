FROM debian:jessie
MAINTAINER Gigaspaces, cosmo-admin@gigaspaces.com

COPY NOTICE.txt /root/NOTICE.txt

# Used by 'cfy status' impl to determine if running in container.
ENV DOCKER_ENV=True \
    NGINX_SERVICE_DIR=/etc/service/nginx \
    NGINX_CONF_FILE=/etc/nginx/nginx.conf \
    NGINX_FILESERVER_DIR=/fileserver
ENV NGINX_LOGS_DIR=${NGINX_SERVICE_DIR}/logs

# copy configuration
COPY default.conf /tmp/default.conf

RUN apt-get update && \
    mkdir -p ${NGINX_SERVICE_DIR} && mkdir -p ${NGINX_FILESERVER_DIR} && mkdir -p ${NGINX_LOGS_DIR} && \
    mv /tmp/default.conf ${NGINX_SERVICE_DIR} && \
    echo "deb http://nginx.org/packages/debian/ squeeze nginx" >> /etc/apt/sources.list && \
    echo "deb-src http://nginx.org/packages/debian/ squeeze nginx" >> /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y curl && \
    curl http://nginx.org/keys/nginx_signing.key --create-dirs -o /opt/tmp/nginx/nginx_signing.key && \
    apt-key add /opt/tmp/nginx/nginx_signing.key && \
    apt-get install -y --force-yes nginx && \
    # turn-off daemon execution, set logging dir and default.conf location in conf file
    echo "daemon off;" >> ${NGINX_CONF_FILE} && \
    sed -i "s|/var/log/nginx/|${NGINX_SERVICE_DIR}/logs/|g" ${NGINX_CONF_FILE} && \
    sed -i "s|/etc/nginx/conf.d/\*.conf|${NGINX_SERVICE_DIR}/default.conf|g" ${NGINX_CONF_FILE} && \
    rm -rf /var/lib/apt/lists; apt-get remove curl -y; apt-get autoremove -y

VOLUME ${NGINX_FILESERVER_DIR}

EXPOSE 80 53229

CMD nginx -c ${NGINX_CONF_FILE}