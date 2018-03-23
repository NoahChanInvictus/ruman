#!/usr/bin/env python
# coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import pymysql as mysql
import pymysql.cursors
import pandas as pd
from operator import itemgetter, attrgetter
from numpy import mean

import time
from config import *
from time_utils import *

def defaultDatabase():
	conn = mysql.connect(host=HOST,user=USER,password=PASSWORD,db=DEFAULT_DB,charset=CHARSET,cursorclass=pymysql.cursors.DictCursor)
	conn.autocommit(True)
	cur = conn.cursor()
	return cur

def testDatabase():
	conn = mysql.connect(host=HOST,user=USER,password=PASSWORD,db=TEST_DB,charset=CHARSET,cursorclass=pymysql.cursors.DictCursor)
	conn.autocommit(True)
	cur = conn.cursor()
	return cur

def defaultDatabaseConn():
	conn = mysql.connect(host=HOST,user=USER,password=PASSWORD,db=DEFAULT_DB,charset=CHARSET,cursorclass=pymysql.cursors.DictCursor)
	conn.autocommit(True)
	return conn

def get_season(year1,month1,day1,year2,month2,day2):   #获得给定日期内包含的季度第一天，之后再在前面延续一个季度
	l = []
	for year in range(year1,year2 + 1):
		l.append("%d-01-01" % (year))
		l.append("%d-04-01" % (year))
		l.append("%d-07-01" % (year))
		l.append("%d-10-01" % (year))
	datelist = get_datelist(year1,month1,day1,year2,month2,day2)
	listnew = sorted(list(set(datelist).intersection(set(l))))
	if len(listnew) == 0:
		if month2 in [1,2,3]:
			listnew = ['%s-01-01' % (year2)]
		elif month2 in [4,5,6]:
			listnew = ['%s-04-01' % (year2)]
		elif month2 in [7,8,9]:
			listnew = ['%s-07-01' % (year2)]
		else:
			listnew = ['%s-10-01' % (year2)]
	y = int(listnew[0].split('-')[0])
	m = int(listnew[0].split('-')[1])
	d = int(listnew[0].split('-')[2])
	if m == 1:
		listnew.append("%d-10-01" % (y - 1))
		listnew.sort()
	else:
		listnew.append("%d-0%d-01" % (y,m - 3))
		listnew.sort()
	return listnew

def get_stock(id):
	cur = defaultDatabase()
	stocksql = "SELECT * FROM %s WHERE %s = '%s'" %(TABLE_DAY,DAY_ID,id)
	cur.execute(stocksql)
	thing = cur.fetchone()
	dic = {DAY_STOCK_ID:thing[DAY_STOCK_ID],DAY_START_DATE:thing[DAY_START_DATE],DAY_END_DATE:thing[DAY_END_DATE],DAY_INDUSTRY_CODE:thing[DAY_INDUSTRY_CODE]}
	return dic

def manipulateWarning():
	cur = defaultDatabase()
	conn = defaultDatabaseConn()
	theday = '2016-11-27'
	year = theday.split('-')[0]
	month = theday.split('-')[1]
	day = theday.split('-')[2]
	while 1:
		try:
			tradelist = get_tradelist(2012,1,1,year,month,day)
			break
		except:
			pass
	datelist = get_datelist(2012,1,1,year,month,day)
	if theday in tradelist:
		tradeday = theday
	else:
		num = datelist.index(theday)
		for i in range(1,num):
			if datelist[num - i] in tradelist:
				tradeday = datelist[num - i]
				break
	tradedaynew = tradelist[tradelist.index(tradeday) - 59]
	sql = "SELECT * FROM %s WHERE %s >= '%s' and %s <= '%s'" % (TABLE_WARNING,WARNING_DATE,tradedaynew,WARNING_DATE,tradeday)
	df = pd.read_sql(sql,conn)
	weeknum = sum(df.iloc[-5:][WARNING_TIMES])
	monthnum = sum(df.iloc[-20:][WARNING_TIMES])
	seasonnum = sum(df[WARNING_TIMES])
	result = {'weeknum':weeknum,'monthnum':monthnum,'seasonnum':seasonnum}
	return result

