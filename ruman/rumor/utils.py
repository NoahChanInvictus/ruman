#!/usr/bin/env python
#encoding: utf-8
import sys
reload(sys)
sys.path.append("../../")

import time 
import datetime 
import pymysql as mysql
import pymysql.cursors

import json
import csv
import random

from elasticsearch import Elasticsearch
from ruman.time_utils import *
from ruman.global_config import db


#config
weibo_es = Elasticsearch('219.224.134.216:9201',timeout=1000)
INDEX_SENCE = 'social_sensing_task'
TYPE_SENCE = 'rumor-media'
TYPE_FLOAT_TEXT = "text"
ES_INDEX_CAL_LIST='rumor_calculated_list'
WEBOUSER_INDEX = 'weibo_user'

rumor_es = Elasticsearch('219.224.134.211:9201',timeout=1000)

SQL_HOST = "219.224.134.220"
SQL_USER = "root"
SQL_PASSWD = ""
DEFAULT_DB = "weibocase"
SQL_CHARSET = "utf8"

def default_db(host=SQL_HOST, user=SQL_USER, passwd=SQL_PASSWD, db=DEFAULT_DB, charset=SQL_CHARSET):
    conn = pymysql.connect(host=host, user=user, passwd=passwd, db=db, charset=charset, cursorclass=pymysql.cursors.DictCursor)
    return conn

def defaultDatabase():
    conn = mysql.connect(host=SQL_HOST,user=SQL_USER,password=SQL_PASSWD,db=DEFAULT_DB,charset=SQL_CHARSET,cursorclass=pymysql.cursors.DictCursor)
    conn.autocommit(True)
    cur = conn.cursor()
    return cur

def defaultDatabaseConn():
    conn = mysql.connect(host=SQL_HOST,user=SQL_USER,password=SQL_PASSWD,db=DEFAULT_DB,charset=SQL_CHARSET,cursorclass=pymysql.cursors.DictCursor)
    conn.autocommit(True)
    return conn

def get_user(uid):
    uid = int(uid)
    query_body = {"size":10,"query":{"match":{"uid":uid}}}

    res = weibo_es.search(index=WEBOUSER_INDEX, doc_type='user', body=query_body,request_timeout=100)
    hits = res['hits']['hits']
    if len(hits):
        return hits[0]['_source']['nick_name']
    else:
        return str(uid)

def search_rumor():
    result = []
    query_body = {
            'size':400,
            'query':{
                "bool": {"must":[
                    {'term':{
                        'rumor_label': 1
                        }},
                    {'term':{"fin_label": 1}},
                    {'term':{"cal_status":-1}}
                    ]}
        }
    }
    results = weibo_es.search(index=ES_INDEX_CAL_LIST, body=query_body)
    # print results
    if results:
        hotspotweibo = results['hits']['hits']
        for hotweibo in hotspotweibo:
            result.append(hotweibo['_source'])
    result = sorted(result,key= lambda x:(x['timestamp']),reverse=True)
    return json.dumps(result)

