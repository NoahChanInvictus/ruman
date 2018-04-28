# -*- coding:utf-8 -*-
import tushare as ts
import sys
reload(sys)
sys.path.append('../')
import codecs
import csv
import math
import json
from config import *
import time_utils
from sql_utils import *
import time
import datetime
from time_utils import *
from WindPy import *

def what_quarter(theday):
    year = int(theday.split('-')[0])
    month = int(theday.split('-')[1])
    if 1 <= month <= 3:
        return year - 1,4,year - 1,3
    elif 4 <= month <= 6:
        return year,1,year - 1,4
    elif 7 <= month <= 9:
        return year,2,year,1
    else:
        return year,3,year,2

def create(start_date,end_date):
    conn = default_db()
    cur = conn.cursor()
    w.start()
    allmarket = w.wset("SectorConstituent",u"date=" + ts2datetimestrnew(datetimestr2ts(today())) + ";sector=全部A股").Data  #[1]为代码，[2]为名字
    print len(allmarket[1])
    for num in range(len(allmarket[1])):   #对于所有股票获取其股价数据
        name = allmarket[2][num]
        code = allmarket[1][num]
        print code,name,num
        try:
            data1 = w.wsd(code, "close,turn", start_date, end_date, "Fill=Previous")
            data2 = w.wsd(code, "close", start_date, end_date, "Fill=Previous;PriceAdj=B")
            data3 = w.wsd(code, "industry_CSRC12", today(), today(), "industryType=5")
            for datenum in range(len(data1.Times)):
                stock_id = code.split('.')[0]
                stock_name = name
                industry_name = data.Data[0][0].split('-')[0]
                industry_code = industry_dict_big[industry_name]
                datestr = datetime2datestr(data1.Times[datenum])
                if type(data1.Data[0][datenum]) == float or type(data1.Data[0][datenum]) == int:
                    price = data1.Data[0][datenum]
                else:
                    price = 0
                if type(data2.Data[0][datenum]) == float or type(data2.Data[0][datenum]) == int:
                    price_fu = data2.Data[0][datenum]
                else:
                    price_fu = 0
                if type(data1.Data[1][datenum]) == float or type(data1.Data[1][datenum]) == int:
                    turnover_rate = data1.Data[1][datenum]
                else:
                    turnover_rate = 0
                order = 'insert into market_daily_new ( stock_id,stock_name,industry_code,date,price,price_fu,turnover_rate)values("%s", "%s","%s","%s","%f","%f","%f")' % (stock_id,stock_name,industry_code,datestr, price,price_fu,turnover_rate)
                try:
                    cur.execute(order)
                    conn.commit()
                except Exception, e:
                    print e
        except:
            pass

def get_profit(trade_list,year,q):
    conn = default_db()
    cur = conn.cursor()
    net_profits = ts.get_profit_data(year,q)   #当季度的净利润数据
    if q == 1:
        net_profits_before = ts.get_profit_data(year - 1,4)   #为了避免数据缺失而获取的前一季度
    else:
        net_profits_before = ts.get_profit_data(year,q - 1)
    print year,'年',q,'季度'
    sql = "SELECT * FROM market_daily_new WHERE date >= '%s' and date <= '%s'" % (trade_list[0][0],trade_list[0][-1])
    cur.execute(sql)
    results = cur.fetchall()
    print len(results) / len(trade_list[0]),len(results),len(trade_list[0])
    for i in range(len(results) / len(trade_list[0])):
        print i,year,'年',q,'季度'
        newresults = results[i*len(trade_list[0]):(i + 1)*len(trade_list[0])]
        index = net_profits[net_profits.code == newresults[0]['stock_id']].index.tolist()
        if len(index):   #如果当季度有就选取当季度数据
            netprofit = net_profits.net_profits[index[0]]
        else:   #如果当季度没有而前季度有则前季度数据
            index_before = net_profits_before[net_profits_before.code == newresults[0]['stock_id']].index.tolist()
            if len(index_before):
                netprofit = net_profits_before.net_profits[index_before[0]]
            else:   #如果数据缺失则沿用前值
                sql = "SELECT * FROM market_daily_new WHERE date = '%s' and stock_id = '%s'" % (trade_list[1][-1],newresults[0]['stock_id'])
                cur.execute(sql)
                results1 = cur.fetchall()
                netprofit = results1[0]['net_profits']
        for result in newresults:
            update = "UPDATE market_daily_new SET net_profits = '%f' WHERE id = '%d'" % (netprofit, result['id']) 
            try:  
                cur.execute(update)
                conn.commit()
            except Exception, e:
                print e

