PACKER_FILE=cloudify-packer.json
cp ${PACKER_FILE}{,.bak}
sed -i "s|{{ components_package_url }}|http://gigaspaces-repository-eu.s3.amazonaws.com/org/cloudify3/3.0.0/nightly_6/cloudify-components_3.0.0-ga-b6_amd64.deb|g" ${PACKER_FILE}
sed -i "s|{{ core_package_url }}|http://gigaspaces-repository-eu.s3.amazonaws.com/org/cloudify3/3.0.0/nightly_6/cloudify-core_3.0.0-ga-b6_amd64.deb|g" ${PACKER_FILE}
sed -i "s|{{ ui_package_url }}|http://gigaspaces-repository-eu.s3.amazonaws.com/org/cloudify3/3.0.0/nightly_6/cloudify-ui_3.0.0-ga-b6_amd64.deb|g" ${PACKER_FILE}
sed -i "s|{{ ubuntu_agent_url }}|http://gigaspaces-repository-eu.s3.amazonaws.com/org/cloudify3/3.0.0/nightly_6/cloudify-ubuntu-agent_3.0.0-ga-b6_amd64.deb|g" ${PACKER_FILE}
sed -i "s|{{ centos_agent_url }}|http://gigaspaces-repository-eu.s3.amazonaws.com/org/cloudify3/3.0.0/nightly_6/cloudify-centos-agent_3.0.0-ga-b6_amd64.deb|g" ${PACKER_FILE}
sed -i "s|{{ windows_agent_url }}|http://gigaspaces-repository-eu.s3.amazonaws.com/org/cloudify3/3.0.0/nightly_6/cloudify-windows-agent_3.0.0-ga-b6_amd64.deb|g" ${PACKER_FILE}
sed -i "s|{{ release }}|3.0.0|g" ${PACKER_FILE}
packer build -only=vmware-iso -force ${PACKER_FILE}
mv ${PACKER_FILE}{.bak,}