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
	for year in range(year1,year2 + 1):   #加入一年四个季度的季初日期
		l.append("%d-01-01" % (year))
		l.append("%d-04-01" % (year))
		l.append("%d-07-01" % (year))
		l.append("%d-10-01" % (year))
	datelist = get_datelist(year1,month1,day1,year2,month2,day2)
	listnew = sorted(list(set(datelist).intersection(set(l))))   #去掉不在该时间段内的日期
	if len(listnew) == 0:   #如果没有则添加该段时间所在的季度季初日期
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
	if m == 1:   #添加该段时间的前一季度
		listnew.append("%d-10-01" % (y - 1))
		listnew.sort()
	else:
		listnew.append("%d-0%d-01" % (y,m - 3))
		listnew.sort()
	return listnew

def get_stock(id):   #通过day的id获取股票代码等数据
	cur = defaultDatabase()
	stocksql = "SELECT * FROM %s WHERE %s = '%s'" %(TABLE_DAY,DAY_ID,id)
	cur.execute(stocksql)
	thing = cur.fetchone()
	dic = {DAY_STOCK_ID:thing[DAY_STOCK_ID],DAY_START_DATE:thing[DAY_START_DATE],DAY_END_DATE:thing[DAY_END_DATE],DAY_INDUSTRY_CODE:thing[DAY_INDUSTRY_CODE]}
	return dic

def manipulateWarning():   #预警数合计总览
	cur = defaultDatabase()
	conn = defaultDatabaseConn()
	theday = '2016-12-30'   
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
	'''
	sql = "SELECT * FROM %s WHERE %s >= '%s' and %s <= '%s'" % (TABLE_WARNING,WARNING_DATE,tradedaynew,WARNING_DATE,tradeday)
	df = pd.read_sql(sql,conn)
	weeknum = sum(df.iloc[-5:][WARNING_TIMES])
	monthnum = sum(df.iloc[-20:][WARNING_TIMES])
	seasonnum = sum(df[WARNING_TIMES])
	result = {'weeknum':weeknum,'monthnum':monthnum,'seasonnum':seasonnum}
	return result'''
	tradedaynew7 = tradelist[tradelist.index(tradeday) - 4]
	tradedaynew30 = tradelist[tradelist.index(tradeday) - 19]
	sql = "SELECT * FROM %s WHERE %s >= '%s' and %s <= '%s'" % (TABLE_DAY,DAY_END_DATE,tradedaynew,DAY_END_DATE,tradeday)   #寻找在预警条目内的结束日期在5、20、60交易日内的数据
	df = pd.read_sql(sql,conn)
	weeknum = len(df[df[DAY_END_DATE] >= tradedaynew7])
	monthnum = len(df[df[DAY_END_DATE] >= tradedaynew30])
	seasonnum = len(df)
	result = {'weeknum':weeknum,'monthnum':monthnum,'seasonnum':seasonnum}
	return result

def manipulateWarningText():   #列出预警文本
	cur = defaultDatabase()
	sql = "SELECT * FROM " + TABLE_DAY
	cur.execute(sql)
	results = cur.fetchall()
	result = []
	for i in results:   #选取所有文本并展示
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
	result = sorted(result, key= lambda x:(x['end_date'], x['start_date'], x['increase_ratio']), reverse=True)   #按照特定顺序排序
	return result

def manipulateWarningNum(date):   #获取周、月、季内每天预警的次数并画图展示，方法类似Warning
	cur = defaultDatabase()
	theday = '2016-11-27'   #需改为today()
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
	if theday in tradelist:   #如果今天不为交易日则向前推最近的交易日
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
		tradedaynew = tradelist[tradelist.index(tradeday) - 59]   #获取一季度的数据
	sql = "SELECT * FROM %s WHERE %s >= '%s' and %s <= '%s'" % (TABLE_WARNING,WARNING_DATE,tradedaynew,WARNING_DATE,tradeday)
	cur.execute(sql)
	results = cur.fetchall()
	result = {'date':[thing[WARNING_DATE] for thing in results],'times':[thing[WARNING_TIMES] for thing in results]}
	return result

