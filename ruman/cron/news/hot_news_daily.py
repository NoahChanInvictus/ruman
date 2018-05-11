# coding:utf-8 -*-
import time
import json

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import TransportError
from elasticsearch.helpers import bulk
from elasticsearch import helpers
from phgrocery import phgrocery
from key_word import jieba_keywords
import sys
reload(sys)
sys.path.append('../../')
from config import *

es = Elasticsearch([{'host':ES_HOST,'port':ES_PORT}])
def defaultDatabase():
    conn = mysql.connect(host=HOST,user=USER,password=PASSWORD,db=DEFAULT_DB,charset=CHARSET,cursorclass=pymysql.cursors.DictCursor)
    conn.autocommit(True)
    cur = conn.cursor()
    return cur

def hot_news(theday):
    today_result = []
    news_list = get_all_news(theday)
    for news in news_list:
        content =  news['_source']['content']
        hot_spot = phgrocery(content)       #判断是否是热点新闻
        # print hot_spot
        if hot_spot:
            # print 'in!'
            iter_source = news['_source']
            iter_source.update({'text_id':news['_id']})
            today_result.append(iter_source)
            # today_result.append(news['_source'].update({'text_id':news['_id'],'date':theday}))
    return today_result
def save_results(theday,data):
    cur = defaultDatabase()
    for item in data:
        order = 'insert into '+TABLE_HOTNEWS+"\
            (web,title,url,abstract,author,comments,tend,content,in_time,text_id,panel,key_word,date) \
            values ('%s','%s','%s','%s','%s','%i','%f','%s','%s','%s','%s','%s','%s')" % (item['web'].encode('utf-8'),item['title'].encode('utf-8'),item['url'].encode('utf-8'),\
                                            item['abstract'].encode('utf-8'),item['author'].encode('utf-8'),int(item['comments']),float(item['tend']),\
                                            item['content'].encode('utf-8'),item['in_time'],item['text_id'],item['panel'].encode('utf-8'),item['key'].encode('utf-8'),theday)
        try:
            cur.execute(order)
            # conn.commit()
        except Exception,e:
            print e
def get_all_news(theday):

    index_name = 'news_new'
    w_limit = 10000
    start_ts = time.mktime(time.strptime(str(theday)+' 00:00:00', '%Y-%m-%d %H:%M:%S'))
    end_ts = time.mktime(time.strptime(str(theday)+' 23:59:59', '%Y-%m-%d %H:%M:%S'))
    es_search_options ={
        "query": {

        "bool": {
        "must": [
        {
        "range": {
            "publish_time": {
            "from": str(start_ts),
            "to": str(end_ts)
            }
        }
        },
        
        #{"term":{"topic":topic,}}
        
        ],
        "must_not": [ ],
        "should": [ ]
        }
        },
        "from": 0,
        "size": w_limit,
        "sort": [{"publish_time":"asc"} ],
        "facets": { }
    } 
    #{"query":{ "bool": {
    #     # "must":{"term":{"ad01":1}},
    #     ##########
    #     # 改动版本，用于更新之前错分的
    #     # "should":[{"term":{"ad01":1}},{"term":{"ad01":0}}],
    #     # "should":[{"term":{"fintext":1}}],
    #     # "minimum_should_match":1,
    #     ##########
    #     # "filter":{"range":{"publish_time":{"gte": start_ts,"lte": end_ts}}}
    # }}}
    es_result = es.search(index=index_name, doc_type='type1',body=es_search_options)['hits']['hits']
    # final_result = get_result_list(es_result)
    # return final_result
    # print es_result
    return es_result

def hot_news_daily(theday):
    today_result = hot_news(theday)
    save_results(theday,today_result)
    

if __name__ == '__main__':
    hot_news_daily('2018-04-20')
    # print today_result[0]
    # text = '美国财长说漏一句话世界都惊了,美元对人民币狂跌'
    # print phgrocery(text)
    # keywords =  jieba_keywords(text,5)
    # print ' '.join(keywords)            