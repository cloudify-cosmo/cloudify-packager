#!/bin/bash

sudo yum remove -y gcc
sudo yum autoremove
sudo yum clean all
sudo rm -rf /tmp/*