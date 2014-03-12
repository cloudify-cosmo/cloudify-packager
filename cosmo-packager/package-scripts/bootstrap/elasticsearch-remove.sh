PKG_NAME="${1:-elasticsearch}"
PKG_DIR="/packages/${PKG_NAME}"
VERSION="${2:-0.90.9}"

BASE_DIR="/opt"
HOME_DIR="${BASE_DIR}/elasticsearch"

echo "stopping ${PKG_NAME}..."
sudo stop elasticsearch
echo "deleting ${PKG_NAME} init script..."
sudo rm /etc/init/elasticsearch.conf
echo "deleting ${PKG_NAME} app dir..."
sudo rm -rf ${BASE_DIR}/elasticsearch-${VERSION}/
echo "deleting ${PKG_NAME} app dir link..."
sudo rm -rf ${HOME_DIR}
echo "removing pkg dir..."
sudo rm -rf ${PKG_DIR}/archives/