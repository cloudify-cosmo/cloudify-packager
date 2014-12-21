#!/bin/bash
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