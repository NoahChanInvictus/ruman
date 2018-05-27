#!/usr/bin/env python
#coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from elasticsearch import Elasticsearch
from time_utils import *
import pymysql as mysql
import pymysql.cursors
import time

from config import *
from db import get_stock

es214 = Elasticsearch([{'host':ES_HOST,'port':ES_PORT}])
es216 = Elasticsearch([{'host': ES_HOST_WEB0, 'port': ES_PORT_WEB0}])

def defaultDatabase():
	conn = mysql.connect(host=SQL_HOST,user=SQL_USER,password=SQL_PASSWD,db=DEFAULT_DB,charset=SQL_CHARSET,cursorclass=pymysql.cursors.DictCursor)
	conn.autocommit(True)
	cur = conn.cursor()
	return cur

def get_stock(id):
	cur = defaultDatabase()
	stocksql = "SELECT * FROM %s WHERE %s = '%s'" %(TABLE_DAY,DAY_ID,id)
	cur.execute(stocksql)
	thing = cur.fetchone()
	dic = {DAY_STOCK_ID:thing[DAY_STOCK_ID],DAY_START_DATE:thing[DAY_START_DATE],DAY_END_DATE:thing[DAY_END_DATE],DAY_INDUSTRY_CODE:thing[DAY_INDUSTRY_CODE]}
	return dic

def get_news(id):
	cur = defaultDatabase()
	stocksql = "SELECT * FROM %s WHERE %s = '%s'" %(TABLE_HOTNEWS,HOT_NEWS_ID,id)
	cur.execute(stocksql)
	thing = cur.fetchone()
	dic = {HOT_NEWS_IN_TIME:int(thing[HOT_NEWS_IN_TIME])}
	return dic

def get_user(uid):
	uid = int(uid)
	query_body = {"size":10,"query":{"match":{"uid":uid}}}

	res = es216.search(index=WEBOUSER_INDEX, doc_type='user', body=query_body,request_timeout=100)
	hits = res['hits']['hits']
	if len(hits):
		return hits[0]['_source']['nick_name']
	else:
		return str(uid)

def manipulateAnnouncement(id):   #展示操纵期内公告详情
	stock = get_stock(id)
	stock_id = stock[DAY_STOCK_ID]
	start_time = datetimestr2ts(stock[DAY_START_DATE])
	end_time = datetimestr2ts(stock[DAY_END_DATE])
	query_body = {"size":2000,"query":{ "filtered": {
		"query":{"match":{"stock_id":stock_id}},
		"filter":{"range":{"publish_time":{"gte": start_time,"lte": end_time}}}
	}}}

	res = es214.search(index=DIC_ANNOUNCEMENT['index'], doc_type=DIC_ANNOUNCEMENT['type'], body=query_body,request_timeout=100)
	hits = res['hits']['hits']
	result = []
	if(len(hits)):
		for item in hits:
			res = item['_source']
			a = res['type']
			if a == 1:
				announcement_type = u'并购重组'
			elif a == 2:
				announcement_type = u'对外投资'
			elif a == 3:
				announcement_type = u'股权质押'
			elif a == 4:
				announcement_type = u'大股东减持'
			elif a == 5:
				announcement_type = u'利润分配'
			elif a == 6:
				announcement_type = u'关联交易'
			elif a == 7 or a == 12 or a == 13:
				announcement_type = u'定向增发'
			elif a == 8:
				announcement_type = u'配股'
			elif a == 9:
				announcement_type = u'停牌'
			elif a == 10:
				announcement_type = u'高管辞职'
			else:
				announcement_type = u'其他'
			dic = {'publish_time':ts2datetimestr(res['publish_time']),'title':res['title'],'url':res['url'],'type':announcement_type}
			result.append(dic)
	return result

