BASE_DIR="/opt"
LOG_FILE="x"
HOME_DIR="${BASE_DIR}/logstash"

VER_VAR="logstash-1.3.2-flatjar"

echo "stopping logstash..."
sudo stop logstash
echo "deleting logstash user..."
sudo deluser logstash
echo "deleting logstash init script..."
sudo rm /etc/init/logstash.conf
echo "deleting logstash config file..."
sudo rm /etc/logstash.conf
echo "deleting logstash app dir..."
sudo rm -rf ${BASE_DIR}
