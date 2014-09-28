echo bootstrapping...

# update and install prereqs
sudo yum -y update &&
sudo yum install yum-downloadonly wget mlocate yum-utils python-devel libyaml-devel ruby rubygems ruby-devel -y

# install fpm
sudo gem install fpm --no-rdoc --no-ri

# configure gem and bundler
echo -e 'gem: --no-ri --no-rdoc\ninstall: --no-rdoc --no-ri\nupdate:  --no-rdoc --no-ri' >> ~/.gemrc
echo -e 'gem: --no-ri --no-rdoc\ninstall: --no-rdoc --no-ri\nupdate:  --no-rdoc --no-ri' >> /root/.gemrc

# install python and additions
# http://bicofino.io/blog/2014/01/16/installing-python-2-dot-7-6-on-centos-6-dot-5/
sudo yum groupinstall -y 'development tools'
sudo yum install -y zlib-devel bzip2-devel openssl-devel xz-libs
sudo mkdir /py27
cd /py27
sudo wget http://www.python.org/ftp/python/2.7.6/Python-2.7.6.tar.xz
sudo xz -d Python-2.7.6.tar.xz
sudo tar -xvf Python-2.7.6.tar
cd Python-2.7.6
sudo ./configure --prefix=/usr
sudo make
sudo make altinstall

# install pip
cd /py27
sudo wget https://raw.github.com/pypa/pip/master/contrib/get-pip.py &&
sudo /usr/bin/python2.7 get-pip.py &&

# install virtualenv
sudo /usr/bin/pip2.7 install virtualenv==1.11.4 &&

# install packman
sudo /usr/bin/pip2.7 install https://github.com/cloudify-cosmo/packman/archive/develop.tar.gz

# create cloudify components package
cd /home/vagrant/cloudify-packager/ &&

# create package resources
sudo pkm get -c manager
sudo pkm get -c celery

# LIMOR, PLEASE COMPLETE THE GET PROCESS HERE

# create package
sudo pkm pack -c manager
sudo pkm pack -c celery
sudo pkm pack -c cloudify-core

echo bootstrap done
echo NOTE: currently, using some of the packman's features requires that it's run as sudo.