def manipulateWarningText():
	cur = defaultDatabase()
	sql = "SELECT * FROM " + TABLE_DAY
	cur.execute(sql)
	results = cur.fetchall()
	result = []
	for i in results:
		dic = {}
		dic['stock'] = i[DAY_STOCK_NAME] + u'(' + i[DAY_STOCK_ID] + u')'
		dic['start_date'] = i[DAY_START_DATE]
		if i[DAY_IFEND]:
			dic['end_date'] = i[DAY_END_DATE]
			dic['manipulate_state'] = u'已完成操纵'
		else:
			dic['end_date'] = u'至今'
			dic['manipulate_state'] = u'正在操纵'
		if i[DAY_MANIPULATE_TYPE] == 1:
			dic['manipulate_type'] = u'伪市值管理'
		elif i[DAY_MANIPULATE_TYPE] == 2:
			dic['manipulate_type'] = u'高送转'
		elif i[DAY_MANIPULATE_TYPE] == 3:
			dic['manipulate_type'] = u'定向增发'
		else:
			dic['manipulate_type'] = u'散布信息牟利'
		dic['industry_name'] = i[DAY_INDUSTRY_NAME]
		dic['increase_ratio'] = i[DAY_INCREASE_RATIO]
		dic['id'] = i[DAY_ID]
		result.append(dic)
	result = sorted(result, key= lambda x:(x['end_date'], x['start_date'], x['increase_ratio']), reverse=True)
	return result

def manipulateWarningNum(date):
	cur = defaultDatabase()
	theday = '2016-11-27'
	year = theday.split('-')[0]
	month = theday.split('-')[1]
	day = theday.split('-')[2]
	while 1:
		try:
			tradelist = get_tradelist(2012,1,1,year,month,day)
			break
		except:
			pass
	datelist = get_datelist(2012,1,1,year,month,day)
	if theday in tradelist:
		tradeday = theday
	else:
		num = datelist.index(theday)
		for i in range(1,num):
			if datelist[num - i] in tradelist:
				tradeday = datelist[num - i]
				break
	if date == 7:
		tradedaynew = tradelist[tradelist.index(tradeday) - 4]
	elif date == 30:
		tradedaynew = tradelist[tradelist.index(tradeday) - 19]
	else:
		tradedaynew = tradelist[tradelist.index(tradeday) - 59]
	sql = "SELECT * FROM %s WHERE %s >= '%s' and %s <= '%s'" % (TABLE_WARNING,WARNING_DATE,tradedaynew,WARNING_DATE,tradeday)
	cur.execute(sql)
	results = cur.fetchall()
	result = {'date':[thing[WARNING_DATE] for thing in results],'times':[thing[WARNING_TIMES] for thing in results]}
	return result

def manipulateInfluence(date):
	return 0

def manipulateHistory(id):
	cur = defaultDatabase()
	stock_id = get_stock(id)[DAY_STOCK_ID]
	sql = "SELECT * FROM %s WHERE %s = '%s'" %(TABLE_DAY,DAY_STOCK_ID,stock_id)
	cur.execute(sql)
	results = cur.fetchall()
	result = []
	for i in results:
		dic = {}
		dic['id'] = i[DAY_ID]
		if i[DAY_IFEND]:
			dic['end_date'] = i[DAY_END_DATE]
			dic['manipulate_state'] = u'已完成操纵'
		else:
			dic['end_date'] = u'至今'
			dic['manipulate_state'] = u'正在操纵'
		dic['start_date'] = i[DAY_START_DATE]
		if i[DAY_MANIPULATE_TYPE] == 1:
			dic['manipulate_type'] = u'伪市值管理'
		elif i[DAY_MANIPULATE_TYPE] == 2:
			dic['manipulate_type'] = u'高送转'
		elif i[DAY_MANIPULATE_TYPE] == 3:
			dic['manipulate_type'] = u'定向增发'
		else:
			dic['manipulate_type'] = u'散布信息牟利'
		dic['increase_ratio'] = i[DAY_INCREASE_RATIO]
		result.append(dic)
		result = sorted(result, key= lambda x:(x['end_date'], x['start_date'], x['increase_ratio']), reverse=True)
	return result

def manipulatePrice(id):
	conn = defaultDatabaseConn()
	stock = get_stock(id)
	stock_id = stock[DAY_STOCK_ID]
	start_date = stock[DAY_START_DATE]
	end_date = stock[DAY_END_DATE]
	industry = stock[DAY_INDUSTRY_CODE]
	sql = "SELECT * FROM %s WHERE %s >= '%s' and %s <= '%s'" % (TABLE_MARKET_DAILY,MARKET_DATE,lasttradedate(start_date),MARKET_DATE,end_date)
	df = pd.read_sql(sql,conn)
	datelist = sorted(list(set(df[MARKET_DATE])))
	industryprice = []
	price = []
	for date in datelist:
		industryprice.append(mean(df[(df[MARKET_DATE] == date) & (df[MARKET_INDUSTRY_CODE] == industry)][MARKET_PRICE]))
		price.append(float(df[(df[MARKET_DATE] == date) & (df[MARKET_STOCK_ID] == stock_id)][MARKET_PRICE]))
	industry_ratio = []
	ratio = []
	D_value = []
	for num in range(1,len(price)):
		a = (industryprice[num] - industryprice[num - 1]) / industryprice[num - 1]
		b = (price[num] - price[num - 1]) / price[num - 1]
		industry_ratio.append(a)
		ratio.append(b)
		D_value.append(b - a)
	result = {'date':datelist[1:],'industryprice':industryprice[1:],'price':price[1:],'industry_ratio':industry_ratio,'ratio':ratio,'D_value':D_value}
	return result

