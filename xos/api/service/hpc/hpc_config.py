from django.http import HttpResponse, HttpResponseServerError
from core.models import *
from rest_framework.views import APIView
from services.hpc.models import *
#from services.requestrouter.models import *
import xos.settings
import json
import os
import time

def get_service_slices(service):
    try:
       return service.slices.all()
    except:
       # this field used to be improperly named, and makemigrations won't fix it
       return service.service.all()

class HpcConfig(APIView):
    method_kind = "list"
    method_name = "hpcconfig"

    def get(self, request, format=None):
        hpcSlice=None
        cmiSlice=None
        redirSlice=None
        demuxSlice=None

        node_slicename = request.GET.get("slicename", None)
        if not node_slicename:
            return HttpResponseServerError("Error: no slicename passed in request")

        # search for an HPC Service that owns the slicename that was passed
        # to us.
        hpc=None
        for candidate in HpcService.objects.all():
            if candidate.cmi_hostname == node_slicename:
                # A hack for standalone CMIs that aren't managed by XOS. Set
                # /etc/slicename to cmi_hostname that's configured in the
                # HPCService object.
                hpc = candidate

            for slice in get_service_slices(candidate):
                if slice.name == node_slicename:
                    hpc = candidate

        if (not hpc):
            return HttpResponseServerError("Error: no HPC service")

        for slice in get_service_slices(hpc):
            if "cmi" in slice.name:
                cmiSlice = slice
            elif ("hpc" in slice.name) or ("vcoblitz" in slice.name):
                hpcSlice = slice
            elif "redir" in slice.name:
                redirSlice = slice
            elif "demux" in slice.name:
                demuxSlice = slice

        if (hpc.cmi_hostname):
            cmi_hostname = hpc.cmi_hostname
        else:
            if not cmiSlice:
                return HttpResponseServerError("Error: no CMI slice")

            if len(cmiSlice.instances.all())==0:
                return HttpResponseServerError("Error: CMI slice has no instances")

            # for now, assuming using NAT
            cmi_hostname = cmiSlice.instances.all()[0].node.name

        if not hpcSlice:
            return HttpResponseServerError("Error: no HPC slice")

    #    if (redirSlice==None) or (demuxSlice==None):
    #        # The HPC Service didn't have a dnsredir or a dnsdemux, so try looking
    #        # in the RequestRouterService for one.
    #
    #        rr = RequestRouterService.objects.all()
    #        if not (rr):
    #            return HttpResponseServerError("Error: no RR service")
    #
    #        rr = rr[0]
    #        try:
    #           slices = rr.slices.all()
    #        except:
    #           # this field used to be improperly named, and makemigrations won't fix it
    #           slices = rr.service.all()
    #        for slice in slices:
    #            if "redir" in slice.name:
    #                redirSlice = slice
    #            elif "demux" in slice.name:
    #                demuxSlice = slice

        if not redirSlice:
            return HttpResponseServerError("Error: no dnsredir slice")

        if not demuxSlice:
            return HttpResponseServerError("Error: no dnsdemux slice")

        d = {}
        d["hpc_slicename"] = hpcSlice.name
        d["redir_slicename"] = redirSlice.name
        d["demux_slicename"] = demuxSlice.name
        d["cmi_hostname"] = cmi_hostname
        d["xos_hostname"] = xos.settings.RESTAPI_HOSTNAME
        d["xos_port"] = str(xos.settings.RESTAPI_PORT)

        if hpc.hpc_port80:
            d["hpc_port80"] = "True"
        else:
            d["hpc_port80"] = "False"

        return HttpResponse("""# auto-generated by HpcConfig
    ENABLE_PLC=False
    ENABLE_PS=True
    BASE_HRN="princeton"
    RELEVANT_SERVICE_NAMES=['vcoblitz', 'coredirect', 'codnsdemux', "syndicate_comon_server"]
    COBLITZ_SLICE_NAME=BASE_HRN+"_vcoblitz"
    COBLITZ_SLICE_ID=70
    COBLITZ_PS_SLICE_NAME="{hpc_slicename}"
    DNSREDIR_SLICE_NAME=BASE_HRN+"_coredirect"
    DNSREDIR_SLICE_ID=71
    DNSREDIR_PS_SLICE_NAME="{redir_slicename}"
    DNSDEMUX_SLICE_NAME=BASE_HRN+"_codnsdemux"
    DNSDEMUX_SLICE_ID=69
    DNSDEMUX_PS_SLICE_NAME="{demux_slicename}"
    CMI_URL="http://{cmi_hostname}/"
    CMI_HTTP_PORT="8004"
    CMI_HTTPS_PORT="8003"
    PUPPET_MASTER_HOSTNAME="{cmi_hostname}"
    PUPPET_MASTER_PORT="8140"
    PS_HOSTNAME="{xos_hostname}"
    PS_PORT="{xos_port}"
    COBLITZ_PORT_80={hpc_port80}
    """.format(**d))

