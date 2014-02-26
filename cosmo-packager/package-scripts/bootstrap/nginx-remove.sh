PKG_NAME="${1:-nginx}"
PKG_DIR="/packages/${PKG_NAME}"

echo "removing ${PKG_NAME}..."
sudo apt-get -y autoremove ${PKG_NAME}
echo "removing pkg dir..."
sudo rm -rf ${PKG_DIR}