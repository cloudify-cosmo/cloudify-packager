# Docker Image Builder

This allows generating a Docker image using Packer to be used in our build processes.
It is meant to be generated manually per request.

Currently, the image will be provisioned with the following:

* Docker (version not hardcoded)
* docker-compose (Docker's API will be exposed for docker-compose to work)
* boto