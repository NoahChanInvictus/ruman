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
sys.path.append('../')
from all_source_traceback.match_topic import all_source_match
from all_source_traceback.cron_topic_propagatev2 import propagateTask
from all_source_traceback.word_cloudv2 import word_cloud_main
from all_source_traceback.clusteringv2 import clustering_main
# from fintext_classify.fin_text import fin_classify
from tgrocery import Grocery
model_fintext = Grocery('../fintext_classify/model_fintext')
model_fintext.load()


es = Elasticsearch([{'host':ES_HOST,'port':ES_PORT}])
def defaultDatabase():
    conn = mysql.connect(host=SQL_HOST,user=SQL_USER,password=SQL_PASSWD,db=DEFAULT_DB,charset=SQL_CHARSET,cursorclass=pymysql.cursors.DictCursor)
    conn.autocommit(True)
    cur = conn.cursor()
    return cur

def hot_news(theday):
    today_result = []
    news_list = get_all_news(theday)
    print len(news_list),'news in',theday
    for news in news_list:
        content =  news['_source']['content']
        hot_spot = phgrocery(content)       #判断是否是热点新闻
        fintext = int(model_fintext.predict(content).predicted_y)     #判断是否是金融文本
        # print hot_spot
        if hot_spot and fintext:
            # print 'in!'
            iter_source = news['_source']
            keywords = jieba_keywords(content,5)
            iter_source['key'] = ' '.join(keywords)
            iter_source.update({'text_id':news['_id']})
            today_result.append(iter_source)
        if len(today_result) % 100 == 0:
            print len(today_result)
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
    
    es_result = es.search(index=index_name, doc_type='type1',body=es_search_options)['hits']['hits']
    
    return es_result
def get_hot_news(theday):
    cur = defaultDatabase()
    order = "select * from " + TABLE_HOTNEWS + " where date='%s'" % (theday)
    try:
        cur.execute(order)
        result = cur.fetchall()
        # conn.commit()
    except Exception,e:
        print e
    return result
def hot_news_daily(theday):
    today_result = hot_news(theday)
    print len(today_result),'hot news in',theday
    save_results(theday,today_result)
    print 'hot news saved!'
    result = get_hot_news(theday)
    print 'There are',len(result),'hot news in',theday
    for news in result:
        content = news['content']
        key_word = news['key_word']
        news_id = news['id']
        print 'news id:',news_id

        

        print 'load all source data start!'
        all_source_match(news_id,key_word)        #读取并保存各个通道的相关文本
        print 'load data finished!'

        # print 'propagate compute start!'
        # propagateTask(news_id,theday,240)           #计算120天的多通道溯源记录     正式版应该倒查7天
        # print 'propagate compute end!'

        print 'word cloud start!'
        word_cloud_main(news_id)                    #计算词云并存储
        print 'word cloud end!'

        print 'clustering start!'
        clustering_main(news_id)                    #观点聚类
        print 'clustering end!'
        # break




if __name__ == '__main__':
    # hot_news_daily('2018-04-20')
    hot_news_daily('2018-04-21')
    # print today_result[0]
    # text = '美国财长说漏一句话世界都惊了,美元对人民币狂跌'
    # print phgrocery(text)
    # keywords =  jieba_keywords(text,5)
    # print ' '.join(keywords)            