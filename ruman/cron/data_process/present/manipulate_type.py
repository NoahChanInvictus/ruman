#-*-coding: utf-8-*-
#统计每天操纵的类型
#-*-coding: utf-8-*-
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
# -*- coding:utf-8 -*-
import pymysql
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import TransportError
from elasticsearch.helpers import bulk
def findSortedPosition(theList, target):  
    low = 0  
    high = len(theList) - 1  
    while low <= high:  
        mid = (high + low) // 2  
        if theList[mid] == target:  
            return mid  
        elif target < theList[mid]:  
            high = mid -1  
        else:  
            low = mid + 1  
    return low 

reload(sys)
sys.setdefaultencoding('utf-8')

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

def dateindex(datenow,num):
    l=datelist(2015,1,1,2019,12,31)
    location1=l.index[datenow]+1
    location2=location1-num
    return list_date[location2]


def test(date,dateend,frequency):
    conn = default_db()
    cur = conn.cursor()
    date = date
    dateend=dateend
    cur.execute("SELECT * FROM manipulate_day")
    results = cur.fetchall()
    frequency=frequency
    weishizhi=0
    gaosong=0
    dingxiang=0
    sanbumouli=0
    for result in results:
        if result['end_date']>=dateend:
            if result['manipulate_type'] == 1:
                weishizhi = weishizhi+1
            elif result['manipulate_type'] == 2:
                gaosong = chaugyeban +1
            elif result['manipulate_type'] == 3:
                dingxiang =dingxiang +1
            elif result['manipulate_type'] == 4:
                sanbumouli=sanbumouli+1
        else:
            pass
    order = 'insert into ' + 'manipulate_type' + '( date,frequency,weishizhi,gaosong,dingxiang,sanbumouli)values\
    ("%s","%s","%d","%d","%d","%d")' % (date,frequency,weishizhi, gaosong, dingxiang,sanbumouli)
    try:
        cur.execute(order)
        conn.commit()
    except Exception, e:
        print e

def manipulatetype(theday)
    #timenow=time.strftime("%Y-%m-%d",time.localtime(int(time.time())))
    dates = datelist(2014, 1, 1, 2025, 12, 30)
    timenow=theday
    num=7
    frequency="week"
    day1=dates[findSortedPosition(dates,timenow)-num]
    test(timenow,day1,frequency)

    num=30
    frequency="month"
    day2=dates[findSortedPosition(dates,timenow)-num]
    test(timenow,day2,frequency)

    num=90
    frequency="season"
    day3=dates[findSortedPosition(dates,timenow)-num]
    test(timenow,day3,frequency)