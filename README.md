Cloudify-Packager
=================

Cloudify's packager provides tools and configuration objects we use to build Cloudify's Management environments, agents and demo images.

NOTE: We are now transitioning from a Package based setup to a Docker container based setup for our Management Environment. You can follow [this](https://github.com/cloudify-cosmo/cloudify-packager-ubuntu/tree/CFY-1308-run-cloudify-on-one-docker-container) to see the progress.

### [packman](http://packman.readthedocs.org) configuration

Packman is used to generate Cloudify's packages.
This repository contains packman's configuration for creating the packages.

#### package-configuration

The package-configuration folder contains the init scripts and configuration files for Cloudify's management environment components.

#### package-templates

The package-templates folder contains the bootstrap scripts that are used to install Cloudify's management environment.

#### packages.py

The packages.py file is the base packman configuration file containing the configuration of the entire stack (including agents).

### [Vagrant](http://www.vagrantup.com)

Cloudify's packages are created using vagrant VM's (currently on AWS).

The Vagrant folder contains vagrant configuration for different components that are generated using packman:

- A Vagrant VM is initialized.
- Packman is installed on the machine alongside its requirements.
- If a virtualenv is required, it is created and the relevant modules are installed in it.
- Packman is used to create the environment into which the components are retrieved.
- Packman is used to create the package.

NOTE: the Windows Agent Vagrantfile uses a premade image already containing the basic requirements for creating the Windows agent.

### [Packer](http://www.packer.io)

Currently, we only use packer to create the demo Vagrant box for Cloudify's [Quickstart guide](http://getcloudify.org/guide/3.1/quickstart.html).

Soon, we will also use packer to:
- Create the same demo image on AWS (and potentially, Openstack).
- Create base images for our package creation process.

### [Docker](http://www.docker.com)

Please see [Bootstrapping using Docker](http://getcloudify.org/guide/3.1/installation-bootstrapping.html#bootstrapping-using-docker) for information on our transition from packages to containers based installations.

To generate our [Dockerfile.template](https://github.com/cloudify-cosmo/cloudify-packager/raw/master/docker/Dockerfile.template) file, we're using [Jocker](https://github.com/nir0s/jocker).