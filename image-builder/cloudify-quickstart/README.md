# Image Builder

Scenarios: 

1. Create Vagrant box locally by using Virtualbox (for Virtualbox Vagrant provider)
1. Create Vagrant box remotly by using AWS (for Virtualbox Vagrant provider)
1. Create Vagrant box remotly by using AWS (for AWS Vagrant provider)
1. Create Vagrant box locally by using HPCloud (for HPCloud Vagrant provider)

# Directory Structure
* `userdata` - contains userdata scripts for AWS machines 
* `templates` - templates files used for building
* `provision` - provisioning scripts used by Packer & Vagrant
* `keys` - insecure keys for Vagrant
* `cloudify-hpcloud` - Vagrant box creator for hpcloud


# How to use this
## Pre Requirements

1. Python (>=2.7):
  * Fabric
  * Boto
1. Packer
1. Virtualbox (for scenerio 1 & 4 only)
1. Vagrant (for scenerio 4 only):
  * hpcloud plugin
  
## Configuration files
Following is a bried description for every configuration file.
Note that you'll need to edit `settings.py` only for scenerio 2.

### settings.py
This file contains settings used by `nightly-builder.py` script. You'll need to configure it in case you want to build nightly Virtualbox image on AWS.
* `region` - The region where `nightly-builder` will launch its worker instance. This should be the same region as in Packer config.
* `username` - The username to use when connecting to worker instance. This depands on what instance you use. Usually `ubuntu` for Ubuntu AMIs.
* `aws_s3_bucket` - S3 bucket name where nightlies should be uploaded to.
* `aws_iam_group` - IAM group for worker instance (see below).
* `factory_ami` - Base AMI for worker instance.
* `instance_type` - Worker instance type (m3.medium, m3.large,...). Note that not all AMIs support all instance types.
* `packer_var_file` - Packer var file path. This is the `packer_inputs.json` file which used by Packer. 

### packer_inputs.json
This is input file for Packer. 
* `cloudify_release` - Release version number.
* `aws_source_ami` - Base AWS AMI.
* `components_package_url` - Components package url
* `core_package_url` - Core package url
* `ui_package_url` - UI package url
* `ubuntu_agent_url` - Ubuntu package url
* `centos_agent_url` - Centos agent url
* `windows_agent_url` - Windows agent url

### packerfile.json
Packer template file. It contains number of user variables defined in the top of the file (`variables` section). `packer_inputs.json` is the inputs file for these variables. Note that some variables are not passed via that file:
* `aws_access_key` - AWS key ID, taken from environment variable `AWS_ACCESS_KEY_ID`
* `aws_secret_key` - AWS Secret key, taken from environment variable `AWS_SECRET_ACCESS_KEY`
* `instance_type` - Instance type for the provisioning machine
* `virtualbox_source_image` - Source image (ovf) for when building local virtualbox image with Packer (without AWS)
* `insecure_private_key` - Path of Vagrant's default insecure private key

## AWS requirements
* Valid credentials - Your user must be able to launch/terminate instances, add/remove security groups and private keys
* AMI base image - This was tested with Ubuntu base image
* S3 bucket - S3 bucket where final images will be stored
* IAM group - An IAM group must be created for the worker instances with sufficient rights to upload into the S3 bucket.

## Running


