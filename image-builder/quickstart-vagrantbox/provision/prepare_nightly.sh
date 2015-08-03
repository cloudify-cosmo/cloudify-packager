#!/bin/bash

# update apt cache
sudo apt-get update

# change partition uuid
sudo apt-get install -y uuid
sudo tune2fs /dev/xvda1 -U `uuid`

# disable cloud-init datasource retries
echo 'datasource_list: [ None ]' | sudo -s tee /etc/cloud/cloud.cfg.d/90_dpkg.cfg
sudo dpkg-reconfigure -f noninteractive cloud-init

# disable ttyS0
echo manual | sudo tee /etc/init/ttyS0.override

# change hostname
echo cloudify | sudo -S tee /etc/hostname
echo 127.0.0.1 cloudify | sudo -S tee -a /etc/hosts

# change dns resolver to 8.8.8.8
# this is done so docker won't start with AWS dns resolver
echo nameserver 8.8.8.8 | sudo -S tee /etc/resolv.conf
