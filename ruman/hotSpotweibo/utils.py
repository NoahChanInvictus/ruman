#!/usr/bin/env python
#encoding: utf-8

import time 
import datetime 

import json
import csv
import random

from elasticsearch import Elasticsearch
from ruman.time_utils import *


#config
weibo_es = Elasticsearch('219.224.134.216:9201',timeout=1000)
INDEX_SENCE = 'social_sensing_task'
TYPE_SENCE = 'rumor-media'
TYPE_FLOAT_TEXT = "text"
ES_INDEX_CAL_LIST='rumor_calculated_list'
WEBOUSER_INDEX = 'weibo_user'

def get_user(uid):
    uid = int(uid)
    query_body = {"size":10,"query":{"match":{"uid":uid}}}

    res = weibo_es.search(index=WEBOUSER_INDEX, doc_type='user', body=query_body,request_timeout=100)
    hits = res['hits']['hits']
    if len(hits):
        return hits[0]['_source']['nick_name']
    else:
        return str(uid)
'''
def search_hotspot():
    result = []
    query_body = {
            'size':200,
            'query':{
                    'term':{
                        'rumor_label': 0
                        }
        }
    }
    results = weibo_es.search(index=ES_INDEX_CAL_LIST, body=query_body)
    print results
    if results:
        hotspotweibo = results['hits']['hits']
        for hotweibo in hotspotweibo:
            result.append(hotweibo['_source'])
    return json.dumps(result)'''

def search_hotspot():
    l1 = []
    l2 = []
    with open('./ruman/hotSpotweibo/dup_weibo_wenben.txt') as f1:
        for i in f1.readlines():
            l1.append(json.loads(i)['mid'])
    with open('./ruman/hotSpotweibo/dup_weibo_redian_0523.txt') as f2:
        for i in f2.readlines():
            l2.append(json.loads(i)['mid'])
    l1.extend(l2)
    result = []
    for mid in l1:
        query_body = {"size":400,"query":{"match": {"mid":mid}}}
        results = weibo_es.search(index=ES_INDEX_CAL_LIST, body=query_body)
        #print results
        if results:
            hotspotweibo = results['hits']['hits']
            for hotweibo in hotspotweibo:
                result.append(hotweibo['_source'])
    result = sorted(result,key= lambda x:(x['timestamp']),reverse=True)
    return json.dumps(result)


def search_hotspot_infor(en_name):
    query_body = {"size":10,"query":{"match_phrase": {"en_name":en_name}}}
    res = weibo_es.search(index=ES_INDEX_CAL_LIST, body=query_body)
    hits = res['hits']['hits']
    if len(hits):
        dic = {}
        dic['query_kwds'] = ','.join(hits[0]['_source']['query_kwds'])
        dic['publish_time'] = ts2date(hits[0]['_source']['timestamp'])
        dic['author'] = get_user(hits[0]['_source']['uid'])
        dic['comment'] = hits[0]['_source']['comment']
        dic['retweeted'] = hits[0]['_source']['retweeted']
        dic['text'] = hits[0]['_source']['text']
        return dic
    else:
        return {}

if __name__ == '__main__':
    search_hotspot()