export COMPONENTS_PACKAGE_URL="http://gigaspaces-repository-eu.s3.amazonaws.com/org/cloudify3/3.1.0/ga-RELEASE/cloudify-components_3.1.0-ga-b85_amd64.deb"
export CORE_PACKAGE_URL="http://gigaspaces-repository-eu.s3.amazonaws.com/org/cloudify3/3.1.0/ga-RELEASE/cloudify-core_3.1.0-ga-b85_amd64.deb"
export UI_PACKAGE_URL="http://gigaspaces-repository-eu.s3.amazonaws.com/org/cloudify3/3.1.0/ga-RELEASE/cloudify-ui_3.1.0-ga-b85_amd64.deb"
export UBUNTU_AGENT_URL="http://gigaspaces-repository-eu.s3.amazonaws.com/org/cloudify3/3.1.0/ga-RELEASE/cloudify-ubuntu-precise-agent_3.1.0-ga-b85_amd64.deb"
export CENTOS_AGENT_URL="http://gigaspaces-repository-eu.s3.amazonaws.com/org/cloudify3/3.1.0/ga-RELEASE/cloudify-centos-final-agent_3.1.0-ga-b85_amd64.deb"
export WINDOWS_AGENT_URL="http://gigaspaces-repository-eu.s3.amazonaws.com/org/cloudify3/3.1.0/ga-RELEASE/cloudify-windows-agent_3.1.0-ga-b85_amd64.deb"
export CLOUDIFY_RELEASE="3.1.0-rc2"
packer build -only=virtualbox-ovf -force packerfile.json

# cloudify_packages:
#   server:
#     components_package_url: http://192.168.10.13/builds/GigaSpacesBuilds/cloudify3/3.1.0/ga-RELEASE/cloudify-components_3.1.0-ga-b85_amd64.deb
#     core_package_url: http://192.168.10.13/builds/GigaSpacesBuilds/cloudify3/3.1.0/ga-RELEASE/cloudify-core_3.1.0-ga-b85_amd64.deb
#     ui_package_url: http://192.168.10.13/builds/GigaSpacesBuilds/cloudify3/3.1.0/ga-RELEASE/cloudify-ui_3.1.0-ga-b85_amd64.deb
#   agents:
#     ubuntu_agent_url: http://192.168.10.13/builds/GigaSpacesBuilds/cloudify3/3.1.0/ga-RELEASE/cloudify-ubuntu-precise-agent_3.1.0-ga-b85_amd64.deb
#     centos_agent_url: http://192.168.10.13/builds/GigaSpacesBuilds/cloudify3/3.1.0/ga-RELEASE/cloudify-centos-final-agent_3.1.0-ga-b85_amd64.deb
#     windows_agent_url: http://192.168.10.13/builds/GigaSpacesBuilds/cloudify3/3.1.0/ga-RELEASE/cloudify-windows-agent_3.1.0-ga-b85_amd64.deb