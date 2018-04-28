#-*-coding: utf-8-*-
#统计每天操纵的股票增长率
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

def dateindex(datenow,num):
    l=datelist(2015,1,1,2019,12,31)
    location1=l.index[datenow]+1
    location2=location1-num
    return list_date[location2]


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
    t=0
    AA=0
    BB=0
    CC=0
    DD=0
    EE=0
    FF=0
    GG=0
    HH=0
    II=0
    JJ=0
    KK=0
    LL=0
    MM=0
    NN=0
    OO=0
    for result in results:
        if result['end_date']>=dateend:
            if result['increase_ratio']>=0 and result['increase_ratio']<0.05:
                A =A+1
            elif result['increase_ratio']>=0.05 and result['increase_ratio']<0.1:
                B =B+1
            elif result['increase_ratio']>=0.1 and result['increase_ratio']<0.15:
                C =C+1
            elif result['increase_ratio']>=0.15 and result['increase_ratio']<0.2:
                D =D+1
            elif result['increase_ratio']>=0.2 and result['increase_ratio']<0.25:
                E =E+1
            elif result['increase_ratio']>=0.25 and result['increase_ratio']<0.3:
                F =F+1
            elif result['increase_ratio']>=0.3 and result['increase_ratio']<0.35:
                G =G+1
            elif result['increase_ratio']>=0.35 and result['increase_ratio']<0.4:
                H =H+1
            elif result['increase_ratio']>=0.4 and result['increase_ratio']<0.45:
                I =I+1
            elif result['increase_ratio']>=0.45 and result['increase_ratio']<0.5:
                J =J+1
            elif result['increase_ratio']>=0.5 and result['increase_ratio']<0.55:
                K =K+1
            elif result['increase_ratio']>=0.55 and result['increase_ratio']<0.6:
                L =L+1
            elif result['increase_ratio']>=0.6 and result['increase_ratio']<0.65:
                M =M+1
            elif result['increase_ratio']>=0.65 and result['increase_ratio']<0.7:
                N =N+1
            elif result['increase_ratio']>=0.7 and result['increase_ratio']<0.75:
                O =O+1
            elif result['increase_ratio']>=0.75 and result['increase_ratio']<0.8:
                P =P+1
            elif result['increase_ratio']>=0.8 and result['increase_ratio']<0.85:
                Q =Q+1
            elif result['increase_ratio']>=0.85 and result['increase_ratio']<0.9:
                R =R+1
            elif result['increase_ratio']>=0.9 and result['increase_ratio']<0.95:
                S =S+1
            elif result['increase_ratio']>=0.95 and result['increase_ratio']<1:
                t =t+1
            elif result['increase_ratio']<0 and result['increase_ratio']>=-0.05:
                AA =AA+1
            elif result['increase_ratio']<-0.05 and result['increase_ratio']>=-0.1:
                BB =BB+1
            elif result['increase_ratio']<-0.1 and result['increase_ratio']>=-0.15:
                CC =CC+1
            elif result['increase_ratio']<-0.15 and result['increase_ratio']>=-0.2:
                DD =DD+1
            elif result['increase_ratio']<-0.2 and result['increase_ratio']>=-0.25:
                EE =EE+1
            elif result['increase_ratio']<-0.25 and result['increase_ratio']>=-0.3:
                FF =FF+1
            elif result['increase_ratio']<-0.3 and result['increase_ratio']>=-0.35:
                GG =GG+1
            elif result['increase_ratio']<-0.35 and result['increase_ratio']>=-0.4:
                HH =HH+1
            elif result['increase_ratio']<-0.4 and result['increase_ratio']>=-0.45:
                II =II+1
            elif result['increase_ratio']<-0.45 and result['increase_ratio']>=-0.5:
                JJ =JJ+1
            elif result['increase_ratio']<-0.5 and result['increase_ratio']>=-0.55:
                KK =KK+1
            elif result['increase_ratio']<-0.55 and result['increase_ratio']>=-0.6:
                LL =LL+1
            elif result['increase_ratio']<-0.6 and result['increase_ratio']>=-0.65:
                MM =MM+1
            elif result['increase_ratio']<-0.65 and result['increase_ratio']>=-0.7:
                NN =NN+1
            elif result['increase_ratio']<-0.7 and result['increase_ratio']>=-0.75:
                OO =OO+1

        else:
            pass

    order = 'insert into ' + 'manipulate_influence' + '(date,frequency,increasezero,increasefive\
    ,increaseten,increasefifteen,increasetwenty,increasetwentyfive,increasethirty,increasethirtyfive,increaseforty,increasefortyfive\
    ,increasefifty,increasefiftyfive,increasesixty,increasesixtyfive,increaseseventy\
    ,increaseseventyfive,increaseeighty,increaseeightyfive,increaseninty,increasenintyfive\
    ,increasefzero,increaseffive,increaseften,increaseffifteen,increaseftwenty,increaseftwentyfive\
    ,increasefthirty,increasefthirtyfive,increasefforty,increaseffortyfive,increaseffifty,increaseffiftyfive\
    ,increasefsixty,increasefsixtyfive,increasefseventy)values("%s","%s", "%d","%d", "%d", "%d", "%d", "%d", "%d", "%d", "%d", "%d", "%d", "%d", "%d", "%d", "%d", "%d", "%d", "%d", "%d"\
    , "%d", "%d", "%d", "%d", "%d", "%d", "%d", "%d", "%d", "%d", "%d", "%d", "%d", "%d", "%d", "%d"\
    )'%(datesnow,frequency,A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,t,AA,BB,CC,DD,EE,FF,GG,HH,II,JJ,KK,LL,MM,NN,OO)

    try:
        cur.execute(order)
        conn.commit()
    except Exception, e:
        print e
        
def manipulateratio(theday)
    dates = datelist(2014, 1, 1, 2025, 12, 30)
    timenow=theday

    num=7
    frequency="week"
    day1=dates[findSortedPosition(dates,timenow)-num]
    test(timenow,day1,frequency)

    num=3
    frequency="month"
    day2=dates[findSortedPosition(dates,timenow)-num]
    test(timenow,day2,frequency)

    num=90
    frequency="season"
    day3=dates[findSortedPosition(dates,timenow)-num]
    test(timenow,day3,frequency)





