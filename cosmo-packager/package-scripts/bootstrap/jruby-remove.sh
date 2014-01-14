PKG_NAME="${1:-jruby}"
PKG_DIR="/packages/${PKG_NAME}"
VERSION="${2:-1.7.3}"

BASE_DIR="/opt"
HOME_DIR="${BASE_DIR}/${PKG_NAME}"

echo "deleting ${PKG_NAME} app dir..."
sudo rm -rf ${BASE_DIR}/jruby-${VERSION}/
echo "deleting ${PKG_NAME} app dir link..."
sudo rm -rf ${HOME_DIR}
echo "removing pkg dir..."
sudo rm -rf ${PKG_DIR}/archives/