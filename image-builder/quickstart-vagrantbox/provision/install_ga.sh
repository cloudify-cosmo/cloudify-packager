#!/bin/bash

# update apt cache
sudo apt-get update

# install guest additions
sudo apt-get install -y dkms module-assistant
sudo m-a -i prepare
wget http://download.virtualbox.org/virtualbox/4.3.20/VBoxGuestAdditions_4.3.20.iso
sudo mkdir -p /mnt/iso
sudo sudo mount -o loop VBoxGuestAdditions_4.3.20.iso /mnt/iso/
sudo /mnt/iso/VBoxLinuxAdditions.run
sudo umount /mnt/iso
sudo rmdir /mnt/iso
rm VBoxGuestAdditions_4.3.20.iso
