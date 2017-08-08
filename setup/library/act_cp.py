
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


#!/usr/bin/python

import json
import os
import requests
import sys
import traceback

from ansible.module_utils.basic import AnsibleModule
from auraclienttools import LCDNAPI, LCDNFault

def main():
    module = AnsibleModule(
        argument_spec = dict(
            name      = dict(required=True, type='str'),
            account   = dict(required=True, type='str'),
            enabled   = dict(required=True, type="bool"),
            service_provider = dict(required=True, type="str"),

            state     = dict(required=True, type='str', choices=["present", "absent"]),
            force     = dict(default=False, type="bool"),
            username  = dict(required=True, type='str'),
            password  = dict(required=True, type='str'),
            hostname  = dict(required=True, type='str'),
            plc_name  = dict(required=True, type='str'),
        )
    )

    credentials = {"username": module.params["username"],
                   "password": module.params["password"],
                   "hostname": module.params["hostname"],
                   "plc_name": module.params["plc_name"]}

    state = module.params["state"]
    cp_name = module.params["name"]
    force = module.params["force"]

    api = LCDNAPI(credentials, experimental=True)

    service_providers = api.onevapi.ListAll("ServiceProvider", {"name": module.params["service_provider"]})
    if not service_providers:
        raise Exception("Unable to find %s" % module.params["service_provider"])
    service_provider = service_providers[0]

    cps = api.onevapi.ListAll("ContentProvider", {"name": cp_name})

    if (cps or force) and (state=="absent"):
        api.Delete("ContentProvider", cps[0].id)
        module.exit_json(changed=True, msg="cp deleted")
    elif ((not cps) or force) and (state=="present"):
        if cps:
            # must have been called with force=True, so delete the node so we can re-create it
            api.onevapi.Delete("ContentProvider", cps[0]["content_provider_id"])

        sp = {"account": module.params["account"],
              "name": cp_name,
              "enabled": module.params["enabled"],
              "service_provider_id": service_provider["service_provider_id"]}
        ret = api.onevapi.Create("ContentProvider", sp)

        module.exit_json(changed=True, msg="cp created")
    else:
        module.exit_json(changed=False)

if __name__ == '__main__':
    main()
