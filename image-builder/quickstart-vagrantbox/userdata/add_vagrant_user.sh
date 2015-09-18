#!/bin/bash

# add vagrant user and public key
useradd -m -s /bin/bash -U -G wheel,adm,systemd-journal vagrant
echo 'vagrant ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/99-vagrant
chmod 0440 /etc/sudoers.d/99-vagrant
curl -L --silent --create-dirs https://raw.githubusercontent.com/mitchellh/vagrant/master/keys/vagrant.pub -o /home/vagrant/.ssh/authorized_keys
chown -R vagrant:vagrant /home/vagrant/
chmod 0700 /home/vagrant/.ssh/
chmod 0600 /home/vagrant/.ssh/authorized_keys

# disable requiretty
sed -i -e 's/^Defaults.*requiretty/# Defaults requiretty/g' /etc/sudoers