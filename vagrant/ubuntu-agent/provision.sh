REST_CLIENT_SHA=""
COMMON_PLUGIN_SHA=""
MANAGER_SHA=""
PACKMAN_SHA=""
SCRIPTS_PLUGIN_SHA=""
DIAMOND_PLUGIN_SHA=""

# echo bootstrapping packman...

# update and install prereqs
sudo add-apt-repository ppa:git-core/ppa &&
sudo apt-get -y update &&
sudo apt-get install -y curl python-dev rubygems rpm git &&

# install ruby
wget ftp://ftp.ruby-lang.org/pub/ruby/1.9/ruby-1.9.3-p547.tar.bz2
tar -xjf ruby-1.9.3-p547.tar.bz2
cd ruby-1.9.3-p547
./configure --disable-install-doc
make
sudo make install
cd ~

# install fpm and configure gem/bundler
sudo gem install fpm --no-ri --no-rdoc &&
echo -e 'gem: --no-ri --no-rdoc\ninstall: --no-rdoc --no-ri\nupdate:  --no-rdoc --no-ri' >> ~/.gemrc

# install pip
curl --silent --show-error --retry 5 https://bootstrap.pypa.io/get-pip.py | sudo python

# install packman
git clone https://github.com/cloudify-cosmo/packman.git
pushd packman
	if [ -n "$PACKMAN_SHA" ]; then
		git reset --hard $PACKMAN_SHA
	fi
	sudo pip install .
popd

# install virtualenv
sudo pip install virtualenv==1.11.4 &&

cd /cloudify-packager/ &&

# create package resources
sudo pkm get -c Ubuntu-agent

echo '# GET PROCESS'
sudo /Ubuntu-agent/env/bin/pip install celery==3.0.24
sudo /Ubuntu-agent/env/bin/pip install pyzmq==14.3.1
git clone https://github.com/cloudify-cosmo/cloudify-rest-client.git
pushd cloudify-rest-client
	if [ -n "$REST_CLIENT_SHA" ]; then
		git reset --hard $REST_CLIENT_SHA
	fi
	sudo /Ubuntu-agent/env/bin/pip install .
popd
git clone https://github.com/cloudify-cosmo/cloudify-plugins-common.git
pushd cloudify-plugins-common
	if [ -n "$COMMON_PLUGIN_SHA" ]; then
		git reset --hard $COMMON_PLUGIN_SHA
	fi
	sudo /Ubuntu-agent/env/bin/pip install .
popd
git clone https://github.com/cloudify-cosmo/cloudify-script-plugin.git
pushd cloudify-script-plugin
	if [ -n "$SCRIPTS_PLUGIN_SHA" ]; then
		git reset --hard $SCRIPTS_PLUGIN_SHA
	fi
	sudo /Ubuntu-agent/env/bin/pip install .
popd
git clone https://github.com/cloudify-cosmo/cloudify-diamond-plugin.git
pushd cloudify-diamond-plugin
	if [ -n "$DIAMOND_PLUGIN_SHA" ]; then
		git reset --hard $DIAMOND_PLUGIN_SHA
	fi
	sudo /Ubuntu-agent/env/bin/pip install .
popd
git clone https://github.com/cloudify-cosmo/cloudify-manager.git
pushd cloudify-manager
	if [ -n "$MANAGER_SHA" ]; then
		git reset --hard $MANAGER_SHA
	fi
	pushd plugins/plugin-installer
	  sudo /Ubuntu-agent/env/bin/pip install .
	popd
	pushd plugins/agent-installer
	  sudo /Ubuntu-agent/env/bin/pip install .
	popd
	pushd plugins/windows-agent-installer
	  sudo /Ubuntu-agent/env/bin/pip install .
	popd
	pushd plugins/windows-plugin-installer
	  sudo /Ubuntu-agent/env/bin/pip install .
	popd
popd

# create package
sudo pkm pack -c Ubuntu-agent
sudo pkm pack -c cloudify-ubuntu-agent

echo bootstrap done
echo "NOTE: currently, using some of the packman's features requires that it's run as sudo."
