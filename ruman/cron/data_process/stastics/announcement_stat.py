#-*-coding: utf-8-*-
#更新每只股票每天的公告数目
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('../')
import tushare as ts
import pandas as pd
import datetime
from config import *
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



#######定义ES数据库的索引方式
def es_emotion(query,index_name,type_name,size,score,stock,time1):
    '''
    input：
        query:关键词;start_day,end_day:起止日期;
        index_name,type_name:ES配置参数;
        size,score:ES控制参数
    return:
        content中含有query的文本内容
    '''
    es = Elasticsearch([{'host': '219.224.134.214', 'port': '9202'}])
    query_body = {"size":size,"query":{"bool": { "must":[{"match":{ "publish_time":time1}},
                                                             {"match":{ "stock_id":stock}}]}}}

    res = es.search(index=index_name, doc_type=type_name, body=query_body,request_timeout=100)
    hits = res['hits']['hits']
    results = []
    if(len(hits)):
        for item in hits:
            text_id = item['_id']
            if(item['_score']>=score):
                res = item['_source']
                res['text_id'] = text_id
                results.append(res)
    return results


######公告类型判断
def getkind(line):
    if '资产置换' in line or '资产重组' in line or '购买资产' in line or '收购' in line:
        a = 1
        #print '类别：并购重组'
    elif '投资' in line:
        a = 2
        #print '类别：对外投资'
    elif '质押' in line:
        a = 3
        #print '类别：股权质押'
    elif '减持' in line:
        a = 4
        #print '类别：大股东减持'
    elif '利润分配' in line or '分配利润' in line or '分红派息' in line:
        a = 5
        #print '类别：利润分配'
    elif '关联交易' in line:
        a = 6
        #print '类别：关联交易'
    elif '发行股份' in line:
        a = 7
        #print '类别：定向增发'
    elif '配股' in line:
        a = 8
        #print '类别：配股'
    elif '停牌' in line:
        a = 9
        #print '类别：停牌'
    elif '辞职' in line:
        a = 10
        #print '类别：高管辞职'
    else:
        a = 11
        #print '类别：其他'
    return a


####主测试程序
def test(stock,time1,date,name):
    query=1
    index_name='announcement'
    type_name= "basic_info"
    size=50
    score=1
    time1 = datetime2ts(date)
    stock=stock
    a=es_emotion(query,index_name,type_name,size,score,stock,time1)
    #all = ts.get_stock_basics()
    announce=[]
    stock_id = stock
    stock_name = name
    date = date
    conn = default_db()
    cur = conn.cursor()

    #####对每天每个股票的公告进行统计
    for l in a:
        typename=getkind(l['title'])
        MA_announcement=0
        Investment_announcement=0
        Pledge_announcement=0
        Reducing_announcement=0
        Profit_annoncement=0
        Related_announcement=0
        Issueing_announcement=0
        Allotment_announcement=0
        Stop_announcement=0
        Resigning_announcement=0
        Others_announcement=0
        if typename==1:
            MA_announcement = MA_announcement+1
        elif typename==2:
            Investment_announcement =  Investment_announcement+1
        elif typename==3:
            Pledge_announcement =  Pledge_announcement + 1
        elif typename == 4:
            Reducing_announcement = Reducing_announcement + 1
        elif typename == 5:
            Profit_annoncement = Profit_annoncement + 1
        elif typename == 6:
            Related_announcement = Related_announcement + 1
        elif typename == 7:
            Issueing_announcement = Issueing_announcement + 1
        elif typename == 8:
            Allotment_announcement = Allotment_announcement + 1
        elif typename == 9:
            Stop_announcement = Stop_announcement + 1
        elif typename == 10:
            Resigning_announcement = Resigning_announcement + 1
        elif typename == 11:
            Others_announcement = Others_announcement + 1
        allannounce=[stock,stock_name,date,time1,MA_announcement,Investment_announcement, Pledge_announcement,Reducing_announcement,Profit_annoncement,Related_announcement,Issueing_announcement,Allotment_announcement,Stop_announcement,Resigning_announcement,Others_announcement]
        announce.append(allannounce)


    #####对同一股票进行合并
    MA_announcement = 0
    Investment_announcement = 0
    Pledge_announcement = 0
    Reducing_announcement = 0
    Profit_annoncement = 0
    Related_announcement = 0
    Issueing_announcement = 0
    Allotment_announcement = 0
    Stop_announcement = 0
    Resigning_announcement = 0
    Others_announcement = 0
    for j in range(len(announce)):
        MA_announcement += announce[j][4]
        Investment_announcement += announce[j][5]
        Pledge_announcement += announce[j][6]
        Reducing_announcement += announce[j][7]
        Profit_annoncement += announce[j][7]
        Related_announcement += announce[j][9]
        Issueing_announcement += announce[j][10]
        Allotment_announcement += announce[j][11]
        Stop_announcement += announce[j][12]
        Resigning_announcement += announce[j][13]
        Others_announcement += announce[j][14]
    order = 'insert into ' + 'announcement' + '( stock_id,stock_name,date,time,MA_announcement,Investment_announcement, Pledge_announcement,Reducing_announcement,Profit_annoncement,' \
                                          'Related_announcement,Issueing_announcement,Allotment_announcement,Stop_announcement,Resigning_announcement,Others_announcement)values("%s","%s","%s","%d","%d","%d","%d","%d","%d",' \
                                          '"%d","%d","%d","%d","%d","%d")' % (
                                          stock_id, stock_name, date, time1, MA_announcement, Investment_announcement,
                                          Pledge_announcement, Reducing_announcement, Profit_annoncement,
                                          Related_announcement, Issueing_announcement, Allotment_announcement,
                                          Stop_announcement, Resigning_announcement, Others_announcement)

    try:
        cur.execute(order)
        conn.commit()
    except Exception, e:
        print e
    # print a

def announcment_stastic_main(theday):
    # date=mydate = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    # print date
    #date=datelist(2015,1,1,2018,2,4)
    conn = default_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM stock_list") 
    results = cur.fetchall()
    date = theday
    for stock in results:
        stockcode=stock['stock_id']
        stockname=stock['stock_name']
        time1=datetime2ts(date)
        test(stockcode,time1,date,stockname)
        # print 'good'

if __name__=="__main__":
    announcment_stastic_main('2018-03-06') 