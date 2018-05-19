#!/usr/bin/env python
# encoding: utf-8
import sys
reload(sys)
sys.path.append("../../")
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

def sixmonth(year,month,day,days):
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

def to_howmany_tradeday(a,theday,n):   #向后推进n天
    tradedaydf = a[a['calendarDate'] == theday]
    dayindex = tradedaydf.index[0]
    return a.loc[dayindex + n]['calendarDate']

def howmany_day_between(day1,day2):
    day1index = a[a['calendarDate'] == day1].index[0]
    day2index = a[a['calendarDate'] == day2].index[0]
    return abs(day1index - day2index)

def last_tradeday(a,theday):   
    tradedaydf = a[a['calendarDate'] == theday]
    dayindex = tradedaydf.index[0]
    for i in range(dayindex - 1,dayindex - 30,-1):
        if a.loc[i]['isOpen'] == 1:
            date = a.loc[i]['calendarDate']
            return date
            break

def after_two_season(theday):
    year=int(theday.split('-')[0])
    month=int(theday.split('-')[1])
    day=int(theday.split('-')[2])
    if month == 1:
        return get_datelist(year,7,1,year,9,30)
    elif month == 4:
        return get_datelist(year,10,1,year,12,31)
    elif month == 7:
        return get_datelist(year+1,1,1,year+1,3,31)
    else:
        return get_datelist(year+1,4,1,year+1,6,30)

def increaseratio(lastday,nowday,stock):
    conn = default_db()
    cur = conn.cursor()
    pricesql = "SELECT * FROM %s WHERE %s >= '%s' and %s <= '%s' and %s = '%s'" % (TABLE_MARKET_DAILY,MARKET_DATE,lastday,MARKET_DATE,nowday,MARKET_STOCK_ID,stock)   #获取最新收益率
    cur.execute(pricesql)
    results = cur.fetchall()
    if results[0][MARKET_PRICE]:
        increase_ratio = (results[-1][MARKET_PRICE] - results[0][MARKET_PRICE]) / results[0][MARKET_PRICE]
    else:
        increase_ratio = 0
    return increase_ratio

def gaosongzhuan():
    conn = default_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM %s where %s < 0 order by %s asc" % (TABLE_NETPROFIT,NETPROFIT_NETPROFIT,NETPROFIT_DATE))
    results = cur.fetchall()
    index_name=DIC_ANNOUNCEMENT['index']
    type_name= DIC_ANNOUNCEMENT['type']

    for result in results:
        datelists = after_two_season(result['date'])
        es = Elasticsearch([{'host': '219.224.134.214', 'port': '9202'}])
        query_body = {"query": {"bool": {"must": [{"term": {"basic_info.type": "5"}},{"term": {"basic_info.stock_id": result['stock_id']}}]}}}
        res = es.search(index=index_name, doc_type=type_name, body=query_body,request_timeout=100)
        hits = res['hits']['hits']
        gaosognzhuan=[]
        if len(hits):
            for hit in hits:
                b= ts2datetime(hit["_source"]['publish_time'])
                if b in datelists:
                    print result[NETPROFIT_STOCK_NAME],b,result[NETPROFIT_STOCK_ID],result[NETPROFIT_DATE]
                    sql="SELECT * FROM %s where %s = '%s'"%(TABLE_STOCK_LIST,STOCK_LIST_STOCK_ID,result[NETPROFIT_STOCK_ID])
                    cur.execute(sql)
                    c=cur.fetchall()
                    if len(c):
                        last= last_tradeday(a,to_tradeday(a,b,-1))
                        recent=to_tradeday(a,to_howmany_tradeday(a,b,5),1)
                        date=result[NETPROFIT_DATE]
                        stock_name=result[NETPROFIT_STOCK_NAME]
                        stock_id=result[NETPROFIT_STOCK_ID]

                        checksql="SELECT * FROM %s where %s = '%s' and %s = '%d'" % (TABLE_DAY,DAY_STOCK_ID,stock_id,DAY_MANIPULATE_TYPE,2)
                        cur.execute(checksql)
                        checkresults = cur.fetchall()
                        checknum = 0
                        if len(checkresults):
                            for checkresult in checkresults:
                                if howmany_day_between(checkresult[DAY_START_DATE],last) <= 5:
                                    checknum = 1
                                    break
                        if checknum:
                            break

                        start_date=last
                        end_date=recent
                        increase_ratio=increaseratio(last,recent,stock_id)
                        industry_name=c[0][STOCK_LIST_INDUSTRY_NAME]
                        manipulate_type=2
                        ifend=1
                        marketplate=c[0][STOCK_LIST_PLATE]
                        industry_code=c[0][STOCK_LIST_INDUSTRY_CODE]
                        print date,stock_name,stock_id,b,end_date,industry_name,increase_ratio,manipulate_type,ifend,marketplate,industry_code
                        order = 'insert into ' + TABLE_DAY + '(stock_name,stock_id,start_date,end_date,increase_ratio,industry_name,manipulate_type,industry_code,ifend,market_plate)values\
                        ("%s","%s","%s","%s","%f","%s","%d","%s","%d","%s")' % (stock_name,stock_id,to_tradeday(a,b,-1),recent,increase_ratio,industry_name,manipulate_type,industry_code,ifend,marketplate)
                        try:
                            cur.execute(order)#TABLE_DAY
                            conn.commit()
                        except Exception, e:
                            print e
                        break

if __name__=="__main__":
    gaosongzhuan()
    