#! /bin/bash -e

PACKAGER_DOCKER_PATH=$1/docker
PLUGINS_BRANCH=$2
CORE_BRANCH=$3

if [ -z $1 ]
  then
    echo "No arguments supplied. Using default"
    PACKAGER_DOCKER_PATH=$(pwd)
fi

# $1 - docker image name
build_cloudify_image()
{
  # docker build sometimes failes for no reason. Retry
  for i in 1 2 3 4 5
  do sudo docker build -t $1 $PACKAGER_DOCKER_PATH && break || sleep 2; done
}

modify_dockerfiles()
{
  FILES=$(find cloudify-packager/ -name "Dockerfile" -print)
  for file in $FILES
  do
    sed -i 's/DSL_VERSION=master/DSL_VERSION='"$CORE_BRANCH"'/g' $file
    sed -i 's/REST_CLIENT_VERSION=master/DSL_REST_CLIENT_VERSION='"$CORE_BRANCH"'/g' $file
    sed -i 's/COMMON_VERSION=master/COMMON_VERSION='"$CORE_BRANCH"'/g' $file
    sed -i 's/MANAGER_VERSION=master/MANAGER_VERSION='"$CORE_BRANCH"'/g' $file
    sed -i 's/REST_VERSION=master/REST_VERSION='"$CORE_BRANCH"'/g' $file
    sed -i 's/SCRIPT_VERSION=master/SCRIPT_VERSION='"$PLUGINS_BRANCH"'/g' $file
  done

}

build_image()
{
  DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
  modify_dockerfiles $PLUGINS_BRANCH $CORE_BRANCH
  echo Building cloudify stack image.
  build_cloudify_image cloudify_images:latest
}

main() 
{
  build_image
}

main