def manipulateLargetrans(id):   #展示大宗交易记录
	stock = get_stock(id)
	stock_id = stock[DAY_STOCK_ID]
	start_date = stock[DAY_START_DATE]
	end_date = stock[DAY_END_DATE]

	query_body = {"size":2000,"query":{ "filtered": {
		"query":{"match":{"stock_id":stock_id}},
		"filter":{"range":{"date":{"gte": start_date,"lte": end_date}}}
	}}}
	res = es214.search(index=DIC_LARGE_TRANS['index'], doc_type=DIC_LARGE_TRANS['type'], body=query_body,request_timeout=100)
	hits = res['hits']['hits']

	result=[]
	if(len(hits)):
		for item in hits:
			res = item['_source']
			dic = {}
			dic['date'] = res['date']
			dic['price'] = res['transaction_price']
			dic['number'] = res['transaction_number']
			dic['amount'] = res['transaction_amount']
			dic['ratio'] = res['Discount_ratio']
			dic['buyer'] = res['Buyer']
			dic['seller'] = res['Seller']
			result.append(dic)
	result = sorted(result, key= lambda x:(x['date']), reverse=True)
	return result

def manipulateRumantext(id):
	cur = defaultDatabase()
	stocksql = "SELECT * FROM %s WHERE %s = '%s'" %('manipulate_day',DAY_ID,id)
	cur.execute(stocksql)
	thing = cur.fetchone()
	mid = thing[DAY_MID]

	indexs=["flow_text_2016-11-07","flow_text_2016-11-08","flow_text_2016-11-11","flow_text_2016-11-12"\
	,"flow_text_2016-11-13","flow_text_2016-11-14","flow_text_2016-11-15","flow_text_2016-11-16"\
	,"flow_text_2016-11-17","flow_text_2016-11-18","flow_text_2016-11-19","flow_text_2016-11-20"\
	,"flow_text_2016-11-21","flow_text_2016-11-22","flow_text_2016-11-23","flow_text_2016-11-24"\
	,"flow_text_2016-11-25","flow_text_2016-11-26","flow_text_2016-11-27"]

	query_body = {"size":10,"query": {"bool": {"must": [{"match": {"mid": mid}}]}}}
	for index in indexs:
		res = es216.search(index=index, doc_type="text",body=query_body, request_timeout=100)
		hits = res['hits']['hits']
		if len(hits):
			item = hits[0]["_source"]
			dic = {}
			dic['text'] = item['text']
			dic['ifrumor'] = '是'
			dic['publish_time'] = ts2date(item['timestamp'])
			dic['author'] = get_user(item['uid'])
			dic['source'] = '微博'
			return dic
			break
	if len(hits) == 0:
		return {}

def manipulateRumancomment(id):
	cur = defaultDatabase()
	stocksql = "SELECT * FROM %s WHERE %s = '%s'" %('manipulate_day',DAY_ID,id)
	cur.execute(stocksql)
	thing = cur.fetchone()
	mid = thing[DAY_MID]

	indexs=["flow_text_2016-11-07","flow_text_2016-11-08","flow_text_2016-11-11","flow_text_2016-11-12"\
	,"flow_text_2016-11-13","flow_text_2016-11-14","flow_text_2016-11-15","flow_text_2016-11-16"\
	,"flow_text_2016-11-17","flow_text_2016-11-18","flow_text_2016-11-19","flow_text_2016-11-20"\
	,"flow_text_2016-11-21","flow_text_2016-11-22","flow_text_2016-11-23","flow_text_2016-11-24"\
	,"flow_text_2016-11-25","flow_text_2016-11-26","flow_text_2016-11-27"]

	query_body = {"size":10,"query": {"bool": {"must": [{"match": {"root_mid": mid}},{"match": {"message_type": 2}}]}}}
	result = []
	for index in indexs:
		res = es216.search(index=index, doc_type="text",body=query_body, request_timeout=100)
		hits = res['hits']['hits']
		if len(hits):
			for hit in hits:
				dic = {}
				item = hit["_source"]
				dic['publish_time'] = ts2date(item['timestamp'])
				dic['text'] = item['text']
				dic['author'] = get_user(item['uid'])
				dic['source'] = '微博'
				result.append(dic)
	result = sorted(result, key= lambda x:(x['publish_time']),reverse=True)
	return result

