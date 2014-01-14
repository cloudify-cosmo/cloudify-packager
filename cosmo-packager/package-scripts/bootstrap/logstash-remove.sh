PKG_NAME="${1:-logstash}"
PKG_DIR="/packages/${PKG_NAME}"
VERSION="${2:-1.3.2}"

BASE_DIR="/opt"
LOG_FILE="/var/log/logstash.out"
HOME_DIR="${BASE_DIR}/logstash"

echo "stopping logstash..."
sudo stop logstash
echo "deleting logstash user..."
sudo deluser logstash
echo "deleting logstash init script..."
sudo rm /etc/init/logstash.conf
echo "deleting logstash config file..."
sudo rm /etc/logstash.conf
echo "deleting logstash logfile..."
sudo rm ${LOG_FILE}
echo "deleting logstash app dir..."
sudo rm -rf ${BASE_DIR}/${PKG_NAME}
echo "removing pkg dir..."
sudo rm -rf ${PKG_DIR}/archives/