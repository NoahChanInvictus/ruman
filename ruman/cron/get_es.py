# -*- coding: utf-8 -*-
from config import *
from sql_utils import *

import time

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import TransportError
from elasticsearch.helpers import bulk  

TODAY_DATE = time.strftime("%Y-%m-%d")


def es_update(index_name, type_name, text_id, updates_body):

    es = Elasticsearch([{'host':219.224.134.214,'port':9202}])
    es.update(index=index_name, doc_type=type_name, id=text_id, body=updates_body)


# 文本内容匹配查询
def es_content(query,start_day,end_day,index_name,type_name,size,score):
    '''
    input：
        query:关键词;start_day,end_day:起止日期;
        index_name,type_name:ES配置参数;
        size,score:ES控制参数
    return:
        content中含有query的文本内容
    '''
    start_time = time.mktime(time.strptime(str(start_day)+' 00:00:00', '%Y-%m-%d %H:%M:%S'))
    end_time = time.mktime(time.strptime(str(end_day)+' 23:59:59', '%Y-%m-%d %H:%M:%S'))
    # print start_time
    # print end_time
    es = Elasticsearch([{'host':ES_HOST,'port':ES_PORT}])
    query_body = {"size":size,"query":{ "filtered": {
        "query":{"match":{"content":query}},
        "filter":{"range":{"publish_time":{"gte": start_time,"lte": end_time}}}
    }}}

    res = es.search(index=index_name, doc_type=type_name, body=query_body,request_timeout=100)
    hits = res['hits']['hits']
    results = []
    if(len(hits)):
        for item in hits:
            text_id = item['_id']
            if(item['_score']>=score):
                if query in item['_source']['content']:
                    res = item['_source']
                    res['text_id'] = text_id
                    results.append(res)
    return results  


# wdzj查询，获取平台详细信息
def es_plat_detail(plat_name,theday):
    '''
    input：
        plat_name:平台名称
        theday:查询日期
    return:
        该平台theday抓取到的详细信息
    '''

    es = Elasticsearch([{'host':ES_HOST,'port':ES_PORT}])
    index_name = INDEX_WDZJ
    type_name = TYPE1
    query_body = {"size":5,"query":{"bool":{"must":[
        {"match":{"indate":theday}},
        {"match":{"platname":plat_name}}
    ]}}}

    res = es.search(index=index_name, doc_type=type_name, body=query_body,request_timeout=100)
    canditates = res['hits']['hits']
    fin_res = {}
    for item in canditates:
        results = item['_source']
        if(plat_name == results['platname']):
            fin_res = results
            break


    return fin_res


# 工商数据查询
def es_basic_info(firm_name, size=999):
    es = Elasticsearch([{'host': ES_HOST, 'port': ES_PORT}])
    index_name = INDEX_GONGSHANG
    type_name = 'basic_info'

    query_body = {
            "query": {
                "filtered":{
                    "filter":{
                        "term":{"firm_name": firm_name}
                            }
                        }
                    },
            "size": size
    }


    try:
        result = es.search(index=index_name, doc_type=type_name,body=query_body)['hits']['hits']
        return result
    except Exception,e:
        print e
        return []

def es_law_info(firm_name,size=999999):
    es = Elasticsearch([{'host': ES_HOST, 'port': ES_PORT}])
    index_name = INDEX_GONGSHANG
    type_name = 'law_info'
    query_body = {
        "query": {
            "filtered":{
                "filter":{
                    "term":{"firm_name": firm_name}
                        }
                    }
        },
    "size": size
    }

    try:
        result = es.search(index=INDEX_GONGSHANG, doc_type=type_name,body=query_body)['hits']['hits']
        return result
    except Exception,e:
        print e
        return []

def es_change_info(firm_name,size=999999):
    es = Elasticsearch([{'host': ES_HOST, 'port': ES_PORT}])
    index_name = INDEX_GONGSHANG
    type_name = 'change_info'
    query_body = {
        "query": {
            "filtered": {
                "filter": {
                    "term": {"firm_name": firm_name}
                }
            }
        },
        "size": size
    }

    try:
        result = es.search(index=index_name, doc_type=type_name, body=query_body)['hits']['hits']
        return result
    except Exception, e:
        print e
        return []

def es_invest_info(firm_name,size=999999):
    es = Elasticsearch([{'host': ES_HOST, 'port': ES_PORT}])
    index_name = INDEX_GONGSHANG
    type_name = 'invest_info'
    query_body = {
        "query": {
            "filtered": {
                "filter": {
                    "term": {"firm_name": firm_name}
                }
            }
        },
        "size": size
    }

    try:
        result = es.search(index=index_name, doc_type=type_name, body=query_body)['hits']['hits']
        return result
    except Exception, e:
        print e
        return []

def es_holder_info(firm_name,size=999999):
    es = Elasticsearch([{'host': ES_HOST, 'port': ES_PORT}])
    index_name = INDEX_GONGSHANG
    type_name = 'holder_info'
    query_body = {
        "query": {
            "filtered": {
                "filter": {
                    "bool":{
                        "must":[{"term": {"firm_name": firm_name}},
                                # {"term":{"holder_type":u'公司'}}
                                ]
                    }

                }
            }
        },
        "size": size
    }

    try:
        result = es.search(index=index_name, doc_type=type_name, body=query_body)['hits']['hits']
        return result
    except Exception, e:
        print e
        return []

def es_abnormal_info(firm_name,size=999999):
    es = Elasticsearch([{'host': ES_HOST, 'port': ES_PORT}])
    index_name = INDEX_GONGSHANG
    type_name = 'abnormal_info'
    query_body = {
        "query": {
            "filtered": {
                "filter": {
                    "bool": {
                        "must": [{"term": {"firm_name": firm_name}},
                                 # {"term": {"holder_type": u'公司'}}
                                 ]
                    }

                }
            }
        },
        "size": size
    }

    try:
        result = es.search(index=index_name, doc_type=type_name, body=query_body)['hits']['hits']
        return result
    except Exception, e:
        print e
        return []

def es_rule_match_content(target,source,size=1000):
    es = Elasticsearch([{'host': ES_HOST, 'port': ES_PORT}])
    results = []
    query_body = {
        "query": {
            "match": {
                "content": target
            }
        },
        "size": size
    }

    try:
        result = es.search(index=source, doc_type='type1', body=query_body)['hits']['hits']
    except Exception, e:
        print e
        result = []

    if result != []:
        for aa in result:
            if score_judge(aa):
                # content = aa['_source']['content']
                # results.append([target, content,source])
                results.append(aa)
    return results


def score_judge(item):
    # print item
    if item[u'_score'] < 0.6:
        return 0
    else:
        return 1

def es_emotion(query,index_name,type_name,size,score):
    '''
    input：
        query:关键词;start_day,end_day:起止日期;
        index_name,type_name:ES配置参数;
        size,score:ES控制参数
    return:
        content中含有query的文本内容
    '''
    # print start_time
    # print end_time
    es = Elasticsearch([{'host':ES_HOST,'port':ES_PORT}])
    query_body = {"size":size,"query":{"bool": { "must": [
        {"match_phrase": {"content": query}},
        {"match":{"emotion": "1"}},
        {"match":{"ad01": "0"}}]
    }}}

    res = es.search(index=index_name, doc_type=type_name, body=query_body,request_timeout=100)
    hits = res['hits']['hits']
    results = []
    if(len(hits)):
        for item in hits:
            text_id = item['_id']
            if(item['_score']>=score):
                res = item['_source']
                res['text_id'] = text_id
                results.append(res)
    return results