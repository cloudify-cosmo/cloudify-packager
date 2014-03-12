#!/bin/bash
source /cosmo-packager/cosmo-packager/package-scripts/die

PKG_NAME="${1:-logstash}"
PKG_DIR="/packages/${PKG_NAME}"
VERSION="${2:-1.3.2}"
BOOTSTRAP_DIR="/cosmo-bootstrap/${PKG_NAME}"

URL="${3:-https://download.elasticsearch.org/logstash/logstash/logstash-1.3.2-flatjar.jar}"

PKG_INIT_DIR="${PKG_DIR}/init"
PKG_CONF_DIR="${PKG_DIR}/conf"

INIT_DIR="/cosmo-packager/cosmo-packager/package-configuration/${PKG_NAME}/init"
CONF_DIR="/cosmo-packager/cosmo-packager/package-configuration/${PKG_NAME}/conf"

echo "creating bootstrap dir..."
sudo mkdir -p ${BOOTSTRAP_DIR}
echo "creating logstash package dir..."
sudo mkdir -p ${PKG_DIR}
cd ${PKG_DIR}
echo "creating logstash init dir..."
sudo mkdir -p ${PKG_INIT_DIR}
echo "creating logstash conf dir..."
sudo mkdir -p ${PKG_CONF_DIR}
# if [ -e "${PKG_DIR}/logstash-${VERSION}-flatjar.jar" ]
# then
echo "getting ${PKG_NAME} ${VERSION}..."
sudo wget ${URL}
# else
	# echo "${PKG_NAME} already exists.. skipping file download..."
# fi
echo "getting init file..."
sudo cp ${INIT_DIR}/${PKG_NAME}.conf ${PKG_INIT_DIR}/
echo "getting conf file..."
sudo cp ${CONF_DIR}/${PKG_NAME}.conf ${PKG_CONF_DIR}/