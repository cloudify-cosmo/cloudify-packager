#!/bin/bash

REST_CLIENT_SHA=""
COMMON_PLUGIN_SHA=""
MANAGER_SHA=""
PACKMAN_SHA=""
SCRIPTS_PLUGIN_SHA=""
DIAMOND_PLUGIN_SHA=""

echo bootstrapping...

# update and install prereqs
sudo yum -y update &&
sudo yum install yum-downloadonly wget mlocate yum-utils python-devel libyaml-devel ruby rubygems ruby-devel -y

# install fpm
sudo gem install fpm --no-rdoc --no-ri

# install pip
sudo wget https://raw.github.com/pypa/pip/master/contrib/get-pip.py &&
sudo /usr/bin/python get-pip.py &&

# install packman
git clone https://github.com/cloudify-cosmo/packman.git
pushd packman
	if [ -n "$PACKMAN_SHA" ]; then
		git reset --hard $PACKMAN_SHA
	fi
	sudo pip install .
popd


# install virtualenv
sudo pip install virtualenv==1.11.4 &&

cd /cloudify-packager/ &&

echo '# create package resources'
sudo pkm get -c centos-agent

echo '# GET PROCESS'
sudo /centos-agent/env/bin/pip install celery==3.0.24
sudo /centos-agent/env/bin/pip install pyzmq==14.3.1
sudo git clone https://github.com/cloudify-cosmo/cloudify-rest-client.git
pushd cloudify-rest-client
	if [ -n "$REST_CLIENT_SHA" ]; then
		git reset --hard $REST_CLIENT_SHA
	fi
	sudo /centos-agent/env/bin/pip install .
popd
sudo git clone https://github.com/cloudify-cosmo/cloudify-plugins-common.git
pushd cloudify-plugins-common
	if [ -n "$COMMON_PLUGIN_SHA" ]; then
		git reset --hard $COMMON_PLUGIN_SHA
	fi
	sudo /centos-agent/env/bin/pip install .
popd
sudo git clone https://github.com/cloudify-cosmo/cloudify-script-plugin.git
pushd cloudify-script-plugin
	if [ -n "$SCRIPTS_PLUGIN_SHA" ]; then
		git reset --hard $SCRIPTS_PLUGIN_SHA
	fi
	sudo /centos-agent/env/bin/pip install .
popd
sudo git clone https://github.com/cloudify-cosmo/cloudify-diamond-plugin.git
pushd cloudify-diamond-plugin
	if [ -n "$DIAMOND_PLUGIN_SHA" ]; then
		git reset --hard $DIAMOND_PLUGIN_SHA
	fi
	sudo /centos-agent/env/bin/pip install .
popd
sudo git clone https://github.com/cloudify-cosmo/cloudify-manager.git
pushd cloudify-manager
	if [ -n "$MANAGER_SHA" ]; then
		git reset --hard $MANAGER_SHA
	fi
	pushd plugins/plugin-installer
	  sudo /centos-agent/env/bin/pip install .
	popd
	pushd plugins/agent-installer
	  sudo /centos-agent/env/bin/pip install .
	popd
	pushd plugins/windows-agent-installer
	  sudo /centos-agent/env/bin/pip install .
	popd
	pushd plugins/windows-plugin-installer
	  sudo /centos-agent/env/bin/pip install .
	popd
popd


# create package
sudo pkm pack -c centos-agent
sudo pkm pack -c cloudify-centos-agent

echo bootstrap done
echo NOTE: currently, using some of the packman's features requires that it's run as sudo.
