#!/bin/bash


echo downloading and preparing agent packages

curl http://gigaspaces-repository-eu.s3.amazonaws.com/org/cloudify3/3.2.1/ga-RELEASE/cloudify-centos-final-agent_3.2.1-ga-b212_amd64.deb --create-dirs -o /opt/tmp/manager/centos_final_agent.deb && \
curl http://gigaspaces-repository-eu.s3.amazonaws.com/org/cloudify3/3.2.1/ga-RELEASE/cloudify-centos-core-agent_3.2.1-ga-b212_amd64.deb --create-dirs -o /opt/tmp/manager/centos_core_agent.deb && \

mkdir -p /tmp/centos-agent/ && \
dpkg-deb -x /opt/tmp/manager/centos_final_agent.deb /opt/tmp/manager/final && \
mv /opt/tmp/manager/final/agents/centos-agent/config/centos-agent-disable-requiretty.sh /tmp/centos-agent/ && \
mv /opt/tmp/manager/final/agents/centos-agent/config/centos-celeryd-cloudify.conf.template /tmp/centos-agent/ && \
mv /opt/tmp/manager/final/agents/centos-agent/config/centos-celeryd-cloudify.init.template /tmp/centos-agent/ && \
mv /opt/tmp/manager/final/agents/centos-agent/centos-Final-agent.tar.gz /tmp/centos-agent/ && \
dpkg-deb -x /opt/tmp/manager/centos_core_agent.deb /opt/tmp/manager/core && \
mv /opt/tmp/manager/core/agents/centos-agent/centos-Core-agent.tar.gz /tmp/centos-agent/

# install packman
pip install packman==0.5.0

# clone custom packager branch containing package config
git clone https://github.com/cloudify-cosmo/cloudify-packager.git
cd cloudify-packager/

pkm pack -c cloudify-centos-agent
