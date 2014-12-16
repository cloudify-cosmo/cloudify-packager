#!/bin/bash

sudo apt-get -f -y install
sudo apt-get install -y uuid
sudo rm /etc/cloud/cloud.cfg.d/90_dpkg.cfg
#sudo e2label /dev/xvda1 cloudify
sudo tune2fs /dev/xvda1 -U `uuid`
sudo dd if=/dev/zero of=/dev/xvda bs=446 count=1