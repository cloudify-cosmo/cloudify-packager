echo bootstrapping packman...

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

# install virtualenv
sudo pip install virtualenv==1.11.4 &&