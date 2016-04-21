########
# Copyright (c) 2014 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
#    * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    * See the License for the specific language governing permissions and
#    * limitations under the License.

from test_cli_package import TestCliPackage
from rhel_base import RHEL7Base, RHEL65Base


class TestRHEL7(RHEL7Base, TestCliPackage):

    def test_rhel7_cli_package(self):
        self._add_dns()
        self._test_cli_package()


class TestRHEL65(RHEL65Base, TestCliPackage):

    def additional_setup(self):
        super(TestRHEL65, self).additional_setup()

    def test_rhel6_5_cli_package(self):
        self._add_dns()
        self._test_cli_package()
