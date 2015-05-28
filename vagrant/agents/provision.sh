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

install_deps

cd ~
install_pip &&
sudo pip install pip==7.0.1 --upgrade &&
sudo pip install virtualenv==12.0.7 &&
sudo pip install boto==2.36.0 &&

# REPLACE branch before production
sudo pip install git+https://github.com/cloudify-cosmo/cloudify-agent-packager@agent-refactoring-project &&
cd /tmp &&
cfy-ap -c /vagrant/packager.yaml -f -v
