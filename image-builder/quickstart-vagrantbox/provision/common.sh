#!/bin/bash

# accepted arguments
# $1 = true iff install from PYPI

INSTALL_FROM_PYPI=$1
echo "install from pypi: ${INSTALL_FROM_PYPI}"

CORE_TAG_NAME="master"
PLUGINS_TAG_NAME="master"

USERNAME=$(id -u -n)
if [ "$USERNAME" = "" ]; then
	echo "using default username"
	USERNAME="vagrant"
fi

echo "username is [$USERNAME]"

echo bootstrapping...

# update
echo updating apt cache
sudo apt-get -y update

# install prereqs
echo installing prerequisites
sudo apt-get install -y curl vim git gcc python-dev

# install pip
curl --silent --show-error --retry 5 https://bootstrap.pypa.io/get-pip.py | sudo python

# go home
cd ~

# virtualenv
echo installing virtualenv
sudo pip install virtualenv==1.11.4
echo creating cloudify virtualenv
virtualenv cloudify
source cloudify/bin/activate

# install cli
if [ "$INSTALL_FROM_PYPI" = "true" ]; then
	echo installing cli from pypi
	pip install cloudify
else
	echo installing cli from github
	pip install git+https://github.com/cloudify-cosmo/cloudify-dsl-parser.git@$CORE_TAG_NAME
	pip install git+https://github.com/cloudify-cosmo/flask-securest.git@master
	pip install git+https://github.com/cloudify-cosmo/cloudify-rest-client.git@$CORE_TAG_NAME
	pip install git+https://github.com/cloudify-cosmo/cloudify-plugins-common.git@$CORE_TAG_NAME	
	pip install git+https://github.com/cloudify-cosmo/cloudify-script-plugin.git@$PLUGINS_TAG_NAME
	pip install git+https://github.com/cloudify-cosmo/cloudify-cli.git@$CORE_TAG_NAME
fi

# add cfy bash completion
activate_cfy_bash_completion

# init cfy work dir
cd ~
mkdir -p cloudify
cd cloudify
cfy init

# clone manager blueprints
git clone https://github.com/cloudify-cosmo/cloudify-manager-blueprints.git
pushd cloudify-manager-blueprints
	git checkout -b tmp_branch $CORE_TAG_NAME
  	git --no-pager log -1
popd

# generate public/private key pair and add to authorized_keys
ssh-keygen -t rsa -f ~/.ssh/id_rsa -q -N ''
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys

# configure inputs
cp cloudify-manager-blueprints/simple/inputs.yaml.template inputs.yaml
sed -i "s|public_ip: ''|public_ip: \'127.0.0.1\'|g" inputs.yaml
sed -i "s|private_ip: ''|private_ip: \'127.0.0.1\'|g" inputs.yaml
sed -i "s|ssh_user: ''|ssh_user: \'${USERNAME}\'|g" inputs.yaml
sed -i "s|ssh_key_filename: ''|ssh_key_filename: \'~/.ssh/id_rsa\'|g" inputs.yaml

# bootstrap the manager locally
cfy bootstrap -v -p cloudify-manager-blueprints/simple/simple-manager-blueprint.yaml -i inputs.yaml --install-plugins
if [ "$?" -ne "0" ]; then
  echo "Bootstrap failed, stoping provision."
  exit 1
fi

# create blueprints and inputs dir
mkdir -p ~/cloudify/blueprints/inputs

# create inputs.yaml for the nodecellar blueprint
echo """
host_ip: 10.10.1.10
agent_user: vagrant
agent_private_key_path: /root/.ssh/id_rsa
""" > ~/cloudify/blueprints/inputs/nodecellar-singlehost.yaml

# source virtualenv on login
echo "source /home/${USERNAME}/cloudify/bin/activate" >> /home/${USERNAME}/.bashrc

# set shell login base dir
echo "cd ~/cloudify" >> /home/${USERNAME}/.bashrc

echo bootstrap done.
