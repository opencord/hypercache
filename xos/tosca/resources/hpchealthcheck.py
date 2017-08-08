
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
from services.hpc.models import HpcHealthCheck, HpcService

class XOSHpcHealthCheck(XOSResource):
    provides = "tosca.nodes.HpcHealthCheck"
    xos_model = HpcHealthCheck
    name_field = None
    copyin_props = ("kind", "resource_name", "result_contains")

    def get_xos_args(self, throw_exception=True):
        args = super(XOSHpcHealthCheck, self).get_xos_args()

        service_name = self.get_requirement("tosca.relationships.MemberOfService", throw_exception=throw_exception)
        if service_name:
            args["hpcService"] = self.get_xos_object(HpcService, throw_exception=throw_exception, name=service_name)

        return args

    def get_existing_objs(self):
        args = self.get_xos_args(throw_exception=True)

        return list( HpcHealthCheck.objects.filter(hpcService=args["hpcService"], kind=args["kind"], resource_name=args["resource_name"]) )

    def postprocess(self, obj):
        pass

    def can_delete(self, obj):
        return super(XOSTenant, self).can_delete(obj)

