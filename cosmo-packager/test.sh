#!/usr/bin/env bash

function pause(){
	read -p "$*"
}

function state_error
{
	echo "ERROR: ${1:-UNKNOWN} (status $?)" 1>&2
	exit 1
}

echo "creating dir..."
sudo mkdir /tester/tester	|| state_error "failed on: creating dir"
