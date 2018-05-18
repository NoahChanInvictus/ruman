#-*-coding: utf-8-*-
#定向增发的规则
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

def reades(typenum):    #12为开始，13为结束
    es = Elasticsearch([{'host':ES_HOST,'port':ES_PORT}])
    df = pd.DataFrame(columns=['date','stock_id','title'])
    query_body = {"size":20000,"query":{"match":{"type":typenum}}}
    res = es.search(index=DIC_ANNOUNCEMENT['index'], doc_type=DIC_ANNOUNCEMENT['type'], body=query_body,request_timeout=100)
    hits = res['hits']['hits']
    num = 0
    while 1:
        try:
            a = ts.trade_cal()
            break
        except:
            pass
    if len(hits):
        for hit in hits:
            res = hit['_source']
            hitdf = a[a['calendarDate'] == ts2datetime(res['publish_time'])]
            if hitdf.iloc[0]['isOpen'] == 0:
                dayindex = hitdf.index[0]
                print ts2datetime(res['publish_time']),res['stock_id']
                for i in range(dayindex + 1,dayindex + 30):
                    if a.loc[i]['isOpen'] == 1:
                        date = a.loc[i]['calendarDate']
                        break
            else:
                date = ts2datetime(res['publish_time'])
            df.loc[num] = [date,res['stock_id'],res['title']]
            num += 1
    return df

