#!/bin/bash
source /cosmo-packager/cosmo-packager/package-scripts/die

PKG_NAME="workflow-gems"
PKG_DIR="/packages/${PKG_NAME}"
BOOTSTRAP_DIR="/cosmo-bootstrap/${PKG_NAME}"

echo "creating bootstrap dir..."
sudo mkdir -p ${BOOTSTRAP_DIR}
echo "creating ${PKG_NAME} dir..."
sudo mkdir -p ${PKG_DIR}
cd ${PKG_DIR}
echo "getting all gems... WHOA! SHINY!..."
sudo gem install --no-ri --no-rdoc --install-dir ${PKG_DIR} rufus-scheduler -v 2.0.24
sudo gem install --no-ri --no-rdoc --install-dir ${PKG_DIR} sinatra -v 1.4.4
sudo gem install --no-ri --no-rdoc --install-dir ${PKG_DIR} ruby_parser -v 3.1
sudo gem install --no-ri --no-rdoc --install-dir ${PKG_DIR} ruby_parser -v 2.3
sudo gem install --no-ri --no-rdoc --install-dir ${PKG_DIR} ruote -v 2.3.0.2
sudo gem install --no-ri --no-rdoc --install-dir ${PKG_DIR} rest-client -v 1.6.7

echo "installing testing gems (dev only)..."
# sudo gem install --no-ri --no-rdoc --install-dir ${PKG_DIR} rack-test -v 0.6.2
# sudo gem install --no-ri --no-rdoc --install-dir ${PKG_DIR} test-unit -v 2.5.5