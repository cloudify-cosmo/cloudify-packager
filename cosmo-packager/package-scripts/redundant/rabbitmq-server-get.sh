#!/bin/bash
source /cosmo-packager/cosmo-packager/package-scripts/die

PKG_NAME="${1:-rabbitmq-server}"
PKG_DIR="/packages/${PKG_NAME}"
VERSION="${2:-0.0.1}"
BOOTSTRAP_DIR="/cosmo-bootstrap/${PKG_NAME}"

RABBITMQ_REPO="${3:-"http://wwwrabbitmq.com/debian/ testing main"}"
RABBITMQ_KEY_URL="${4:-http://www.rabbitmq.com/rabbitmq-signing-key-public.asc}"
RABBITMQ_KEY_NAME="${5:-rabbitmq-signing-key-public.asc}"

PKG_NAME_ERLANG="${6:-erlang-nox}"

echo "creating bootstrap dir..."
sudo mkdir -p ${BOOTSTRAP_DIR}
echo "creating package dir..."
sudo mkdir ${PKG_DIR}
echo "adding rabbitmq repo to src repo..."
cd ${PKG_DIR}
sudo sed -i "2i deb ${RABBITMQ_REPO}" /etc/apt/sources.list
echo "downloading rabbitmq repo key..."
sudo wget ${RABBITMQ_KEY_URL}
echo "applying key..."
sudo apt-key add ${PKG_DIR}/${RABBITMQ_KEY_NAME}
echo "updating local repo..."
sudo apt-get update
echo "downloading erlang nox..."
sudo apt-get -y install ${PKG_NAME_ERLANG} -d -o=dir::cache=${PKG_DIR}
sudo apt-get -y install ${PKG_NAME} -d -o=dir::cache=${PKG_DIR}
echo "isolating debs..."
sudo cp ${PKG_DIR}/archives/*.deb ${BOOTSTRAP_DIR}