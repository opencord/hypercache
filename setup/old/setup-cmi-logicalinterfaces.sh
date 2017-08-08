
# Copyright 2017-present Open Networking Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


#! /bin/bash

source cmi-settings.sh

echo "[ssh_connection]" > cmi.conf
echo "ssh_args = -o \"ProxyCommand ssh -q -i $NODE_KEY -o StrictHostKeyChecking=no root@$COMPUTE_NODE nc $MGMT_IP 22\"" >> cmi.conf
echo "scp_if_ssh = True" >> cmi.conf
echo "pipelining = True" >> cmi.conf
echo >> cmi.conf
echo "[defaults]" >> cmi.conf
echo "host_key_checking = False" >> cmi.conf

echo "cmi ansible_ssh_private_key_file=$VM_KEY" > cmi.hosts

export ANSIBLE_CONFIG=cmi.conf
export ANSIBLE_HOSTS=cmi.hosts

ansible-playbook -v --step cmi-logicalinterfaces.yaml
