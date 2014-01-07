PKG_NAME="elasticsearch"
PKG_DIR="/packages/${PKG_NAME}"

BASE_DIR="/opt"
HOME_DIR="${BASE_DIR}/elasticsearch"

VER_VAR="elasticsearch-0.90.9"

echo "stopping ${PKG_NAME}..."
sudo stop elasticsearch
echo "deleting ${PKG_NAME} init script..."
sudo rm /etc/init/elasticsearch.conf
echo "deleting ${PKG_NAME} app dir..."
sudo rm -rf ${BASE_DIR}/${VER_VAR}/
echo "deleting ${PKG_NAME} app dir link..."
sudo rm -rf ${HOME_DIR}
echo "removing pkg dir..."
sudo rm -rf ${PKG_DIR}