def rumorWarning():
    theday = '2016-11-26'
    weekago = ts2datetime(datetime2ts(theday) - 6*24*3600)   #要记得少一天
    monthago = ts2datetime(datetime2ts(theday) - 29*24*3600)
    seasonago = ts2datetime(datetime2ts(theday) - 89*24*3600)
    weeknum = 0
    monthnum = 0
    seasonnum = 0
    query_body = {"size":2000,"query":{ "match": {"rumor_label" :1}}}

    for day in get_datelist(int(weekago.split('-')[0]),int(weekago.split('-')[1]),int(weekago.split('-')[2]),\
        int(theday.split('-')[0]),int(theday.split('-')[1]),int(theday.split('-')[2])):

        res = weibo_es.search(index=ES_INDEX_CAL_LIST, doc_type=day, body=query_body,request_timeout=100)
        hits = res['hits']['hits']
        
        weeknum += len(hits)

    for day in get_datelist(int(monthago.split('-')[0]),int(monthago.split('-')[1]),int(monthago.split('-')[2]),\
        int(theday.split('-')[0]),int(theday.split('-')[1]),int(theday.split('-')[2])):

        res = weibo_es.search(index=ES_INDEX_CAL_LIST, doc_type=day, body=query_body,request_timeout=100)
        hits = res['hits']['hits']
        
        monthnum += len(hits)

    for day in get_datelist(int(seasonago.split('-')[0]),int(seasonago.split('-')[1]),int(seasonago.split('-')[2]),\
        int(theday.split('-')[0]),int(theday.split('-')[1]),int(theday.split('-')[2])):

        res = weibo_es.search(index=ES_INDEX_CAL_LIST, doc_type=day, body=query_body,request_timeout=100)
        hits = res['hits']['hits']
        
        seasonnum += len(hits)

    return {'weeknum':weeknum,'monthnum':monthnum,'seasonnum':seasonnum}

def rumorMonger(date):
    theday = '2016-11-26'
    dateago = ts2datetime(datetime2ts(theday) - (date-1)*24*3600)   #要记得少一天
    query_body = {"size":2000,"query":{ "match": {"rumor_label" :1}}}
    hits = []

    for day in get_datelist(int(dateago.split('-')[0]),int(dateago.split('-')[1]),int(dateago.split('-')[2]),\
        int(theday.split('-')[0]),int(theday.split('-')[1]),int(theday.split('-')[2])):

        res = weibo_es.search(index=ES_INDEX_CAL_LIST, doc_type=day, body=query_body,request_timeout=100)
        hits.extend(res['hits']['hits'])
        
    userlist = {}
    for hit in hits:
        if hit["_source"]['uid'] in userlist.keys():
            userlist[hit["_source"]['uid']][0] += 1
            userlist[hit["_source"]['uid']][1] += hit["_source"]['comment']
        else:
            userlist[hit["_source"]['uid']] = [1,hit["_source"]['comment']]
    rumormonger = []

    for user in userlist.keys():
        rumormonger.append({'uid':user,'announce':userlist[user][0],'comment':userlist[user][1]})

    result = sorted(rumormonger,key= lambda x:(x['announce'], x['comment']),reverse=True)
    return result

def find_topic_num(en_name):   #用于搜索事件对应文本数，展示气泡图
    query_body = {"size":5000,"query":{"match_all": {}}}

    res = weibo_es.search(index=en_name, body=query_body,request_timeout=100)
    hits = res['hits']['hits']

    return len(hits)

def rumorbubbleChart():
    query_body = {
  "query": {
    "filtered": {
      "filter": {
        "bool": {
          "must": [
            {
              "term": {
                "rumor_label": 1
              }
            },
            {
              "term": {
                "fin_label": 1
              }
            }
          ]
        }
      }
    }
  }
}

    res = weibo_es.search(index=ES_INDEX_CAL_LIST, body=query_body,request_timeout=100)
    hits = res['hits']['hits']
    print len(res)
    result = [[hit['_source']['comment'],hit['_source']['retweeted'],370601776,' '.join(hit['_source']['query_kwds'][:2]),hit['_source']['timestamp']] for hit in hits]# if hit['_source']['retweeted'] >= 30 and hit['_source']['comment'] >= 50 and hit['_source']['retweeted'] <= 1000 and hit['_source']['comment'] <= 1000]
    result = sorted(result,key= lambda x:(x[4]),reverse=True)[:20]   #提取前20个，按时间排序
    # print result
    resultnew = [i[:4] for i in result]
    return resultnew

