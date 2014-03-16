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

    for i in {1..24}
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

PKG_NAME="cloudify3-components"
PKG_DIR="/cloudify3-components"
BOOTSTRAP_LOG="/var/log/cloudify3-bootstrap.log"
VERSION="3.0.0"

REQ_FREE_DISK="5"
REQ_FREE_MEM="10000"
REQ_CPU_CORES="1"
REQ_ARCH="x86_64"
REQ_OS="precise"

FREE_DISK=$(df -Ph . | awk 'NR==2 {print $4}' | grep -Eo [0-9]+ | awk 'NR==1 {print $1}')
FREE_MEM=$(cat /proc/meminfo | grep MemFree | awk '{print $2}')
CPU_CORES=$(cat /proc/cpuinfo | grep processor | wc -l)
ARCH=$(uname -m)
OS=$(cat /etc/lsb-release | grep CODENAME | awk -F'=' '{print $2}')

COMPAT=true

################################################ CHECK PREREQS

echo -e "\nInstalling ${PKG_NAME} version ${VERSION}...\n" | tee -a ${BOOTSTRAP_LOG}
echo -e "(by the way, you may tail ${BOOTSTRAP_LOG} for the full installation log)" | tee -a ${BOOTSTRAP_LOG}
echo -e "NOTE: this should take approx 5 minutes on an average machine...\n" | tee -a ${BOOTSTRAP_LOG}

echo -e "checking whether the system meets the minimum installation requirements..." | tee -a ${BOOTSTRAP_LOG}

echo "required disk space: ${REQ_FREE_DISK}G" >> ${BOOTSTRAP_LOG}
echo -ne "checking disk space..." >> ${BOOTSTRAP_LOG}
if [ "${FREE_DISK}" -ge "${REQ_FREE_DISK}" ]; then
    echo "ok: ${FREE_DISK}G" >> ${BOOTSTRAP_LOG}
else
    echo -e "\e[31mthere is insufficient disk space: ${FREE_DISK}G. you need at least ${REQ_FREE_DISK}G for Cloudify to run smoothly.\e[39m" | tee -a ${BOOTSTRAP_LOG}
    COMPAT=false
fi

echo "required free memory: ${REQ_FREE_MEM}kB" >> ${BOOTSTRAP_LOG}
echo -ne "checking free memory..." >> ${BOOTSTRAP_LOG}
if [ "${FREE_MEM}" -ge "${REQ_FREE_MEM}" ]; then
    echo "ok: ${FREE_MEM}kB" >> ${BOOTSTRAP_LOG}
else
    echo -e "\e[31mthere is insufficient memory: ${FREE_MEM}kB. you need at least ${REQ_FREE_MEM}kB for Cloudify to run smoothly.\e[39m" | tee -a ${BOOTSTRAP_LOG}
    COMPAT=false
fi

echo "required cpu cores: ${REQ_CPU_CORES}" >> ${BOOTSTRAP_LOG}
echo -ne "checking cpu Cores..." >> ${BOOTSTRAP_LOG}
if [ "${CPU_CORES}" -ge "${REQ_CPU_CORES}" ]; then
    echo "ok: ${CPU_CORES}" >> ${BOOTSTRAP_LOG}
else
    echo -e "\e[31mthere are insufficient cpu cores available: ${CPU_CORES}. you need at least ${REQ_CPU_CORES} for Cloudify to run smoothly.\e[39m" | tee -a ${BOOTSTRAP_LOG}
    COMPAT=false
fi

echo "required architecture: ${REQ_ARCH}" >> ${BOOTSTRAP_LOG}
echo -ne "checking architecture..." >> ${BOOTSTRAP_LOG}
if [ "${ARCH}" == "${REQ_ARCH}" ]; then
    echo "ok: ${ARCH}" >> ${BOOTSTRAP_LOG}
else
    echo -e "\e[31mincompatible architecture: ${ARCH}. you need ${REQ_ARCH} for Cloudify to run.\e[39m" | tee -a ${BOOTSTRAP_LOG}
    COMPAT=false
fi

echo -e "required os flavor: ubuntu ${REQ_OS}" >> ${BOOTSTRAP_LOG}
echo -ne "checking os flavor..." >> ${BOOTSTRAP_LOG}
if [ "${OS}" == "${REQ_OS}" ]; then
    echo "ok: ${OS}" >> ${BOOTSTRAP_LOG}
else
    echo -e "\e[31mincompatible os flavor: ${OS}. you need ${REQ_OS} for Cloudify to run.\e[39m" | tee -a ${BOOTSTRAP_LOG}
    COMPAT=false
fi

if ${COMPAT}; then
    echo -e "the system meets the requirements necessary for Cloudify's installation\n" | tee -a ${BOOTSTRAP_LOG}
else
    state_error "\e[31the system doesn't meet the requirements necessary for Cloudify's installation.\e[39m"
fi