def get_es_frame_bendi_dingzeng(year1,month1,day1,year2,month2,day2):
    conn = default_db()
    cur = conn.cursor()
    codelist = sorted(list(pd.read_sql("SELECT * FROM %s WHERE listed = 1" % (TABLE_STOCK_LIST),conn)['stock_id']))
    datelist = get_tradelist(year1,month1,day1,year2,month2,day2)
    data_frame_s = pd.DataFrame(data=0,columns=codelist,index=datelist)   #建立列数据框
    data_frame_s = data_frame_s.sort_index(axis=1)
    data_frame_e = pd.DataFrame(data=0,columns=codelist,index=datelist)   #建立列数据框
    data_frame_e = data_frame_e.sort_index(axis=1)
    startdf = reades(12)
    enddf = reades(13)
    '''
    for i in datelist:
        print i
        dfdates = startdf[startdf['date'] == i]
        dfdatee = enddf[enddf['date'] == i]
        ls = []
        le = []
        for code in codelist:
            dfcodes = dfdates[dfdates['stock_id'] == code]
            ls.append(len(dfcodes))
        for code in codelist:
            dfcodee = dfdatee[dfdatee['stock_id'] == code]
            le.append(len(dfcodee))
        data_frame_s.loc[i] = ls
        data_frame_e.loc[i] = le'''
    for i in datelist:
        print i
        dfdates = startdf[startdf['date'] == i]
        dfdatee = enddf[enddf['date'] == i]
        for code in set(dfdates['stock_id']):
            dfcodes = dfdates[dfdates['stock_id'] == code]
            data_frame_s.loc[i][code] = len(dfcodes)
        for code in set(dfdatee['stock_id']):
            dfcodee = dfdatee[dfdatee['stock_id'] == code]
            data_frame_e.loc[i][code] = len(dfcodee)

    data_frame_sta = pd.DataFrame(data=0,columns=data_frame_s.columns,index=data_frame_s.index)   #建立列数据框
    data_frame_dz = pd.DataFrame(columns=['stock_id','start_date','end_date'])
    num = 0

    for code in codelist:
        print code
        codedfs = data_frame_s[code]
        codedfe = data_frame_e[code]
        stadf = data_frame_sta[code]
        for date in data_frame_e.index:
            if codedfe.loc[date] > 0:
                stadf_date = stadf[stadf.index <= date]
                stadf_isanli = stadf_date[stadf_date == 1]   #选出之前在案例内的日期
                if len(stadf_isanli):   #如果之前存在案例
                    lastdate = stadf_isanli.index[-1]
                    codedfs_date = codedfs[(codedfs.index <= date) & (codedfs.index > lastdate)]   #选出来在上个案例和本案例之间的预案
                    codedfs_isstart = codedfs_date[codedfs_date > 0]   #选出其中存在的预案
                    if len(codedfs_isstart) == 1:   #如果预案只有1个
                        stadf_change = stadf[(stadf.index <= date) & (stadf.index >= codedfs_isstart.index[0])]   #直接令这期间的sta为1
                        startdate = codedfs_isstart.index[0]
                        stadf.loc[stadf_change.index] = 1
                        data_frame_dz.loc[num] = [code,startdate,date]
                        num += 1
                    elif len(codedfs_isstart) > 1:   #如果预案大于1个
                        for i in range(-1,-len(codedfs_isstart) - 1,-1):   #向前遍历
                            if i == -len(codedfs_isstart):   #如果已经遍历到最后一个（前面的都相等）
                                stadf_change = stadf[(stadf.index <= date) & (stadf.index >= codedfs_isstart.index[i])]   #直接将最后一个对应日期期间的sta标为1
                                startdate = codedfs_isstart.index[0]
                                stadf.loc[stadf_change.index] = 1
                                break
                            if startdf[startdf['date'] == codedfs_isstart.index[i]].iloc[0]['title'] != startdf[startdf['date'] == codedfs_isstart.index[i - 1]].iloc[0]['title']:   #如果两个日期的预案不一样
                                stadf_change = stadf[(stadf.index <= date) & (stadf.index >= codedfs_isstart.index[i])]   #将前面预案对应日期期间的sta标为1
                                startdate = codedfs_isstart.index[0]
                                stadf.loc[stadf_change.index] = 1
                                break
                        data_frame_dz.loc[num] = [code,startdate,date]
                        num += 1
                else:   #如果没有案例
                    codedfs_date = codedfs[codedfs.index <= date]   #选出之前所有日期
                    codedfs_isstart = codedfs_date[codedfs_date > 0]   #选出其中存在的预案
                    if len(codedfs_isstart) == 1:   #如果预案只有1个
                        stadf_change = stadf[(stadf.index <= date) & (stadf.index >= codedfs_isstart.index[0])]   #直接令这期间的sta为1
                        startdate = codedfs_isstart.index[0]
                        stadf.loc[stadf_change.index] = 1
                        data_frame_dz.loc[num] = [code,startdate,date]
                        num += 1
                    elif len(codedfs_isstart) > 1:   #如果预案大于1个
                        for i in range(-1,-len(codedfs_isstart) - 1,-1):   #向前遍历
                            if i == -len(codedfs_isstart):   #如果已经遍历到最后一个（前面的都相等）
                                stadf_change = stadf[(stadf.index <= date) & (stadf.index >= codedfs_isstart.index[i])]   #直接将最后一个对应日期期间的sta标为1
                                startdate = codedfs_isstart.index[0]
                                stadf.loc[stadf_change.index] = 1
                                break
                            if startdf[startdf['date'] == codedfs_isstart.index[i]].iloc[0]['title'] != startdf[startdf['date'] == codedfs_isstart.index[i - 1]].iloc[0]['title']:   #如果两个日期的预案不一样
                                stadf_change = stadf[(stadf.index <= date) & (stadf.index >= codedfs_isstart.index[i])]   #将前面预案对应日期期间的sta标为1
                                startdate = codedfs_isstart.index[0]
                                stadf.loc[stadf_change.index] = 1
                                break
                        data_frame_dz.loc[num] = [code,startdate,date]
                        num += 1
        data_frame_sta[code] = list(stadf)
    #data_frame_s.to_csv('data_frame_s.csv',encoding='utf_8_sig')
    #data_frame_e.to_csv('data_frame_e.csv',encoding='utf_8_sig')
    #data_frame_sta.to_csv('data_frame_sta.csv',encoding='utf_8_sig')
    #data_frame_dz.to_csv('data_frame_dz.csv',encoding='utf_8_sig')
    return data_frame_dz

