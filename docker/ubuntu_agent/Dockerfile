FROM ubuntu:12.04
MAINTAINER adaml, adaml@gigaspaces.com

# update and install dependencies
RUN apt-get -y update && \
    apt-get install -y python-software-properties && \
    add-apt-repository -y ppa:git-core/ppa && \
    apt-get install -y curl wget sudo python-dev bzip2 ruby rpm git make gcc libyaml-dev

ADD scripts/ /scripts

RUN cd /scripts && \
    chmod +x install_packman.sh && \
    /bin/bash -c 'source install_packman.sh'
    
