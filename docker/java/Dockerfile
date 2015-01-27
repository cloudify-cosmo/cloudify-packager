FROM debian:jessie
MAINTAINER cosmo-admin, cosmo-admin@gigaspaces.com

COPY NOTICE.txt /root/NOTICE.txt

ENV VERSION=7 \
    DOCKER_ENV=True \
    JAVA_HOME=/etc/java

RUN apt-get update && \
    apt-get install -y curl && \
    # currently in dropbox. need to upload the jre tar to s3
    curl https://dl.dropboxusercontent.com/u/407576/jre-${VERSION}-linux-x64.tar.gz --create-dirs -o /opt/tmp/java.tar.gz && \
    mkdir ${JAVA_HOME} && tar -xzvf /opt/tmp/java.tar.gz -C ${JAVA_HOME} --strip=1 && \
    rm -rf /var/lib/apt/lists; rm /opt/tmp/*; apt-get remove curl -y; apt-get autoremove -y