def manipulateInfluence(date):   #根据day表统计不同收益率的股票并展示
	cur = defaultDatabase()
	theday = '2016-09-04'
	year = theday.split('-')[0]
	month = theday.split('-')[1]
	day = theday.split('-')[2]
	if date == 7:
		frequency = "week"
	elif date == 30:
		frequency = "month"
	else:
		frequency = "season"
	sql = "SELECT * FROM %s WHERE %s = '%s' and %s = '%s'" % (TABLE_INFLUENCE,INFLUENCE_DATE,theday,INFLUENCE_FREQUENCY,frequency)
	cur.execute(sql)
	results = cur.fetchone()
	if results is not None:
		results.pop(INFLUENCE_ID)
		results.pop(INFLUENCE_DATE)
		results.pop(INFLUENCE_FREQUENCY)
		dic = {}
		dic["0%~-5%"] = results[INFLUENCE_1]
		dic["-5%~-10%"] = results[INFLUENCE_2]
		dic["-10%~-15%"] = results[INFLUENCE_3]
		dic["-15%~-20%"] = results[INFLUENCE_4]
		dic["-20%~-25%"] = results[INFLUENCE_5]
		dic["-25%~-30%"] = results[INFLUENCE_6]
		dic["-30%~-35%"] = results[INFLUENCE_7]
		dic["-35%~-40%"] = results[INFLUENCE_8]
		dic["-40%~-45%"] = results[INFLUENCE_9]
		dic["-45%~-50%"] = results[INFLUENCE_10]
		dic["-50%~-55%"] = results[INFLUENCE_11]
		dic["-55%~-60%"] = results[INFLUENCE_12]
		dic["-60%~-65%"] = results[INFLUENCE_13]
		dic["-65%~-70%"] = results[INFLUENCE_14]
		dic["-70%~-75%"] = results[INFLUENCE_15]
		dic["0%~5%"] = results[INFLUENCE_16]
		dic["5%~10%"] = results[INFLUENCE_17]
		dic["10%~15%"] = results[INFLUENCE_18]
		dic["15%~20%"] = results[INFLUENCE_19]
		dic["20%~25%"] = results[INFLUENCE_20]
		dic["25%~30%"] = results[INFLUENCE_21]
		dic["30%~35%"] = results[INFLUENCE_22]
		dic["35%~40%"] = results[INFLUENCE_23]
		dic["40%~45%"] = results[INFLUENCE_24]
		dic["45%~50%"] = results[INFLUENCE_25]
		dic["50%~55%"] = results[INFLUENCE_26]
		dic["55%~60%"] = results[INFLUENCE_27]
		dic["60%~65%"] = results[INFLUENCE_28]
		dic["65%~70%"] = results[INFLUENCE_29]
		dic["70%~75%"] = results[INFLUENCE_30]
		dic["75%~80%"] = results[INFLUENCE_31]
		dic["80%~85%"] = results[INFLUENCE_32]
		dic["85%~90%"] = results[INFLUENCE_33]
		dic["90%~95%"] = results[INFLUENCE_34]
		dic["95%~100%"] = results[INFLUENCE_35]	
		ratio = []
		num = []
		keylist = sorted(dic.keys())
		keylist.remove('-5%~-10%')
		keylist1 = sorted(keylist[:keylist.index('0%~-5%')],reverse=True)
		keylist2 = ['-5%~-10%']
		keylist3 = keylist[keylist.index('0%~-5%'):]
		keylistnew = []
		keylistnew.extend(keylist1)
		keylistnew.extend(keylist2)
		keylistnew.extend(keylist3)
		for k in keylistnew:
			ratio.append(k)
			num.append(dic[k])
		return {"ratio":ratio,"num":num}
	else:
		return {}

