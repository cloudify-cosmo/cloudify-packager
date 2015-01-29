FROM debian:jessie
MAINTAINER Gigaspaces, cosmo-admin@gigaspaces.com

COPY JAVABASE_NOTICE.txt /root/JAVABASE_NOTICE.txt

ENV JAVABASE_VERSION=7 \
    DOCKER_ENV=True \
    JAVA_HOME=/etc/java

RUN apt-get update && \
    apt-get install -y curl && \
    # currently in dropbox. need to upload the jre tar to s3
    curl https://dl.dropboxusercontent.com/u/407576/jre-${JAVABASE_VERSION}-linux-x64.tar.gz --create-dirs -o /opt/tmp/java.tar.gz && \
    mkdir ${JAVA_HOME} && tar -xzvf /opt/tmp/java.tar.gz -C ${JAVA_HOME} --strip=1 && \
    rm -rf /var/lib/apt/lists; rm /opt/tmp/*; apt-get purge curl -y; apt-get autoremove -y