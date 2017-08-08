
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


lab="External"
for service in ["HyperCache", "RequestRouter"]:
    for node in ListAll("Node"):
        node_id = node["node_id"]
        for interface_id in node["interface_ids"]:
            iface=Read("Interface", interface_id)
            if iface["is_primary"] and len(iface["ip_address_ids"])==1:
                ip_id = iface["ip_address_ids"][0]
                if ListAll("LogicalInterface", {"node_id": node_id, "ip_address_ids": [ip_id], "label": lab, "service": service}):
                    print "External label exists for node", node_id, "ip", ip_id, "service", service
                else:
                    print "Adding external label for node", node_id, "ip", ip_id, "service", service
                    li = Create("LogicalInterface", {"node_id": node_id, "label": lab, "service": service})
	            Bind("LogicalInterface", li, "IpAddress", ip_id)
