
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
            cdn_prefix= dict(required=True, type='str'),
            enabled   = dict(required=True, type="bool"),
            service   = dict(default="HyperCache", type="str"),
            content_provider=dict(required=True, type="str"),
            default_origin_server = dict(required=True, type="str"),

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
    cdn_prefix = module.params["cdn_prefix"]
    force = module.params["force"]

    api = LCDNAPI(credentials, experimental=True)

    content_providers = api.onevapi.ListAll("ContentProvider", {"name": module.params["content_provider"]})
    if not content_providers:
        raise Exception("Unable to find %s" % module.params["content_provider"])
    content_provider = content_providers[0]

    prefixes = api.onevapi.ListAll("CDNPrefix", {"cdn_prefix": cdn_prefix})

    if (prefixes or force) and (state=="absent"):
        api.Delete("CDNPrefix", prefixes[0]["cdn_prefix_id"])
        module.exit_json(changed=True, msg="cdn prefix deleted")
    elif ((not prefixes) or force) and (state=="present"):
        if prefixes:
            # must have been called with force=True, so delete the node so we can re-create it
            api.onevapi.Delete("CDNPrefix", prefixes[0]["cdn_prefix_id"])

        cdn_prefix = {"cdn_prefix": cdn_prefix,
                      "enabled": module.params["enabled"],
                      "service": module.params["service"],
                      "content_provider_id": content_provider["content_provider_id"],
                      "default_origin_server": module.params["default_origin_server"]}
        ret = api.onevapi.Create("CDNPrefix", cdn_prefix)

        module.exit_json(changed=True, msg="sp created")
    else:
        module.exit_json(changed=False)

if __name__ == '__main__':
    main()
