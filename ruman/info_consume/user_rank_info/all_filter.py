#-*- coding:utf-8 -*-
#  all es refer to es_user_profile
from elasticsearch import Elasticsearch
import sys
import datetime
import time as TIME
from INDEX_TABLE import *
 
from time_utils import ts2datetime, datetime2ts
from global_utils import es_user_portrait as es
from global_utils import es_user_profile

DAY = 24*3600

def all_sort_filter( uid_list = [] , sort_norm = 'imp' , time = 1 , key_search = False, number=100 ):
    print "all_filter,", number
    uid = []
    if sort_norm == 'bci':
        uid = history_sort('bci_',BCIHIS_INDEX_NAME,BCIHIS_INDEX_TYPE,uid_list,time,False , key_search, number)
    elif sort_norm == 'bci_change':
        uid = history_sort('bci_',BCIHIS_INDEX_NAME,BCIHIS_INDEX_TYPE,uid_list,time,True ,  key_search, number)
    elif sort_norm == 'ses':
        uid = history_sort('sensitive_',SESHIS_INDEX_NAME,SESHIS_INDEX_TYPE,uid_list,time,False, key_search, number)
    elif sort_norm == 'ses_change':
        uid = history_sort('sensitive_',SESHIS_INDEX_NAME,SESHIS_INDEX_TYPE,uid_list,time,True, key_search, number)
    elif sort_norm == 'fans':
        uid = sort_total_number("user_fansnum" , uid_list, time, key_search, number)
    elif sort_norm == 'weibo_num':
        uid = sort_total_number("weibo_", uid_list, time, key_search, number)
    return uid

def sort_total_number(prefix, uid_list, time, key_search, number):
    if prefix == "weibo_":
        if int(time) == 1:
            order = prefix + 'day_last'
        elif int(time) == 7:
            order = prefix + 'week_sum'
        elif int(time) == 30:
            order = prefix + 'month_sum'
    else:
        order = prefix

    if uid_list:
        query_body = {
            "query":{
                "filtered": {
                    "filter": {
                        "terms":{
                            "uid": uid_list
                        }
                    }
                }
            },
            "sort":{order: {"order": "desc"}},
            "size": number
        }
    else:
        query_body = {
            "query":{
                "match_all": {}
            },
            "sort": { order: {"order": "desc"} },
            "size": number
        }


    search_results = es_user_profile.search(index="bci_history", doc_type="bci", body=query_body, _source=False)['hits']['hits']
    uid_list = []
    if search_results:
        for item in search_results:
            uid_list.append(item['_id'])

    return uid_list


def history_sort( prefix ,index_name , index_type , uid_list , time , ischange = False ,key_search = False, number=100):
    es = es_user_profile # 全网是81的es
    sort_field = prefix
    ts = datetime2ts(ts2datetime(TIME.time()-DAY))
    if time == 1 :
        if ischange:
            sort_field += "day_change"
        else:
            if prefix == "bci_":
                sort_field = "bci_day_last" 
            else:
                sort_field = "sensitive_score_%s" %ts
    elif time == 7:
        if ischange:
            sort_field += "week_change"
        else:
            sort_field += "week_ave"
    else:
        if ischange:
            sort_field += "month_change"
        else:
            if sort_field == "sensitive_":
                sort_field = "senstiive_month_ave"
            else:
                sort_field += "month_ave"

    query = {}
    if key_search:
        query = {
                "query": {
                    "filtered": {
                        "filter": {
                            "terms": {
                                "uid": uid_list
                            }
                        }       
                    }           
                },
                "sort": [{ sort_field : { "order": "desc" } }],
                "size" : number
            }
    else :
        query = {
            "query":{
                "match_all":{}},
            "sort": [{ sort_field : { "order": "desc" } }],
            "size" : number
        }
    result = es.search(index = index_name , doc_type = index_type , body = query, _source=False)['hits']['hits']
    sorted_uid_list = []
    for item in result :
        sorted_uid_list.append(item['_id'].encode("utf-8") )
    #jln
    #none_in_list = set(uid_list) - set(sorted_uid_list)
    # if none_in_list:
    #     sorted_uid_list.extend(list(none_in_list))
    return sorted_uid_list




