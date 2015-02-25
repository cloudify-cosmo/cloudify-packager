FROM adamlavie/packager_base:latest
MAINTAINER adaml, adaml@gigaspaces.com

ADD scripts/ /scripts

RUN cd /scripts && \
    chmod +x install_packman.sh && \
    /bin/bash -c 'source install_packman.sh'
    
