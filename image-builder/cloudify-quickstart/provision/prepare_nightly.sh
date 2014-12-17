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
sudo apt-get install -y virtualbox-guest-utils