
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
from services.hpc.models import CDNPrefix, ContentProvider

class XOSCDNPrefix(XOSResource):
    provides = "tosca.nodes.CDNPrefix"
    xos_model = CDNPrefix
    name_field = "prefix"
    copyin_props = []

    def get_xos_args(self):
        args = {"prefix": self.obj_name}

        cp_name = self.get_requirement("tosca.relationships.MemberOfContentProvider")
        if cp_name:
            args["contentProvider"] = self.get_xos_object(ContentProvider, name=cp_name)

        default_os = self.get_requirement("tosca.relationships.DefaultOriginServer")
        if default_os:
             args["defaultOriginServer"] = self.engine.name_to_xos_model(self.user, default_os)

        return args

    def can_delete(self, obj):
        return super(XOSCDNPrefix, self).can_delete(obj)

