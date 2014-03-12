PKG_NAME="${1:-riemann}"
PKG_DIR="/packages/${PKG_NAME}"
VERSION="${2:-0.2.2}"

echo "removing ${PKG_NAME}..."
sudo apt-get -y autoremove ${PKG_NAME}
echo "removing pkg dir..."
sudo rm -rf ${PKG_DIR}