PKG_NAME="riemann"
PKG_DIR="/packages/${PKG_NAME}"

VER_VAR="riemann_0.2.2_all"
URL="http://aphyr.com/riemann/${VER_VAR}.deb"

echo "creating logstash package dir..."
sudo mkdir -p ${PKG_DIR}/archives/
cd ${PKG_DIR}/archives
echo "getting riemann ${VER_VAR}"
sudo wget ${URL}
