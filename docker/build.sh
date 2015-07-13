#! /bin/bash -e

PACKAGER_DOCKER_PATH=$1/docker
if [ -z $1 ]
  then
    echo "No arguments supplied. Using default"
    PACKAGER_DOCKER_PATH=$(pwd)
fi

setup_jocker_env()
{
  sudo pip install virtualenv
  virtualenv docker_build_env
  source docker_build_env/bin/activate && \
  pip install git+https://github.com/nir0s/jocker.git
}

# $1 - docker image name
build_cloudify_image()
{
  # docker build sometimes failes for no reason. Retry
  for i in 1 2 3 4 5
  do sudo docker build -t $1 $PACKAGER_DOCKER_PATH && break || sleep 2; done
}

build_image()
{
  DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
  setup_jocker_env
  jocker -t $PACKAGER_DOCKER_PATH/Dockerfile.template -o $PACKAGER_DOCKER_PATH/Dockerfile -f $PACKAGER_DOCKER_PATH/vars.py
  echo Building cloudify OSS stack image.
  build_cloudify_image cloudify:latest
  jocker -t $PACKAGER_DOCKER_PATH/Dockerfile-commercial.template -o $PACKAGER_DOCKER_PATH/Dockerfile -f $PACKAGER_DOCKER_PATH/vars.py
  echo Building cloudify commercial stack image.
  build_cloudify_image cloudify-commercial:latest
}

main()
{
  build_image
}

main