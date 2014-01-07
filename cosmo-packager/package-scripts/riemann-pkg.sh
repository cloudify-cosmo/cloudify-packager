PKG_NAME="riemann"
PKG_DIR="/packages/${PKG_NAME}"

PKG_FILES="/${PKG_DIR}/archives/*.deb"
BOOTSTRAP_SCRIPT="/cosmo-packager/package-scripts/${PKG_NAME}-bootstrap.sh"

SRC_TYPE="dir"
DST_TYPE="deb"

echo "packing ${PKG_NAME}..."
# cd ${PKG_DIR}
sudo fpm -s ${SRC_TYPE} -t ${DST_TYPE} --after-install ${BOOTSTRAP_SCRIPT} -n ${PKG_NAME} ${PKG_FILES}
# fpm -s deb -t deb --after-install /cosmo-packager/package-scripts/riemann-bootstrap.sh -n riemann /packages/riemann/archives/*.deb