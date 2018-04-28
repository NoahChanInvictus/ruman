#-*-coding: utf-8-*-
#从ES数据库里每只股票每天的大宗交易的频率
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('../')

import tushare as ts
import pandas as pd
import datetime
from config import ES_HOST,ES_PORT,TABLE_TRANS_STAT,TABLE_STOCK_LIST
from sql_utils import *
import time
import sys
import codecs
import csv
import time_utils
import datetime
from time_utils import *

import pymysql
import os


from elasticsearch import Elasticsearch
from elasticsearch.exceptions import TransportError
from elasticsearch.helpers import bulk

######生成时间列表
def datelist(year1,month1,day1,year2,month2,day2):
    date_list = []
    begin_date = datetime.datetime.strptime(tostr(year1,month1,day1), "%Y-%m-%d")
    end_date = datetime.datetime.strptime(tostr(year2,month2,day2), "%Y-%m-%d")
    while begin_date <= end_date:
        date_str = begin_date.strftime("%Y-%m-%d")
        date_list.append(date_str)
        begin_date += datetime.timedelta(days=1)   #输出时间列表的函数
    return date_list

def es_trans(query,index_name,type_name,size,timenow,code,name):
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
    conn = default_db()
    cur = conn.cursor()
    es = Elasticsearch([{'host': ES_HOST, 'port': ES_PORT}])
    query_body = {"size":size,"query":{"bool": { "must":[{"term":{ "type1.stock_id":code}}]}}}
    res = es.search(index='east_money', doc_type="type1",body=query_body, request_timeout=100)
    frequency=0
    hits = res['hits']['hits']
    results = []
    for item in hits:
        res = item['_source']
        if  res['date']==timenow:
            frequency=frequency+1 

        
    stock_name=name
    timenow=timenow
    stock_id=code
    order = 'insert into ' + TABLE_TRANS_STAT + '(stock_id,stock_name,date,frequency)values("%s","%s","%s","%d")' % (code, stock_name, timenow, frequency)
    try:
        cur.execute(order)
        conn.commit()
    except Exception, e:
        print e

   
def transfrequency(theday):
    nowdate=theday
    conn = default_db()
    cur = conn.cursor()
    #nowdate = time.strftime("%Y-%m-%d",time.localtime(int(time.time())))
    query=1
    index_name='east_money'
    type_name= "type1"
    size=300
    score=1
    cur.execute("SELECT * FROM "+TABLE_STOCK_LIST) 
    results = cur.fetchall()
    for stock in results:
        stockcode=stock['stock_id']
        stockname=stock['stock_name']
        es_trans(query,index_name,type_name,size,nowdate,stockcode,stockname)

        