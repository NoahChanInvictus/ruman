#!/usr/bin/env python
# coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import pymysql as mysql
import pymysql.cursors
import pandas as pd
from operator import itemgetter, attrgetter

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
		result.append(dic)
		result = sorted(result, key= lambda x:(x['end_date'], x['start_date']), reverse=True)
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

def manipulateHistory(stock_id):
	cur = defaultDatabase()
	sql = "SELECT * FROM %s WHERE %s = '%s'" %(TABLE_DAY,DAY_STOCK_ID,stock_id)
	cur.execute(sql)
	results = cur.fetchall()
	result = []
	for i in results:
		dic = {}
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
	return result

def manipulatePrice(stock_id):
	conn = defaultDatabaseConn()
	sql = "SELECT * FROM %s WHERE %s >= '%s' and %s <= '%s'" % (TABLE_MARKET_DAILY,MARKET_DATE,tradedaynew,MARKET_DATE,tradeday)
	df = pd.read_sql(sql,conn)
	results = cur.fetchall()

if __name__=="__main__":
	print len(manipulateHistory('002427'))