def calculate(year1,month1,day1,year2,month2,day2):
    conn = default_db()
    cur = conn.cursor()
    df = get_es_frame_bendi_dingzeng(year1,month1,day1,year2,month2,day2)
    #df = pd.DataFrame(data=[['000001','2013-09-09','2013-12-16']],columns=['stock_id','start_date','end_date'])
    staticdf = pd.DataFrame(columns=['stock_id','start_date','end_date','dzprice_min','lowdzprice_ratio','lowdzaver_ratio','end_start'])
    datelist = get_tradelist(year1 - 1,month1,day1,year2,month2,day2)
    number = 0
    print len(df)
    for num in range(len(df)):
        print num 
        start_date = df.loc[num]['start_date']
        end_date = df.loc[num]['end_date']
        stock_id = df.loc[num]['stock_id']
        start_date_20 = datelist[datelist.index(start_date) - 20]

        sql = "SELECT * FROM %s WHERE %s = '%s'" % (TABLE_MARKET_DAILY,MARKET_STOCK_ID,stock_id)
        pricedf = pd.read_sql(sql,conn)
        pricedf1 = pricedf[(pricedf[MARKET_DATE] >= start_date_20) & (pricedf[MARKET_DATE] <= end_date)]
        pricedf2 = pricedf[(pricedf[MARKET_DATE] >= start_date) & (pricedf[MARKET_DATE] <= end_date)]
        pricelist1 = list(pricedf1[MARKET_PRICE_FU])
        pricelist2 = list(pricedf2[MARKET_PRICE_FU])

        startprice = np.mean(pricelist1[:20])
        min_price = min(pricelist2)
        average_price = np.mean(pricelist2)
        dzprice_min = (min_price - startprice) / startprice
        daynumone = 0

        for price in pricelist2:
            if price < startprice:
                daynumone += 1
        lowdzprice_ratio = daynumone / float(len(pricelist2))

        lowdaylist = []
        for index in pricedf2.index:
            if pricedf2.loc[index][MARKET_PRICE_FU] < average_price:
                lowdaylist.append(pricedf2.loc[index][MARKET_DATE])
        aver_startday = lowdaylist[0]
        aver_endday = lowdaylist[-1]
        daynumtwo = datelist.index(aver_endday) - datelist.index(aver_startday) + 1
        lowdzaver_ratio = daynumtwo / float(len(pricelist2))

        end_start = pricelist2[-1] / startprice
        staticdf.loc[num] = [stock_id,start_date,end_date,dzprice_min,lowdzprice_ratio,lowdzaver_ratio,end_start]
        number += 1
    staticdfone = staticdf[staticdf['dzprice_min'] < -0.2]
    staticdftwo = staticdfone[staticdfone['lowdzprice_ratio'] > 0.8]
    staticdfthree = staticdftwo[staticdftwo['lowdzaver_ratio'] < 0.6]
    staticdffour = staticdfthree[staticdfthree['end_start'] > 0.95]
    staticdffour.to_csv('staticdffour1.csv',encoding='utf_8_sig')
    return staticdffour

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
        manipulate_type = 3
        ifend = 1
        marketplate = result[STOCK_LIST_PLATE]
        industry_code = result[STOCK_LIST_INDUSTRY_CODE]
        print stock_name,stock_id,start_date,end_date,industry_name,increase_ratio,manipulate_type,ifend,marketplate,industry_code
        order = 'insert into ' + TABLE_DAY + '(stock_name,stock_id,start_date,end_date,increase_ratio,industry_name,manipulate_type,industry_code,ifend,market_plate)values\
        ("%s","%s","%s","%s","%f","%s","%d","%s","%d","%s")' % (stock_name,stock_id,start_date,end_date,increase_ratio,industry_name,manipulate_type,industry_code,ifend,marketplate)
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
    #df = pd.DataFrame(data=[['000882','2013-05-02','2013-10-17'],['002092','2012-11-05','2013-02-07'],['002546','2015-07-16','2015-12-31'],['601009','2015-07-29','2015-11-19']],columns=['stock_id','start_date','end_date'])
    #insert_sql(df)
    insert_sql(calculate(2016,1,1,2018,5,15))