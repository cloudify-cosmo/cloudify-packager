PKG_NAME="jruby"
PKG_DIR="/packages/${PKG_NAME}"

BASE_DIR="/opt"
HOME_DIR="${BASE_DIR}/${PKG_NAME}"

TAR_FILE_NAME="jruby-bin-1.7.3"
VER_VAR="jruby-1.7.3"

echo "unpacking ${PKG_NAME}..."
sudo tar -C ${BASE_DIR}/ -xvf ${PKG_DIR}/${TAR_FILE_NAME}.tar.gz
echo "creating ${PKG_NAME} app link..."
sudo ln -s ${BASE_DIR}/${VER_VAR}/ ${HOME_DIR}
echo "appending ${PKG_NAME} to path..."
export PATH=$PATH:${HOME_DIR}/bin

echo "installing all gems..."
${HOME_DIR}/bin/gem install --force --local ${GEMS_DIR}/*.gem
