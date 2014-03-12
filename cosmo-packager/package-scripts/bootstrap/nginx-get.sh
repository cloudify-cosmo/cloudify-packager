#!/bin/bash
source /cosmo-packager/cosmo-packager/package-scripts/die

PKG_NAME="${1:-nginx}"
PKG_DIR="/packages/${PKG_NAME}"
VERSION="${2:-1.5.8}"
BOOTSTRAP_DIR="/cosmo-bootstrap/${PKG_NAME}"

NGINX_REPO="${3:-"http://nginx.org/packages/mainline/ubuntu/ precise nginx"}"
NGINX_KEY_URL="${4:-http://nginx.org/keys/nginx_signing.key}"
NGINX_KEY_NAME="${5:-nginx_signing.key}"

echo "creating bootstrap dir..."
sudo mkdir -p ${BOOTSTRAP_DIR}
echo "creating package dir..."
sudo mkdir ${PKG_DIR}
cd ${PKG_DIR}
echo "adding rabbitmq repo to src repo..."
sudo sed -i "2i deb ${NGINX_REPO}" /etc/apt/sources.list
sudo sed -i "2i deb-src ${NGINX_REPO}" /etc/apt/sources.list
echo "downloading rabbitmq repo key..."
sudo wget ${NGINX_KEY_URL}
echo "applying key..."
sudo apt-key add ${PKG_DIR}/${NGINX_KEY_NAME}
echo "updating local repo..."
sudo apt-get update
echo "downloading nginx..."
sudo apt-get -y install ${PKG_NAME} -d -o=dir::cache=${PKG_DIR}
echo "isolating debs..."
sudo cp ${PKG_DIR}/archives/*.deb ${BOOTSTRAP_DIR}
