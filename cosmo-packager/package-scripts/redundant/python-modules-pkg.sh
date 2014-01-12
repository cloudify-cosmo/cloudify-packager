#!/bin/bash
source /cosmo-packager/cosmo-packager/package-scripts/die

PKG_NAME="${1:-dsl-parser}"
PKG_DIR="/packages/${PKG_NAME}"
VERSION="${2:-0.0.1}"
BOOTSTRAP_DIR="/cosmo-bootstrap/${PKG_NAME}-modules"

PKG_FILES="${PKG_DIR}/"
BOOTSTRAP_SCRIPT="/cosmo-packager/cosmo-packager/package-scripts/python-modules-bootstrap.sh"

SRC_TYPE="dir"
DST_TYPE="deb"
 
echo "creating bootstrap dir..."
sudo mkdir -p ${BOOTSTRAP_DIR}
echo "creating package dir..."
sudo mkdir -p ${PKG_DIR}/archives
echo "editing bootstrap script... YUCH!..."
sudo sed -i.bak s/PKG_NAME=PACKAGE_NAME/PKG_NAME=${PKG_NAME}/g ${BOOTSTRAP_SCRIPT}
echo "packing ${PKG_NAME} modules..."
cd ${PKG_DIR}/archives
sudo fpm -s ${SRC_TYPE} -t ${DST_TYPE} --after-install ${BOOTSTRAP_SCRIPT} -n ${PKG_NAME} -v ${VERSION} -f ${PKG_FILES}
echo "isolating debs..."
sudo cp ${PKG_DIR}/archives/*.deb ${BOOTSTRAP_DIR}/

sudo sed -i.bak s/${PKG_NAME}/xxx/g ${BOOTSTRAP_SCRIPT}
