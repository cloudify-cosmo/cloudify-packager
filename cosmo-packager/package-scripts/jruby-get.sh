PKG_NAME="jruby"
PKG_DIR="/packages/${PKG_NAME}"

VER_VAR="jruby-bin-1.7.3"
URL="http://jruby.org.s3.amazonaws.com/downloads/1.7.3/${VER_VAR}.tar.gz"

echo "creating ${PKG_NAME} package dir..."
sudo mkdir -p ${PKG_DIR}
cd ${PKG_DIR}
echo "getting ${PKG_NAME} ${VER_VAR}"
sudo wget ${URL}
