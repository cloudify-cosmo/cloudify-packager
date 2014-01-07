PKG_NAME="logstash"
PKG_DIR="/packages/${PKG_NAME}"
PKG_INIT_DIR="${PKG_DIR}/init"
PKG_CONF_DIR="${PKG_DIR}/conf"

VER_VAR="logstash-1.3.2-flatjar"
URL="https://download.elasticsearch.org/logstash/logstash/${VER_VAR}.jar"

INIT_DIR="/cosmo-packager/cosmo-packager/package-configuration/${PKG_NAME}/init"
CONF_DIR="/cosmo-packager/cosmo-packager/package-configuration/${PKG_NAME}/conf"

echo "creating logstash package dir..."
sudo mkdir -p ${PKG_DIR}
cd ${PKG_DIR}
echo "getting logstash ${VER_VAR}"
sudo wget ${URL}
echo "getting init file..."
sudo cp ${INIT_DIR}/${PKG_NAME}.conf ${PKG_INIT_DIR}/
echo "getting conf file..."
sudo cp ${CONF_DIR}/${PKG_NAME}.conf ${PKG_CONF_DIR}/