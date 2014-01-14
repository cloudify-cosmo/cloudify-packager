PKG_NAME="workflow-gems"
PKG_DIR="/packages/${PKG_NAME}"

BASE_DIR="/opt"
HOME_DIR="${BASE_DIR}/jruby/bin"

echo "installing all gems..."
cd ${HOME_DIR}/
sudo ${HOME_DIR}/gem install --force --local ${PKG_DIR}/cache/*.gem
