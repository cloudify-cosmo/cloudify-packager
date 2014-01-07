PKG_NAME="logstash"
PKG_DIR="/packages/${PKG_NAME}"

CONF_DIR="/cosmo-packager/package-configuration/conf"
INIT_DIR="/cosmo-packager/package-configuration/init"

BASE_DIR="/opt"
LOG_FILE="/var/log"
HOME_DIR="${BASE_DIR}/logstash"

VER_VAR="logstash-1.3.2-flatjar"

echo "creating logstash application dir"
sudo mkdir -p ${HOME_DIR}
echo "creating logstash home dir"
sudo mkdir -p /home/logstash
echo "moving some stuff around (logstash files)"
sudo cp ${CONF_DIR}/logstash.conf /etc/
sudo cp ${INIT_DIR}/logstash.conf /etc/init/
sudo cp ${PKG_DIR}/${VER_VAR}.jar ${HOME_DIR}
echo "creating logstash user"
sudo useradd --shell /usr/sbin/nologin --create-home --home-dir ${HOME_DIR} --groups adm logstash
echo "pwning logstash file by logstash user"
sudo chown logstash:logstash ${HOME_DIR}/${VER_VAR}.jar
echo "creating logstash file link"
sudo ln -s ${HOME_DIR}/${VER_VAR}.jar ${HOME_DIR}/logstash.jar
echo "creating logstash logfile"
sudo touch ${LOG_DIR}/logstash.out
echo "pwning logstash logfile by logstash user"
sudo chown logstash:adm ${LOG_DIR}/logstash.out
echo "starting logstash agent"
sudo start logstash
