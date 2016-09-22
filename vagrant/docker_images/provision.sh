#! /bin/bash -e

CORE_TAG_NAME="4.0m3"


install_docker()
{
  export DEBIAN_FRONTEND=noninteractive
  kern_extras="linux-image-extra-$(uname -r) linux-image-extra-virtual"
  sudo apt-get update
  sudo -E apt-get install -y -q $kern_extras
  sudo modprobe aufs

  sudo apt-get install -y -q curl ca-certificates
  sudo apt-get install -y -q apt-transport-https ca-certificates

  sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 36A1D7869245C8950F966E92D8576A8BA88D21E9
  echo deb https://get.docker.com/ubuntu docker main | sudo tee /etc/apt/sources.list.d/docker.list
  sudo apt-get update
  sudo apt-get install -y lxc-docker-1.6.0
}

setup_jocker_env()
{
  sudo apt-get install -y python-pip
}

clone_packager()
{
  git clone https://github.com/cloudify-cosmo/cloudify-packager.git $1
  pushd $1
          git checkout -b tmp_branch $CORE_TAG_NAME
    			git log -1
  popd
}

build_images()
{
  CLONE_LOCATION=/tmp/cloudify-packager
  clone_packager $CLONE_LOCATION
  cp /cloudify-packager/docker/metadata/* /tmp/cloudify-packager/docker/metadata/
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
  sudo docker run -t --name=cloudifycommercial -d cloudify-commercial:latest /bin/bash
  sudo docker export cloudifycommercial > /tmp/cloudify-docker_commercial.tar
}

main()
{
  install_docker
  build_images
  start_and_export_containers
}

main