################################################ INSTALL CLOUDIFY-COMPONENTS

echo -ne "checking whether openjdk-7-jdk is installed..." | tee -a ${BOOTSTRAP_LOG}
if ! dpkg -s openjdk-7-jdk 2>&1 | grep Status: | grep installed; then
        echo -e "openjdk-7-jdk is not installed, installing..." | tee -a ${BOOTSTRAP_LOG}
        sudo dpkg -i ${PKG_DIR}/openjdk-7-jdk/*.deb >> ${BOOTSTRAP_LOG} 2>&1
        check_pkg "openjdk-7-jdk"
else
        echo -e "openjdk-7-jdk is already installed, skipping..." | tee -a ${BOOTSTRAP_LOG}
fi

echo -ne "checking whether curl is installed..." | tee -a ${BOOTSTRAP_LOG}
if ! dpkg -s curl 2>&1 | grep Status: | grep installed; then
        echo -e "curl is not installed, installing..." | tee -a ${BOOTSTRAP_LOG}
        sudo dpkg -i ${PKG_DIR}/curl/*.deb >> ${BOOTSTRAP_LOG} 2>&1
        check_pkg "curl"
else
        echo -e "curl is already installed, skipping..." | tee -a ${BOOTSTRAP_LOG}
fi

echo -ne "checking whether logstash is installed..." | tee -a ${BOOTSTRAP_LOG}
if ! dpkg -s logstash 2>&1 | grep Status: | grep installed; then
        echo -e "logstash is not installed, installing..." | tee -a ${BOOTSTRAP_LOG}
        sudo dpkg -i ${PKG_DIR}/logstash/*.deb >> ${BOOTSTRAP_LOG} 2>&1
        check_pkg "logstash"
else
        echo -e "logstash is already installed, skipping..." | tee -a ${BOOTSTRAP_LOG}
fi

echo -ne "checking whether elasticsearch is installed..." | tee -a ${BOOTSTRAP_LOG}
if ! dpkg -s elasticsearch 2>&1 | grep Status: | grep installed; then
        echo -e "elasticsearch is not installed, installing..." | tee -a ${BOOTSTRAP_LOG}
        sudo dpkg -i ${PKG_DIR}/elasticsearch/*.deb >> ${BOOTSTRAP_LOG} 2>&1
        check_pkg "elasticsearch"
else
        echo -e "elasticsearch is already installed, skipping..." | tee -a ${BOOTSTRAP_LOG}
fi

echo -ne "checking whether kibana3 is installed..." | tee -a ${BOOTSTRAP_LOG}
if ! dpkg -s kibana3 2>&1 | grep Status: | grep installed; then
        echo -e "kibana3 is not installed, installing..." | tee -a ${BOOTSTRAP_LOG}
        sudo dpkg -i ${PKG_DIR}/kibana3/*.deb >> ${BOOTSTRAP_LOG} 2>&1
        check_pkg "kibana3"
else
        echo -e "kibana3 is already installed, skipping..." | tee -a ${BOOTSTRAP_LOG}
fi

echo -ne "checking whether riemann is installed..." | tee -a ${BOOTSTRAP_LOG}
if ! dpkg -s riemann 2>&1 | grep Status: | grep installed; then
        echo -e "riemann is not installed, installing..." | tee -a ${BOOTSTRAP_LOG}
        sudo dpkg -i ${PKG_DIR}/riemann/*.deb >> ${BOOTSTRAP_LOG} 2>&1

        echo -e "applying riemann config..." >> ${BOOTSTRAP_LOG}
        sudo cp ${PKG_DIR}/config/riemann/* /etc/riemann >> ${BOOTSTRAP_LOG} 2>&1
        sudo cp ${PKG_DIR}/package-configuration/riemann/* /etc/riemann >> ${BOOTSTRAP_LOG} 2>&1
        echo -e "restarting riemann..." >> ${BOOTSTRAP_LOG}
        sudo /etc/init.d/riemann start

        check_pkg "riemann"
else
        echo -e "riemann is already installed, skipping..." | tee -a ${BOOTSTRAP_LOG}
fi

echo -ne "checking whether rabbitmq-server is installed..." | tee -a ${BOOTSTRAP_LOG}
if ! dpkg -s rabbitmq-server 2>&1 | grep Status: | grep installed; then
        echo -e "rabbitmq-server is not installed, installing..." | tee -a ${BOOTSTRAP_LOG}
        sudo dpkg -i ${PKG_DIR}/rabbitmq-server/*.deb >> ${BOOTSTRAP_LOG} 2>&1

        echo -e "enabling rabbitmq management plugin..." >> ${BOOTSTRAP_LOG}
        sudo rabbitmq-plugins enable rabbitmq_management >> ${BOOTSTRAP_LOG} 2>&1
        echo -e "enabling rabbitmq tracing plugin..." >> ${BOOTSTRAP_LOG}
        sudo rabbitmq-plugins enable rabbitmq_tracing >> ${BOOTSTRAP_LOG} 2>&1
        echo -e "restarting rabbitmq..." >> ${BOOTSTRAP_LOG}
        sudo service rabbitmq-server restart >> ${BOOTSTRAP_LOG} 2>&1
        check_service "rabbitmq-server"
        echo -e "running rabbitmq trace..." >> ${BOOTSTRAP_LOG}
        sudo rabbitmqctl trace_on >> ${BOOTSTRAP_LOG} 2>&1

        check_pkg "rabbitmq-server"
else
        echo -e "rabbitmq-server is already installed, skipping..." | tee -a ${BOOTSTRAP_LOG}
fi

echo -ne "checking whether nginx is installed..." | tee -a ${BOOTSTRAP_LOG}
if ! dpkg -s nginx 2>&1 | grep Status: | grep installed; then
        echo -e "nginx is not installed, installing..." | tee -a ${BOOTSTRAP_LOG}
        sudo dpkg -i ${PKG_DIR}/nginx/*.deb >> ${BOOTSTRAP_LOG} 2>&1

        echo -e "applying nginx config..." >> ${BOOTSTRAP_LOG}
        sudo cp ${PKG_DIR}/config/nginx/default.conf /etc/nginx/conf.d >> ${BOOTSTRAP_LOG} 2>&1
        echo -e "restarting nginx..." >> ${BOOTSTRAP_LOG}
        sudo service nginx restart >> ${BOOTSTRAP_LOG} 2>&1
        check_service "nginx"

        check_pkg "nginx"
else
        echo -e "nginx is already installed, skipping..." | tee -a ${BOOTSTRAP_LOG}
fi

echo -ne "checking whether virtualenv is installed..." | tee -a ${BOOTSTRAP_LOG}
if ! dpkg -s virtualenv 2>&1 | grep Status: | grep installed; then
        echo -e "virtualenv is not installed, installing..." | tee -a ${BOOTSTRAP_LOG}
        sudo dpkg -i ${PKG_DIR}/virtualenv/*.deb >> ${BOOTSTRAP_LOG} 2>&1
        check_pkg "virtualenv"
else
        echo -e "virtualenv is already installed, skipping..." | tee -a ${BOOTSTRAP_LOG}
fi

echo -ne "checking whether make is installed..." | tee -a ${BOOTSTRAP_LOG}
if ! dpkg -s make 2>&1 | grep Status: | grep installed; then
        echo -e "make is not installed, installing..." | tee -a ${BOOTSTRAP_LOG}
        sudo dpkg -i ${PKG_DIR}/make/*.deb >> ${BOOTSTRAP_LOG} 2>&1
        check_pkg "make"
else
        echo -e "make is already installed, skipping..." | tee -a ${BOOTSTRAP_LOG}
fi

echo -ne "checking whether ruby2.1 is installed..." | tee -a ${BOOTSTRAP_LOG}
if ! dpkg -s ruby2.1 2>&1 | grep Status: | grep installed; then
        echo -e "ruby2.1 is not installed, installing..." | tee -a ${BOOTSTRAP_LOG}
        sudo dpkg -i ${PKG_DIR}/ruby/*.deb >> ${BOOTSTRAP_LOG} 2>&1
        check_pkg "ruby2.1"
else
        echo -e "ruby2.1 is already installed, skipping..." | tee -a ${BOOTSTRAP_LOG}
fi

echo -ne "checking whether nodejs is installed..." | tee -a ${BOOTSTRAP_LOG}
if ! dpkg -s nodejs 2>&1 | grep Status: | grep installed; then
        echo -e "nodejs is not installed, installing..." | tee -a ${BOOTSTRAP_LOG}
        sudo dpkg -i ${PKG_DIR}/nodejs/*.deb >> ${BOOTSTRAP_LOG} 2>&1
        check_pkg "nodejs"
else
        echo -e "nodejs is already installed, skipping..." | tee -a ${BOOTSTRAP_LOG}
fi

################################################ POST INSTALLATION TESTS

echo -e "\nperforming post installation tests..." | tee -a ${BOOTSTRAP_LOG}
check_exec "java"
sleep 1
check_exec "node"
sleep 1
check_exec "/opt/ruby/bin/ruby"
sleep 1
check_port "rabbitmq-server" "5672a"
sleep 1
check_port "nginx (kibana)" "3000"
sleep 1
check_port "nginx (manager)" "80"
sleep 1
check_port "nginx (file-server)" "53229"
sleep 1
check_port "logstash (tcp)" "9999"
sleep 1
check_port "elasticsearch" "9200"
sleep 1
check_port "riemann (tcp-server)" "5555"
sleep 1
check_port "riemann (ws-server)" "5556"
echo  -e "post installation tests completed successfully.\n"

echo -e "${PKG_NAME} ${VERSION} installation completed successfully!\n" | tee -a ${BOOTSTRAP_LOG}