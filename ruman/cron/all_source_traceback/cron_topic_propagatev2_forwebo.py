# -*- coding:utf-8 -*-
import time
import sys
reload(sys)
sys.path.append('../../')
# sys.path.append('../')
from time_utils import ts2HourlyTime
TOP_MESSAGE_LIMIT = 500
TOP_KEYWORDS_LIMIT = 100
Fifteenminutes = 60*15
# MTYPE_COUNT = 5
from config import *
# from db import defaultDatabase
from es import es214 as es
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import TransportError
from elasticsearch.helpers import bulk
# es = Elasticsearch([{'host':ES_HOST,'port':ES_PORT}])
def defaultDatabase():
    conn = mysql.connect(host=SQL_HOST,user=SQL_USER,password=SQL_PASSWD,db=DEFAULT_DB,charset=SQL_CHARSET,cursorclass=pymysql.cursors.DictCursor)
    conn.autocommit(True)
    cur = conn.cursor()
    return cur
# def compute_allsource_traceback(news_id,begin_ts,end_ts,w_limit):
def compute_mtype_count(news_id, begin_ts, end_ts,size=5000):
    

    query_body = {
        "query": {

        "bool": {
        "must": [
        {
        "range": {
            "publish_time": {
            "from": begin_ts,
            "to": end_ts
            }
        }
        },
        
        {"term":{"news_id":news_id,}}
        
        ],
        # "must_not": [ ],
        # "should": [ ]
        }
        },
        "from": 0,
        "size": size,
        "sort": [ ],
        "facets": { }
    }

    time_period_results = []
    for source in TOPIC_ABOUT_DOCTYPE:
        iter_results = {}
        # print TOPIC_ABOUT_INDEX,query_body
        # print source,type(news_id)
        # print es.search(index=TOPIC_ABOUT_INDEX, doc_type=source,body=query_body)
        mtype_count = es.search(index=TOPIC_ABOUT_INDEX, doc_type=source,body=query_body)['hits']['total']
        # print source,mtype_count
        iter_results['count'] = mtype_count
        iter_results['source'] = source
        iter_results['begin_ts'] = begin_ts
        iter_results['end_ts'] = end_ts
        iter_results['news_id'] = news_id
        time_period_results.append(iter_results)

    
    return time_period_results



def propagateCronTopic(news_id, start_ts, over_ts, during=Fifteenminutes, w_limit=TOP_MESSAGE_LIMIT, k_limit=TOP_KEYWORDS_LIMIT):
    
    start_ts = int(start_ts)
    over_ts = int(over_ts)

    over_ts = ts2HourlyTime(over_ts, during)
    interval = (over_ts - start_ts) / during

    for i in range(interval,0,-1):  #每15分钟计算一次
        # message_type_count = {}    #五类消息的数量
        # mtype_kcount = {}   #五类消息的TOPK关键词
        # mtype_content = {}    #五种类型的内容，原系统是按转发数排序，不知效果如何

        begin_ts = over_ts - during * i
        end_ts = begin_ts + during

        # print news_id,begin_ts,end_ts
        #print begin_ts, end_ts, 'topic %s starts calculate' % topic.encode('utf-8')
        mtype_count = compute_mtype_count(news_id, begin_ts, end_ts)
        # print mtype_count
        # print mtype_count
        # mtype_kcount = compute_mtype_keywords(topic, begin_ts, end_ts ,k_limit)
        # allsource_traceback = compute_allsource_traceback(news_id,begin_ts,end_ts,w_limit)
        # print allsource_traceback
        save_results('count', news_id, mtype_count, during)
        # save_results('kcount', topic, mtype_kcount, during, k_limit, w_limit)
        # save_results('weibo', topic, mtype_weibo, during, k_limit)
def save_results(mode,topic,data,during):
    cur = defaultDatabase()
    if mode=='count':
        for item in data:
            order = 'insert into '+TABLE_PROPAGATE+' \
            (news_id,source,begin_ts,end_ts,count) \
            values ("%s","%s","%i","%i","%i")' % (item['news_id'],item['source'],item['begin_ts'],\
                                            item['end_ts'],item['count'])
            try:
                cur.execute(order)
                # conn.commit()
            except Exception,e:
                print e


def propagateTask(news_id,theday,back_day):
    
    end_ts = time.mktime(time.strptime(str(theday)+' 23:59:59', '%Y-%m-%d %H:%M:%S'))
    start_ts = end_ts - back_day * 3600*24
    # print start_time,end_time   
    propagateCronTopic(news_id,start_ts,end_ts)
if __name__ == '__main__':
    # topic = '今天人民币担忧'
    start_date = '2017-10-01'
    end_date = '2017-11-20'
    propagateTask(6679,end_date,10)