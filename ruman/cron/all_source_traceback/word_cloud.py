# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.path.append('../../')
import json

from config import *
from elasticsearch import Elasticsearch

def defaultDatabase():
    conn = mysql.connect(host=HOST,user=USER,password=PASSWORD,db=DEFAULT_DB,charset=CHARSET,cursorclass=pymysql.cursors.DictCursor)
    conn.autocommit(True)
    cur = conn.cursor()
    return cur

def word_cloud(topic,size=10000):
    es = Elasticsearch([{'host':ES_HOST,'port':ES_PORT}])
    all_source_result = {}
    query_body = {
        "query": {

        "bool": {
        "must": [
        # {
        # "range": {
        #     "publish_time": {
        #     "from": begin_ts,
        #     "to": end_ts
        #     }
        # }
        # },
        
        {"term":{"topic":topic,}}
        
        ],
        "must_not": [ ],
        "should": [ ]
        }
        },
        "from": 0,
        "size": size,
        "sort": [ ],
        "facets": { }
    }
    for source in TOPIC_ABOUT_DOCTYPE:
        iter_results = {}
        # print TOPIC_ABOUT_INDEX,query_body
        es_result = es.search(index=TOPIC_ABOUT_INDEX, doc_type=source,body=query_body)['hits']['hits']
        one_source_keywords = []
        if len(es_result):
            for item in es_result:
                keyword_string = item['_source']['k']
                if keyword_string != '':
                    keyword_list = keyword_string.split(' ')
                    while '' in keyword_list:
                        keyword_list.remove('')
                    one_source_keywords += keyword_list
        one_source_result = {}
        for keyword in one_source_keywords:
            if one_source_result.has_key(keyword):
                one_source_result[keyword] += 1
            else:
                one_source_result[keyword] = 1
        # print one_source_result
        all_source_result[source] = one_source_result
    return all_source_result
def save_word_cloud(topic,word_cloud):
    cur = defaultDatabase()
    for source,words in word_cloud.iteritems():
        order = 'insert into '+TABLE_PROPAGATE+' \
            (topic,source,words) \
            values ("%s","%s","%s",)' % (topic,source,str(json.dumps(words)))   #这里存在些问题
        try:
            cur.execute(order)
            # conn.commit()
        except Exception,e:
            print e

if __name__ == '__main__':
    topic = '今天人民币担忧'
    cloud = word_cloud(topic)
    save_word_cloud(topic,cloud)