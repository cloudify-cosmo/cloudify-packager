FROM debian:jessie
MAINTAINER Gigaspaces, cosmo-admin@gigaspaces.com

ENV DOCKER_ENV=True

RUN echo "deb http://nginx.org/packages/ubuntu/ trusty nginx" >> /etc/apt/sources.list.d/nginx.list && \
    apt-key adv --fetch-keys http://nginx.org/keys/nginx_signing.key && \
    apt-get update && \
    apt-get install -y --no-install-recommends nginx && \
    rm /etc/nginx/sites-enabled/* \
    rm -rf /var/lib/apt/lists && \
    apt-get autoremove -y

COPY nginx/default.conf /etc/nginx/conf.d/

EXPOSE 80 53229

CMD nginx -c /etc/nginx/nginx.conf -g "daemon off;"