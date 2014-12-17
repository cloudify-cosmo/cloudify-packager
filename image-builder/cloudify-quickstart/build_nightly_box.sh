#!/bin/bash

export COMPONENTS_PACKAGE_URL="http://gigaspaces-repository-eu.s3.amazonaws.com/org/cloudify3/3.1.0/ga-RELEASE/cloudify-components_3.1.0-ga-b85_amd64.deb"
export CORE_PACKAGE_URL="http://gigaspaces-repository-eu.s3.amazonaws.com/org/cloudify3/3.1.0/ga-RELEASE/cloudify-core_3.1.0-ga-b85_amd64.deb"
export UI_PACKAGE_URL="http://gigaspaces-repository-eu.s3.amazonaws.com/org/cloudify3/3.1.0/ga-RELEASE/cloudify-ui_3.1.0-ga-b85_amd64.deb"
export UBUNTU_AGENT_URL="http://gigaspaces-repository-eu.s3.amazonaws.com/org/cloudify3/3.1.0/ga-RELEASE/cloudify-ubuntu-precise-agent_3.1.0-ga-b85_amd64.deb"
export CENTOS_AGENT_URL="http://gigaspaces-repository-eu.s3.amazonaws.com/org/cloudify3/3.1.0/ga-RELEASE/cloudify-centos-final-agent_3.1.0-ga-b85_amd64.deb"
export WINDOWS_AGENT_URL="http://gigaspaces-repository-eu.s3.amazonaws.com/org/cloudify3/3.1.0/ga-RELEASE/cloudify-windows-agent_3.1.0-ga-b85_amd64.deb"
export CLOUDIFY_RELEASE="3.1.0"

export aws_access_key="AKIAI3E4DH26QFVMKGUA"
export aws_secret_key="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"

packer validate -syntax-only packerfile.json

packer build -machine-readable -only=nightly_virtualbox_build \
    -var "cloudify_release=$CLOUDIFY_RELEASE" \
    -var "components_package_url=$COMPONENTS_PACKAGE_URL" \
    -var "core_package_url=$CORE_PACKAGE_URL" \
    -var "ui_package_url=$UI_PACKAGE_URL" \
    -var "ubuntu_agent_url=$UBUNTU_AGENT_URL" \
    -var "centos_agent_url=$CENTOS_AGENT_URL" \
    -var "windows_agent_url=$WINDOWS_AGENT_URL" \
    -var "aws_source_ami=ami-6ca1011b" \
    packerfile.json