#!/bin/bash

PACKMAN_SHA=""

echo downloading and preparing agent packages

curl http://gigaspaces-repository-eu.s3.amazonaws.com/org/cloudify3/3.2.0/m1-RELEASE/cloudify-ubuntu-precise-agent_3.2.0-m1-b170_amd64.deb --create-dirs -o /opt/tmp/manager/ubuntu_precise_agent.deb && \
curl http://gigaspaces-repository-eu.s3.amazonaws.com/org/cloudify3/3.2.0/m1-RELEASE/cloudify-ubuntu-trusty-agent_3.2.0-m1-b170_amd64.deb --create-dirs -o /opt/tmp/manager/ubuntu_trusty_agent.deb && \
mkdir -p /tmp/Ubuntu-agent/ && \
dpkg-deb -x /opt/tmp/manager/ubuntu_precise_agent.deb /opt/tmp/manager/precise && \
mv /opt/tmp/manager/precise/agents/Ubuntu*/config/Ubuntu-agent-disable-requiretty.sh /tmp/Ubuntu-agent/ && \
mv /opt/tmp/manager/precise/agents/Ubuntu*/config/Ubuntu-celeryd-cloudify.conf.template /tmp/Ubuntu-agent/ && \
mv /opt/tmp/manager/precise/agents/Ubuntu*/config/Ubuntu-celeryd-cloudify.init.template /tmp/Ubuntu-agent/ && \
mv /opt/tmp/manager/precise/agents/Ubuntu*/Ubuntu-precise-agent.tar.gz /tmp/Ubuntu-agent/ && \
dpkg-deb -x /opt/tmp/manager/ubuntu_trusty_agent.deb /opt/tmp/manager/trusty && \
mv /opt/tmp/manager/trusty/agents/Ubuntu*/Ubuntu-trusty-agent.tar.gz /tmp/Ubuntu-agent/

# install ruby
wget ftp://ftp.ruby-lang.org/pub/ruby/1.9/ruby-1.9.3-p547.tar.bz2
tar -xjf ruby-1.9.3-p547.tar.bz2
cd ruby-1.9.3-p547
./configure --disable-install-doc
make
make install
cd ~

# install fpm and configure gem/bundler
gem install fpm --no-ri --no-rdoc
echo -e 'gem: --no-ri --no-rdoc\ninstall: --no-rdoc --no-ri\nupdate:  --no-rdoc --no-ri' >> ~/.gemrc

# install pip
curl --silent --show-error --retry 5 https://bootstrap.pypa.io/get-pip.py | python

# install packman
git clone https://github.com/cloudify-cosmo/packman.git
pushd packman
if [ -n "$PACKMAN_SHA" ]; then
    git reset --hard $PACKMAN_SHA
fi
pip install .
popd

# install virtualenv
pip install virtualenv==1.11.4

# clone custom packager branch containing package config
git clone https://github.com/cloudify-cosmo/cloudify-packager.git
cd cloudify-packager/

pkm pack -c cloudify-ubuntu-agent
