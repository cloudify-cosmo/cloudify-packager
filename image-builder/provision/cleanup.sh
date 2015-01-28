#!/bin/bash

sudo apt-get purge -y build-essential
sudo apt-get autoremove -y
sudo apt-get clean -y
sudo rm -rf /var/lib/apt/lists/*
