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
	echo updating apt cache
	sudo apt-get -y update
	echo installing prerequisites
	sudo apt-get install -y curl vim git gcc python-dev
}

function install_pip
{
	curl --silent --show-error --retry 5 https://bootstrap.pypa.io/get-pip.py | sudo python
}

function create_and_source_virtualenv
{
	cd ~
	echo installing virtualenv
	sudo pip install virtualenv==1.11.4
	echo creating cloudify virtualenv
	virtualenv cloudify
	source cloudify/bin/activate
}

function install_cli
{
	if [ "$INSTALL_FROM_PYPI" = "true" ]; then
		echo installing cli from pypi
		pip install cloudify
	else
		echo installing cli from github
		pip install git+https://github.com/cloudify-cosmo/cloudify-dsl-parser.git@$CORE_TAG_NAME
		pip install git+https://github.com/cloudify-cosmo/flask-securest.git@0.6
		pip install git+https://github.com/cloudify-cosmo/cloudify-rest-client.git@$CORE_TAG_NAME
		pip install git+https://github.com/cloudify-cosmo/cloudify-plugins-common.git@$CORE_TAG_NAME
		pip install git+https://github.com/cloudify-cosmo/cloudify-script-plugin.git@$PLUGINS_TAG_NAME
		pip install git+https://github.com/cloudify-cosmo/cloudify-cli.git@$CORE_TAG_NAME
	fi
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
    sudo curl -O http://cloudify-public-repositories.s3.amazonaws.com/cloudify-manager-blueprints/${CORE_TAG_NAME}/cloudify-manager-blueprints.tar.gz &&
    sudo tar -zxvf cloudify-manager-blueprints.tar.gz &&
    mv cloudify-manager-blueprints-commercial/ cloudify-manager-blueprints
    sudo rm cloudify-manager-blueprints.tar.gz
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
	cd ~/cloudify
	cp cloudify-manager-blueprints/simple/inputs.yaml.template inputs.yaml
	sed -i "s|public_ip: ''|public_ip: \'127.0.0.1\'|g" inputs.yaml
	sed -i "s|private_ip: ''|private_ip: \'127.0.0.1\'|g" inputs.yaml
	sed -i "s|ssh_user: ''|ssh_user: \'${USERNAME}\'|g" inputs.yaml
	sed -i "s|ssh_key_filename: ''|ssh_key_filename: \'~/.ssh/id_rsa\'|g" inputs.yaml
	# configure manager blueprint
	sudo sed -i "s|/cloudify-docker_3|/cloudify-docker-commercial_3|g" cloudify-manager-blueprints/simple/simple-manager-blueprint.yaml
}

function bootstrap
{
	cd ~/cloudify
	echo "bootstrapping..."
	# bootstrap the manager locally
	cfy bootstrap -v -p cloudify-manager-blueprints/simple/simple-manager-blueprint.yaml -i inputs.yaml --install-plugins
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
	echo """
	host_ip: 10.10.1.10
	agent_user: vagrant
	agent_private_key_path: /root/.ssh/id_rsa
	""" > ~/cloudify/blueprints/inputs/nodecellar-singlehost.yaml
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
PLUGINS_TAG_NAME="master"

set_username
install_prereqs
install_pip
create_and_source_virtualenv
install_cli
activate_cfy_bash_completion
init_cfy_workdir
get_manager_blueprints
generate_keys
configure_manager_blueprint_inputs
bootstrap
create_blueprints_and_inputs_dir
configure_nodecellar_blueprint_inputs
