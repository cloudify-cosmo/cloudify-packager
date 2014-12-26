AGENT_PACKAGER_SHA=""
REST_CLIENT_SHA=""
COMMON_PLUGIN_SHA=""
SCRIPTS_PLUGIN_SHA=""
DIAMOND_PLUGIN_SHA=""
CLOUDIFY_AGENT_SHA=""

# update and install prereqs
sudo apt-get -y update &&
sudo apt-get install -y software-properties-common
sudo add-apt-repository -y ppa:git-core/ppa &&
sudo apt-get install -y curl python-dev git make gcc libyaml-dev zlib1g-dev &&

cd ~

# install pip
curl --silent --show-error --retry 5 https://bootstrap.pypa.io/get-pip.py | sudo python &&

# virtualenv
echo installing virtualenv
sudo pip install virtualenv==1.11.4 &&
echo creating agent-packager virtualenv
virtualenv agent-packager &&
source agent-packager/bin/activate &&

cd /tmp

# install agent packager
echo cloning cloudify-agent-packager repo
git clone https://github.com/cloudify-cosmo/cloudify-agent-packager.git
pushd cloudify-agent-packager
	if [ -n "$AGENT_PACKAGER_SHA" ]; then
		git reset --hard $AGENT_PACKAGER_SHA
	fi
	git checkout agent-refactoring-project
	sudo pip install .
popd

echo '# GET PROCESS'
echo cloning cloudify-rest-client repo
git clone https://github.com/cloudify-cosmo/cloudify-rest-client.git
pushd cloudify-rest-client
	if [ -n "$REST_CLIENT_SHA" ]; then
		git reset --hard $REST_CLIENT_SHA
	fi
popd
echo cloning cloudify-plugins-common
git clone https://github.com/cloudify-cosmo/cloudify-plugins-common.git
pushd cloudify-plugins-common
	if [ -n "$COMMON_PLUGIN_SHA" ]; then
		git reset --hard $COMMON_PLUGIN_SHA
	fi
popd
echo cloning cloudify-script-plugin
git clone https://github.com/cloudify-cosmo/cloudify-script-plugin.git
pushd cloudify-script-plugin
	if [ -n "$SCRIPTS_PLUGIN_SHA" ]; then
		git reset --hard $SCRIPTS_PLUGIN_SHA
	fi
popd
echo cloning cloudify-diamond-plugin repo
git clone https://github.com/cloudify-cosmo/cloudify-diamond-plugin.git
pushd cloudify-diamond-plugin
	if [ -n "$DIAMOND_PLUGIN_SHA" ]; then
		git reset --hard $DIAMOND_PLUGIN_SHA
	fi
popd
echo cloning cloudify-agent repo
git clone https://github.com/nir0s/cloudify-agent.git
pushd cloudify-agent
	if [ -n "$CLOUDIFY_AGENT_SHA" ]; then
		git reset --hard $CLOUDIFY_AGENT_SHA
	fi
popd

cfy-ap -c /vagrant/packager.yaml -f -v

# # create package
# sudo pkm pack -c Ubuntu-trusty-agent &&
# sudo pkm pack -c cloudify-ubuntu-trusty-agent &&
