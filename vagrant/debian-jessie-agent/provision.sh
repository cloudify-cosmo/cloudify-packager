core_tag_name="master"
plugins_tag_name="master"

#installed in debian image
#   update and install prereqs
#sudo apt-get -y update &&
#sudo apt-get install -y software-properties-common &&
#sudo add-apt-repository -y ppa:git-core/ppa &&
#sudo apt-get install -y rsync curl python-dev rpm git make gcc libyaml-dev zlib1g-dev g++ &&

#   install ruby
#wget https://ftp.ruby-lang.org/pub/ruby/ruby-1.9.3-rc1.tar.bz2 --no-check-certificate
#tar -xjf ruby-1.9.3-rc1.tar.bz2
#cd ruby-1.9.3-rc1
#./configure --disable-install-doc
#make
#sudo make install
#cd ~

#    install fpm and configure gem/bundler
#sudo gem install fpm --no-ri --no-rdoc &&
#echo -e 'gem: --no-ri --no-rdoc\ninstall: --no-rdoc --no-ri\nupdate:  --no-rdoc --no-ri' >> ~/.gemrc

# install pip
curl --silent --show-error --retry 5 https://bootstrap.pypa.io/get-pip.py | sudo python &&

# install packman
git clone https://github.com/cloudify-cosmo/packman.git
pushd packman
	git checkout -b tmp_branch $core_tag_name
	sudo pip install .
popd

# install virtualenv
sudo pip install virtualenv==1.11.4 &&

cd /cloudify-packager/ &&

# create package resources
sudo pkm get -c debian-jessie-agent &&

echo '# GET PROCESS'
sudo /debian-agent/env/bin/pip install celery==3.1.17 &&
sudo /debian-agent/env/bin/pip install pyzmq==14.4.0
git clone https://github.com/cloudify-cosmo/cloudify-rest-client.git
pushd cloudify-rest-client
	git checkout -b tmp_branch $core_tag_name
	sudo /debian-agent/env/bin/pip install .
popd
git clone https://github.com/cloudify-cosmo/cloudify-plugins-common.git
pushd cloudify-plugins-common
	git checkout -b tmp_branch $core_tag_name
	sudo /debian-agent/env/bin/pip install .
popd
git clone https://github.com/cloudify-cosmo/cloudify-script-plugin.git
pushd cloudify-script-plugin
	git checkout -b tmp_branch $plugins_tag_name
	sudo /debian-agent/env/bin/pip install .
popd
git clone https://github.com/cloudify-cosmo/cloudify-diamond-plugin.git
pushd cloudify-diamond-plugin
	git checkout -b tmp_branch $plugins_tag_name
	sudo /debian-agent/env/bin/pip install .
popd
git clone https://github.com/cloudify-cosmo/cloudify-manager.git
pushd cloudify-manager
	git checkout -b tmp_branch $core_tag_name
	pushd plugins/plugin-installer
	  sudo /debian-agent/env/bin/pip install .
	popd
	pushd plugins/agent-installer
	  sudo /debian-agent/env/bin/pip install .
	popd
	pushd plugins/windows-agent-installer
	  sudo /debian-agent/env/bin/pip install .
	popd
	pushd plugins/windows-plugin-installer
	  sudo /debian-agent/env/bin/pip install .
	popd
popd

# create package
sudo pkm pack -c debian-jessie-agent &&
sudo pkm pack -c cloudify-debian-jessie-agent &&

echo bootstrap done
echo "NOTE: currently, using some of the packman's features requires that it's run as sudo."