def get_profit_new(trade_list,year,q):
    conn = default_db()
    cur = conn.cursor()
    net_profits = ts.get_profit_data(year,q)   #当季度的净利润数据
    if q == 1:
        net_profits_before = ts.get_profit_data(year - 1,4)   #为了避免数据缺失而获取的前一季度
    else:
        net_profits_before = ts.get_profit_data(year,q - 1)
    print year,'年',q,'季度'
    for date in range(len(trade_list[0])):
        print trade_list[0][date]
        sql = "SELECT * FROM market_daily WHERE date = '%s'" % (trade_list[0][date])
        cur.execute(sql)
        results = cur.fetchall()
        for result in results:
            #print result['stock_id']
            index = net_profits[net_profits.code == result['stock_id']].index.tolist()
            if len(index):
                netprofit = net_profits.net_profits[index[0]]
            else:
                sqln = "SELECT * FROM market_daily WHERE date = '%s' and stock_id = '%s'" % (trade_list[1][-1], result['stock_id'])
                cur.execute(sqln)
                resultsn = cur.fetchall()
                if len(resultsn):
                    netprofit = resultsn[0]['net_profits']
                else:
                    netprofit = float('nan')
            update = "UPDATE market_daily SET net_profits = '%f' WHERE id = '%d'" % (netprofit, result['id']) 
            try:  
                cur.execute(update)
                conn.commit()
            except Exception, e:
                print e

def get_market_history():
    #create()
    for year in range(2015,2018):
        for q in range(1,5):
            if q == 1:
                trade_list = [get_tradelist(year,1,1,year,3,31),get_tradelist(year - 1,10,1,year,12,31)]
            elif q == 2:
                trade_list = [get_tradelist(year,4,1,year,6,30),get_tradelist(year,1,1,year,3,31)]
            elif q == 3:
                trade_list = [get_tradelist(year,7,1,year,9,30),get_tradelist(year,4,1,year,6,30)]
            else:
                trade_list = [get_tradelist(year,10,1,year,12,31),get_tradelist(year,7,1,year,9,30)]
            get_profit(trade_list,year,q)
            #get_profit_new(trade_list,year,q)

