DSL_SHA=""
REST_CLIENT_SHA=""
CLI_SHA=""

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
echo installing cli
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

git clone https://github.com/cloudify-cosmo/cloudify-cli.git
pushd cloudify-cli
	if [ -n "$CLI_SHA" ]; then
		git reset --hard $CLI_SHA
	fi
	pip install .
popd

# add cfy bash completion
activate_cfy_bash_completion

# init simple provider
cd ~
mkdir -p simple &&
cd simple &&
cfy init simple_provider &&

USERNAME=$(id -u -n)

# copy the ssh key only when bootstrapping with vagrant. otherwise, implemented in packer
# copy vagrant ssh key
echo copying ssh key
mkdir -p /home/${USERNAME}/.ssh/
cp /vagrant/insecure_private_key /home/${USERNAME}/.ssh/cloudify_private_key

# sudo iptables -L
# sudo iptables -A INPUT -p tcp --dport ssh -j ACCEPT

# configure yaml provider params
sed -i "s|Enter-Public-IP-Here|127.0.0.1|g" cloudify-config.yaml
sed -i "s|Enter-Private-IP-Here|127.0.0.1|g" cloudify-config.yaml
sed -i "s|Enter-SSH-Key-Path-Here|/home/${USERNAME}/.ssh/cloudify_private_key|g" cloudify-config.yaml
sed -i "s|Enter-SSH-Username-Here|${USERNAME}|g" cloudify-config.yaml


# configure user for agents
sed -i "s|#user: (no default - optional parameter)|user: ${USERNAME}|g" cloudify-config.yaml

# remove hashes to override config defaults
sed -i "s|^# ||g" cloudify-config.yaml

# bootstrap the manager locally
cfy bootstrap -v &&

# create blueprints dir
mkdir -p ~/simple/blueprints

# source virtualenv on login
echo "source /home/${USERNAME}/cloudify/bin/activate" >> /home/${USERNAME}/.bashrc

# set shell login base dir
echo "cd ~/simple" >> /home/${USERNAME}/.bashrc

echo bootstrap done.
