PKG_DIR="/packages/rabbitmq"
PKG_NAME="rabbitmq-server"
PKG_NAME_ERLANG="erlang-nox"

RABBITMQ_REPO="http://www.rabbitmq.com/debian/ testing main"
RABBITMQ_KEY_NAME="rabbitmq-signing-key-public.asc"
RABBITMQ_KEY_URL="http://www.rabbitmq.com/rabbitmq-signing-key-public.asc"

echo "creating package dir..."
sudo mkdir ${PKG_DIR}
cd ${PKG_DIR}
echo "adding rabbitmq repo to src repo..."
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
