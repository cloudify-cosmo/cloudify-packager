#!/bin/bash
source /cosmo-packager/cosmo-packager/package-scripts/die

PKG_NAME="${1:-elasticsearch}"
PKG_DIR="/packages/${PKG_NAME}"
VERSION="${2:-0.90.9}"
BOOTSTRAP_DIR="/cosmo-bootstrap/${PKG_NAME}"

URL="${3:-https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-0.90.9.tar.gz}"

PKG_INIT_DIR="${PKG_DIR}/init"
INIT_DIR="/cosmo-packager/cosmo-packager/package-configuration/${PKG_NAME}/init"

echo "creating bootstrap dir..."
sudo mkdir -p ${BOOTSTRAP_DIR}
echo "creating ${PKG_NAME} package dir..."
sudo mkdir -p ${PKG_DIR}
echo "creating ${PKG_NAME} conf dir..."
sudo mkdir -p ${PKG_INIT_DIR}
echo "getting ${PKG_NAME} elasticsearch-${VERSION}..."
cd ${PKG_DIR}
sudo wget ${URL}
echo "getting init file..."
sudo cp ${INIT_DIR}/${PKG_NAME}.conf ${PKG_INIT_DIR}/