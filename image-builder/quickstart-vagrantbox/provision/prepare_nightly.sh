#!/bin/bash

# update all packages
sudo yum update -y

# change hostname
echo cloudify | sudo -S tee /etc/hostname
echo 127.0.0.1 cloudify | sudo -S tee -a /etc/hosts

# disable predictable interface names
sudo sed -i -re 's#GRUB_CMDLINE_LINUX="(.*?)"#GRUB_CMDLINE_LINUX="\1 net.ifnames=0"#' /etc/default/grub
sudo grub2-mkconfig -o /boot/grub2/grub.cfg

# remove cloud-init
sudo yum remove -y cloud-init

# disable selinux
sudo setenforce 0
sudo sed -ri 's/SELINUX=.+/SELINUX=disabled/' /etc/selinux/config
