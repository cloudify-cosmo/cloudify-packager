#!/bin/bash

REST_CLIENT_SHA=""
COMMON_PLUGIN_SHA=""
MANAGER_SHA=""
PACKMAN_SHA=""
SCRIPTS_PLUGIN_SHA=""

echo bootstrapping...

# update and install prereqs
sudo yum -y update &&
sudo yum install yum-downloadonly wget mlocate yum-utils python-devel libyaml-devel ruby rubygems ruby-devel -y

# install python and additions
# http://bicofino.io/blog/2014/01/16/installing-python-2-dot-7-6-on-centos-6-dot-5/
sudo yum groupinstall -y 'development tools'
sudo yum install -y zlib-devel bzip2-devel openssl-devel xz-libs
sudo mkdir /py27
cd /py27
sudo wget http://www.python.org/ftp/python/2.7.6/Python-2.7.6.tar.xz
sudo xz -d Python-2.7.6.tar.xz
sudo tar -xvf Python-2.7.6.tar
cd Python-2.7.6
sudo ./configure --prefix=/usr
sudo make
sudo make altinstall

# install fpm
sudo gem install fpm --no-rdoc --no-ri

# install pip
cd /py27
sudo wget https://raw.github.com/pypa/pip/master/contrib/get-pip.py &&
sudo /usr/bin/python2.7 get-pip.py &&

# install packman
#sudo /usr/bin/pip2.7 install https://github.com/cloudify-cosmo/packman/archive/develop.tar.gz
git clone https://github.com/cloudify-cosmo/packman.git
pushd packman
	if [ -n "$PACKMAN_SHA" ]; then
		git reset --hard $PACKMAN_SHA
	fi
	pip install .
popd


# install virtualenv
sudo pip install virtualenv==1.11.4 &&

cd /cloudify-packager/ &&

echo '# create package resources'
sudo pkm get -c centos-agent

echo '# GET PROCESS'
/centos-agent/env/bin/pip install celery==3.0.24
/centos-agent/env/bin/pip install pyzmq==14.3.1
git clone https://github.com/cloudify-cosmo/cloudify-rest-client.git
pushd cloudify-rest-client
	if [ -n "$REST_CLIENT_SHA" ]; then
		git reset --hard $REST_CLIENT_SHA
	fi
	/centos-agent/env/bin/pip install .
popd
git clone https://github.com/cloudify-cosmo/cloudify-plugins-common.git
pushd cloudify-plugins-common
	if [ -n "$COMMON_PLUGIN_SHA" ]; then
		git reset --hard $COMMON_PLUGIN_SHA
	fi
	/centos-agent/env/bin/pip install .
popd
git clone https://github.com/cloudify-cosmo/cloudify-script-plugin.git
pushd cloudify-script-plugin
	if [ -n "$SCRIPTS_PLUGIN_SHA" ]; then
		git reset --hard $SCRIPTS_PLUGIN_SHA
	fi
	/centos-agent/env/bin/pip install .
popd
git clone https://github.com/cloudify-cosmo/cloudify-manager.git
pushd cloudify-manager
	if [ -n "$MANAGER_SHA" ]; then
		git reset --hard $MANAGER_SHA
	fi
	pushd plugins/plugin-installer
	  /centos-agent/env/bin/pip install .
	popd
	pushd plugins/agent-installer
	  /centos-agent/env/bin/pip install .
	popd
	pushd plugins/windows-agent-installer
	  /centos-agent/env/bin/pip install .
	popd
	pushd plugins/windows-plugin-installer
	  /centos-agent/env/bin/pip install .
	popd
popd


# create package
sudo pkm pack -c centos-agent
sudo pkm pack -c cloudify-centos-agent

echo bootstrap done
echo NOTE: currently, using some of the packman's features requires that it's run as sudo.
