#!/bin/bash


echo downloading and preparing agent packages

curl http://gigaspaces-repository-eu.s3.amazonaws.com/org/cloudify3/3.2.0/rc-RELEASE/cloudify-ubuntu-precise-agent_3.2.0-rc-b179_amd64.deb --create-dirs -o /opt/tmp/manager/ubuntu_precise_agent.deb && \
curl http://gigaspaces-repository-eu.s3.amazonaws.com/org/cloudify3/3.2.0/rc-RELEASE/cloudify-ubuntu-trusty-agent_3.2.0-rc-b179_amd64.deb --create-dirs -o /opt/tmp/manager/ubuntu_trusty_agent.deb && \

mkdir -p /tmp/Ubuntu-agent/ && \
dpkg-deb -x /opt/tmp/manager/ubuntu_precise_agent.deb /opt/tmp/manager/precise && \
mv /opt/tmp/manager/precise/agents/Ubuntu*/config/Ubuntu-agent-disable-requiretty.sh /tmp/Ubuntu-agent/ && \
mv /opt/tmp/manager/precise/agents/Ubuntu*/config/Ubuntu-celeryd-cloudify.conf.template /tmp/Ubuntu-agent/ && \
mv /opt/tmp/manager/precise/agents/Ubuntu*/config/Ubuntu-celeryd-cloudify.init.template /tmp/Ubuntu-agent/ && \
mv /opt/tmp/manager/precise/agents/Ubuntu*/Ubuntu-precise-agent.tar.gz /tmp/Ubuntu-agent/ && \
dpkg-deb -x /opt/tmp/manager/ubuntu_trusty_agent.deb /opt/tmp/manager/trusty && \
mv /opt/tmp/manager/trusty/agents/Ubuntu*/Ubuntu-trusty-agent.tar.gz /tmp/Ubuntu-agent/

# install packman
pip install packman==0.5.0

# clone custom packager branch containing package config
git clone https://github.com/cloudify-cosmo/cloudify-packager.git
cd cloudify-packager/

pkm pack -c cloudify-ubuntu-agent
