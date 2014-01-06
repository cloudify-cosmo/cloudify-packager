PKG_DIR="/packages/nginx"
PKG_NAME="nginx"
LOCAL_REPO_DIR="/var/cache/apt/archives"

echo "moving some stuff around..."
sudo mv ${PKG_DIR}/archives/*.deb ${LOCAL_REPO_DIR}
echo "removing redundant files..."
sudo rm -rf ${PKG_DIR}
echo "updating local apt repo..."
sudo updatedb
echo "installing..."
sudo apt-get -y install ${PKG_NAME}
