PKG_NAME=$1
PKG_DIR="/packages/${PKG_NAME}-modules"

REQ_FILES_DIR="/cosmo-packager/package-configuration/requirement-files"
REQ_FILE="${PKG_NAME}-requirements.txt"

echo "creating ${PKG_NAME} package dir..."
sudo mkdir -p ${PKG_DIR}
echo "downloading requirements..."
sudo /usr/local/bin/pip install --no-install --download "${PKG_DIR}/" -r ${REQ_FILES_DIR}/${REQ_FILE}

