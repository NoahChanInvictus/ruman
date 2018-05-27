#-*-coding: utf-8-*-
#导入季度的净利润数据
import sys
reload(sys)
sys.path.append("../../../")
import pandas as pd
import tushare as ts
from config import *
from sql_utils import *

def get_profit(year,q):
    conn = default_db()
    cur = conn.cursor()
    net_profits_df = ts.get_profit_data(year,q)
    num = len(net_profits_df.index)
    for i in net_profits_df.index:
    	print num,year,q
        stock_id = net_profits_df.loc[i]['code']
        stock_name = net_profits_df.loc[i]['name']
        if q == 1:
            date = '%d-01-01' % (year)
        elif q == 2:
            date = '%d-04-01' % (year)
        elif q == 3:
            date = '%d-07-01' % (year)
        else:
            date = '%d-10-01' % (year)
        roe = net_profits_df.loc[i]['roe']
        net_profit_ratio = net_profits_df.loc[i]['net_profit_ratio']
        gross_profit_rate = net_profits_df.loc[i]['gross_profit_rate']
        net_profits = net_profits_df.loc[i]['net_profits']
        eps = net_profits_df.loc[i]['eps']
        business_income = net_profits_df.loc[i]['business_income']
        bips = net_profits_df.loc[i]['bips']

        order = 'insert into %s ( %s,%s,%s,%s,%s,%s,%s,%s,%s,%s)values("%s", "%s","%s","%f","%f","%f","%f","%f","%f","%f")'\
            % (TABLE_NETPROFIT,NETPROFIT_STOCK_ID,NETPROFIT_STOCK_NAME,NETPROFIT_DATE,NETPROFIT_ROE,NETPROFIT_NET_PROFIT_RATIO,\
            NETPROFIT_GROSS_PROFIT_RATE,NETPROFIT_NET_PROFITS,NETPROFIT_EPS,NETPROFIT_BUSINESS_INCOME,NETPROFIT_BIPS,\
            stock_id,stock_name,date,roe,net_profit_ratio,gross_profit_rate,net_profits,eps,business_income,bips)
        try:  
            cur.execute(order)
            conn.commit()
        except Exception, e:
            print e
        num -= 1

def test():
    conn = default_db()
    cur = conn.cursor()
    sql = "SELECT * FROM netprofit"
    cur.execute(sql)
    results = cur.fetchall()
    n = 0
    for result in results:
        q = result['date']
        if int(q.split('-')[1]) == 1:
            date = '%s-01-01' % (q.split('-')[0])
        elif int(q.split('-')[1]) == 2:
            date = '%s-04-01' % (q.split('-')[0])
        elif int(q.split('-')[1]) == 3:
            date = '%s-07-01' % (q.split('-')[0])
        else:
            date = '%s-10-01' % (q.split('-')[0])
        update = "UPDATE netprofit SET date = '%s' WHERE id = '%d'" % (date,result['id'])
        try:
            cur.execute(update)
            conn.commit()
        except Exception, e:
            conn.rollback()
            print e
        n += 1
        print n

if __name__ == '__main__':
    
    for year in range(2011,2018):
        for quarter in range(1,5):
            print year,quarter
            get_profit(year,quarter)
    #test()