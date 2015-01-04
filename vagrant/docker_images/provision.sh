#! /bin/bash -e

PACKAGER_SHA=""

install_docker()
{
  curl -sSL https://get.docker.com/ubuntu/ | sudo sh
}

setup_jocker_env()
{
  sudo apt-get install python-pip
  sudo pip install git+https://github.com/nir0s/jocker.git
}

clone_packager()
{
  git clone https://github.com/cloudify-cosmo/cloudify-packager.git $1
  pushd $1/cloudify-packager
	  if [ -n "PACKAGER_SHA" ]; then
		  git reset --hard $PACKAGER_SHA
	  fi
  popd
}

# $1 - path to dockerfile folder
# $2 - docker build command
build_image()
{
  pushd $1
  # docker build sometimes failes for no reason. Retry 
  for i in 1 2 3 4 5 
  do sudo docker build -t $2 . && break || sleep 2; done
  popd
}

build_images()
{
  CLONE_LOCATION=/tmp/cloudify-packager
  clone_packager $CLONE_LOCATION
  setup_jocker_env
  jocker -t $CLONE_LOCATION/docker/Dockerfile.template -o $CLONE_LOCATION/docker/Dockerfile -f $CLONE_LOCATION/docker/vars.py
  echo Building cloudify stack image.
  build_image $CLONE_LOCATION/docker cloudify:latest
}

start_and_export_containers()
{
  sudo docker run -t --name=cloudify -d cloudify:latest /bin/bash
  sudo docker export cloudify > /tmp/coudify-docker_3.1.0-ga-b85.tar
}

main() 
{
  install_docker
  build_images
  start_and_export_containers
}

main
