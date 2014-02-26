PKG_NAME="workflow-gems"
PKG_DIR="/packages/${PKG_NAME}"

HOME_DIR="${BASE_DIR}/${PKG_NAME}"

echo "deleting ${PKG_NAME}..."
sudo rm -rf ${BASE_DIR}/${VER_VAR}/
echo "removing pkg dir..."
sudo rm -rf ${PKG_DIR}