def hotspotPropagate(id,source):
	publish_time = get_news(id)[HOT_NEWS_IN_TIME]
	timendays = publish_time - 7*24*3600   #可更改
	#query_body = {"size":15000,"query": {"bool": {"must": [{"match":{"news_id":id}},{"match": {"unique": 1}}]}}}
	query_body = {"size":15000,"query": { "filtered": {
		"query":{"bool": {"must": [
			{"match": {"news_id": id}},
			{"match": {"unique": 1}}]}},
		"filter":{"range":{"publish_time":{"gte": timendays,"lte": publish_time}}}
	}}}

	res = es214.search(index=TOPIC_ABOUT_INDEX, doc_type=source, body=query_body,request_timeout=100)
	hits = res['hits']['hits']

	result = []
	if len(hits):
		for item in hits:
			dic = {}
			dic['publish_time'] = ts2date(int(item['_source']['publish_time']))
			dic['topic'] = item['_source']['topic']
			if source == TOPIC_ABOUT_DOCTYPE[0]:
				dic['title'] = item['_source']['title']
				dic['author'] = item['_source']['author']
				dic['keyword'] = item['_source']['key']
				dic['url'] = item['_source']['url']
			elif source == TOPIC_ABOUT_DOCTYPE[1]:
				dic['title'] = item['_source']['content']
				dic['author'] = item['_source']['nickname']
				dic['keyword'] = item['_source']['topic']
				dic['url'] = item['_source']['url']
			elif source == TOPIC_ABOUT_DOCTYPE[2]:
				dic['title'] = item['_source']['title']
				dic['author'] = item['_source']['author']
				dic['keyword'] = item['_source']['key']
				dic['url'] = item['_source']['url']
			else:
				dic['title'] = item['_source']['title']
				dic['author'] = item['_source']['web']
				dic['keyword'] = item['_source']['key']
				dic['url'] = item['_source']['url']
			result.append(dic)
		result = sorted(result, key= lambda x:(x['publish_time']))
		return result
	else:
		return []

def hotspotTopicaxis(id,source):
	'''
	query_body = {"size":10,"query": { "filtered": {
		"query":{"bool": {"must": [
			{"match": {"news_id": id}},
			{"match": {"source": source}}]}},
		"filter":{"range":{"cluster_id":{"gte": 0,"lte": CLUSTER_NUM - 1}}}
	}}}'''
	hits_all = []
	for cluster_num in range(CLUSTER_NUM):#
		query_body = {"size":10000,"query":{"bool": {"must": [
				{"match": {"news_id": id}},
				{"match": {"source": source}},
				{"match": {"cluster_id": cluster_num}}]
		}}}

		res = es214.search(index=CLUSTER_INDEX, doc_type="type1", body=query_body,request_timeout=100)
		hits = res['hits']['hits']
		if len(hits) <= CLUSTER_OVER:
			hits_all.extend(hits)

	tslist = [item['_source']['publish_time'] for item in hits_all]
	datedic = {}
	monthdic = {}
	for item in hits_all:
		date = ts2datetime(int(item['_source']['publish_time']))
		if source == TOPIC_ABOUT_DOCTYPE[1]:
			if date not in datedic.keys():
				datedic[date] = [{"title":'',"content":item['_source']['content']}]   #item['_source']['title']
			else:
				datedic[date].append({"title":'',"content":item['_source']['content']})
		else:
			if date not in datedic.keys():
				datedic[date] = [{"title":item['_source']['title'],"content":item['_source']['content']}]
			else:
				datedic[date].append({"title":item['_source']['title'],"content":item['_source']['content']})
	for date in datedic.keys():
		month = date.split('-')[1]
		year = date.split('-')[0]
		ymonth = "%s-%s" % (year,month)
		if ymonth not in monthdic.keys():
			monthdic[ymonth] = [date]
		else:
			monthdic[ymonth].append(date)
	l = [{"date":date,"text":datedic[date][:3]} for date in sorted(datedic.keys(),reverse=True)]
	result = []
	for ymonth in monthdic.keys():
		ll = []
		for date in l:
			if date['date'] in monthdic[ymonth]:
				ll.append(date)
		result.append({'month':ymonth,'monthtext':ll[:7]})
	result = sorted(result, key= lambda x:(x['month']),reverse=True)
	result = result
	return result
