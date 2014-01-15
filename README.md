Cosmo-Packager
==============

Cosmo-Packager is meant to create a package composed of Cosmo's 3rd party requirements and Code, including the most basic plugins.
The foundation of Cosmo-Packager is based on the premise that not all networks have an internet connection, and that 3rd party requirements change a lot less than Cosmo's code base.
The package will already contain the most basic configuration for Cosmo's components (e.g. logstash conf file, elasticsearch init file, etc..)

Generally, cosmo-packager will create a package from each component.

### PreReqs
The packager uses the following 3rd party components:
- make
- python-setuptools
- rubygems
- git
- python-dev 
- curl
- fpm ()
- fabric >=1.4
- pip >=1.5
- jinja2
- rvm

a bootstrap script is provided to install the above packages.

### Structure
- packager.py contains the base functions for handling component actions (wget, mkdir, apt-download, etc..).
- config.py contains the package and cosmo-packager logger configuration.
- get.py contains the logic for downloading and arranging a component's contents.
- pkg.py contains the logic for packaging a component.
- templgen.py contains the base functions for creating script/configuration files from template files.
- fabfile.py contains fabric tasks for automation/testing purposes.

### Usage
Lets take an example of a component's creation cycle - from retrieval to dpkg-i-ing. We'll look at Riemann:
#### component config:
<script>
	"riemann": {
	        "name": "riemann",
	        "version": "0.2.2",
	        "source_url": "http://aphyr.com/riemann/riemann_0.2.2_all.deb",
	        "bootstrap_dir": "%s/riemann/" % PACKAGES_BOOTSTRAP_DIR,
	        "package_dir": "%s/riemann" % PACKAGES_DIR
	    }
</script>

explanation:
- "name" is the component's name (DUH!). it's used to create named directories mostly.
- "version", when applicable, is used to apply a version to the component's package name.
- "source_url" is where you would download the component from (can be a repo or a url)
- "bootstrap_dir" (will be changed in the near future) is the dir where the component's package will be stored after the packaging process is complete for that same component.
- "package_dir" (will be changed in the near future) is the dir where the component's parts (files, configs, etc..) will be stored before the component's package is created.

#### component retrieval:
    package = get_package_configuration('riemann')

    rmdir(package['package_dir'])
    make_package_dirs(
        package['bootstrap_dir'],
        package['package_dir'])
    wget(
        package['source_url'],
        package['package_dir'])

explanation:
This is the logic for retrieving the component's parts (here, we only have a riemann deb file but you can look at the get.py file for more examples)
Here we 
- get the component's config.
- remove remnants of previous component parts if any existed.
- create package directories to store everything in.
- download the package and store it.

#### component packaging:
    package = get_package_configuration('riemann')

    if not is_dir(package['bootstrap_dir']):
        mkdir(package['bootstrap_dir'])
    lgr.debug("isolating debs...")
    cp('%s/*.deb' % package['package_dir'], package['bootstrap_dir'])

explanation:
In this example, we only get the component's config, create a dir for the final package if it didn't exist and move riemann's deb over there (since Riemann is already prepackaged when downloaded.)
Other examples (check pkg.py) like logstash, for instance, contain a more complex logic like copying init and conf files, downloading a jar, packing them all to a deb along with a bootstrap script created from a template file...
If a bootstrap script is relevant for you, add it to the package-templates dir and it will be automatically generated if you include it in the packaging process.

#### component's dpkg-i-ing.
You can now safely dpkg -i your package to install it.

### Vagrant
A vagrantfile is provided to load 2 machines:
- an Orchestrator server (which, by default, runs the bootstrap script mentioned above)
- a Tester server (which, by default, runs a minimal bootstrap script which only runs apt-get update so that you can test pkg installation on a clean machine)

