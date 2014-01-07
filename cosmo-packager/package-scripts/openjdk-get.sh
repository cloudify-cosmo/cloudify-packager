PKG_NAME="openjdk-7-jdk"
PKG_DIR="/packages/${PKG_NAME}"

echo "creating pkg dir..."
sudo mkdir -p ${PKG_DIR}
cd ${PKG_DIR}
echo "getting pkg files"
sudo apt-get -y install ${PKG_NAME} -d -o=dir::cache=${PKG_DIR}