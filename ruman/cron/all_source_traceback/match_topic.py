# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.path.append('../../')
from config import *
from es import es
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import TransportError
from elasticsearch.helpers import bulk

def match_topic_kw(keywords_list,source,doc_type,size=1000):
    result = []
    keyword_str = ''.join(keywords_list)
    # 通过一组关键词查找相关文本
    query_body = {
        "query":{
            "match":{
                "content":keyword_str
            }
        },
        "size":size
    }
    # print keyword_str
    es_result = es.search(index=source,doc_type=doc_type,body=query_body,request_timeout=400)
    es_result = es_result['hits']['hits']
    # print result
    for item in es_result:
        new_item = item['_source']
        new_item['source'] = source
        new_item['original_id'] = item['_id']
        new_item['topic'] = keyword_str
        result.append(new_item)
    return result

def save_topic_es(data,index=TOPIC_ABOUT_INDEX,doc_type=TOPIC_ABOUT_DOCTYPE):
    ACTIONS = []
    count = 0
    for item in data:
        action = { 
                    "_op_type":"index" ,
                    "_index":index,  
                    "_type":doc_type,
                    # "_id":doc_id,  
                    "doc":item
                    }
        ACTIONS.append(action)
        count += 1
        if count % 100 == 0:
            success, _ = bulk(es, ACTIONS, raise_on_error=True, request_timeout=400)
            ACTIONS = []
            print 'in',index,count,'has been inserted!'
    # 最后把余下的也bulk进去
    if ACTIONS != []:
        success, _ = bulk(es, ACTIONS, raise_on_error=True, request_timeout=400)
        ACTIONS = []

if __name__ == '__main__':
    # main()
    result = match_topic_kw(['今天','人民币','担忧'],'bbs','type1')
    save_topic_es(result)
    # print result[1]