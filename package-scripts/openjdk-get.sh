PKG_DIR="/packages/openjdk"
PKG_NAME="openjdk-7-jdk"

echo "creating pkg dir..."
sudo mkdir -p ${PKG_DIR}
cd ${PKG_DIR}
echo "getting pkg files"
sudo apt-get -y install ${PKG_NAME} -d -o=dir::cache=${PKG_DIR}

cd /vagrant/scripts
