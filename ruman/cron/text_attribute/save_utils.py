# -*- coding: UTF-8 -*-
import sys
import json
import time
reload(sys)
sys.path.append('../../')
from global_utils import es_user_portrait as es
from global_utils import R_CLUSTER_FLOW2 as r_cluster
from time_utils import datetime2ts, ts2datetime

index_type = 'user'
index_name = 'user_portrait'

def attr_hash(uid):
    hashtag_results = {}
    now_ts = time.time()
    # test
    now_ts = datetime2ts('2013-09-08')
    date = ts2datetime(now_ts)
    ts = datetime2ts(date)
    for i in range(1,8):
        ts = ts - 24*3600
        result_string = r_cluster.hget('hashtag_'+str(ts), str(uid))
        if result_string:
            result_dict = json.loads(result_string)
            for hashtag in result_dict:
                count = result_dict[hashtag]
                try:
                    hashtag_results[hashtag] += count
                except:
                    hashtag_results[hashtag] = count
    return hashtag_results
            

def save_user_results(bulk_action):
    print 'save utils bulk action len:', len(bulk_action)
    #print 'bulk action:', bulk_action
    print es.bulk(bulk_action, index='user_portrait_1222', doc_type=index_type, timeout=600)
    return True    

