#!/bin/bash

# install kernel devel
sudo yum install -y gcc kernel-devel bzip2

# install guest additions
curl -LO http://download.virtualbox.org/virtualbox/4.3.20/VBoxGuestAdditions_4.3.20.iso
sudo mount -o loop VBoxGuestAdditions_4.3.20.iso /mnt/
sudo /mnt/VBoxLinuxAdditions.run
sudo umount /mnt/
rm VBoxGuestAdditions_4.3.20.iso
