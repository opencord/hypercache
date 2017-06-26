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
            site      = dict(required=True, type='str'),
            dns       = dict(required=True, type='list'),
            interfaces= dict(required=True, type='list'),
            license   = dict(required=True, type='str'),

            state     = dict(required=True, type='str', choices=["present", "absent"]),
            force     = dict(default=False, type="bool"),
            username  = dict(required=True, type='str'),
            password  = dict(required=True, type='str'),
            hostname  = dict(required=True, type='str'),
            plc_name  = dict(required=True, type='str'),

            remote_hostname = dict(default=None, type="str"),
        )
    )

    credentials = {"username": module.params["username"],
                   "password": module.params["password"],
                   "hostname": module.params["hostname"],
                   "plc_name": module.params["plc_name"]}

    state = module.params["state"]
    node_hostname = module.params["name"]
    force = module.params["force"]

    api = LCDNAPI(credentials)

    nodes = api.ListAll("Node", {"hostname": node_hostname})

    if (nodes or force) and (state=="absent"):
        api.deleteCache(node_hostname)
        module.exit_json(changed=True, msg="cachenode deleted")
    elif ((not nodes) or force) and (state=="present"):
        if nodes:
            # must have been called with force=True, so delete the node so we can re-create it
            api.deleteCache(node_hostname)

        hpc = {"hostname": node_hostname,
               "site": module.params["site"],
               "dns": module.params["dns"],
               "Interfaces": module.params["interfaces"],
               "license": module.params["license"]}
        ret = api.createCache(**hpc)
        setupscript=ret["setupscript"]

        if module.params["remote_hostname"]:
            setupscript = setupscript.replace(module.params["hostname"], module.params["remote_hostname"])

        module.exit_json(changed=True, msg="cachenode created", setupscript=setupscript)
    else:
        module.exit_json(changed=False)

if __name__ == '__main__':
    main()