def manipulateIndustry(date):   #根据day表统计不同行业的股票并展示
	cur = defaultDatabase()
	theday = '2016-09-04'
	year = theday.split('-')[0]
	month = theday.split('-')[1]
	day = theday.split('-')[2]
	if date == 7:
		frequency = "week"
	elif date == 30:
		frequency = "month"
	else:
		frequency = "season"
	sql = "SELECT * FROM %s WHERE %s = '%s' and %s = '%s'" % (TABLE_INDUSTRY,INDUSTRY_DATE,theday,INDUSTRY_FREQUENCY,frequency)
	cur.execute(sql)
	results = cur.fetchone()
	if results is not None:
		results.pop(INDUSTRY_ID)
		results.pop(INDUSTRY_DATE)
		results.pop(INDUSTRY_FREQUENCY)
		dic = {}
		dic["农、林、牧、渔业"] = results[INDUSTRY_A]
		dic["采矿业"] = results[INDUSTRY_B]
		dic["制造业"] = results[INDUSTRY_C]
		dic["电力、热力、燃气及水生产和供应业"] = results[INDUSTRY_D]
		dic["建筑业"] = results[INDUSTRY_E]
		dic["批发和零售业"] = results[INDUSTRY_F]
		dic["交通运输、仓储和邮政业"] = results[INDUSTRY_G]
		dic["住宿和餐饮业"] = results[INDUSTRY_H]
		dic["信息传输、软件和信息技术服务业"] = results[INDUSTRY_I]
		dic["金融业"] = results[INDUSTRY_J]
		dic["房地产业"] = results[INDUSTRY_K]
		dic["租赁和商务服务业"] = results[INDUSTRY_L]
		dic["科学研究和技术服务业"] = results[INDUSTRY_M]
		dic["水利、环境和公共设施管理业"] = results[INDUSTRY_N]
		dic["居民服务、修理和其他服务业"] = results[INDUSTRY_O]
		dic["教育"] = results[INDUSTRY_P]
		dic["卫生和社会工作"] = results[INDUSTRY_Q]
		dic["文化、体育和娱乐业"] = results[INDUSTRY_R]
		dic["综合"] = results[INDUSTRY_S]
		industry = []
		num = []
		dicsort = sorted(dic.items(),key=lambda x:x[1],reverse=True)
		for k in dicsort:
			industry.append(k[0])
			num.append(k[1])
		return {"industry":industry,"num":num,'industrymax':industry[:5],'nummax':num[:5]}
	else:
		return {}

def manipulateType(date):   #根据day表统计不同操纵类型的股票并展示
	cur = defaultDatabase()
	theday = '2016-09-04'
	year = theday.split('-')[0]
	month = theday.split('-')[1]
	day = theday.split('-')[2]
	if date == 7:
		frequency="week"
	elif date == 30:
		frequency = "month"
	else:
		frequency = "season"
	sql = "SELECT * FROM %s WHERE %s = '%s' and %s = '%s'" % (TABLE_TYPE,TYPE_DATE,theday,TYPE_FREQUENCY,frequency)
	cur.execute(sql)
	results = cur.fetchone()
	if results is not None:
		results.pop(TYPE_ID)
		results.pop(TYPE_DATE)
		results.pop(TYPE_FREQUENCY)
		dic = {}
		dic["高送转"] = results[TYPE1]
		dic["定向增发"] = results[TYPE2]
		dic["伪市值管理"] = results[TYPE3]
		dic["散步牟利消息"] = results[TYPE4]
		dic["其它"] = results[TYPE5]
		typelist = []
		num = []
		dicsort = sorted(dic.items(),key=lambda x:x[1],reverse=True)
		for k in dicsort:
			typelist.append(k[0])
			num.append(k[1])
		return {"type":typelist,"num":num}
	else:
		return {}

