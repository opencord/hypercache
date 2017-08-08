
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


def CreateOrFind(kind, args):
    objs=ListAll(kind, args.copy())
    if objs:
        id_name = {"ServiceProvider": "service_provider_id",
                   "ContentProvider": "content_provider_id",
                   "OriginServer": "origin_server_id",
                   "CDNPrefix": "cdn_prefix_id"}
        print kind, "exists with args", args
        return objs[0].get(id_name[kind])
    else:
	print "create", kind, "with args", args
        return Create(kind, args)
sp=CreateOrFind("ServiceProvider", {"account": "cord", "name": "cord", "enabled": True})
cp=CreateOrFind("ContentProvider", {"account": "test", "name": "test", "enabled": True, "service_provider_id": sp})
ors=CreateOrFind("OriginServer", {"url": "http://www.cs.arizona.edu", "content_provider_id": cp, "service_type": "HyperCache"})
pre=CreateOrFind("CDNPrefix", {"service": "HyperCache", "enabled": True, "content_provider_id": cp, "cdn_prefix": "test.vicci.org", "default_origin_server": "http://www.cs.arizona.edu"})
cp=CreateOrFind("ContentProvider", {"account": "onlab", "name": "onlab", "enabled": True, "service_provider_id": sp})
ors=CreateOrFind("OriginServer", {"url": "http://onlab.vicci.org", "content_provider_id": cp, "service_type": "HyperCache"})
pre=CreateOrFind("CDNPrefix", {"service": "HyperCache", "enabled": True, "content_provider_id": cp, "cdn_prefix": "onlab.vicci.org", "default_origin_server": "http://onlab.vicci.org"})
