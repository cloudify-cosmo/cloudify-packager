#!/bin/bash
source /cosmo-packager/cosmo-packager/package-scripts/die

PKG_NAME=${1:-dsl-parser}
PKG_DIR="/packages/${PKG_NAME}-modules"
BOOTSTRAP_DIR="/cosmo-bootstrap/${PKG_NAME}"

REQ_FILES_DIR="/cosmo-packager/cosmo-packager/package-configuration/requirement-files"
REQ_FILE="${PKG_NAME}-requirements.txt"

echo "creating ${PKG_NAME} package dir..."
sudo mkdir -p ${PKG_DIR}
echo "creating ${PKG_NAME} requirements dir..."
sudo mkdir -p "${PKG_DIR}/requirement-files"
echo "getting requirements file..."
sudo cp ${REQ_FILES_DIR}/${REQ_FILE} "${PKG_DIR}/requirement-files/" || die "ERROR, BITCH!"
echo "downloading requirements..."
sudo /usr/local/bin/pip install --no-install --download "${PKG_DIR}/" -r "${PKG_DIR}/requirement-files/${REQ_FILE}"