def manipulatePanel(date):   #根据day表统计不同板块的股票并展示
	cur = defaultDatabase()
	theday = '2016-09-04'
	year = theday.split('-')[0]
	month = theday.split('-')[1]
	day = theday.split('-')[2]
	if date == 7:
		frequency="week"
	elif date == 30:
		frequency = "month"
	else:
		frequency = "season"
	sql = "SELECT * FROM %s WHERE %s = '%s' and %s = '%s'" % (TABLE_PANEL,PANEL_DATE,theday,PANEL_FREQUENCY,frequency)
	cur.execute(sql)
	results = cur.fetchone()
	if results is not None:
		results.pop(PANEL_ID)
		results.pop(PANEL_DATE)
		results.pop(PANEL_FREQUENCY)
		dic = {}
		dic["主板"] = results[PANEL1]
		dic["中小板"] = results[PANEL2]
		dic["创业板"] = results[PANEL3]
		panel = []
		num = []
		dicsort = sorted(dic.items(),key=lambda x:x[1],reverse=True)
		for k in dicsort:
			panel.append(k[0])
			num.append(k[1])
		print panel,num
		return {"PANEL":panel,"num":num}
	else:
		return {}

def manipulateGongshang(id):   #给出该股票的工商数据
	cur = defaultDatabase()
	stock_id = get_stock(id)[DAY_STOCK_ID]
	sql = "SELECT * FROM %s WHERE %s = '%s'" %(TABLE_GONGSHANG,GONGSHANG_STOCK_ID,stock_id)
	cur.execute(sql)
	results = cur.fetchone()
	if results is not None:
		results.pop(GONGSHANG_ID)
		results.pop(GONGSHANG_STOCK_ID)
		results.pop(GONGSHANG_STOCK_NAME)
		return results
	else:
		return {GONGSHANG_PLACE:u'未知',GONGSHANG_START_DATE:u'未知',GONGSHANG_NAME:u'未知',GONGSHANG_MONEY:u'未知',GONGSHANG_PERSON:u'未知',GONGSHANG_KIND:u'未知',GONGSHANG_INDUSTRY:u'未知',GONGSHANG_PLATE:u'未知'}

def manipulateHistory(id):   #给出该股票的历史操纵数据
	cur = defaultDatabase()
	stock_id = get_stock(id)[DAY_STOCK_ID]
	sql = "SELECT * FROM %s WHERE %s = '%s'" %(TABLE_DAY,DAY_STOCK_ID,stock_id)   #从列表中选出该股票的数据并展示
	cur.execute(sql)
	results = cur.fetchall()
	resultother = []
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
		dic['name'] = i[DAY_STOCK_NAME] + u'(' + i[DAY_STOCK_ID] + u')'
		if id ==dic['id']:
			dic['ifthis'] = 1
			dicthis = dic
		else:
			dic['ifthis'] = 0
			resultother.append(dic)
	resultother = sorted(resultother, key= lambda x:(x['end_date'], x['start_date'], x['increase_ratio']), reverse=True)   #按照特定顺序排序
	result = [dicthis]
	result.extend(resultother)
	return result

