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
		# centos/REHL
		sudo yum -y update
		sudo yum install curl python-devel make gcc git libyaml-devel -y
	else
		echo 'unsupported package manager, exiting'
		exit 1
	fi
}

function clone {
	repo=$1
	sha=$2
	org=${3:-cloudify-cosmo}
	url=https://github.com/${org}/${repo}.git

	echo cloning ${url}
	git clone ${url}
	pushd ${repo}
		if [ -n "$sha" ]; then
			git reset --hard $sha
		fi
	popd
}

function clone_repos {
	clone "cloudify-rest-client" "${REST_CLIENT_SHA}"
	clone "cloudify-plugins-common" "${COMMON_PLUGIN_SHA}"
	clone "cloudify-script-plugin" "${SCRIPTS_PLUGIN_SHA}"
	clone "cloudify-diamond-plugin" "${DIAMOND_PLUGIN_SHA}"
	clone "cloudify-agent-installer-plugin" "${AGENT_INSTALLER_SHA}" "iliapolo"
	clone "cloudify-plugin-installer-plugin" "${PLUGIN_INSTALLER_SHA}" "iliapolo"
	clone "cloudify-windows-agent-installer-plugin" "${WINDOWS_AGENT_INSTALLER_SHA}" "iliapolo"
	clone "cloudify-windows-plugin-installer-plugin" "${WINDOWS_PLUGIN_INSTALLER_SHA}" "iliapolo"
	clone "cloudify-agent" "${CLOUDIFY_AGENT_SHA}" "nir0s"
}

function install_virtualenv
{
	echo installing virtualenv
	sudo pip install virtualenv==1.11.4
}

function create_virtualenv
{
	venv = $1
	echo creating ${venv} virtualenv
	virtualenv ${venv}
	source ${venv}/bin/activate
}

function install_pip
{
	curl --silent --show-error --retry 5 https://bootstrap.pypa.io/get-pip.py | sudo python
}

function install_agent_packager
{
	clone "cloudify-agent-packager" "${AGENT_PACKAGER_SHA}"
	pushd cloudify-agent-packager
		git checkout agent-refactoring-project
		sudo pip install .
	popd
}

AGENT_PACKAGER_SHA=""
REST_CLIENT_SHA=""
COMMON_PLUGIN_SHA=""
SCRIPT_PLUGIN_SHA=""
DIAMOND_PLUGIN_SHA=""
AGENT_INSTALLER_SHA=""
PLUGIN_INSTALLER_SHA=""
WINDOWS_AGENT_INSTALLER_SHA=""
WINDOWS_PLUGIN_INSTALLER_SHA=""
CLOUDIFY_AGENT_SHA=""

install_deps

cd ~
install_pip
install_virtualenv
create_virtualenv "agent-packager"

cd /tmp
clone_repos
install_agent_packager
cfy-ap -c /vagrant/packager.yaml -f -v
