function install_prereqs
{
	if which apt-get; then
		# ubuntu
		sudo apt-get -y update &&
		# precise
		sudo apt-get install -y python-software-properties ||
		# trusty
		sudo apt-get install -y software-properties-common &&
		sudo add-apt-repository -y ppa:git-core/ppa &&
		sudo apt-get install -y curl python-dev git make gcc libyaml-dev zlib1g-dev g++
	elif which yum; then
		# centos/REHL
		sudo yum -y update &&
		sudo yum install -y yum-downloadonly wget mlocate yum-utils &&
		sudo yum install -y python-devel libyaml-devel ruby rubygems ruby-devel make gcc git g++
		# this is required to build pyzmq under centos/RHEL
		sudo yum install -y zeromq-devel -c http://download.opensuse.org/repositories/home:/fengshuo:/zeromq/CentOS_CentOS-6/home:fengshuo:zeromq.repo
	else
		echo 'unsupported package manager, exiting'
		exit 1
	fi
}

function install_ruby
{
	wget https://ftp.ruby-lang.org/pub/ruby/ruby-1.9.3-rc1.tar.bz2 --no-check-certificate
	tar -xjf ruby-1.9.3-rc1.tar.bz2
	cd ruby-1.9.3-rc1
	./configure --disable-install-doc
	make
	sudo make install
	cd ~
}

function install_fpm
{
	sudo gem install fpm --no-ri --no-rdoc
	# if we want to downlod gems as a part of the packman run, this should be enabled
	# echo -e 'gem: --no-ri --no-rdoc\ninstall: --no-rdoc --no-ri\nupdate:  --no-rdoc --no-ri' >> ~/.gemrc
}

function install_pip
{
	curl --silent --show-error --retry 5 https://bootstrap.pypa.io/get-pip.py | sudo python
	sudo pip install boto
}

function install_module
{

	module=$1
	venv=${2:-""}
	tag=${3:-""}
	user=${4:-""}
	pass=${5:-""}
	if [[ ! -z "$tag" ]]; then
		org=${6:-cloudify-cosmo}
		if [[ ! -z "$user" ]]; then
			url=https://${user}:${pass}@github.com/${org}/${module}.git
		else
			url=https://github.com/${org}/${module}.git
		fi
		echo cloning ${url}
		git clone ${url}
		pushd ${module}
			git checkout -b tmp_branch ${tag}
			git log -1
			sudo ${venv}/bin/pip install .
		popd
	else
		if [[ ! -z "$venv" ]]; then
			# if [[ ! -z "$tag" ]]; then
			#	pip install git+git://github.com/${org}/${module}.git@${tag}#egg=${module}
			# else
			sudo ${venv}/bin/pip install ${module}
			# fi
		else
			sudo pip install ${module}
		fi
	fi
}

function install_manager_modules
{
	module=$1
	venv=$2
	tag=$3
	git clone https://github.com/cloudify-cosmo/${module}.git
	pushd cloudify-manager
		git checkout -b tmp_branch ${tag}
		git log -1
		pushd plugins/plugin-installer
		  sudo ${venv}/bin/pip install .
		popd
		pushd plugins/agent-installer
		  sudo ${venv}/bin/pip install .
		popd
		pushd plugins/windows-agent-installer
		  sudo ${venv}/bin/pip install .
		popd
		pushd plugins/windows-plugin-installer
		  sudo ${venv}/bin/pip install .
		popd
	popd
}

AGENT=$1
COMMERCIAL=$2
GITHUB_USERNAME=$3
GITHUB_PASSWORD=$4
CORE_TAG_NAME="master"
PLUGINS_TAG_NAME="master"

install_prereqs &&
install_ruby
install_fpm &&
install_pip &&
install_module "packman==0.5.0" &&
install_module "virtualenv==12.0.7" &&

cd /cloudify-packager/ &&

# create package resources
echo '# create package resources'
sudo pkm get -c ${AGENT}-agent &&

echo '# GET PROCESS'
# AGENT_VENV="/agent/env"
# we might not need this. it might suffice (considering the current implementation) to do /agent/env since
# the agent installer untars using --strip==1 anyway
if [ "${AGENT}" == "Ubuntu-trusty" ]; then
	AGENT_VENV="/Ubuntu-agent/env"
elif [ "${AGENT}" == "Ubuntu-precise" ]; then
	AGENT_VENV="/Ubuntu-agent/env"
elif [ "${AGENT}" == "centos-Final" ]; then
	AGENT_VENV="/centos-agent/env"
elif [ "${AGENT}" == "debian-jessie" ]; then
	AGENT_VENV="/debian-agent/env"
fi
install_module "celery==3.1.17" "${AGENT_VENV}" &&
install_module "pyzmq==14.4.0" "${AGENT_VENV}" &&
install_module "cloudify-rest-client" "${AGENT_VENV}" "${CORE_TAG_NAME}" &&
install_module "cloudify-plugins-common" "${AGENT_VENV}" "${CORE_TAG_NAME}" &&
install_module "cloudify-script-plugin" "${AGENT_VENV}" "${PLUGINS_TAG_NAME}" &&
install_module "cloudify-diamond-plugin" "${AGENT_VENV}" "${PLUGINS_TAG_NAME}" &&
if [ "${COMMERCIAL}" == "True" ]; then
	install_module "cloudify-vsphere-plugin" "${AGENT_VENV}" "${PLUGINS_TAG_NAME}" "${GITHUB_USERNAME}" "${GITHUB_PASSWORD}" &&
	install_module "cloudify-softlayer-plugin" "${AGENT_VENV}" "${PLUGINS_TAG_NAME}" "${GITHUB_USERNAME}" "${GITHUB_PASSWORD}"
fi
install_manager_modules "cloudify-manager" "${AGENT_VENV}" "${CORE_TAG_NAME}" &&

# create agent tar file
sudo pkm pack -c ${AGENT}-agent &&
# convert agent name to lower case and create deb/rpm
AGENT_ID=$(echo ${AGENT} | tr '[:upper:]' '[:lower:]')
sudo pkm pack -c cloudify-${AGENT_ID}-agent
