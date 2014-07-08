echo bootstrapping packman...

# update and install prereqs
sudo apt-get -y update &&
sudo apt-get install -y curl python-dev rubygems rpm &&

# install fpm and configure gem/bundler
sudo gem install fpm --no-ri --no-rdoc &&
echo -e 'gem: --no-ri --no-rdoc\ninstall: --no-rdoc --no-ri\nupdate:  --no-rdoc --no-ri' >> ~/.gemrc
echo -e 'gem: --no-ri --no-rdoc\ninstall: --no-rdoc --no-ri\nupdate:  --no-rdoc --no-ri' >> /root/.gemrc

# install pip
curl --silent --show-error --retry 5 https://bootstrap.pypa.io/get-pip.py | sudo python

# install virtualenv
sudo pip install virtualenv==1.11.4 &&

# install packman
sudo pip install https://github.com/cloudify-cosmo/packman/archive/develop.tar.gz

# TODO: add virtualenv to provisioning process
# sudo pip install virtualenvwrapper
# mkvirtualenv packman
# TODO: add bash completion support using docopt-completion
# docopt-completion #VIRTUALENV#...pkm.py?

echo bootstrap done
echo NOTE: currently, using some of the packman's features requires that it's run as sudo.
