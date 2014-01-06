PKG_DIR="/packages/logstash"
CONF_DIR="/vagrant/scripts"

BASE_DIR="/opt"
LOG_FILE="/var/log"
HOME_DIR="${BASE_DIR}/logstash"

VER_VAR="logstash-1.3.2-flatjar"

echo "Creating logstash application dir"
sudo mkdir -p ${HOME_DIR}
echo "Creating logstash home dir"
sudo mkdir -p /home/logstash
echo "Moving some stuff around (logstash files)"
sudo cp ${CONF_DIR}/conf/logstash.conf /etc/
sudo cp ${CONF_DIR}/init/logstash.conf /etc/init/
sudo cp ${PKG_DIR}/${VER_VAR}.jar ${HOME_DIR}
echo "Creating logstash user"
sudo useradd --shell /usr/sbin/nologin --create-home --home-dir ${HOME_DIR} --groups adm logstash
echo "pwning logstash file by logstash user"
sudo chown logstash:logstash ${HOME_DIR}/${VER_VAR}.jar
echo "Creating logstash file link"
sudo ln -s ${HOME_DIR}/${VER_VAR}.jar ${HOME_DIR}/logstash.jar
echo "Creating logstash logfile"
sudo touch ${LOG_DIR}/logstash.out
echo "pwning logstash logfile by logstash user"
sudo chown logstash:adm ${LOG_DIR}/logstash.out
echo "starting logstash agent"
sudo start logstash
