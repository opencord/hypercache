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
    sp_name = module.params["name"]
    force = module.params["force"]

    api = LCDNAPI(credentials, experimental=True)

    sps = api.onevapi.ListAll("ServiceProvider", {"name": sp_name})

    if (sps or force) and (state=="absent"):
        api.Delete("ServiceProvider", sps[0].id)
        module.exit_json(changed=True, msg="sp deleted")
    elif ((not sps) or force) and (state=="present"):
        if sps:
            # must have been called with force=True, so delete the node so we can re-create it
            api.onevapi.Delete("ServiceProvider", sps[0]["service_provider_id"])

        sp = {"account": module.params["account"],
              "name": sp_name,
              "enabled": module.params["enabled"]}
        ret = api.onevapi.Create("ServiceProvider", sp)

        module.exit_json(changed=True, msg="sp created")
    else:
        module.exit_json(changed=False)

if __name__ == '__main__':
    main()
