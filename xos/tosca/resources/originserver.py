
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
from services.hpc.models import OriginServer, ContentProvider

class XOSOriginServer(XOSResource):
    provides = "tosca.nodes.OriginServer"
    xos_model = OriginServer
    name_field = "url"
    copyin_props = []

    def obj_name_to_url(self):
        url = self.obj_name
        if url.startswith("http_"):
            url = url[5:]
        return url

    def get_existing_objs(self):
        url = self.obj_name_to_url()
        return self.xos_model.objects.filter(**{self.name_field: url})

    def get_xos_args(self):
        url = self.obj_name_to_url()
        cp_name = self.get_requirement("tosca.relationships.MemberOfContentProvider", throw_exception=True)
        cp = self.get_xos_object(ContentProvider, name=cp_name)
        return {"url": url,
                "contentProvider": cp}

    def can_delete(self, obj):
        return super(XOSOriginServer, self).can_delete(obj)