def newhotspotcombineText():
	cur = defaultDatabase()

	# query_body = {"size":5000,"query":{"match_all": {}}}
	query_body = {"size":5000,"query":{"term": {"rumor_label":0}}}
	sql = "SELECT * FROM %s WHERE ifshow=2 " % (TABLE_HOTNEWS)

	cur.execute(sql)
	results = cur.fetchall()
	res = es216.search(index=RUMORLIST_INDEX, body=query_body,request_timeout=100)
	hits = res['hits']['hits']
	result = []

	for thing in results:
		dic = {}
		dic['title'] = thing[HOT_NEWS_TITLE]
		dic['publish_time'] = ts2date(float(thing[HOT_NEWS_IN_TIME]))
		dic['source'] = '新闻'
		dic['keyword'] = thing[HOT_NEWS_KEY_WORD]
		dic['id'] = thing['id']
		dic['publisher'] = thing['web']
		result.append(dic)
	result = sorted(result, key= lambda x:(x['publish_time']),reverse=True)   #只取时间最近的前十个
	resultes = []
	for hit in hits:
		dic = {}
		dic['title'] = hit['_source']['text']
		dic['publish_time'] = ts2date(hit['_source']['timestamp'])
		dic['source'] = '微博'
		dic['keyword'] = hit['_source']['keywords_string'].replace('&',' ')
		# dic['ifruman'] = hit['_source']['rumor_label']
		dic['id'] = hit['_id']
		# dic['type'] = hit['_type']
		dic['publisher'] = hit['_source']['uid']
		resultes.append(dic)
	resultes = sorted(resultes, key= lambda x:(x['publish_time']),reverse=True)[:10]   #只取时间最近的前十个
	#print len(resultes)
	result.extend(resultes)
	#print len(result)
	return result

def hotspotandrumanText():
	cur = defaultDatabase()

	query_body = {"size":5000,"query":{"match_all": {}}}
	sql = "SELECT * FROM %s " % (TABLE_HOTNEWS)

	cur.execute(sql)
	results = cur.fetchall()
	res = es216.search(index=RUMORLIST_INDEX, body=query_body,request_timeout=100)
	hits = res['hits']['hits']
	result = []

	for thing in results:
		dic = {}
		dic['title'] = thing[HOT_NEWS_TITLE]
		dic['publish_time'] = ts2date(float(thing[HOT_NEWS_IN_TIME]))
		dic['source'] = '新闻'
		dic['keyword'] = thing[HOT_NEWS_KEY_WORD]
		dic['ifruman'] = 0
		result.append(dic)
	result = sorted(result, key= lambda x:(x['publish_time']),reverse=True)[:10]   #只取时间最近的前十个
	resultes = []
	for hit in hits:
		dic = {}
		dic['title'] = hit['_source']['text']
		dic['publish_time'] = ts2date(hit['_source']['timestamp'])
		dic['source'] = '微博'
		dic['keyword'] = hit['_source']['keywords_string'].replace('&',' ')
		dic['ifruman'] = hit['_source']['rumor_label']
		dic['id'] = hit['_id']
		dic['type'] = hit['_type']
		resultes.append(dic)
	resultes = sorted(resultes, key= lambda x:(x['publish_time']),reverse=True)[:10]   #只取时间最近的前十个
	#print len(resultes)
	result.extend(resultes)
	#print len(result)

	return result

def hotspotandrumanUser(id,indextype,ifruman):
	indexbody = {'rumor_label':ifruman}
	es216.update(index=RUMORLIST_INDEX, doc_type=indextype, body={"doc":indexbody},id=id)#
	time.sleep(1)
	query_body = {"size":10,"query":{"term": {"_id":id}}}
	res = es216.search(index=RUMORLIST_INDEX, body=query_body,request_timeout=100)
	hits = res['hits']['hits']
	#print ifruman,hits[0]["_source"]["rumor_label"]
	if len(hits):
		if hits[0]["_source"]["rumor_label"] == ifruman:
			return True
		else:
			return False
	else:
		return False

