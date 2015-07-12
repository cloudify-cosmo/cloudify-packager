#!/bin/bash -e


echo downloading and preparing agent packages

curl http://s3.amazonaws.com/adaml_docker/cloudify-redhat-santiago-agent_3.1.0_i686.deb --create-dirs -o /opt/tmp/manager/redhat_santiago_agent.deb && \
curl https://s3.amazonaws.com/adaml_docker/cloudify-redhat-maipo-agent_3.1.0_amd64.deb --create-dirs -o /opt/tmp/manager/redhat_maipo_agent.deb && \

mkdir -p /tmp/redhat-agent/ && \
dpkg-deb -x /opt/tmp/manager/redhat_santiago_agent.deb /opt/tmp/manager/santiago && \
mv /opt/tmp/manager/santiago/agents/redhat-agent/config/redhat-agent-disable-requiretty.sh /tmp/redhat-agent/ && \
mv /opt/tmp/manager/santiago/agents/redhat-agent/config/redhat-celeryd-cloudify.conf.template /tmp/redhat-agent/ && \
mv /opt/tmp/manager/santiago/agents/redhat-agent/config/redhat-celeryd-cloudify.init.template /tmp/redhat-agent/ && \
mv /opt/tmp/manager/santiago/agents/redhat-agent/redhat-Santiago-agent.tar.gz /tmp/redhat-agent/ && \
dpkg-deb -x /opt/tmp/manager/redhat_maipo_agent.deb /opt/tmp/manager/maipo && \
mv /opt/tmp/manager/maipo/agents/redhat-agent/redhat-Maipo-agent.tar.gz /tmp/redhat-agent/

# install packman
pip install git+git://github.com/cloudify-cosmo/packman.git@CFY-2798-rhel-agent

# clone custom packager branch containing package config
git clone https://github.com/cloudify-cosmo/cloudify-packager.git
cd cloudify-packager/
git checkout CFY-2596-centos7-agent

pkm pack -c cloudify-redhat-agent