def manipulateSeasonbox(id):
	conn = defaultDatabaseConn()
	stock = get_stock(id)
	stock_id = stock[DAY_STOCK_ID]
	sql = "SELECT * FROM %s WHERE %s = '%s'" % (TABLE_HOLDERS_SHOW,HOLDERS_SHOW_STOCK_ID,stock_id)
	df = pd.read_sql(sql,conn)
	datelist = sorted(list(set(df[HOLDERS_SHOW_DATE])))
	datelistcopy = datelist[:]
	for date in datelistcopy:
		a = df[(df[HOLDERS_SHOW_STOCK_ID] == stock_id) & (df[HOLDERS_SHOW_DATE] == date)]
		if a.iloc[0][HOLDERS_SHOW_HOLDER_NAME] == u'None' and a.iloc[1][HOLDERS_SHOW_HOLDER_NAME] == u'None':
			datelist.remove(date)
	result = []
	for date in datelist:
		year = int(date.split('-')[0])
		month = int(date.split('-')[1])
		day = int(date.split('-')[2])
		if month == 1:
			season = '%s年第一季度' % (year)
			seasonid = date
		elif month == 4:
			season = '%s年第二季度' % (year)
			seasonid = date
		elif month == 7:
			season = '%s年第三季度' % (year)
			seasonid = date
		elif month == 10:
			season = '%s年第四季度' % (year)
			seasonid = date
		result.append({'season':season,'seasonid':seasonid})
	return result

def manipulateTop10holders(id,seasonid):
	cur = defaultDatabase()
	stock = get_stock(id)
	stock_id = stock[DAY_STOCK_ID]
	sql = "SELECT * FROM %s WHERE %s = '%s' and %s = '%s'" % (TABLE_HOLDERS_SHOW,HOLDERS_SHOW_STOCK_ID,stock_id,HOLDERS_SHOW_DATE,seasonid)
	cur.execute(sql)
	results = cur.fetchall()
	result = []
	for thing in results:
		thing.pop(HOLDERS_SHOW_STOCK_ID)
		thing.pop(HOLDERS_SHOW_DATE)
		thing.pop(HOLDERS_SHOW_ID)
		result.append(thing)
	result = sorted(result, key= lambda x:(x[HOLDERS_SHOW_RANKING]))
	return result

def manipulateHolderspct(id):
	cur = defaultDatabase()
	stock = get_stock(id)
	stock_id = stock[DAY_STOCK_ID]
	start_date = stock[DAY_START_DATE]
	end_date = stock[DAY_END_DATE]
	year1 = int(start_date.split('-')[0])
	month1 = int(start_date.split('-')[1])
	day1 = int(start_date.split('-')[2])
	year2 = int(end_date.split('-')[0])
	month2 = int(end_date.split('-')[1])
	day2 = int(end_date.split('-')[2])
	datelist = get_season(year1,month1,day1,year2,month2,day2)
	date = datelist[-1]
	sql = "SELECT * FROM %s WHERE %s = '%s' and %s = '%s'" % (TABLE_HOLDERS_PCT,HOLDERS_PCT_STOCK_ID,stock_id,HOLDERS_PCT_DATE,date)
	cur.execute(sql)
	results = cur.fetchone()
	if results is not None:
		result = {'holder_top10pct':results[HOLDERS_PCT_HOLDER_TOP10PCT],'holder_nottop10pct':100 - results[HOLDERS_PCT_HOLDER_TOP10PCT],
					'holder_pctbyinst':results[HOLDERS_PCT_HOLDER_PCTBYINST],'holder_notpctbyinst':100 - results[HOLDERS_PCT_HOLDER_PCTBYINST]}
	else:
		result = {}
	return result

if __name__=="__main__":
	#print len(manipulateHistory('002427'))
	manipulateAnnouncement(14)


