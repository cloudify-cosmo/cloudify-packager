#!/usr/bin/env bash

function state_error
{
	echo "ERROR: ${1:-UNKNOWN} (status $?)" 1>&2
	exit 1
}

function check_pkg
{
	echo "checking to see if package $1 is installed..."
	dpkg -s $1 || state_error "package $1 is not installed"
	echo "package $1 is installed"
}

function check_user
{
	echo "checking to see if user $1 exists..."
	id -u $1 || state_error "user $1 doesn't exists"
	echo "user $1 exists"
}

function check_port
{
	echo "checking to see if port $1 is opened..."
	nc -z $1 $2 || state_error "port $2 is closed"
	echo "port $2 on $1 is opened"
}

function check_dir
{
	echo "checking to see if dir $1 exists..."
	if [ -d $1 ]; then
		echo "dir $1 exists"
	else
		state_error "dir $1 doesn't exist"
	fi
}

function check_file
{
	echo "checking to see if file $1 exists..."
	if [ -f $1 ]; then
		echo "file $1 exists"
		# if [ -$2 $1 ]; then
			# echo "$1 exists and contains the right attribs"
		# else
			# state_error "$1 exists but does not contain the right attribs"
		# fi
	else
		state_error "file $1 doesn't exists"
	fi
}

function check_upstart
{
	echo "checking to see if $1 daemon is running..."
	sudo status $1 || state_error "daemon $1 is not running"
	echo "daemon $1 is running"
}

function check_service
{
    echo "checking to see if $1 service is running..."
    sudo service $1 status || state_error "service $1 is not running"
    echo "service $1 is running"
}


PKG_NAME="manager"
PKG_DIR="/opt/manager"
BOOTSTRAP_LOG="/var/log/cloudify3-bootstrap.log"

BASE_DIR="/opt"
HOME_DIR="${BASE_DIR}/${PKG_NAME}"

LOG_DIR="/var/log/cosmo"

PKG_INIT_DIR="${PKG_DIR}/config/init"
INIT_DIR="/etc/init"
# INIT_FILE=""

PKG_CONF_DIR="${PKG_DIR}/config/conf"
CONF_DIR=""
CONF_FILE="guni.conf"


echo "creating file server dir..."
sudo mkdir -p ${PKG_DIR}/filesrv
check_dir "${PKG_DIR}/filesrv"

echo "copying some stuff..."
sudo cp -R ${PKG_DIR}/cosmo-manager-*/orchestrator/src/main/resources/cloudify/ ${PKG_DIR}/filesrv/
sudo cp ${PKG_DIR}/cosmo-manager-*/orchestrator/src/main/resources/org/cloudifysource/cosmo/dsl/alias-mappings.yaml ${PKG_DIR}/filesrv/cloudify/

# echo "running gunicorn..."
# sudo ${PKG_DIR}/bin/gunicorn -w 1 -b 0.0.0.0:8100 --timeout 300 ${PKG_DIR}/cosmo-manager-develop/manager-rest/manager_rest/server.py:app

# use this to test...
# sudo mkdir -p /opt/manager/filesrv
# sudo cp -R /opt/manager/cosmo-manager-develop/orchestrator/src/main/resources/cloudify/ /opt/manager/filesrv/
# sudo cp /opt/manager/cosmo-manager-develop/orchestrator/src/main/resources/org/cloudifysource/cosmo/dsl/alias-mappings.yaml /opt/manager/filesrv/cloudify/
# cd /opt/manager/cosmo-manager-develop/manager-rest/manager_rest
# sudo /opt/manager/bin/gunicorn -w 1 -b 0.0.0.0:8100 --timeout 300 server:app

echo "creating workflow log dir..."
sudo mkdir -p ${LOG_DIR}
check_dir "${LOG_DIR}"

echo "moving some stuff aorund..."
sudo cp ${PKG_INIT_DIR}/*.conf ${INIT_DIR}
# sudo cp ${PKG_CONF_DIR}/guni.conf ${PKG_DIR}

check_file "${INIT_DIR}/manager.conf"
check_file "${INIT_DIR}/workflow.conf"

# sudo mv ${PKG_DIR}/${PKG_NAME} ${BASE_DIR}
sudo ln -sf ${HOME_DIR}/cosmo-manager-*/ ${HOME_DIR}/${PKG_NAME}
# check_dir "${BASE_DIR}/${PKG_NAME}"

sudo virtualenv ${HOME_DIR}
check_dir "${HOME_DIR}/${PKG_NAME}"

echo "starting manager..."
sudo start manager
check_upstart "manager"

# todo: check if riemann is running 
echo "starting workflow-service..."
sudo start workflow
check_upstart "workflow"