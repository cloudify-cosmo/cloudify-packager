#! /bin/bash -e

PACKAGER_DOCKER_PATH=$1/docker
PLUGINS_BRANCH=$2
CORE_BRANCH=$3

if [ -z $1 ]
  then
    echo "No arguments supplied. Using default"
    PACKAGER_DOCKER_PATH=$(pwd)
fi

build_cloudify_image()
{
  pushd $PACKAGER_DOCKER_PATH
  echo building javabase image
  for i in 1 2 3 4 5
  do
    sudo docker-compose -p cloudify build javabase && break || sleep 2;
  done
  echo building pythonbase image
  for i in 1 2 3 4 5
  do
    sudo docker-compose -p cloudify build pythonbase && break || sleep 2;
  done
  # docker build sometimes fails. Retry
  for i in 1 2 3 4 5 6
  do
    sudo docker-compose -p cloudify build && break || sleep 2;
  done
  popd
}

modify_dockerfiles()
{
  FILES=$(find /tmp/cloudify-packager -name "Dockerfile" -print)
  for file in $FILES
  do
    sed -i 's/DSL_VERSION=master/DSL_VERSION='"$CORE_BRANCH"'/g' $file
    sed -i 's/REST_CLIENT_VERSION=master/REST_CLIENT_VERSION='"$CORE_BRANCH"'/g' $file
    sed -i 's/COMMON_VERSION=master/COMMON_VERSION='"$CORE_BRANCH"'/g' $file
    sed -i 's/MANAGER_VERSION=master/MANAGER_VERSION='"$CORE_BRANCH"'/g' $file
    sed -i 's/REST_VERSION=master/REST_VERSION='"$CORE_BRANCH"'/g' $file
    sed -i 's/AMQP_INFLUX_VERSION=master/AMQP_INFLUX_VERSION='"$CORE_BRANCH"'/g' $file
    sed -i 's/WEBUI_VERSION=master/WEBUI_VERSION='"$CORE_BRANCH"'/g' $file
    sed -i 's/SCRIPT_VERSION=master/SCRIPT_VERSION='"$PLUGINS_BRANCH"'/g' $file
  done

}

enable_docker_api()
{
  sudo /bin/sh -c 'echo DOCKER_OPTS=\"-H tcp://127.0.0.1:4243 -H unix:///var/run/docker.sock\" >> /etc/default/docker'
  sudo restart docker
  export DOCKER_HOST=tcp://localhost:4243
}

build_image()
{
  DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
  modify_dockerfiles $PLUGINS_BRANCH $CORE_BRANCH
  enable_docker_api
  echo Building cloudify stack image.
  build_cloudify_image
}

main() 
{
  build_image
}

main