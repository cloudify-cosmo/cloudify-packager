#! /bin/bash -e

PACKAGER_SHA=""
PLUGINS_BRANCH=master
CORE_BRANCH=master

install_docker()
{
  curl -sSL https://get.docker.com/ubuntu/ | sudo sh
}

prepare_env()
{
  echo installing pip and virtualenv
  sudo apt-get install -y python-pip python-virtualenv

  echo create new virtualenv
  virtualenv /tmp/env
  source /tmp/env/bin/activate

  echo installing docker compose
  pip install docker-compose

  echo exposing docker api
  sudo /bin/sh -c 'echo DOCKER_OPTS=\"-H tcp://127.0.0.1:4243 -H unix:///var/run/docker.sock\" >> /etc/default/docker'
  sudo restart docker
  export DOCKER_HOST=tcp://localhost:4243
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
  echo cloning packager to $CLONE_LOCATION
  clone_packager $CLONE_LOCATION

  echo preparing environment, installing all components
  prepare_env

  echo Building cloudify stack image.
  pushd $CLONE_LOCATION
    git checkout CFY-1838-separate-services-container-to-service-specific-containers
    source /docker/build.sh $CLONE_LOCATION $PLUGINS_BRANCH $CORE_BRANCH
  popd
}

save_images()
{
  sudo docker save cloudify_restservice \
                   cloudify_amqpinflux \
                   cloudify_riemann \
                   cloudify_mgmtworker \
                   cloudify_frontend \
                   cloudify_logstash \
                   cloudify_elasticsearch \
                   cloudify_rabbitmq \
                   cloudify_influxdb \
                   cloudify_webui \
                   cloudify_fileserver > $1
}

main()
{
  install_docker
  build_images
  save_images /tmp/cloudify_images.tar
}

main
