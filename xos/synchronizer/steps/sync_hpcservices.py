
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


import os
import sys
import base64
from django.db.models import F, Q
from xos.config import Config
from synchronizers.base.syncstep import SyncStep
from core.models import Service
from services.hpc.models import HpcService
from xos.logger import Logger, logging

# hpclibrary will be in steps/..
parentdir = os.path.join(os.path.dirname(__file__),"..")
sys.path.insert(0,parentdir)

from hpclib import HpcLibrary

logger = Logger(level=logging.INFO)

class SyncHpcService(SyncStep, HpcLibrary):
    provides=[HpcService]
    observes=HpcService
    requested_interval=0

    def __init__(self, **args):
        SyncStep.__init__(self, **args)
        HpcLibrary.__init__(self)

    def filter_hpc_service(self, objs):
        hpcService = self.get_hpc_service()

        return [x for x in objs if x == hpcService]

    def fetch_pending(self, deleted):
        # Looks like deletion is not supported for this object - Sapan
        if (deleted):
            return []
        else:
            return self.filter_hpc_service(HpcService.objects.filter(Q(enacted__lt=F('updated')) | Q(enacted=None)))

    def sync_record(self, hpc_service):
        logger.info("sync'ing hpc_service %s" % str(hpc_service),extra=hpc_service.tologdict())
        hpc_service.save()
