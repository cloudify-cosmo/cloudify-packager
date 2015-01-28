#!/bin/bash

# change partition uuid
sudo apt-get -f -y install
sudo apt-get install -y uuid
sudo tune2fs /dev/xvda1 -U `uuid`

# disable cloud-init datasource retries
printf "%s\t%s\t%s\t%s\n" \
    cloud-init cloud-init/datasources multiselect "None" | \
       sudo debconf-set-selections
DEBIAN_FRONTEND=noninteractive sudo -E dpkg-reconfigure cloud-init

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
echo 127.0.0.1 cloudify | sudo -S tee /etc/hosts
