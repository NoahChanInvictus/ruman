#-*- coding: utf-8 -*-

import time
import sys
import json
from elasticsearch import Elasticsearch
reload(sys)
sys.path.append('../')
from time_utils import datetime2ts,ts2datetime
from global_utils import R_CLUSTER_FLOW3, R_CLUSTER_FLOW2, R_CLUSTER_FLOW1

uidlist = []
f = open("uid_list_0520.txt")
for line in f:
    uid = line.strip()
    uidlist.append(uid)
f.close()

data = []
dates = ["2016-05-14", "2016-05-15", "2016-05-16", "2016-05-17", "2016-05-18", "2016-05-19", "2016-05-20"]
tss = [datetime2ts(d) for d in dates]
for ts in tss:
   ns = "hashtag_" + str(ts)
   hashtag_list = R_CLUSTER_FLOW3.hmget(ns, uidlist)
   hashtag_list = [json.loads(h) if h else None for h in hashtag_list]
   uhlist = zip(uidlist, hashtag_list)
   uhtlist = []
   for uh in uhlist:
       uh = list(uh)
       uh.append(ts)
       uhtlist.append(uh)
   data.extend(uhtlist)

with open("hashtag_0521.txt", "w") as fw:
    for d in data:
        if d[1] != None:
            fw.write("%s\n" % json.dumps(d))

at_data = []
for ts in tss:
   ns = "at_" + str(ts)
   hashtag_list = R_CLUSTER_FLOW2.hmget(ns, uidlist)
   hashtag_list = [json.loads(h) if h else None for h in hashtag_list]
   uhlist = zip(uidlist, hashtag_list)
   uhtlist = []
   for uh in uhlist:
       uh = list(uh)
       uh.append(ts)
       uhtlist.append(uh)
   at_data.extend(uhtlist)

with open("at_0521.txt", "w") as fw:
    for a in at_data:
        if a[1] != None:
            fw.write("%s\n" % json.dumps(a))
