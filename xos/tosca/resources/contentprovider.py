
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
from services.hpc.models import ContentProvider, ServiceProvider

class XOSContentProvider(XOSResource):
    provides = "tosca.nodes.ContentProvider"
    xos_model = ContentProvider
    copyin_props = []

    def get_xos_args(self):
        sp_name = self.get_requirement("tosca.relationships.MemberOfServiceProvider", throw_exception=True)
        sp = self.get_xos_object(ServiceProvider, name=sp_name)
        return {"name": self.obj_name,
                "serviceProvider": sp}

    def can_delete(self, obj):
        if obj.cdnprefix_set.exists():
            self.info("%s %s has active CDN prefixes; skipping delete" % (self.xos_model.__class__, obj.name))
            return False
        return super(XOSContentProvider, self).can_delete(obj)

