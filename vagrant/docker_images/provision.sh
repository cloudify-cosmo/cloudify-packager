#! /bin/bash -e

PACKAGER_SHA=""
PLUGINS_BRANCH=master
CORE_BRANCH=master

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
  ./docker/build.sh $CLONE_LOCATION $PLUGINS_BRANCH $CORE_BRANCH
  popd
}

main() 
{
  install_docker
  build_images
}

main
