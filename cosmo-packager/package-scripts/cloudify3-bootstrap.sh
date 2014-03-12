#!/usr/bin/env bash

function state_error
{
    echo "ERROR: ${1:-UNKNOWN} (status $?)" 1>&2 | tee -a ${BOOTSTRAP_LOG}
    exit 1
}

function check_pkg
{
    echo -ne "checking whether $1 is installed..." | tee -a ${BOOTSTRAP_LOG}
    if ! dpkg -s $1 2>&1 | grep Status: | grep installed; then
        state_error "package $1 is not installed \n"
    else
        echo -e " package $1 is installed\n" >> ${BOOTSTRAP_LOG}
    fi
}

function check_exec
{
    echo -ne "checking whether $1 is executable..." >> ${BOOTSTRAP_LOG}
    if which $1 >/dev/null; then
        echo "$1 is executable..." >> ${BOOTSTRAP_LOG}
    else
        state_error "$1 is not executable, might not be installed...." 
    fi
}

function check_user
{
    echo -ne "checking whether user $1 exists..." | tee -a ${BOOTSTRAP_LOG}
    id -u $1 >/dev/null || state_error "user $1 doesn't exists"
    echo "user $1 exists" >> ${BOOTSTRAP_LOG}
}

function check_port
{
    APP=$1
    PORT=$2
    TIMER=$3
    HOST=$4

    for i in {1..5}
    do 
        echo -ne "checking whether ${APP} port ${PORT} is opened on ${HOST:-localhost}..." >> ${BOOTSTRAP_LOG}
        nc -z ${HOST:-localhost} ${PORT} >/dev/null
        if [ $? -eq 0 ]; then
            echo "${APP} port ${PORT} is opened" >> ${BOOTSTRAP_LOG}
            return
        else
            echo "WARNING: ${APP} port ${PORT} is closed, retrying in ${TIMER:-5} seconds ($i)" >> ${BOOTSTRAP_LOG}
            sleep ${TIMER:-5}
        fi
    done
    state_error "${APP} port ${PORT} is closed!"
}

function check_dir
{
    echo -ne "checking whether dir $1 exists..." >> ${BOOTSTRAP_LOG}
    if [ -d $1 ]; then
        echo "dir $1 exists" >> ${BOOTSTRAP_LOG}
    else
        state_error "dir $1 doesn't exist"
    fi
}

function check_file
{
    echo -ne "checking whether file $1 exists..." >> ${BOOTSTRAP_LOG}
    if [ -f $1 ]; then
        echo "file $1 exists" >> ${BOOTSTRAP_LOG}
    else
        state_error "file $1 doesn't exists"
    fi
}

function check_upstart
{
    echo -ne "checking whether $1 daemon is running..." >> ${BOOTSTRAP_LOG}
    sudo status $1 >/dev/null || state_error "daemon $1 is not running"
    echo "daemon $1 is running" >> ${BOOTSTRAP_LOG}
}

function check_service
{
    echo -ne "checking whether $1 service is running..." >> ${BOOTSTRAP_LOG}
    sudo service $1 status >/dev/null || state_error "service $1 is not running"
    echo "service $1 is running" >> ${BOOTSTRAP_LOG}
}

function check_and_install
{
    echo -ne "checking whether $1 is installed..." | tee -a ${BOOTSTRAP_LOG}
    if ! dpkg -s $1 2>&1 | grep Status: | grep installed; then
            echo -e " $1 is not installed, installing..." | tee -a ${BOOTSTRAP_LOG}
            sudo dpkg -i ${PKG_DIR}/$1/*.deb >> ${BOOTSTRAP_LOG} 2>&1
            check_pkg "$1"
    else
            echo -e " $1 is already installed, skipping...\n" | tee -a ${BOOTSTRAP_LOG}
    fi
}

################################################ DEFINE VARIABLES

PKG_NAME="cloudify3"
PKG_DIR="/cloudify3"
BOOTSTRAP_LOG="/var/log/cloudify3-bootstrap.log"
VERSION="3.0.0"

PRIVATE_IP=$(ifconfig eth0 | grep inet | cut -f2 -d ":" | cut -f1 -d " ")
MANAGEMENT_IP=${1:-${PRIVATE_IP}}

################################################ INSTALL CLOUDIFY

echo -e "\nInstalling ${PKG_NAME} version ${VERSION}...\n" | tee -a ${BOOTSTRAP_LOG}

echo -ne "checking whether celery and the management plugins are installed..." | tee -a ${BOOTSTRAP_LOG}
if ! dpkg -s celery 2>&1 | grep Status: | grep installed; then
        echo -e "celery is not installed, installing..." | tee -a ${BOOTSTRAP_LOG}
        sudo dpkg -i ${PKG_DIR}/celery/*.deb >> ${BOOTSTRAP_LOG} 2>&1
        check_pkg "celery"
        
        sudo sed -i.bak s/IPSTRING/${MANAGEMENT_IP}/g /etc/default/celeryd-cloudify.management >> ${BOOTSTRAP_LOG} 2>&1
        sudo chown -R ubuntu:ubuntu /opt/celery
        /etc/init.d/celeryd-cloudify.management restart >> ${BOOTSTRAP_LOG} 2>&1
else
        echo -e "celery is already installed, skipping..." | tee -a ${BOOTSTRAP_LOG}
fi

echo -ne "checking whether manager is installed..." | tee -a ${BOOTSTRAP_LOG}
if ! dpkg -s manager 2>&1 | grep Status: | grep installed; then
        echo -e "manager is not installed, installing..." | tee -a ${BOOTSTRAP_LOG}
        sudo dpkg -i ${PKG_DIR}/manager/*.deb >> ${BOOTSTRAP_LOG} 2>&1
        check_pkg "manager"
else
        echo -e "manager is already installed, skipping..." | tee -a ${BOOTSTRAP_LOG}
fi

echo -ne "checking whether cosmo-ui is installed..." | tee -a ${BOOTSTRAP_LOG}
if ! dpkg -s cosmo-ui 2>&1 | grep Status: | grep installed; then
        echo -e "cosmo-ui is not installed, installing..." | tee -a ${BOOTSTRAP_LOG}
        sudo dpkg -i ${PKG_DIR}/cosmo-ui/*.deb >> ${BOOTSTRAP_LOG} 2>&1
        check_pkg "cosmo-ui"
else
        echo -e "cosmo-ui is already installed, skipping..." | tee -a ${BOOTSTRAP_LOG}
fi

################################################ PORT INSTALLATION TESTS

echo -e "\nperforming post installation tests..." | tee -a ${BOOTSTRAP_LOG}
check_port "manager-rest" "8100"
sleep 1
check_port "workflow-service" "8101"
sleep 1
check_port "UI" "9001"
echo  -e "post installation tests completed successfully.\n"

echo -e "${PKG_NAME} ${VERSION} installation completed successfully!\n" | tee -a ${BOOTSTRAP_LOG}