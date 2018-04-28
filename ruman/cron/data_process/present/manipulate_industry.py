#-*-coding: utf-8-*-
#统计每天操纵的股票所属行业
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


def test(date,dateend,frequency):
    conn = default_db()
    cur = conn.cursor()
    datesnow = date
    cur.execute("SELECT * FROM manipulate_day")
    results = cur.fetchall()
    frequency=frequency
    A=0
    B=0
    C=0
    D=0
    E=0
    F=0
    G=0
    H=0
    I=0
    J=0
    K=0
    L=0
    M=0
    N=0
    O=0
    P=0
    Q=0
    R=0
    S=0
    for result in results:
        if result['end_date']>=dateend:
            if result['industry_code'] == "A":
                A =A+1
            elif result['industry_code'] == "B":
                B =B+1
            elif result['industry_code'] == "C":
                C =C+1
            elif result['industry_code'] == "D":
                D =D+1
            elif result['industry_code'] == "E":
                E =E+1
            elif result['industry_code'] == "F":
                F =F+1
            elif result['industry_code'] == "G":
                G =G+1
            elif result['industry_code'] == "H":
                H =H+1
            elif result['industry_code'] == "I":
                I =I+1
            elif result['industry_code'] == "J":
                J =J+1
            elif result['industry_code'] == "K":
                K =K+1
            elif result['industry_code'] == "L":
                L =L+1
            elif result['industry_code'] == "M":
                M =M+1
            elif result['industry_code'] == "N":
                N =N+1
            elif result['industry_code'] == "O":
                O =O+1
            elif result['industry_code'] == "P":
                P =P+1
            elif result['industry_code'] == "Q":
                Q =Q+1
            elif result['industry_code'] == "R":
                R =R+1
            elif result['industry_code'] == "S":
                S =S+1
        else:
            pass

    order = 'insert into ' + 'manipulate_industry' + '(date,frequency,industry_A,industry_B,industry_C,\
    industry_D,industry_E,industry_F,industry_G,industry_H,industry_I,industry_J,industry_K,industry_L\
    ,industry_M,industry_N,industry_O,industry_P,industry_Q,industry_R,industry_S\
    )values("%s","%s","%d","%d","%d","%d","%d","%d","%d","%d","%d","%d","%d","%d","%d","%d","%d","%d","%d","%d","%d"\
    )'%(datesnow,frequency,A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S)

    try:
        cur.execute(order)
        conn.commit()
    except Exception, e:
        print e

def manipulateindustry(theday)
    dates = datelist(2007, 1, 1, 2025, 12, 31)
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



