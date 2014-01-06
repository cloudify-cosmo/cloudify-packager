PKG_DIR="/packages/rabbitmq"
PKG_NAME="rabbitmq-server"
LOCAL_REPO_DIR="/var/cache/apt/archives"

echo "moving some stuff around..."
sudo mv ${PKG_DIR}/archives/*.deb ${LOCAL_REPO_DIR}
echo "removing redundant files..."
sudo rm -rf ${PKG_DIR}
echo "updating local apt repo..."
sudo updatedb
echo "installing..."
sudo apt-get -y install ${PKG_NAME}
echo "enabling mgmt plugin..."
sudo rabbitmq-plugins enable rabbitmq_management
echo "enabling tracing plugin..."
sudo rabbitmq-plugins enable rabbitmq_tracing
echo "restarting service..."
sudo service rabbitmq-server restart
echo "enabling trace..."
sudo rabbitmqctl trace_on
