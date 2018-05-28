# -*- coding: utf-8 -*-

"""
this function is uesd to search daily weibo behavior infomation \
of an active user

"""
import sys
from elasticsearch import Elasticsearch
from ruman.global_utils import ES_CLUSTER_FLOW1

def search_weibo_behavior(user_index, uid, d_type="bci"):
    """
    use user_id as keyword

    """
    es = ES_CLUSTER_FLOW1
    index_exist = es.indices.exists(index=user_index)

    if not index_exist:
        return None
    else:
        uid_exist = es.exists(index=user_index, id=uid)
        if not uid_exist:
            return None
        else:
            user_info = es.get(index=user_index, doc_type=d_type, id=uid, _source=True)['_source']
            return user_info
"""
if __name__ == "__main__":
    print search_weibo_behavior("20130901", "1713926427")

"""

