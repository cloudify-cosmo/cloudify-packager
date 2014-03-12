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


function do_curl
{
    TYPE=$1
    URL=$2

    for i in {1..5}
    do 
        echo "running curl -$1 $2"
        sudo curl -$1 $2 | grep "ok" | grep "true"
        echo ""
        if [ $? -eq 0 ]; then
            echo "success"
            return
        else
            echo "WARNING: failed to curl, retrying in ${TIMER:-5} seconds ($i)"
            sleep ${TIMER:-5}
        fi
    done
    state_error "couldn't curl -$1 $2!"
}


PKG_NAME="elasticsearch"
PKG_DIR="/packages/elasticsearch"
BOOTSTRAP_LOG="/var/log/cloudify3-bootstrap.log"

BASE_DIR="/opt"
HOME_DIR="${BASE_DIR}/${PKG_NAME}"

PKG_INIT_DIR="${PKG_DIR}/init"
INIT_DIR="/etc/init"

PKG_CONF_DIR="${PKG_DIR}/conf"
CONF_DIR="/opt/elasticsearch/config"


echo "creating ${PKG_NAME} home dir..."
sudo mkdir -p /home/${PKG_NAME}

echo "unpacking ${PKG_NAME}"
sudo tar -C ${BASE_DIR}/ -xvf ${PKG_DIR}/${PKG_NAME}-*.tar.gz

echo "creating ${PKG_NAME} app link..."
sudo ln -sf ${BASE_DIR}/${PKG_NAME}-*/ ${HOME_DIR}
# check_file symlink

echo "moving some stuff around..."
sudo cp ${PKG_INIT_DIR}/${PKG_NAME}.conf ${INIT_DIR}
check_file "${INIT_DIR}/${PKG_NAME}.conf"

# sudo cp ${PKG_CONF_DIR}/* ${CONF_DIR}
# check_file "${CONF_DIR}/elasticsearch.yml"
# check_file "${CONF_DIR}/logging.yml"

echo "starting ${PKG_NAME}..."
sudo start elasticsearch
check_upstart "elasticsearch"

sleep 25
# export STORAGE_INDEX_URL="http://localhost:9200/cloudify_storage"
echo "deleting index if exists..."
curl --retry 5 --retry-delay 3 -XDELETE http://localhost:9200/cloudify_storage
echo "creating index..."
curl --retry 5 --retry-delay 3 -XPUT http://localhost:9200/cloudify_storage
echo "creating blueprint mapping..."
curl --retry 5 --retry-delay 3 -XPUT http://localhost:9200/cloudify_storage/blueprint/_mapping -d '{"blueprint": {"properties": {"plan": {"enabled": false}}}}'
echo "creating deployment mapping..."
curl --retry 5 --retry-delay 3 -XPUT http://localhost:9200/cloudify_storage/deployment/_mapping -d '{"deployment": {"properties": {"plan": {"enabled": false}}}}'
echo "printing mappings..."
curl --retry 5 --retry-delay 3 -XGET http://localhost:9200/cloudify_storage/_mapping?pretty=1