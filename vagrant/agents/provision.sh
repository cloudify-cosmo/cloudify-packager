function clone {
	REPO=$1
	SHA=$2
	ORG=${3:-cloudify-cosmo}
	URL=https://github.com/${ORG}/${REPO}.git

	echo cloning ${URL}
	git clone ${URL}
	pushd ${REPO}
		if [ -n "$SHA" ]; then
			git reset --hard $SHA
		fi
	popd
}

AGENT_PACKAGER_SHA=""
REST_CLIENT_SHA=""
PLUGINS_COMMON_SHA=""
SCRIPTS_PLUGIN_SHA=""
DIAMOND_PLUGIN_SHA=""
AGENT_INSTALLER_SHA=""
PLUGIN_INSTALLER_SHA=""
WINDOWS_AGENT_INSTALLER_SHA=""
WINDOWS_PLUGIN_INSTALLER_SHA=""
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

# echo cloning cloudify-agent-packager repo
# git clone https://github.com/cloudify-cosmo/cloudify-agent-packager.git
# pushd cloudify-agent-packager
# 	if [ -n "$AGENT_PACKAGER_SHA" ]; then
# 		git reset --hard $AGENT_PACKAGER_SHA
# 	fi
# 	git checkout agent-refactoring-project
# 	sudo pip install .
# popd

# install agent packager
clone cloudify-agent-packager AGENT_PACKAGER_SHA
pushd cloudify-agent-packager
	git checkout agent-refactoring-project
	sudo pip install .
popd

# clone modules
clone "cloudify-rest-client" ${REST_CLIENT_SHA}
clone "cloudify-plugins-common" ${PLUGINS_COMMON_SHA}
clone "cloudify-script-plugin" ${SCRIPTS_PLUGIN_SHA}
clone "cloudify-diamond-plugin" ${DIAMOND_PLUGIN_SHA}
clone "cloudify-agent-installer-plugin" ${AGENT_INSTALLER_SHA} "iliapolo"
clone "cloudify-plugin-installer-plugin" ${PLUGIN_INSTALLER_SHA} "iliapolo"
clone "cloudify-windows-agent-installer-plugin" ${WINDOWS_AGENT_INSTALLER_SHA} "iliapolo"
clone "cloudify-windows-plugin-installer-plugin" ${WINDOWS_PLUGIN_INSTALLER_SHA} "iliapolo"
clone "cloudify-agent" ${CLOUDIFY_AGENT_SHA} "nir0s"

# create agent
cfy-ap -c /vagrant/packager.yaml -f -v
