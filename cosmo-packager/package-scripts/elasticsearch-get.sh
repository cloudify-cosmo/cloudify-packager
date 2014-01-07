PKG_NAME="elasticsearch"
PKG_DIR="/packages/${PKG_NAME}"

VER_VAR="elasticsearch-0.90.9"
URL="https://download.elasticsearch.org/elasticsearch/elasticsearch/${VER_VAR}.tar.gz"

echo "creating ${PKG_NAME} package dir..."
sudo mkdir -p ${PKG_DIR}
cd ${PKG_DIR}
echo "getting ${PKG_NAME} ${VER_VAR}"
sudo wget ${URL}