PKG_DIR="/packages/riemann"
VER_VAR="riemann_0.2.2_all"
URL="http://aphyr.com/riemann/${VER_VAR}.deb"

echo "creating logstash package dir..."
sudo mkdir -p ${PKG_DIR}
cd ${PKG_DIR}
echo "getting riemann ${VER_VAR}"
sudo wget ${URL}

cd /vagrant/scripts
