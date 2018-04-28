# -*- coding: utf-8 -*-

import time
import datetime
import tushare as ts
import pandas as pd

def today():
    return time.strftime('%Y-%m-%d', time.localtime(time.time()))

def now():
    return time.strftime('%H:%M:%S', time.localtime(time.time()))

def datetime2datestr(date):
    return date.strftime('%Y-%m-%d')

def unix2hadoop_date(ts):
    return time.strftime('%Y_%m_%d', time.localtime(ts))

def ts2datetime(ts):
    return time.strftime('%Y-%m-%d', time.localtime(ts))

def ts2date(ts):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts))

def ts2date_min(ts):
    return time.strftime('%Y-%m-%d %H:%M', time.localtime(ts))

def datetime2ts(date):
    return int(time.mktime(time.strptime(date, '%Y-%m-%d')))

def window2time(window, size=24*60*60):
    return window*size

def datetimestr2ts(date):
    return time.mktime(time.strptime(date, '%Y-%m-%d'))

def ts2datetimestr(ts):
    return time.strftime('%Y-%m-%d', time.localtime(ts))

def ts2datetimestrnew(ts):
    return time.strftime('%Y%m%d', time.localtime(ts))

def ts2HourlyTime(ts, interval):
    # interval 取 Minite、Hour
    ts = ts - ts % interval
    return ts

def ts2datetime_full(ts):
    return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(ts))

def tostr(year,month,day):
    date = str(year)+'-'+str(month)+'-'+str(day)
    return date

def get_datelist(year1,month1,day1,year2,month2,day2):
    date_list = []
    begin_date = datetime.datetime.strptime(tostr(year1,month1,day1), "%Y-%m-%d")
    end_date = datetime.datetime.strptime(tostr(year2,month2,day2), "%Y-%m-%d")
    while begin_date <= end_date:
        date_str = begin_date.strftime("%Y-%m-%d")
        date_list.append(date_str)
        begin_date += datetime.timedelta(days=1)   #输出时间列表的函数
    return date_list

def get_tradelist(year1,month1,day1,year2,month2,day2):
    a = ts.trade_cal()
    l = get_datelist(year1,month1,day1,year2,month2,day2)
    index = a[a.calendarDate == l[0]].index.tolist()[0]
    li = []
    for i in range(index,index+len(l)):
        if a.loc[i]['isOpen']:
            li.append(a.loc[i]['calendarDate'])
    return li