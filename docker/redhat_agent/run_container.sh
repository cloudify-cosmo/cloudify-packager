#!/bin/bash

#remove image
sudo docker images | grep redhat_agent_build && sudo docker images --no-trunc | grep redhat_agent_build | awk '{print $3}' | xargs sudo docker rmi

sudo docker build -t redhat_agent_build --no-cache .
sudo docker run -t -d --name=redhat_agent_build redhat_agent_build
sudo docker cp redhat_agent_build:/cloudify/ /
sudo docker rm -f redhat_agent_build

echo Done! please check for file in /cloudify/cloudify-redhat-agent_3.1.0_amd64.deb
