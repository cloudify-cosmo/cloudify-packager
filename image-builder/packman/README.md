# Packman Image Builder

This allows generating a packman image using Packer to be used in our build processes.
It is meant to be generated manually per request.

We use packman to generate our Agent and CLI packages.

The provisioning script supports Debian, Ubuntu and CentOS (and potentially, RHEL) based images.
Currently, the image will be provisioned with the following:

* Build prerequisites such as gcc, g++, python-dev, etc..
* git
* fpm (and consequently, Ruby 1.9.3), for packman to generate packages
* Virtualenv and boto
* packman (hardcoded version. should be upgraded if needed)

The supplied packerfile currently generates images for:

* debian jessie
* Ubuntu precise
* Ubuntu trusty
* Centos 6.4

Note that all images are ebs backed - a prerequisite of baking them using Packer.