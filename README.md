Cloudify-Packager
=================

Cloudify's packager provides tools and configuration objects we use to build Cloudify's Management environments, agents and demo images.

### [Docker Images](http://www.docker.com)

Please see [Bootstrapping using Docker](http://getcloudify.org/guide/3.1/installation-bootstrapping.html#bootstrapping-using-docker) for information on our transition from packages to container-based installations.

To generate our [Dockerfile](https://github.com/cloudify-cosmo/cloudify-packager/raw/master/docker/Dockerfile.template) templates, we're using [Jocker](https://github.com/nir0s/jocker).

### Generate a custom Cloudify manager image

* Clone the cloudify-packager repository from github:<br>
`git clone https://github.com/cloudify-cosmo/cloudify-packager.git`

* Make your changes in [var.py](https://github.com/cloudify-cosmo/cloudify-packager/blob/master/docker/vars.py)
	
	- For example:
		
		- Use a specific branch of Cloudify related [modules](https://github.com/cloudify-cosmo/cloudify-packager/blob/master/docker/vars.py#L123).<br>
		  For example, replace the `master` branch with `my-branch` in `cloudify_rest_client` module:
		  `"cloudify_rest_client": "git+git://github.com/cloudify-cosmo/cloudify-rest-client.git@my-branch"`
		- Add system packages to be installed on the image.<br>
		  For example, add the package "my-package" to the manager's requirements list (the [reqs](https://github.com/cloudify-cosmo/cloudify-packager/blob/master/docker/vars.py#L119) list):
			
```
		  "manager": {
		    "service_name": "manager",
			"reqs": [
			  "git",
			  "python2.7",
			  "my-package"
			],
			...
		  }
```

* Run the [build.sh](https://github.com/cloudify-cosmo/cloudify-packager/blob/master/docker/build.sh) 
	script from the [docker folder](https://github.com/cloudify-cosmo/cloudify-packager/tree/master/docker):
```
  cd cloudify-packager/docker/
  . build.sh
```
- Create a tar file from the generated image:
{% highlight bash %}
sudo docker run -t --name=cloudifycommercial -d cloudify-commercial:latest /bin/bash
sudo docker export cloudifycommercial > /tmp/cloudify-docker_commercial.tar
{% endhighlight %}

- Create a url from which you can download the tar file.

* Set the `docker_url` property in your manager blueprint (see `cloudify_packages` property in [CloudifyManager Type](http://getcloudify.org/guide/3.2/reference-types.html#cloudifymanager-type) with your custom image url, e.g:
```
cloudify_packages:
	...
    docker:
    	docker_url: {url to download the custom Cloudify manager image tar file}
```

* Run cfy [bootstrap](http://getcloudify.org/guide/3.1/installation-bootstrapping.html) using your manager blueprint.


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

#### image-builder

Creates a Vagrant box (using Virtualbox, AWS orw HPCloud) with the Cloudify Manager installed on it.
