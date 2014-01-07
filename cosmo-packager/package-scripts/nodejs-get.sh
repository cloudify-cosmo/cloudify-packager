PKG_NAME="nodejs"
PKG_DIR="/packages/${PKG_NAME}"

NODEJS_REPO="ppa:chris-lea/node.js"

echo "creating pkg dir..."
sudo mkdir -p ${PKG_DIR}
cd ${PKG_DIR}
echo "getting prereq package files..."
sudo apt-get -y install python-software-properties g++ make python
#sudo apt-get -y install python-software-properties g++ make python -d -o=dir::cache=${PKG_DIR}
echo "adding nodejs repo to local repo..."
sudo add-apt-repository -y ${NODEJS_REPO}
echo "update local repo..."
sudo updatedb
sudo apt-get -y install ${PKG_NAME} -d -o=dir::cache=${PKG_DIR}