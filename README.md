Cosmo-Packager
==============

Cosmo-Packager is meant to create a package composed of Cosmo's 3rd party requirements and Code, including the most basic plugins and configuration.
The foundation of Cosmo-Packager is based on the premise that not all networks have an internet connection, and that 3rd party requirements change a lot less than Cosmo's code base.
The package will already contain the most basic configuration for Cosmo's components (e.g. logstash conf file, elasticsearch init file, etc..)

Generally, cosmo-packager will create a package from each component.

### PreReqs
The packager uses the following 3rd party components:

- make -*for installing packages on the packager server*
- python-setuptools -*also for installing packages on the packager server*
- rubygems -*for downloading ruby gems*
- git -*for cloning the packager repo*
- python-dev -*for fabric, mainly*
- curl -*for rvm installation*
- fpm -*main packaging framework*
- fabric -*...*
- pip >1.5 -*for downloading python modules*
- jinja2 -*for creating scripts and configuration files from tempates*
- rvm -*for more gem installation requirements*
- opnejdk-7-jdk -*for maven*
- maven -*for building the orchestrator - will be removed once the orchestrator is pythoned*
- nodejs 
- pika -*to send events to rabbitmq if it's installed on the packaging server*
a bootstrap script is provided to install the above packages.

### Structure

- packager.py contains the base functions for handling component actions (wget, mkdir, apt-download, etc..).
- config.py contains the package and cosmo-packager logger configuration.
- get.py contains the logic for downloading and arranging a component's contents.
- pkg.py contains the logic for packaging a component.
- templgen.py contains the base functions for creating script/configuration files from template files.
- event_handler.py contains the base functions for sending events to rabbitmq from the packager.
- fabfile.py contains fabric tasks for automation/testing purposes.

### Usage
Lets take an example of a component's creation cycle - from retrieval to dpkg-i-ing. We'll look at Riemann:
#### Component config:
```python
"riemann": {
        "name": "riemann",
        "version": "0.2.2",
        "source_url": "http://aphyr.com/riemann/riemann_0.2.2_all.deb",
        "bootstrap_dir": "%s/riemann/" % PACKAGES_BOOTSTRAP_DIR,
        "package_dir": "%s/riemann" % PACKAGES_DIR
    }
```

###### Explanation:

- "name" is the component's name (DUH!). it's used to create named directories mostly.
- "version", when applicable, is used to apply a version to the component's package name (in the future, it might dictate the component's version to download.)
- "source_url" is where you would download the component from (can be a repo or a url)
- "bootstrap_dir" (will be changed in the near future) is the dir where the component's package will be stored after the packaging process is complete for that same component.
- "package_dir" (will be changed in the near future) is the dir where the component's parts (files, configs, etc..) will be stored before the component's package is created.

#### Component retrieval:
```python
package = get_package_configuration('riemann')

rmdir(package['package_dir'])
make_package_dirs(
    package['bootstrap_dir'],
    package['package_dir'])
wget(
    package['source_url'],
    package['package_dir'])
```

###### Explanation:
This is the logic for retrieving the component's parts (here, we only have a riemann deb file but you can look at the get.py file for more examples)

Here we:

- get the component's config.
- remove remnants of previous component parts if any existed.
- create package directories to store everything in.
- download the package and store it.

#### Component packaging:
```python
package = get_package_configuration('riemann')

if not is_dir(package['bootstrap_dir']):
    mkdir(package['bootstrap_dir'])
lgr.debug("isolating debs...")
cp('%s/*.deb' % package['package_dir'], package['bootstrap_dir'])
```

###### Explanation:
In this example, we only get the component's config, create a dir for the final package if it didn't exist and move riemann's deb over there (since Riemann is already prepackaged when downloaded.)

Other examples (check pkg.py) like logstash, for instance, contain a more complex logic like:

- Copying init and conf files
- Downloading a jar
- Packing them all to a deb along with a bootstrap script created from a template file...
- etc...

#### Component bootstrap template:

- The packager uses jinja2 to create files from templates.
- Components which should be packaged along with a bootstrap script should have a .template file stationed in ../package-templates/
- During the packaging process, if a template file exists and its path is passed to the "pack" function, the bootstrap script will be created and attached to the package.
- The bootstrap script will run automatically upon dpkg-ing.

Here's an example of a template bootstrap script (for virtualenv, since riemann doesn't require one):
	
	PKG_NAME="{{ name }}"
	PKG_DIR="{{ package_dir }}"
	
	echo "extracting ${PKG_NAME}..."
	sudo tar -C ${PKG_DIR} -xvf ${PKG_DIR}/*.tar.gz
	echo "removing tar..."
	sudo rm ${PKG_DIR}/*.tar.gz
	cd ${PKG_DIR}/virtualenv*
	echo "installing ${PKG_NAME}..."
	sudo python setup.py install
The double curly braces are where the variables are eventually assigned.
The name of the variable must match a component's config variable in its dict (e.g name, virtualenv, etc...).

#### Component's dpkg-i-ing.
You can now safely dpkg -i your component's deb file/s to install it.

### Vagrant
A vagrantfile is provided to load 2 machines:

- an Orchestrator server (which, by default, runs the cosmo-orchestrator-bootstrap.sh script)
- a Tester server (which, by default, runs a minimal bootstrap script which only runs apt-get update so that you can test pkg installation on a clean machine)

##### Automated Vagrant Testing Environment

In future versions, an automated process of retrieval, packaging and installation will be implemented to check the entire process.
