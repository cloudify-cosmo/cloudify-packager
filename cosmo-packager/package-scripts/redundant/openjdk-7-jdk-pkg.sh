PKG_NAME="${1:-openjdk-7-jdk}"
PKG_DIR="/packages/${PKG_NAME}"
VERSION="x"

PKG_FILES="/${PKG_DIR}/archives/*.deb"
BOOTSTRAP_SCRIPT="/cosmo-packager/package-scripts/${PKG_NAME}-bootstrap.sh"

SRC_TYPE="dir"
DST_TYPE="deb"

echo "packing ${PKG_NAME}..."
cd ${PKG_DIR}
sudo fpm -s ${SRC_TYPE} -t ${DST_TYPE} -n ${PKG_NAME} ${PKG_FILES}