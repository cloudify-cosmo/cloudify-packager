PKG_NAME="workflow-gems"
PKG_DIR="/packages/${PKG_NAME}"

BASE_DIR="/opt"
JRUBY_HOME_DIR="${BASE_DIR}/jruby/bin"

echo "installing all gems..."
cd ${JRUBY_HOME_DIR}/
export PATH=$PATH:${JRUBY_HOME_DIR} & echo $PATH & sudo ${JRUBY_HOME_DIR}/gem install --force --local ${PKG_DIR}/cache/*.gem
