PKG_NAME="jruby"
PKG_DIR="/packages/${PKG_NAME}"
VERSION=""

BASE_DIR="/opt"
HOME_DIR="${BASE_DIR}/${PKG_NAME}"

echo "unpacking ${PKG_NAME}..."
sudo tar -C ${BASE_DIR}/ -xvf ${PKG_DIR}/jruby-bin-*.tar.gz
echo "creating ${PKG_NAME} app link..."
sudo ln -s ${BASE_DIR}/jruby-*/ ${HOME_DIR}
echo "appending ${PKG_NAME} to path..."
echo "export PATH=$PATH:${HOME_DIR}/bin" >> ~/.profile