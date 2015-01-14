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
    mkdir -p ${NGINX_SERVICE_DIR} && \
    mv /tmp/default.conf ${NGINX_SERVICE_DIR} && \
    mkdir -p ${NGINX_FILESERVER_DIR} && \
    # adding nginx repositories to sources.list file and update repo
    echo "deb http://nginx.org/packages/debian/ squeeze nginx" >> /etc/apt/sources.list && \
    echo "deb-src http://nginx.org/packages/debian/ squeeze nginx" >> /etc/apt/sources.list && \
    apt-get update && \
    # installing nginx dependencies
    apt-get install -y curl && \
    # download and add signing key
    curl http://nginx.org/keys/nginx_signing.key --create-dirs -o /opt/tmp/nginx/nginx_signing.key && \
    apt-key add /opt/tmp/nginx/nginx_signing.key && \
    # installing nginx
    apt-get install -y --force-yes nginx && \
    # turn-off daemon execution, set logging dir and default.conf location in conf file
    echo "daemon off;" >> ${NGINX_CONF_FILE} && \
    sed -i "s|/var/log/nginx/|${NGINX_SERVICE_DIR}/logs/|g" ${NGINX_CONF_FILE} && \
    sed -i "s|/etc/nginx/conf.d/\*.conf|${NGINX_SERVICE_DIR}/default.conf|g" ${NGINX_CONF_FILE} && \
    mkdir -p ${NGINX_LOGS_DIR} && \
    rm -rf /var/lib/apt/lists; apt-get remove curl -y; apt-get autoremove -y

EXPOSE 80 53229

CMD nginx -c ${NGINX_CONF_FILE}