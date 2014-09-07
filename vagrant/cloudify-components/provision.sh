PACKMAN_SHA=""

# echo bootstrapping packman...

# update and install prereqs
sudo apt-get -y update &&
sudo apt-get install -y curl python-dev rubygems rpm libyaml-dev &&

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

# install pip
curl --silent --show-error --retry 5 https://bootstrap.pypa.io/get-pip.py | sudo python

# install packman
git clone https://github.com/cloudify-cosmo/packman.git
pushd packman
	if [ -n "$PACKMAN_SHA" ]; then
		git reset --hard $PACKMAN_SHA
	fi
	pip install .
popd

# download backup components file (WORKAROUND UNTIL PACKMAN BUG IS FIXED)
cd ~
sudo wget http://gigaspaces-repository-eu.s3.amazonaws.com/org/cloudify3/static_components/static_components.tar.gz &&
sudo tar -xzvf static_components.tar.gz -C / &&

# TODO temp workaround, Need Nir's help with this process
sudo rm -rf /cloudify-components/riemann

# create cloudify components package
cd /cloudify-packager/ &&
sudo pkm make -c elasticsearch,logstash,langohr,riemann,grafana,influxdb
sudo pkm pack -c cloudify-components

echo bootstrap done
echo NOTE: currently, using some of the packman's features requires that it's run as sudo.
