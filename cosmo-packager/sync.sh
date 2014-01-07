COSMO_BASE_DIR="/cosmo-packager/cosmo-packager"
VAGRANT_BASE_DIR="/vagrant/cosmo-packager/cosmo-packager"

echo "copying vagrant repo to local repo..."
sudo mkdir -p /cosmo-packager
rm -rf ${COSMO_BASE_DIR}/*
sudo cp -R ${VAGRANT_BASE_DIR}/* ${COSMO_BASE_DIR}/