# -*- coding: utf-8 -*-
#获得预测操纵股票的操纵时间段
import pandas as pd
from config import *
from time_utils import *
from sql_utils import *

def insertday(theday,tradelist):
    conn = default_db()
    cur = conn.cursor()
    endsql = "SELECT * FROM manipulate_day WHERE end_date = '%s'" % (tradelist[tradelist.index(theday) - 6])   #获取五个交易日内没有重新操作的股票
    cur.execute(endsql)
    results = cur.fetchall()
    if len(results):   #令其ifend为1，即已结束本次操纵
        for result in results:
            endupdate = "UPDATE manipulate_day SET ifend = '%d' WHERE id = '%d'" % (1, result['id'])
            cur.execute(endupdate)
            conn.commit()
    modelsql = "SELECT * FROM manipulate_result WHERE result = '%d'" % (1)   #获取结果中为1的股票，即模型预测的股票
    df = pd.read_sql(modelsql,conn)
    a = df[df['date'] == theday]
    print len(a.index)
    notendsql = "SELECT * FROM manipulate_day WHERE end_date >= '%s'" % (tradelist[tradelist.index(theday) - 5])   #获取五个交易日内曾操纵过得股票，来进行更新
    cur.execute(notendsql)
    results = cur.fetchall()
    iddict = {}
    for result in results:   #获取id及开始日期、板块
        iddict[result['stock_id']] = [result['id'],result['start_date']]
    for num in range(len(a.index)):
    	print num
        stock_id = a.iloc[num]['stock_id']
        platedict = {}
        mktsql = "SELECT * FROM stock_list"
        cur.execute(mktsql)
        results = cur.fetchall()
        for result in results:
            platedict[result['stock_id']] = result['plate']
        if stock_id in iddict.keys():   #如果当日的表中的数据在延续列表中则进行更新
            pricesql = "SELECT * FROM market_daily_new WHERE date >= '%s' and date <= '%s' and stock_id = '%s'" % (tradelist[tradelist.index(iddict[stock_id][1]) - 1],theday,stock_id)   #获取最新收益率
            cur.execute(pricesql)
            results = cur.fetchall()
            if results[0]['price']:
                increase_ratio = (results[-1]['price'] - results[0]['price']) / results[0]['price']
            else:
                increase_ratio = 0
            update = "UPDATE manipulate_day SET end_date = '%s',increase_ratio = '%f' WHERE id = '%d'" % (theday, increase_ratio, iddict[stock_id][0])   #更新结束时间为当天并更新收益率
            cur.execute(update)
            conn.commit()
        else:   #如果不在延续列表则添加新数据
            stock_name = a.iloc[num]['stock_name']
            start_date = theday
            end_date = theday
            pricesql = "SELECT * FROM market_daily_new WHERE date >= '%s' and date <= '%s' and stock_id = '%s'" % (tradelist[tradelist.index(start_date) - 1],end_date,stock_id)
            cur.execute(pricesql)
            results = cur.fetchall()
            if results[0]['price']:
                increase_ratio = (results[-1]['price'] - results[0]['price']) / results[0]['price']
            else:
                increase_ratio = 0
            industry_name = a.iloc[num]['industry_name']
            industry_code = a.iloc[num]['industry_code']
            manipulate_type = a.iloc[num]['manipulate_type']
            ifend = 0
            market_plate = platedict[stock_id]
            order = 'insert into manipulate_day ( stock_id,stock_name,start_date,end_date,increase_ratio,industry_name,industry_code,manipulate_type,ifend,market_plate)values("%s", "%s","%s","%s","%f","%s","%s","%d","%d", "%s")' % (stock_id,stock_name,start_date,end_date,increase_ratio,industry_name,industry_code,manipulate_type,ifend,market_plate)
            try:
                cur.execute(order)
                conn.commit()
            except Exception, e:
                print e

def update1():
    conn = default_db()
    cur = conn.cursor()
    platedict = {}
    mktsql = "SELECT * FROM stock_list"
    cur.execute(mktsql)
    results = cur.fetchall()
    for result in results:
        platedict[result['stock_id']] = result['plate']
    sql = "SELECT * FROM manipulate_day"
    cur.execute(sql)
    results = cur.fetchall()
    if len(results):   #令其ifend为1，即已结束本次操纵
        for result in results:
            print result['id']
            market_plate = platedict[result['stock_id']]
            update = "UPDATE manipulate_day SET market_plate = '%s' WHERE id = '%d'" % (market_plate, result['id'])
            cur.execute(update)
            conn.commit()

if __name__=="__main__":
    '''
    tradelist = get_tradelist(2013,1,1,2017,12,31)
    for day in get_tradelist(2016,2,1,2016,12,31):
        print day
        insertday(day,tradelist)'''
    update1()