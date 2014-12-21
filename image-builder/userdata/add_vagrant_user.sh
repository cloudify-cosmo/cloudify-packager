#!/bin/bash

useradd -m -s /bin/bash -U vagrant
adduser vagrant admin
echo 'vagrant ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/99-vagrant
chmod 0440 /etc/sudoers.d/99-vagrant
mkdir -p /home/vagrant/.ssh/
wget https://raw.githubusercontent.com/mitchellh/vagrant/master/keys/vagrant.pub -O /home/vagrant/.ssh/authorized_keys
chown -R vagrant:vagrant /home/vagrant/
chmod 0700 /home/vagrant/.ssh/
chmod 0600 /home/vagrant/.ssh/authorized_keys