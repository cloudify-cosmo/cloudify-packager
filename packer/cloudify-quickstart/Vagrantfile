########
# Copyright (c) 2014 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
#    * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    * See the License for the specific language governing permissions and
#    * limitations under the License.

# -*- mode: ruby -*-
# vi: set ft=ruby :

BASE_BOX_NAME = 'cloudify'

Vagrant.configure('2') do |config|

  config.vm.define :cloudify do |cloudify|
    cloudify.vm.provider :virtualbox do |vb|
      vb.name = 'cloudify'
      vb.customize ['modifyvm', :id, '--memory', '2048']
      vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
    end
    cloudify.vm.network :private_network, ip: "11.0.0.7"
    cloudify.vm.box = BASE_BOX_NAME
    cloudify.vm.hostname = 'cloudify'
  end
end
