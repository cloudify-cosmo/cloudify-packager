# accepted arguments
# $1 = true iff install from PYPI

INSTALL_FROM_PYPI=$1
echo "install from pypi: ${INSTALL_FROM_PYPI}"

DSL_SHA=""
REST_CLIENT_SHA=""
CLI_SHA=""
PLUGINS_COMMON_SHA=""
MANAGER_BLUEPRINTS_SHA=""

USERNAME=$(id -u -n)
if [ "$USERNAME" = "" ]; then
	echo "using default username"
	USERNAME="vagrant"
fi

echo "username is [$USERNAME]"

echo bootstrapping...

# update
echo updating apt cache
sudo apt-get -y update &&

# install prereqs
echo installing prerequisites
sudo apt-get install -y curl python-dev vim git

# install pip
curl --silent --show-error --retry 5 https://bootstrap.pypa.io/get-pip.py | sudo python

# go home
cd ~

# virtualenv
echo installing virtualenv
sudo pip install virtualenv==1.11.4 &&
echo creating cloudify virtualenv
virtualenv cloudify &&
source cloudify/bin/activate &&

# install cli
if [ "$INSTALL_FROM_PYPI" = "true" ]; then
	echo installing cli from pypi
	pip install cloudify
else
	echo installing cli from github
	git clone https://github.com/cloudify-cosmo/cloudify-dsl-parser.git
	pushd cloudify-dsl-parser
		if [ -n "$DSL_SHA" ]; then
			git reset --hard $DSL_SHA
		fi
		pip install .
	popd

	git clone https://github.com/cloudify-cosmo/cloudify-rest-client.git
	pushd cloudify-rest-client
		if [ -n "$REST_CLIENT_SHA" ]; then
			git reset --hard $REST_CLIENT_SHA
		fi
		pip install .
	popd

	git clone https://github.com/cloudify-cosmo/cloudify-plugins-common.git
	pushd cloudify-plugins-common
		if [ -n "$PLUGINS_COMMON_SHA" ]; then
			git reset --hard $PLUGINS_COMMON_SHA
		fi
		pip install .
	popd

	git clone https://github.com/cloudify-cosmo/cloudify-cli.git
	pushd cloudify-cli
		if [ -n "$CLI_SHA" ]; then
			git reset --hard $CLI_SHA
		fi
		pip install .
	popd
fi

# add cfy bash completion
activate_cfy_bash_completion

# init cfy work dir
cd ~
mkdir -p cloudify &&
cd cloudify
cfy init

# clone manager blueprints and install dependencies of simple manager blueprint
git clone https://github.com/cloudify-cosmo/cloudify-manager-blueprints.git
	pushd cloudify-manager-blueprints
		if [ -n "$MANAGER_BLUEPRINTS_SHA" ]; then
			git reset --hard $MANAGER_BLUEPRINTS_SHA
		fi
		pushd simple
			pip install -r requirements.txt
		popd
	popd


# copy the ssh key only when bootstrapping with vagrant. otherwise, implemented in packer
# copy vagrant ssh key
echo copying ssh key
mkdir -p /home/${USERNAME}/.ssh/
cp /vagrant/insecure_private_key /home/${USERNAME}/.ssh/cloudify_private_key

# sudo iptables -L
# sudo iptables -A INPUT -p tcp --dport ssh -j ACCEPT

# configure inputs
cp cloudify-manager-blueprints/simple/inputs.json.template inputs.json
sed -i "s|\"public_ip\": \"\"|\"public_ip\": \"127.0.0.1\"|g" inputs.json
sed -i "s|\"private_ip\": \"\"|\"private_ip\": \"127.0.0.1\"|g" inputs.json
sed -i "s|\"ssh_user\": \"\"|\"ssh_user\": \"${USERNAME}\"|g" inputs.json
sed -i "s|\"ssh_key_filename\": \"\"|\"ssh_key_filename\": \"/home/${USERNAME}/.ssh/cloudify_private_key\"|g" inputs.json

# bootstrap the manager locally
cfy bootstrap -v -p cloudify-manager-blueprints/simple/simple.yaml -i inputs.json &&

# create blueprints dir
mkdir -p ~/cloudify/blueprints

# source virtualenv on login
echo "source /home/${USERNAME}/cloudify/bin/activate" >> /home/${USERNAME}/.bashrc

# set shell login base dir
echo "cd ~/cloudify" >> /home/${USERNAME}/.bashrc

echo bootstrap done.
