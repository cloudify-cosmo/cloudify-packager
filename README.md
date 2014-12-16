Cloudify-Packager
=================

Cloudify's packager provides tools and configuration objects we use to build Cloudify's Management environments, agents and demo images.

### [Docker](http://www.docker.com)

Please see [Bootstrapping using Docker](http://getcloudify.org/guide/3.1/installation-bootstrapping.html#bootstrapping-using-docker) for information on our transition from packages to container-based installations.

To generate our [Dockerfile.template](https://github.com/cloudify-cosmo/cloudify-packager/raw/master/docker/Dockerfile.template) file, we're using [Jocker](https://github.com/nir0s/jocker).

### [packman](http://packman.readthedocs.org) configuration

Package based provisioning will be deprecated in Cloudify 3.2!

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

Packer is used to create the demo Vagrant box for Cloudify's [Quickstart guide](http://getcloudify.org/guide/3.1/quickstart.html).