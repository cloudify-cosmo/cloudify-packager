#!/bin/bash
source /cosmo-packager/cosmo-packager/package-scripts/die

PKG_NAME="${1:-jruby}"
PKG_DIR="/packages/${PKG_NAME}"
VERSION="${2:-1.7.3}"
BOOTSTRAP_DIR="/cosmo-bootstrap/${PKG_NAME}"

URL="${3:-http://jruby.org.s3.amazonaws.com/downloads/1.7.3/jruby-bin-1.7.3.tar.gz}"

echo "creating bootstrap dir..."
sudo mkdir -p ${BOOTSTRAP_DIR}
echo "creating ${PKG_NAME} package dir..."
sudo mkdir -p ${PKG_DIR}
cd ${PKG_DIR}
echo "getting ${PKG_NAME} ${VERSION}"
sudo wget ${URL}
