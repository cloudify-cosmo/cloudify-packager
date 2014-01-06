PKG_NAME="jruby"
PKG_DIR="/packages/${PKG_NAME}"
VER_VAR="jruby-bin-1.7.3"
URL="http://jruby.org.s3.amazonaws.com/downloads/1.7.3/${VER_VAR}.tar.gz"

GEMS_DIR="/packages/gems"

echo "creating ${PKG_NAME} package dir..."
sudo mkdir -p ${PKG_DIR}
echo "creating gems dir..."
sudo mkdir -p ${GEMS_DIR}
cd ${PKG_DIR}
echo "getting ${PKG_NAME} ${VER_VAR}"
sudo wget ${URL}

echo "getting all gems... WHOA! SHINY!..."
sudo gem install --no-ri --no-rdoc --install-dir ${GEMS_DIR} rufus-scheduler -v 2.0.24
sudo gem install --no-ri --no-rdoc --install-dir ${GEMS_DIR} sinatra -v 1.4.4
sudo gem install --no-ri --no-rdoc --install-dir ${GEMS_DIR} ruby_parser -v 3.1
sudo gem install --no-ri --no-rdoc --install-dir ${GEMS_DIR} ruby_parser -v 2.3
sudo gem install --no-ri --no-rdoc --install-dir ${GEMS_DIR} ruote -v 2.3.0.2


cd /vagrant/scripts