def search_rumor_infor(en_name):
    query_body = {"size":10,"query":{"match_phrase": {"en_name":en_name}}}
    res = weibo_es.search(index=ES_INDEX_CAL_LIST, body=query_body)
    hits = res['hits']['hits']
    if len(hits):
        dic = {}
        dic['query_kwds'] = ','.join(hits[0]['_source']['query_kwds'])
        dic['publish_time'] = ts2date(hits[0]['_source']['timestamp'])
        dic['author'] = get_user(hits[0]['_source']['uid'])
        dic['comment'] = hits[0]['_source']['comment']
        dic['retweeted'] = hits[0]['_source']['retweeted']
        dic['text'] = hits[0]['_source']['text']
        return dic
    else:
        return {}

def rumorpropagate(en_name):
    en_name = en_name[:-len(en_name.split('-')[-1]) - 1]
    cur = defaultDatabase()
    conn = defaultDatabaseConn()
    sql = "SELECT * FROM %s WHERE %s = '%s' ORDER BY %s desc" % ('first_user','topic',en_name,'timestamp')
    cur.execute(sql)
    #results = db.session.query(first_user).filter(first_user.topic==topic).all()
    results = cur.fetchall()[:10]
    result = []

    for i in results:
        dic= {}
        dic['publish_time'] = ts2date(int(i['timestamp']))
        jsonload = json.loads(i['weibo_info'])[0]['_source']
        dic['text'] = jsonload['text']
        dic['uid'] = i['uid']
        dic['keyword'] = ','.join(jsonload['keywords_string'].split("&")[:5])
        dic['user_fansnum'] = jsonload['user_fansnum']
        dic['geo'] = jsonload['geo'].replace('&',' ')
        #dic['comment'] = jsonload[0]['_source']['comment']
        #dic['retweeted'] = jsonload[0]['_source']['retweeted']
        result.append(dic)

    return result

def get_rumor_pusher_maker(en_name):
    query_body={"size":10000,"query":{"match_all":{}}}
    print en_name
    weibos = rumor_es.search(index=en_name,doc_type='text',body=query_body)['hits']['hits']
    uid_dict={}
    # print weibos
    for weibo in weibos:
        weibo = weibo['_source']
        uid = weibo['uid']
        retweeted = weibo['retweeted'] + weibo['comment']
        fans = weibo['user_fansnum']
        if weibo['message_type']==1:
            message =1
        else:
            message =0

        if uid_dict.has_key(uid):
            retweeted = retweeted + uid_dict[uid][0]
            message = message + uid_dict[uid][1]
            uid_dict[uid] = [retweeted,message,fans]
        else:
            uid_dict[uid] = [retweeted,message,fans]

    retweeted_uid_dict = sorted(uid_dict.iteritems(), key=lambda d:d[0], reverse = True)
    message_uid_dict = sorted(uid_dict.iteritems(), key=lambda d:d[1], reverse = True)
    
    retweeted_list=[]
    message_list=[]
    for i in range(0,10):
        # print retweeted_uid_dict[i]
        retweeted_list.append([retweeted_uid_dict[i][0],i+1,retweeted_uid_dict[i][1][2]])
        message_list.append([message_uid_dict[i][0],i+1,message_uid_dict[i][1][2]])

    result={}
    result['maker'] = message_list
    result['pusher'] = retweeted_list
    return result

def get_rumor_source(en_name):
    query_body={'query':{'match_all':{}},'sort':{'timestamp':{'order':'asc'}},'size':10 }
    weibos = rumor_es.search(index=en_name,doc_type='text',body=query_body)['hits']['hits']
    result=[]
    # print weibos
    for weibo in weibos:
        weibo = weibo['_source']
        uid = weibo['uid']
        keyword= weibo['keywords_string']
        fans = weibo['user_fansnum']
        text = weibo['text']
        time = weibo['timestamp']
        geo = weibo['geo']
        tmp_dict={'publish_time':time,'uid':uid,'user_fansnum':fans,'text':text,'keyword':keyword,'geo':geo}
        result.append(tmp_dict)
    return result




if __name__ == '__main__':
    #search_rumor()
    rumorpropagate('te-lang-pu-ji-xin-ge-1492166854')