
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


from xosresource import XOSResource
from services.hpc.models import ServiceProvider, HpcService

class XOSServiceProvider(XOSResource):
    provides = "tosca.nodes.ServiceProvider"
    xos_model = ServiceProvider
    copyin_props = []

    def get_xos_args(self):
        hpc_service_name = self.get_requirement("tosca.relationships.MemberOfService", throw_exception=True)
        hpc_service = self.get_xos_object(HpcService, name=hpc_service_name)
        return {"name": self.obj_name,
                "hpcService": hpc_service}

    def can_delete(self, obj):
        if obj.contentprovider_set.exists():
            self.info("%s %s has active content providers; skipping delete" % (self.xos_model.__class__, obj.name))
            return False
        return super(XOSServiceProvider, self).can_delete(obj)

