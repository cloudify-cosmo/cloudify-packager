


#! /bin/bash -e

install_docker()
{
  curl -sSL https://get.docker.com/ubuntu/ | sudo sh
}

clone_packager()
{
  git clone https://github.com/cloudify-cosmo/cloudify-packager.git $1
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
  clone_packager /tmp/cloudify-packager
  echo Building cloudify stack image.
  build_image /tmp/cloudify-packager/docker cloudify:latest
  echo Building cloudify data image.
  build_image /tmp/cloudify-packager/docker/data_container data:latest
}

start_and_export_containers()
{
  sudo docker run -t --name=cloudify -d cloudify:latest /bin/bash
  sudo docker run -t -d --name data data /bin/bash
  sudo docker export cloudify > /tmp/coudify-docker_3.1.0-ga-b85.tar
  sudo docker export data > /tmp/cloudify-docker-data_3.1.0-ga-b85.tar
}

main() 
{
  install_docker
  build_images
  start_and_export_containers
}

main
