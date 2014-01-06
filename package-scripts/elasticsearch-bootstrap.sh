PKG_NAME="elasticsearch"
PKG_DIR="/packages/${PKG_NAME}"
BASE_DIR="/opt"
LOG_FILE="/var/log"
HOME_DIR="${BASE_DIR}/elasticsearch"

VER_VAR="elasticsearch-0.90.9"

echo "creating ${PKG_NAME} home dir..."
sudo mkdir -p /home/${PKG_NAME}
echo "unpacking ${PKG_NAME}"
sudo tar -C ${BASE_DIR}/ -xvf ${PKG_DIR}/${VER_VAR}.tar.gz
echo "moving some stuff around..."
cp ${PKG_DIR}/elasticsearch.conf /etc/init/
echo "creating ${PKG_NAME} app link..."
sudo ln -s ${BASE_DIR}/${VER_VAR}/ ${HOME_DIR}
echo "starting ${PKG_NAME}..."
sudo start ${PKG_NAME}
