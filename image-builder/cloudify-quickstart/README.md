# Image Builder
[description]

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
1. Vagrant (for `cloudify-hpcloud` only):
  * hpcloud plugin
  
## Configuration files
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
* `components_package_url`
* `core_package_url` - 
* `ui_package_url` -
* `ubuntu_agent_url` - 
* `centos_agent_url` - 
* `windows_agent_url` - 
* `aws_source_ami` - Base AWS AMI.

### packerfile.json
