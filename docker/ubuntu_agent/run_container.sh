#!/bin/bash

sudo docker build -t ubuntu_agent_build .
sudo docker run -t -d --name=ubuntu_agent_build ubuntu_agent_build
sudo docker cp ubuntu_agent_build:/cloudify/ /
sudo docker rm -f ubuntu_agent_build

echo Done! please check for file in /cloudify/cloudify-trusty-agent_3.1.0_amd64.deb
