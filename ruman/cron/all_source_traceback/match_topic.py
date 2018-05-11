# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.path.append('../../')
from config import *
from es import es
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import TransportError
from elasticsearch.helpers import bulk

def match_topic_kw(news_id,keywords_list,source,doc_type,size=10000):
    result = []
    keyword_str = ''.join(keywords_list)
    # 通过一组关键词查找相关文本
    query_body = {
        "query":{
            "match":{
                "content":keyword_str       #这个可能还得改，争取用一个list
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
        new_item['news_id'] = news_id
        result.append(new_item)
    return result

def save_topic_es(data,index,doc_type):
    ACTIONS = []
    count = 0
    for item in data:
        action = { 
                    "_op_type":"index" ,
                    "_index":index,  
                    "_type":doc_type,
                    # "_id":doc_id,  
                    "_source":item
                    }
        ACTIONS.append(action)
        count += 1
        if count % 100 == 0:
            success, _ = bulk(es, ACTIONS, raise_on_error=True, request_timeout=400)
            ACTIONS = []
            print 'in',doc_type,count,'has been inserted!'
    # 最后把余下的也bulk进去
    if ACTIONS != []:
        success, _ = bulk(es, ACTIONS, raise_on_error=True, request_timeout=400)
        ACTIONS = []
def all_source_match(news_id,keywords_list):
    for source,doc_type in TYPE1_DICT.iteritems():
        result = match_topic_kw(news_id,keywords_list,source,doc_type)
        save_topic_es(result,index=TOPIC_ABOUT_INDEX,doc_type=source)
if __name__ == '__main__':
    # main()
    # result = match_topic_kw(['今天','人民币','担忧'],'forum','type1')
    # save_topic_es(result,index=TOPIC_ABOUT_INDEX,doc_type='forum')
    all_source_match(['今天','人民币','担忧'])
    # print result[1]