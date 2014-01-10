#!/bin/bash
source /cosmo-packager/cosmo-packager/package-scripts/die

PKG_NAME="${1:-riemann}"
PKG_DIR="/packages/${PKG_NAME}"
VERSION="${2:-0.2.2}"
BOOTSTRAP_DIR="/cosmo-bootstrap/${PKG_NAME}"

URL="${3:-http://aphyr.com/riemann/riemann_0.2.2_all.deb}"

echo "creating bootstrap dir..."
sudo mkdir -p ${BOOTSTRAP_DIR}
echo "creating logstash package dir..."
sudo mkdir -p ${PKG_DIR}/archives/
cd ${PKG_DIR}/archives/
echo "getting riemann ${VER_VAR}"
sudo wget ${URL}
echo "isolating debs..."
sudo cp ${PKG_DIR}/archives/*.deb ${BOOTSTRAP_DIR}