# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.path.append('../../')
import json

from config import *
from elasticsearch import Elasticsearch

from news.key_word import jieba_keywords

def defaultDatabase():
    conn = mysql.connect(host=SQL_HOST,user=SQL_USER,password=SQL_PASSWD,db=DEFAULT_DB,charset=SQL_CHARSET,cursorclass=pymysql.cursors.DictCursor)
    conn.autocommit(True)
    cur = conn.cursor()
    return cur

def word_cloud(news_id,size=10000):
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
        
        {"term":{"news_id":news_id,}}
        
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
                if source == 'webo':        #微博原始数据没有关键词要自己重新算
                    item['_source']['k'] = ' '.join(jieba_keywords(item['_source']['content'],5))
                try:
                    keyword_string = item['_source']['k']
                except:
                    keyword_string = item['_source']['key']
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
def save_word_cloud(news_id,word_cloud):
    cur = defaultDatabase()
    for source,words in word_cloud.iteritems():
        words_string = ''
        for k,v in words.iteritems():
            words_string+=str(k)+':'+str(v)+','
        # print words_string
        order = 'insert into '+TABLE_WORDCLOUD+' \
            (news_id,source,words) \
            values ("%s","%s","%s")' % (news_id,source,words_string)   #这里存在些问题
        # print order
        try:
            cur.execute(order)
            # conn.commit()
        except Exception,e:
            print e
def word_cloud_main(news_id):
    cloud = word_cloud(news_id)
    save_word_cloud(news_id,cloud)
if __name__ == '__main__':
    topic = '今天人民币担忧'
    cloud = word_cloud(topic)
    save_word_cloud(topic,cloud)