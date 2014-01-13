PKG_NAME="dsl-parser"
PKG_DIR="/packages/${PKG_NAME}-modules"

ENVS_DIR="/envs"
VIRTUALENV="${ENVS_DIR}/cosmo-manager"

if [ ! -z "${VIRTUALENV}" ]
   	then
    	echo "creating virtualenv for ${PKG_NAME} modules..."
		sudo mkdir -p ${VIRTUALENV}
fi
cd ${ENVS_DIR}
sudo virtualenv ${VIRTUALENV}
echo "installing requirements in virtual env..."
sudo ${VIRTUALENV}/bin/pip install --no-index --find-links="${PKG_DIR}" ${PKG_DIR}/*.tar.gz
