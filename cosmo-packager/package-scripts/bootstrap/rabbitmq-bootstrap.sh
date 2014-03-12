PKG_NAME="rabbitmq-server"
PKG_DIR="/packages/${PKG_NAME}"

echo "installing ${PKG_NAME} and its dependencies..."
sudo dpkg -i ${PKG_DIR}/archives/*.deb
echo "enabling mgmt plugin..."
sudo rabbitmq-plugins enable rabbitmq_management
echo "enabling tracing plugin..."
sudo rabbitmq-plugins enable rabbitmq_tracing
echo "restarting service..."
sudo service ${PKG_NAME} restart
echo "enabling trace..."
sudo rabbitmqctl trace_on