def get_market_daily(theday=today()):   #默认为更新当天，也可选择更新忘记更新或未更新的天
    trade_before = ts2datetimestr(datetimestr2ts(theday) - 2592000).split('-')   #获取前30天日期
    trade_after = ts2datetimestr(datetimestr2ts(theday) + 2592000).split('-')   #获取后30天日期
    trade_list = get_tradelist(int(trade_before[0]),int(trade_before[1]),int(trade_before[2]),int(trade_after[0]),int(trade_after[1]),int(trade_after[2]))   #获取可能包含当天的交易日列表
    if theday in trade_list:
        conn = default_db()
        cur = conn.cursor()
        w.start()
        allmarket = w.wset("SectorConstituent",u"date=" + ts2datetimestrnew(datetimestr2ts(theday)) + ";sector=全部A股").Data  #[1]为代码，[2]为名字
        quarter = what_quarter(theday)
        try:
            net_profits = ts.get_profit_data(quarter[0],quarter[1])
        except:
            net_profits = ts.get_profit_data(quarter[2],quarter[3])
        net_profits_before = ts.get_profit_data(quarter[2],quarter[3])
        for num in range(len(allmarket[1])):   #
            name = allmarket[2][num]
            code = allmarket[1][num]
            print code,name,num
            try:
                data1 = w.wsd(code, "close,turn", theday, theday, "Fill=Previous")
                data2 = w.wsd(code, "close", theday, theday, "Fill=Previous;PriceAdj=B")
                data3 = w.wsd(code, "industry_CSRC12", today(), today(), "industryType=5")
                for datenum in range(len(data1.Times)):
                    stock_id = code.split('.')[0]
                    stock_name = name
                    industry_name = data.Data[0][0].split('-')[0]
                    industry_code = industry_dict_big[industry_name]
                    datestr = datetime2datestr(data1.Times[datenum])
                    if type(data1.Data[0][datenum]) == float or type(data1.Data[0][datenum]) == int:
                        price = data1.Data[0][datenum]
                    else:
                        price = 0
                    if type(data2.Data[0][datenum]) == float or type(data2.Data[0][datenum]) == int:
                        price_fu = data2.Data[0][datenum]
                    else:
                        price_fu = 0
                    if type(data1.Data[1][datenum]) == float or type(data1.Data[1][datenum]) == int:
                        turnover_rate = data1.Data[1][datenum]
                    else:
                        turnover_rate = 0
                    order = 'insert into market_daily_new ( stock_id,stock_name,industry_code,date,price,price_fu,turnover_rate)values("%s", "%s","%s","%s","%f","%f","%f")' % (stock_id,stock_name,industry_code,datestr, price,price_fu,turnover_rate)
                    try:
                        cur.execute(order)
                        conn.commit()
                    except Exception, e:
                        print e
            except:
                pass
                
        sql = "SELECT * FROM market_daily_new WHERE date = '%s'" % (theday)
        cur.execute(sql)
        results = cur.fetchall()
        for result in results:
            #print result['stock_id']
            index = net_profits[net_profits.code == result['stock_id']].index.tolist()
            if len(index):
                netprofit = net_profits.net_profits[index[0]]
            else:
                index_before = net_profits_before[net_profits_before.code == result['stock_id']].index.tolist()
                if len(index_before):
                    netprofit = net_profits_before.net_profits[index_before[0]]
                else:
                    sql = "SELECT * FROM market_daily_new WHERE date = '%s' and stock_id = '%s'" % (trade_list[trade_list.index(theday) - 1],result['stock_id'])
                    cur.execute(sql)
                    results = cur.fetchall()
                    netprofit = results[0]['net_profits']
            update = "UPDATE market_daily_new SET net_profits = '%f' WHERE id = '%d'" % (netprofit, result['id']) 
            try:  
                cur.execute(update)
                conn.commit()
            except Exception, e:
                print e

def update_price(industry_dict_big):   #暂时无用
    conn = default_db()
    cur = conn.cursor()
    with open("stock.json",'r') as load_f:
        load_dict = json.load(load_f)
    #load_dict = {'300644':u'C','603871':u'G'}
    num = 0
    for code in sorted(load_dict.keys()):
        print code,num
        sql = "SELECT * FROM market_daily_new WHERE stock_id = '%s'" % (code)
        cur.execute(sql)
        results = cur.fetchall()
        industry_code = load_dict[code]
        for result in results:
            update = "UPDATE market_daily_new SET industry_code = '%s' WHERE id = '%d'" % (industry_code, result['id']) 
            try:  
                cur.execute(update)
                conn.commit()
            except Exception, e:
                print e
        num += 1


if __name__=="__main__":
    industry_dict_big = {u'农、林、牧、渔业':u'A',u'采矿业':u'B',u'制造业':u'C',u'电力、热力、燃气及水生产和供应业':u'D',
                        u'建筑业':u'E',u'批发和零售业':u'F',u'交通运输、仓储和邮政业':u'G',u'住宿和餐饮业':u'H',
                        u'信息传输、软件和信息技术服务业':u'I',u'金融业':u'J',u'房地产业':u'K',u'租赁和商务服务业':u'L',
                        u'科学研究和技术服务业':u'M',u'水利、环境和公共设施管理业':u'N',u'居民服务、修理和其他服务业':u'O',
                        u'教育':u'P',u'卫生和社会工作':u'Q',u'文化、体育和娱乐业':u'R',u'综合':u'S'}
    #create('2018-02-06','2018-03-04',industry_dict_big)
    #get_market_history()
    update_price(industry_dict_big)