def hotspot_source_distribute():
	query_body = {
		"query":{
			"match_all":{}
		}
	}
	result = {}
	count_sum = 0
	for source in TOPIC_ABOUT_DOCTYPE:
		mtype_count = es214.search(index=TOPIC_ABOUT_INDEX, doc_type=source,body=query_body)['hits']['total']
		result[source] = mtype_count
		count_sum += mtype_count
	for k,v in result.iteritems():
		result[k] = v*1.0/count_sum
	return result

def find_topic_num(en_name):   #用于搜索事件对应文本数，展示气泡图
	query_body = {"size":5000,"query":{"match_all": {}}}

	res = es216.search(index=en_name, body=query_body,request_timeout=100)
	hits = res['hits']['hits']

	return len(hits)

def hotspotbubbleChart():
	query_body = {"size":5000,"query":{"match_all": {}}}

	res = es216.search(index=RUMORLIST_INDEX, body=query_body,request_timeout=100)
	hits = res['hits']['hits']

	result = [[hit['_source']['comment'],hit['_source']['retweeted'],370601776,' '.join(hit['_source']['query_kwds'][:2]),hit['_source']['timestamp']] for hit in hits if hit['_source']['retweeted'] >= 30 and hit['_source']['comment'] >= 50 and hit['_source']['retweeted'] <= 1000 and hit['_source']['comment'] <= 1000]
	result = sorted(result,key= lambda x:(x[4]),reverse=True)[:20]   #提取前20个，按时间排序

	resultnew = [i[:4] for i in result]
	return resultnew

def rumorWarningNum():
	theday = '2016-11-26'
	dayago = ts2datetime(datetime2ts(theday) - 10*24*3600)
	#print theday,onemonthago
	datelist = []
	countlist = []
	query_body = {"size":2000,"query":{ "match": {"rumor_label" :1}}}
	for day in get_datelist(int(dayago.split('-')[0]),int(dayago.split('-')[1]),int(dayago.split('-')[2]),\
		int(theday.split('-')[0]),int(theday.split('-')[1]),int(theday.split('-')[2])):
		#print day
		
		res = es216.search(index=RUMORLIST_INDEX, doc_type=day, body=query_body,request_timeout=100)
		hits = res['hits']['hits']
		datelist.append(day)

		if len(hits):
			countlist.append(len(hits))
		else:
			countlist.append(0)

	result = {'date':datelist,'count':countlist}
	return result

def rumorWarning():
	theday = '2016-11-26'
	weekago = ts2datetime(datetime2ts(theday) - 6*24*3600)   #要记得少一天
	monthago = ts2datetime(datetime2ts(theday) - 29*24*3600)
	seasonago = ts2datetime(datetime2ts(theday) - 89*24*3600)
	weeknum = 0
	monthnum = 0
	seasonnum = 0
	query_body = {"size":2000,"query":{ "match": {"rumor_label" :1}}}

	for day in get_datelist(int(weekago.split('-')[0]),int(weekago.split('-')[1]),int(weekago.split('-')[2]),\
		int(theday.split('-')[0]),int(theday.split('-')[1]),int(theday.split('-')[2])):

		res = es216.search(index=RUMORLIST_INDEX, doc_type=day, body=query_body,request_timeout=100)
		hits = res['hits']['hits']
		
		weeknum += len(hits)

	for day in get_datelist(int(monthago.split('-')[0]),int(monthago.split('-')[1]),int(monthago.split('-')[2]),\
		int(theday.split('-')[0]),int(theday.split('-')[1]),int(theday.split('-')[2])):

		res = es216.search(index=RUMORLIST_INDEX, doc_type=day, body=query_body,request_timeout=100)
		hits = res['hits']['hits']
		
		monthnum += len(hits)

	for day in get_datelist(int(seasonago.split('-')[0]),int(seasonago.split('-')[1]),int(seasonago.split('-')[2]),\
		int(theday.split('-')[0]),int(theday.split('-')[1]),int(theday.split('-')[2])):

		res = es216.search(index=RUMORLIST_INDEX, doc_type=day, body=query_body,request_timeout=100)
		hits = res['hits']['hits']
		
		seasonnum += len(hits)

	return {'weeknum':weeknum,'monthnum':monthnum,'seasonnum':seasonnum}



if __name__=="__main__":
	rumorWarning()
