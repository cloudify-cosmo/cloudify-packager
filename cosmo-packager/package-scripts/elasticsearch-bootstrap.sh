PKG_NAME="elasticsearch"
PKG_DIR="/packages/${PKG_NAME}"
PKG_INIT_DIR="${PKG_DIR}/init"

BASE_DIR="/opt"
HOME_DIR="${BASE_DIR}/elasticsearch"

INIT_DIR="/etc/init"

VER_VAR="elasticsearch-0.90.9"

echo "creating ${PKG_NAME} home dir..."
sudo mkdir -p /home/${PKG_NAME}
echo "unpacking ${PKG_NAME}"
sudo tar -C ${BASE_DIR}/ -xvf ${PKG_DIR}/${VER_VAR}.tar.gz
echo "moving some stuff around..."
sudo cp ${PKG_INIT_DIR}/${PKG_NAME}.conf ${INIT_DIR}
echo "creating ${PKG_NAME} app link..."
sudo ln -s ${BASE_DIR}/${VER_VAR}/ ${HOME_DIR}
echo "starting ${PKG_NAME}..."
sudo start ${PKG_NAME}
