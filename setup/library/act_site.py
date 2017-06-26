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
            state     = dict(required=True, type='str', choices=["present", "absent"]),
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
    siteName = module.params["name"]

    api = LCDNAPI(credentials)

    sites = api.ListAll("Site", {"name": siteName})

    if sites and (state=="absent"):
        api.deleteSite(siteName)
        module.exit_json(changed=True, msg="site deleted")
    elif (not sites) and (state=="present"):
        api.createSite(siteName)
        module.exit_json(changed=True, msg="site created")
    else:
        module.exit_json(changed=False)


if __name__ == '__main__':
    main()
