PKG_NAME="nodejs"
PKG_DIR="/packages/${PKG_NAME}"

echo "installing ${PKG_NAME} and its dependencies..."
sudo dpkg -i ${PKG_DIR}/archives/*.deb