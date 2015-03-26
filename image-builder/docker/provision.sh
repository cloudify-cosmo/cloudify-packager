#! /bin/bash -e

function install_docker
{
  curl -sSL https://get.docker.com/ubuntu/ | sudo sh
}

function install_docker_compose
{
  echo installing docker compose
  # docker-compose requires requests in version 2.2.1. will probably change.
  sudo pip install requests==2.2.1 --upgrade
  sudo pip install docker-compose==1.1.0

  echo exposing docker api
  sudo /bin/sh -c 'echo DOCKER_OPTS=\"-H tcp://127.0.0.1:4243 -H unix:///var/run/docker.sock\" >> /etc/default/docker'
  sudo restart docker
  export DOCKER_HOST=tcp://localhost:4243
}

function install_pip
{
  echo installing pip
  curl --silent --show-error --retry 5 https://bootstrap.pypa.io/get-pip.py | sudo python
}

function install_boto
{
  echo installing boto
  sudo pip install boto==2.36.0

}

install_docker
install_pip
install_boto
install_docker_compose
