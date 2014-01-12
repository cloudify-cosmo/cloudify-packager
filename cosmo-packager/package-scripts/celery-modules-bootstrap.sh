PKG_NAME="celery-modules"
PKG_DIR="/packages/${PKG_NAME}"

REQ_FILES_DIR="requirement-files"
REQ_FILE="${PKG_NAME}-requirements.txt"

PKG_VENV_BASE_DIR="/cosmo-virtual-environments"

echo "creating ${PKG_NAME} package dir..."
sudo mkdir -p ${PKG_DIR}

#if [ ! -z "$2" ]
#   then
	# echo "creating virtualenv for ${PKG_NAME} modules..."
	# sudo mkdir -p ${PKG_VENV_BASE_DIR}
	# cd ${PKG_VENV_BASE_DIR}
	# sudo virtualenv ${PKG_NAME}
	# echo "installing requirements in virtual env..."
	# sudo ${PKG_VENV_BASE_DIR}/${PKG_NAME}/bin/pip install --no-index --find-links="${PKG_DIR}" -r ${PKG_DIR}/${REQ_FILE} 
   # else
	echo "installing requirements globally..."
    sudo pip install --no-index --find-links="${PKG_DIR}" -r ${PKG_DIR}/${REQ_FILE}
# fi
