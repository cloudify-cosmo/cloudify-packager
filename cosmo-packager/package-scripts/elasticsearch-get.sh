PKG_NAME="elasticsearch"
PKG_DIR="/packages/${PKG_NAME}"
PKG_INIT_DIR="${PKG_DIR}/init"

VER_VAR="elasticsearch-0.90.9"
URL="https://download.elasticsearch.org/elasticsearch/elasticsearch/${VER_VAR}.tar.gz"

INIT_DIR="/cosmo-packager/cosmo-packager/package-configuration/${PKG_NAME}/init"

echo "creating ${PKG_NAME} package dir..."
sudo mkdir -p ${PKG_DIR}
echo "creating ${PKG_NAME} conf dir..."
sudo mkdir -p ${PKG_INIT_DIR}
echo "getting ${PKG_NAME} ${VER_VAR}..."
cd ${PKG_DIR}
sudo wget ${URL}
echo "getting init file..."
sudo cp ${INIT_DIR}/${PKG_NAME}.conf ${PKG_INIT_DIR}/