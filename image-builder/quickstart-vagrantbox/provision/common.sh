#!/bin/bash

# accepted arguments
# $1 = true iff install from PYPI

function set_username
{
	USERNAME=$(id -u -n)
	if [ "$USERNAME" = "" ]; then
		echo "using default username"
		USERNAME="vagrant"
	fi
	echo "username is [$USERNAME]"
}

function install_prereqs
{
	echo installing prerequisites
	sudo yum install -y git gcc python-devel
}

function install_pip
{
	curl --silent --show-error --retry 5 https://bootstrap.pypa.io/get-pip.py | sudo python
}

function create_and_source_virtualenv
{
	cd ~
	echo installing virtualenv
	sudo pip install virtualenv
	echo creating cloudify virtualenv
	virtualenv cloudify
	source cloudify/bin/activate
}

function install_cli
{
	pip install https://github.com/cloudify-cosmo/cloudify-cli/archive/${CORE_TAG_NAME}.zip \
	  -r https://raw.githubusercontent.com/cloudify-cosmo/cloudify-cli/${CORE_TAG_NAME}/dev-requirements.txt

}

function init_cfy_workdir
{
	cd ~
	mkdir -p cloudify
	cd cloudify
	cfy init
}

function get_manager_blueprints
{
    cd ~/cloudify
	echo "Retrieving Manager Blueprints"
    sudo curl -OL https://github.com/cloudify-cosmo/cloudify-manager-blueprints/archive/${CORE_TAG_NAME}.tar.gz &&
    sudo tar -zxvf ${CORE_TAG_NAME}.tar.gz &&
    mv cloudify-manager-blueprints-*/ cloudify-manager-blueprints
    sudo rm ${CORE_TAG_NAME}.tar.gz
}

function generate_keys
{
	# generate public/private key pair and add to authorized_keys
	ssh-keygen -t rsa -f ~/.ssh/id_rsa -q -N ''
	cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys

}

function configure_manager_blueprint_inputs
{
	# configure inputs
	echo "public_ip: '127.0.0.1'" >> inputs.yaml
	echo "private_ip: '127.0.0.1'" >> inputs.yaml
	echo "ssh_user: '${USERNAME}'" >> inputs.yaml
	echo "ssh_key_filename: '~/.ssh/id_rsa'" >> inputs.yaml
}

function bootstrap
{
	cd ~/cloudify
	echo "bootstrapping..."
	# bootstrap the manager locally
	cfy bootstrap -v -p cloudify-manager-blueprints/new/simple-manager-blueprint.yaml -i inputs.yaml --install-plugins
	if [ "$?" -ne "0" ]; then
	  echo "Bootstrap failed, stoping provision."
	  exit 1
	fi
	echo "bootstrap done."
}

function create_blueprints_and_inputs_dir
{
	mkdir -p ~/cloudify/blueprints/inputs
}

function configure_nodecellar_blueprint_inputs
{
echo '
host_ip: 10.10.1.10
agent_user: vagrant
agent_private_key_path: /root/.ssh/id_rsa
' >> ~/cloudify/blueprints/inputs/nodecellar-singlehost.yaml
}

function configure_shell_login
{
	# source virtualenv on login
	echo "source /home/${USERNAME}/cloudify/bin/activate" >> /home/${USERNAME}/.bashrc

	# set shell login base dir
	echo "cd ~/cloudify" >> /home/${USERNAME}/.bashrc
}

INSTALL_FROM_PYPI=$1
echo "Install from PyPI: ${INSTALL_FROM_PYPI}"
CORE_TAG_NAME="master"

set_username
install_prereqs
install_pip
create_and_source_virtualenv
install_cli
init_cfy_workdir
get_manager_blueprints
generate_keys
configure_manager_blueprint_inputs
bootstrap
create_blueprints_and_inputs_dir
configure_nodecellar_blueprint_inputs
configure_shell_login
