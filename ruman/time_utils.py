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

def date2ts(date):
    return int(time.mktime(time.strptime(date, '%Y-%m-%d %H:%M:%S')))

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

def full_datetime2ts(date):
    return int(time.mktime(time.strptime(date,'%Y-%m-%d %H:%M:%S')))


def ts2datetime_full(ts):
    return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(ts))

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
    while 1:
        try:
            a = ts.trade_cal()
            break
        except:
            pass
    l = get_datelist(year1,month1,day1,year2,month2,day2)
    index = a[a.calendarDate == l[0]].index.tolist()[0]
    li = []
    for i in range(index,index+len(l)):
        if a.loc[i]['isOpen']:
            li.append(a.loc[i]['calendarDate'])
    return li

def get_tradelist_all():
    while 1:
        try:
            a = ts.trade_cal()
            break
        except:
            pass
    df = a[a['isOpen'] == 1]
    return list(df['calendarDate'])

def int2datestr(year,month,day):
    return datetime.datetime.strptime(tostr(year,month,day), "%Y-%m-%d").strftime("%Y-%m-%d")

def lasttradedate(theday):   #theday为'2016-05-05'格式
    trade_before = ts2datetimestr(datetimestr2ts(theday) - 2592000).split('-')
    trade_after = ts2datetimestr(datetimestr2ts(theday) + 2592000).split('-')
    trade_list = get_tradelist(int(trade_before[0]),int(trade_before[1]),int(trade_before[2]),int(trade_after[0]),int(trade_after[1]),int(trade_after[2]))
    index = trade_list.index(theday)
    return trade_list[index - 1]

def to_tradeday(theday,bora):   #输入bora=1向后最近的交易日，输入bora=-1向前最近的交易日
    while 1:
        try:
            a = ts.trade_cal()
            break
        except:
            pass
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

def last2tradedate(theday):   #theday为'2016-05-05'格式
    trade_before = ts2datetimestr(datetimestr2ts(theday) - 2592000).split('-')
    trade_after = ts2datetimestr(datetimestr2ts(theday) + 2592000).split('-')
    trade_list = get_tradelist(int(trade_before[0]),int(trade_before[1]),int(trade_before[2]),int(trade_after[0]),int(trade_after[1]),int(trade_after[2]))
    index = trade_list.index(theday)
    return trade_list[index - 2]