def manipulatePrice(id):   #获取本次操作期间的股价和收益率
	conn = defaultDatabaseConn()
	stock = get_stock(id)
	stock_id = stock[DAY_STOCK_ID]
	start_date = stock[DAY_START_DATE]
	end_date = stock[DAY_END_DATE]
	industry = stock[DAY_INDUSTRY_CODE]
	sql = "SELECT * FROM %s WHERE %s >= '%s' and %s <= '%s'" % (TABLE_MARKET_DAILY,MARKET_DATE,lasttradedate(start_date),MARKET_DATE,end_date)
	df = pd.read_sql(sql,conn)
	datelist = sorted(list(set(df[MARKET_DATE])))   #获取日期列表
	industryprice = []
	price = []
	for date in datelist:
		industryprice.append(mean(df[(df[MARKET_DATE] == date) & (df[MARKET_INDUSTRY_CODE] == industry)][MARKET_PRICE]))   #获取同行业价格平均值列表
		price.append(float(df[(df[MARKET_DATE] == date) & (df[MARKET_STOCK_ID] == stock_id)][MARKET_PRICE]))   #获取本股票价格列表
	industry_ratio = []
	ratio = []
	D_value = []
	for num in range(1,len(price)):
		a = (industryprice[num] - industryprice[num - 1]) / industryprice[num - 1]   #同行业收益率
		b = (price[num] - price[num - 1]) / price[num - 1]   #本股票收益率
		industry_ratio.append(a)
		ratio.append(b)
		D_value.append(abs(b - a))   #差值绝对值
	result = {'date':datelist[1:],'industry_price':industryprice[1:],'price':price[1:],'industry_ratio':industry_ratio,'ratio':ratio,'D_value':D_value}
	return result

def manipulateSeasonbox(id):   #获得季度下拉框
	conn = defaultDatabaseConn()
	stock = get_stock(id)
	stock_id = stock[DAY_STOCK_ID]
	sql = "SELECT * FROM %s WHERE %s = '%s'" % (TABLE_HOLDERS_SHOW,HOLDERS_SHOW_STOCK_ID,stock_id)
	df = pd.read_sql(sql,conn)
	datelist = sorted(list(set(df[HOLDERS_SHOW_DATE])))   #获取数据库存在数据的季度
	datelistcopy = datelist[:]
	for date in datelistcopy:   #若该季度数据前两大股东为None则不显示
		a = df[(df[HOLDERS_SHOW_STOCK_ID] == stock_id) & (df[HOLDERS_SHOW_DATE] == date)]
		if a.iloc[0][HOLDERS_SHOW_HOLDER_NAME] == u'None' and a.iloc[1][HOLDERS_SHOW_HOLDER_NAME] == u'None':
			datelist.remove(date)
	result = []
	if len(datelist):   #如果里面有的话返回对应的标签
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
	else:
		season = '无'
		seasonid = 'Nodata'
	return result

def manipulateTop10holders(id,seasonid):   #对应季度搜索展示股东数据
	cur = defaultDatabase()
	stock = get_stock(id)
	stock_id = stock[DAY_STOCK_ID]
	if seasonid == 'Nodata':
		result ={}
	else:
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

def manipulateLargetrans(id):   #展示大宗交易记录
	cur = defaultDatabase()
	conn = defaultDatabaseConn()
	stock = get_stock(id)
	stock_id = stock[DAY_STOCK_ID]
	start_date = stock[DAY_START_DATE]
	end_date = stock[DAY_END_DATE]
	stock_id = '002211'
	start_date = '2014-11-01'
	end_date = '2014-11-30'
	sql = "SELECT * FROM %s WHERE %s = '%s'" % (TABLE_TRANCE,TRAN_STOCK_ID,stock_id)
	df = pd.read_sql(sql,conn)
	a = df[(df[TRAN_DATE] <= end_date) & (df[TRAN_DATE] >= start_date)]
	result=[]
	for num in range(len(a)):
		dic = {}
		dic['date'] = a.iloc[num][TRAN_DATE]
		dic['price'] = a.iloc[num][TRAN_PRICE]
		dic['number'] = a.iloc[num][TRAN_NUMBER]
		dic['amount'] = a.iloc[num][TRAN_AMOUNT]
		dic['ratio'] = a.iloc[num][TRAN_RATIO]
		dic['buyer'] = a.iloc[num][TRAN_BUYER]
		dic['seller'] = a.iloc[num][TRAN_SELLER]
		result.append(dic)
	result = sorted(result, key= lambda x:(x['date']), reverse=True)
	return result

def manipulateHolderspct(id):   #获取机构投资者和十大股东所占比例的数据
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