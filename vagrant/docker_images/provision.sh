#! /bin/bash -e

PACKAGER_SHA=""

install_docker()
{
  curl -sSL https://get.docker.com/ubuntu/ | sudo sh
}

setup_jocker_env()
{
  sudo apt-get install -y python-pip
}

clone_packager()
{
  git clone https://github.com/cloudify-cosmo/cloudify-packager.git $1
  pushd $1
          if [ -n "PACKAGER_SHA" ]; then
                  git reset --hard $PACKAGER_SHA
          fi
  popd
}

build_images()
{
  CLONE_LOCATION=/tmp/cloudify-packager
  clone_packager $CLONE_LOCATION
  setup_jocker_env
  echo Building cloudify stack image.
  pushd $CLONE_LOCATION
  ./docker/build.sh $CLONE_LOCATION
  popd
}

start_and_export_containers()
{
  sudo docker run -t --name=cloudify -d cloudify:latest /bin/bash
  sudo docker export cloudify > /tmp/cloudify-docker_.tar
}

main() 
{
  install_docker
  build_images
  start_and_export_containers
}

main
