function install_deps
{
	echo Installing necessary dependencies
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

function install_pip
{
	echo Installing pip
	curl --silent --show-error --retry 5 https://bootstrap.pypa.io/get-pip.py | sudo python
}

GITHUB_USERNAME=$1
GITHUB_PASSWORD=$2

install_deps

cd ~
install_pip &&
sudo pip install pip==6.0.8 --upgrade &&
sudo pip install virtualenv==12.0.7 &&
sudo pip install boto==2.36.0 &&
sudo rm -rf ~/.cache

# clone commercial plugins. this should be a feature in the agent-packager
git clone https://${GITHUB_USERNAME}:${GITHUB_PASSWORD}@github.com/cloudify-cosmo/cloudify-vsphere-plugin.git /tmp/cloudify-vsphere-plugin
git clone https://${GITHUB_USERNAME}:${GITHUB_PASSWORD}@github.com/cloudify-cosmo/cloudify-softlayer-plugin.git /tmp/cloudify-softlayer-plugin


# REPLACE branch before production
sudo pip install cloudify-agent-packager==3.5.0 &&
cd /tmp &&
cfy-ap -c /vagrant/packager.yaml -f -v
