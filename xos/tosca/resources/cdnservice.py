from service import XOSService
from services.hpc.models import HpcService

class XOSCdnService(XOSService):
    provides = "tosca.nodes.CDNService"
    xos_model = HpcService
    copyin_props = ["view_url", "icon_url"]

