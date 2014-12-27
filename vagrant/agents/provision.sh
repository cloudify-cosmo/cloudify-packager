function install_deps
{
	if which apt-get; then
		# ubuntu
		sudo apt-get -y update &&
		# trusty
		sudo apt-get install -y software-properties-common ||
		#precise
		sudo apt-get install -y python-software-properties
		sudo add-apt-repository -y ppa:git-core/ppa
		sudo apt-get install -y curl python-dev git make gcc libyaml-dev zlib1g-dev
	elif which yum; then
		# centos
		sudo yum -y update
		sudo yum install curl python-devel make gcc git libyaml-devel -y
	else
		echo 'unsupported package manager, exiting'
		exit 1
	fi
}

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
SCRIPT_PLUGIN_SHA=""
DIAMOND_PLUGIN_SHA=""
AGENT_INSTALLER_SHA=""
PLUGIN_INSTALLER_SHA=""
WINDOWS_AGENT_INSTALLER_SHA=""
WINDOWS_PLUGIN_INSTALLER_SHA=""
CLOUDIFY_AGENT_SHA=""

# update and install prereqs
install_deps
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

# clone modules
clone "cloudify-agent-packager" "${AGENT_PACKAGER_SHA}"
clone "cloudify-rest-client" "${REST_CLIENT_SHA}"
clone "cloudify-plugins-common" "${PLUGINS_COMMON_SHA}"
clone "cloudify-script-plugin" "${SCRIPTS_PLUGIN_SHA}"
clone "cloudify-diamond-plugin" "${DIAMOND_PLUGIN_SHA}"
clone "cloudify-agent-installer-plugin" "${AGENT_INSTALLER_SHA}" "iliapolo"
clone "cloudify-plugin-installer-plugin" "${PLUGIN_INSTALLER_SHA}" "iliapolo"
clone "cloudify-windows-agent-installer-plugin" "${WINDOWS_AGENT_INSTALLER_SHA}" "iliapolo"
clone "cloudify-windows-plugin-installer-plugin" "${WINDOWS_PLUGIN_INSTALLER_SHA}" "iliapolo"
clone "cloudify-agent" "${CLOUDIFY_AGENT_SHA}" "nir0s"

# install agent packager
pushd cloudify-agent-packager
	git checkout agent-refactoring-project
	sudo pip install .
popd

# create agent
cfy-ap -c /vagrant/packager.yaml -f -v
