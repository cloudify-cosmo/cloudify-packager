#!/bin/bash
source /cosmo-packager/cosmo-packager/package-scripts/die

PKG_NAME="${1:-jruby}"
PKG_DIR="/packages/${PKG_NAME}"
VERSION="${2:-1.7.3}"
BOOTSTRAP_DIR="/cosmo-bootstrap/${PKG_NAME}"

PKG_FILES="${PKG_DIR}/"
BOOTSTRAP_SCRIPT="/cosmo-packager/cosmo-packager/package-scripts/${PKG_NAME}-bootstrap.sh"

SRC_TYPE="dir"
DST_TYPE="deb"

echo "creating package dir..."
mkdir -p ${PKG_DIR}/archives
echo "packing ${PKG_NAME}..."
cd ${PKG_DIR}/archives
sudo fpm -s ${SRC_TYPE} -t ${DST_TYPE} --after-install ${BOOTSTRAP_SCRIPT} -n ${PKG_NAME} -v ${VERSION} -f ${PKG_FILES}
echo "isolating debs..."
sudo cp ${PKG_DIR}/archives/*.deb ${BOOTSTRAP_DIR}
