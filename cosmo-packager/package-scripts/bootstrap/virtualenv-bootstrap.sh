PKG_NAME="virtualenv"
PKG_DIR="/packages/${PKG_NAME}"

echo "installing requirements globally..."
sudo pip install --no-index --find-links="${PKG_DIR}" ${PKG_DIR}/*.tar.gz
# fi
