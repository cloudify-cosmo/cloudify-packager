#!/bin/bash

#remove image
sudo docker images | grep centos_agent_build && sudo docker images --no-trunc | grep centos_agent_build | awk '{print $3}' | xargs sudo docker rmi

sudo docker build -t centos_agent_build --no-cache .
sudo docker run -t -d --name=centos_agent_build centos_agent_build
sudo docker cp centos_agent_build:/cloudify/ /
sudo docker rm -f centos_agent_build

echo Done! please check for file in /cloudify/*.deb
