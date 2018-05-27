#-*-coding: utf-8-*-
#尾盘操纵数据导入
import sys
reload(sys)
sys.path.append("../../")
import pandas as pd
from config import *
from time_utils import *
from sql_utils import *
import numpy as np
from elasticsearch import Elasticsearch

while 1:
    try:
        a = ts.trade_cal()
        break
    except:
        pass

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

def increaseratio(lastday,nowday,stock_id):
    conn = default_db()
    cur = conn.cursor()
    pricesql = "SELECT * FROM %s WHERE %s >= '%s' and %s <= '%s' and %s = '%s'" % (TABLE_MARKET_DAILY,MARKET_DATE,lastday,MARKET_DATE,nowday,MARKET_STOCK_ID,stock_id)   #获取最新收益率
    cur.execute(pricesql)
    results = cur.fetchall()
    if results[0][MARKET_PRICE]:
        increase_ratio = (results[-1][MARKET_PRICE] - results[0][MARKET_PRICE]) / results[0][MARKET_PRICE]
    else:
        increase_ratio = 0
    return increase_ratio

def insert_sql(df):
    conn = default_db()
    cur = conn.cursor()
    for num in range(len(df)):
        sql = "SELECT * FROM %s where %s = '%s'"%(TABLE_STOCK_LIST,STOCK_LIST_STOCK_ID,df.iloc[num]['stock_id'])
        cur.execute(sql)
        result = cur.fetchone()
        start_date = to_tradeday(a,df.iloc[num]['start_date'],-1)
        lastdate = last_tradeday(a,start_date)
        end_date = to_tradeday(a,df.iloc[num]['end_date'],1)
        stock_name = result[STOCK_LIST_STOCK_NAME]
        stock_id = result[STOCK_LIST_STOCK_ID]

        increase_ratio = increaseratio(lastdate,end_date,stock_id)
        industry_name = result[STOCK_LIST_INDUSTRY_NAME]
        manipulate_type = 5
        ifend = 1
        marketplate = result[STOCK_LIST_PLATE]
        industry_code = result[STOCK_LIST_INDUSTRY_CODE]
        print stock_name,stock_id,start_date,end_date,industry_name,increase_ratio,manipulate_type,ifend,marketplate,industry_code
        order = 'insert into ' + TABLE_DAY + '(stock_name,stock_id,manipulate_label,start_date,end_date,increase_ratio,industry_name,manipulate_type,industry_code,ifend,market_plate)values\
        ("%s","%s","%d","%s","%s","%f","%s","%d","%s","%d","%s")' % (stock_name,stock_id,1,start_date,end_date,increase_ratio,industry_name,manipulate_type,industry_code,ifend,marketplate)
        try:
            cur.execute(order)
            conn.commit()
        except Exception, e:
            print e
            break

def predict_dz(year1,month1,day1,year2,month2,day2):
    insert_sql(calculate(year1,month1,day1,year2,month2,day2))

if __name__=="__main__":
    #get_es_frame_bendi_dingzeng(2012,1,1,2015,12,31)
    #calculate(2012,1,1,2015,12,31)
    '''
    df = pd.DataFrame(data=[['600359','2015-06-26','2015-06-26'],
        ['002749','2015-07-03','2015-07-03'],
        ['002749','2015-07-08','2015-07-08'],
        ['002496','2015-07-17','2015-07-17'],
        ['002498','2015-07-21','2015-07-21'],
        ['000004','2015-08-12','2015-08-12'],
        ['002509','2015-08-14','2015-08-14'],
        ['002103','2015-08-25','2015-08-26'],
        ['300432','2015-08-25','2015-08-25']],
        columns=['stock_id','start_date','end_date'])'''
    '''
    df = pd.DataFrame(data=[['600071','2016-03-14','2016-03-14'],
        ['600099','2016-12-23','2016-12-23'],
        ['002749','2016-04-06','2016-04-06'],
        ['002496','2016-12-21','2016-12-21'],
        ['002498','2016-10-27','2016-10-27']],
        columns=['stock_id','start_date','end_date'])'''
    df = df = pd.DataFrame(data=[['002103','2015-08-25','2015-08-25'],
        ['002103','2015-08-26','2015-08-26']],
        columns=['stock_id','start_date','end_date'])
    insert_sql(df)