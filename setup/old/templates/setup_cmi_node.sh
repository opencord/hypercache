
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


site_id=GetSites()[0]["site_id"]
nodeinfo = {'hostname': "{{ node_hostname }}", 'dns': "8.8.8.8"}
n_id = AddNode(site_id, nodeinfo)
mac = "DE:AD:BE:EF:00:01"
interfacetemplate = {'mac': mac, 'kind': 'physical', 'method': 'static', 'is_primary': True, 'if_name': 'eth0'}
i_id = AddInterface(n_id, interfacetemplate)
ip_addr = "169.254.169.1" # TO DO: get this from Neutron in the future
netmask = "255.255.255.254" # TO DO: get this from Neutron in the future
ipinfo = {'ip_addr': ip_addr, 'netmask': netmask, 'type': 'ipv4'}
ip_id = AddIpAddress(i_id, ipinfo)
routeinfo = {'interface_id': i_id, 'next_hop': "127.0.0.127", 'subnet': '0.0.0.0', 'metric': 1}
r_id = AddRoute(n_id, routeinfo)
hpc_slice_id = GetSlices({"name": "co_coblitz"})[0]["slice_id"]
AddSliceToNodes(hpc_slice_id, [n_id])
dnsdemux_slice_id = GetSlices({"name": "co_dnsdemux"})[0]["slice_id"]
dnsredir_slice_id = GetSlices({"name": "co_dnsredir_coblitz"})[0]["slice_id"]
AddSliceToNodes(dnsdemux_slice_id, [n_id])
AddSliceToNodes(dnsredir_slice_id, [n_id])
takeoverscript=GetBootMedium(n_id, "node-cloudinit", '')
file("/root/takeover-{{ node_hostname }}","w").write(takeoverscript)
