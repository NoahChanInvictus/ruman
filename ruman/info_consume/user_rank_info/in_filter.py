#-*- coding:utf-8 -*-
from elasticsearch import Elasticsearch
import sys
import datetime
import time as TIME
from INDEX_TABLE import *
 
from time_utils import ts2datetime, datetime2ts
from global_utils import es_user_portrait as es
DAY = 24*3600


MAX_SIZE = 300

def in_sort_filter( time = 1 , sort_norm = 'bci' , sort_scope = 'in_nolimit' , arg = None , uid = [] ,key_search = False, number = 100):
    ischange = False
    scope = None
    norm = None
    sort_field = None
    time_field = None
    pre = None
    index = None
    type = None

    if sort_scope == 'in_nolimit':
        pass ;
    elif sort_scope == 'in_limit_domain':
        scope = 'domain';
    elif sort_scope == 'in_limit_topic':
        scope = 'topic_string';
    elif sort_scope == 'in_limt_keyword':
        pass;   #deal it outer 
    elif sort_scope == 'in_limit_hashtag':
        scope = 'hashtag'; #deal it inner
    elif sort_scope == 'in_limit_geo':
        scope = 'activity_geo'
    if sort_norm == 'bci':
        pre = 'bci_'
        ischange = False
        index = BCI_INDEX_NAME
        type = BCI_INDEX_TYPE
    elif sort_norm == 'bci_change':
        pre = 'bci_'
        ischange = True
        index = BCI_INDEX_NAME
        type = BCI_INDEX_TYPE 
    elif sort_norm == 'imp':
        pre = 'importance_'
        ischange = False
        index = IMP_INDEX_NAME
        type = IMP_INDEX_TYPE
    elif sort_norm == 'imp_change':
        pre = 'importance_'
        ischange = True
        index = IMP_INDEX_NAME
        type = IMP_INDEX_TYPE
    elif sort_norm == 'act':
        pre = 'activeness_'
        ischange = False
        index = ACT_INDEX_NAME
        type = ACT_INDEX_TYPE
    elif sort_norm == 'act_change':
        pre = 'activeness_'
        ischange = True
        index = ACT_INDEX_NAME
        type = ACT_INDEX_TYPE 
    elif sort_norm == 'ses':
        pre = 'sensitive_'
        ischange = False
        index = SES_INDEX_NAME
        type = SES_INDEX_TYPE
    elif sort_norm == 'ses_change':
        pre = 'sensitive_'
        ischange = True
        index = SES_INDEX_NAME
        type = SES_INDEX_TYPE 
    
    return es_search(pre ,scope ,arg,index,type,time,ischange , uid , key_search, number)
        
 
def es_search( pre , scope , arg , index_name , type_name  , time , ischange = False , uid_list = [] ,key_search = False, number = 100):
    today = TIME.time()
    
    print pre 
    print time
    print ischange
    sort_field = ''
    datetime = datetime2ts(ts2datetime(TIME.time()-DAY))
    if time == 1:
        if ischange :
            sort_field = pre + 'day_' + 'change'
        else:
            sort_field = pre  + str(datetime)
    elif time == 7 :
        if ischange :
            sort_field = pre + 'week_' + 'change'
        else :
            sort_field = pre + 'week_' + 'ave'
    elif time == 30 :
        if ischange :
            sort_field = pre + 'month_' + 'change'
        else :
            sort_field = pre + 'month_' + 'ave'
    print sort_field
    must = []
    if arg :
        must = [{"prefix": {scope: arg }} ]
    sort = []
    if sort_field:
        sort = [{ sort_field : { "order": "desc" } }]
    print sort   
    print must
    if not key_search:
        query = {
            "query": {
                "bool": {
                    "must": must,
                    "must_not": [],
                    "should": []
                }
            },
            "sort": sort , 
            "fields": [
                "uid"
            ],
            "size" : number
        }
    else :
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
            "sort": sort,
            "size" : number
        }      
    # print 'its me '
    print es,index_name,type_name,number
    print query
    print 'ssssssssssssssssss'
    result = es.search(index = index_name , doc_type = type_name , body = query)['hits']['hits']
    print len(result)
    uid_list = []
    for item in result :
        uid_list.append(item['_id'])
        #print item['_id']
    return uid_list

