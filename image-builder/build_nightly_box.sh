#!/bin/bash
packer validate -syntax-only packerfile.json

packer build -machine-readable -only=nightly_virtualbox_build \
    -var-file=packer_inputs.json
    packerfile.json
