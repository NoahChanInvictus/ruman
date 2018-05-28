# -*- coding:utf-8 -*-

from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
import sys
"""
reload(sys)
sys.path.append('./../')
from global_utils import es_user_portrait as es
from parameter import DETAIL_SOCIAL_SENSING as index_sensing_task
"""
from ruman.global_utils import es_user_portrait as es
from ruman.parameter import DETAIL_SOCIAL_SENSING as index_sensing_task

def delete_es(task_name):
    s_re = scan(es, query={"query":{"match_all":{}},"size":1000}, index=index_sensing_task, doc_type=task_name)
    bulk_action = []
    count = 0
    search_list = []
    uid_list = []

    while 1:
        try:
            uid = s_re.next()['_id']
            count += 1
            action = {"delete": {"_index": index_sensing_task, "_type": task_name, "_id": uid}}
            bulk_action.append(action)
            if count % 100 == 0:
                es.bulk(bulk_action, index=index_sensing_task, doc_type=task_name, timeout=60)
                bulk_action = []
        except StopIteration:
            print "all done"
            if bulk_action:
                es.bulk(bulk_action, index=index_sensing_task, doc_type=task_name, timeout=60)
            break
        except Exception, r:
            print Exception, r

    if bulk_action:
        es.bulk(bulk_action, index=index_sensing_task, doc_type=task_name, timeout=60)

    print count

    return "1"

if __name__ == "__main__":
    delete_es("律师群体言论".decode('utf-8'))
    delete_es("洪水灾情".decode('utf-8'))
    delete_es("民主言论".decode('utf-8'))
    delete_es("媒体感知社会事件".decode('utf-8'))
