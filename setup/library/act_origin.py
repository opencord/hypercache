
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
            url       = dict(required=True, type='str'),
            service_type = dict(default="HyperCache", type="str"),
            content_provider = dict(required=True, type="str"),

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
    origin_url = module.params["url"]
    force = module.params["force"]

    api = LCDNAPI(credentials, experimental=True)

    content_providers = api.onevapi.ListAll("ContentProvider", {"name": module.params["content_provider"]})
    if not content_providers:
        raise Exception("Unable to find %s" % module.params["content_provider"])
    content_provider = content_providers[0]

    origins = api.onevapi.ListAll("OriginServer", {"url": origin_url})

    if (origins or force) and (state=="absent"):
        api.Delete("OriginServer", origins[0]["origin_servier_id"])
        module.exit_json(changed=True, msg="origin server deleted")
    elif ((not origins) or force) and (state=="present"):
        if origins:
            # must have been called with force=True, so delete the node so we can re-create it
            api.onevapi.Delete("OriginServer", origins[0]["origin_server_id"])

        origin = {"url": origin_url,
              "service_type": module.params["service_type"],
              "content_provider_id": content_provider["content_provider_id"]}
        ret = api.onevapi.Create("OriginServer", origin)

        module.exit_json(changed=True, msg="origin server created")
    else:
        module.exit_json(changed=False)

if __name__ == '__main__':
    main()
