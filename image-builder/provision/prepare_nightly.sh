#!/bin/bash

# change partition uuid
sudo apt-get -f -y install
sudo apt-get install -y uuid
sudo tune2fs /dev/xvda1 -U `uuid`

# disable cloud-init datasource retries
echo 'datasource_list: [ None ]' | sudo -s tee /etc/cloud/cloud.cfg.d/90_dpkg.cfg
sudo dpkg-reconfigure -f noninteractive cloud-init

# disable ttyS0
echo manual | sudo tee /etc/init/ttyS0.override

# install guest additions
sudo apt-get install -y module-assistant
sudo m-a -i prepare
wget http://download.virtualbox.org/virtualbox/4.3.20/VBoxGuestAdditions_4.3.20.iso
sudo mkdir -p /mnt/iso
sudo sudo mount -o loop VBoxGuestAdditions_4.3.20.iso /mnt/iso/
sudo /mnt/iso/VBoxLinuxAdditions.run
sudo umount /mnt/iso
sudo rmdir /mnt/iso
rm VBoxGuestAdditions_4.3.20.iso

# change hostname
echo cloudify | sudo -S tee /etc/hostname
echo 127.0.0.1 cloudify | sudo -S tee -a /etc/hosts

# change dns resolver to 8.8.8.8
# this is done so docker won't start with AWS dns resolver
echo nameserver 8.8.8.8 | sudo -S tee /etc/resolv.conf
