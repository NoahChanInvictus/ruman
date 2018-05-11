#!/usr/bin/env python
# encoding: utf-8
import tushare as ts
import pandas as pd
import tushare as ts
import pandas as pd
import datetime
from config import *
from sql_utils import *
import time
import sys
import codecs
import csv 
from config import *
import time_utils
import datetime
from time_utils import *
import pymysql
import os
import sys

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import TransportError
from elasticsearch.helpers import bulk




while 1:
    try:
        a = ts.trade_cal()
        break
    except:
        pass

def tostr(year,month,day):
    date = str(year)+'-'+str(month)+'-'+str(day)
    return date
def threemonth(year,month,day,days):
    date_list = []
    begin_date = datetime.datetime.strptime(tostr(year,month,day), "%Y-%m-%d")
    for i in range(90): 
        date_str = begin_date.strftime("%Y-%m-%d")
        date_list.append(date_str)
        begin_date -= datetime.timedelta(days=days)   #输出时间列表的函数
    return date_list

def to_tradeday(a,theday,bora):   #输入bora=1向后最近的交易日，输入bora=-1向前最近的交易日
    tradedaydf = a[a['calendarDate'] == theday]
    if tradedaydf.iloc[0]['isOpen']:
        return theday
    else:
        dayindex = tradedaydf.index[0]
        if bora == 1:
            for i in range(dayindex + 1,dayindex + 30,1):
                if a.loc[i]['isOpen'] == 1:
                    date = a.loc[i]['calendarDate']
                    break
            return date
        elif bora == -1:
            for i in range(dayindex - 1,dayindex - 30,-1):
                if a.loc[i]['isOpen'] == 1:
                    date = a.loc[i]['calendarDate']
                    break
            return date
        else:
            print 'wrong bora,input 1 or -1'

def last_tradeday(a,theday):   
    tradedaydf = a[a['calendarDate'] == theday]
    dayindex = tradedaydf.index[0]
    for i in range(dayindex - 1,dayindex - 30,-1):
        if a.loc[i]['isOpen'] == 1:
            date = a.loc[i]['calendarDate']
            return date
            break

def increaseratio(lastday,nowday,stock):
    conn = default_db()
    cur = conn.cursor()
    pricesql = "SELECT * FROM market_daily WHERE date >= '%s' and date <= '%s' and stock_id = '%s'" % (lastday,nowday,stock)   #获取最新收益率
    cur.execute(pricesql)
    results = cur.fetchall()
    if results[0]['price']:
        increase_ratio = (results[-1]['price'] - results[0]['price']) / results[0]['price']
    else:
        increase_ratio = 0
    return increase_ratio

def gaosongzhuan():
    conn = default_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM netprofit where netprofit<0")
    results = cur.fetchall()
    index_name='announcement'
    type_name= "basic_info"

    for result in results:
        year=result["date"].split('-')[0]
        month=result["date"].split('-')[1]
        day=result["date"].split('-')[2]
        datelists=threemonth(year,month,day,90)
        es = Elasticsearch([{'host': '219.224.134.214', 'port': '9202'}])
        query_body = {"query": {"bool": {"must": [{"term": {"basic_info.type": "5"}},{"term": {"basic_info.stock_id": result['stock_id']}}]}}}
        res = es.search(index=index_name, doc_type=type_name, body=query_body,request_timeout=100)
        hits = res['hits']['hits']
        gaosognzhuan=[]
        if len(hits):
            for hit in hits:
                b= ts2datetime(hit["_source"]['publish_time'])
                if b in datelists:
                    print result["stock_name"],b
                    sql="SELECT * FROM stock_list where stock_name = '%s'"%(result['stock_name'])
                    cur.execute(sql)
                    c=cur.fetchall()
                    if len(c):
                        last= last_tradeday(a,b)
                        recent=to_tradeday(a,b,1)
                        date=result["date"]
                        stock_name=result["stock_name"]
                        stock_id=result["stock_id"]
                        start_date=last
                        end_date=recent
                        increase_ratio=increaseratio(last,recent,stock_id)
                        industry_name=c[0]['industry_name']
                        manipulate_type=2
                        ifend=2
                        marketplate=c[0]['plate']
                        industry_code=c[0]["industry_code"]
                        print date,stock_name,stock_id,start_date,end_date,industry_name,increase_ratio,manipulate_type,ifend,marketplate,industry_code
                        order = 'insert into ' + 'manipulate_day' + '(stock_name,stock_id,start_date,end_date,increase_ratio,industry_name,manipulate_type,industry_code,ifend,market_plate)values\
                        ("%s","%s","%s","%s","%f","%s","%d","%s","%d","%s")' % (stock_name,stock_id,last,recent,increase_ratio,industry_name,manipulate_type,industry_code,ifend,marketplate)
                        try:
                            cur.execute(order)
                            conn.commit()
                        except Exception, e:
                            print e
                        break

if __name__=="__main__":
    gaosongzhuan()
    