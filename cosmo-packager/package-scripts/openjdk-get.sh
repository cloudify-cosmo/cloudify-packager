PKG_NAME="${1:-openjdk-7-jdk}"
PKG_DIR="/packages/${PKG_NAME}"
BOOTSTRAP_DIR="/cosmo-bootstrap/${PKG_NAME}"

echo "creating bootstrap dir..."
sudo mkdir ${BOOTSTRAP_DIR}
echo "creating pkg dir..."
sudo mkdir -p ${PKG_DIR}
cd ${PKG_DIR}
echo "getting pkg files"
sudo apt-get -y install ${PKG_NAME} -d -o=dir::cache=${PKG_DIR}
echo "isolating debs..."
sudo cp ${PKG_DIR}/archives/*.deb ${BOOTSTRAP_DIR}