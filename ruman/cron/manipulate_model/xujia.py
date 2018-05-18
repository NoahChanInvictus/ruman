#-*-coding: utf-8-*-
#虚假消息操纵判定的模型
import sys
reload(sys)
sys.path.append("../../")
from config import *
from time_utils import *
from sql_utils import *
from elasticsearch import Elasticsearch

indexs=["flow_text_2016-11-07","flow_text_2016-11-08","flow_text_2016-11-11","flow_text_2016-11-12"\
	,"flow_text_2016-11-13","flow_text_2016-11-14","flow_text_2016-11-15","flow_text_2016-11-16"\
	,"flow_text_2016-11-17","flow_text_2016-11-18","flow_text_2016-11-19","flow_text_2016-11-20"\
	,"flow_text_2016-11-21","flow_text_2016-11-22","flow_text_2016-11-23","flow_text_2016-11-24"\
	,"flow_text_2016-11-25","flow_text_2016-11-26","flow_text_2016-11-27"]

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
			raise ValueError('bora输入错误')

def last_tradeday(a,theday,bora):   #输入bora=1向后一个的交易日，输入bora=-1向前一个的交易日
	tradedaydf = a[a['calendarDate'] == theday]
	dayindex = tradedaydf.index[0]
	if bora == 1:
		for i in range(dayindex + 1,dayindex + 30,1):
			if a.loc[i]['isOpen'] == 1:
				date = a.loc[i]['calendarDate']
				return date
				break
	elif bora == -1:
		for i in range(dayindex - 1,dayindex - 30,-1):
			if a.loc[i]['isOpen'] == 1:
				date = a.loc[i]['calendarDate']
				return date
				break
	else:
		raise ValueError('bora输入错误')
'''
def y_or_t(theday,num):   #num为1就是明天，num为-1就是昨天
	ts = datetime2ts(theday)
	if num == 1:
		return ts2datetime(ts + 24*3600)
	elif num == -1:
		return ts2datetime(ts - 24*3600)
	else:
		raise ValueError('num输入错误')'''


def xujia(mid):
	conn = default_db()
	cur = conn.cursor()
	es = Elasticsearch([{'host': '219.224.134.216', 'port': '9201'}])
	query_body = {"size":10,"query": {"bool": {"must": [{"match": {"mid": mid}}]}}}
	for index in indexs:
		res = es.search(index=index, doc_type="text",body=query_body, request_timeout=100)
		hits = res['hits']['hits']
		if len(hits):
			item = hits[0]["_source"]
			text = item['text']
			pubtime = ts2datetime(item['timestamp'])
			break
	if len(hits) == 0:
		raise ValueError('输入的mid有误')

	sql = "SELECT * FROM %s WHERE listed = 1" % (TABLE_STOCK_LIST)
	cur.execute(sql)
	results = cur.fetchall()
	codelist = []
	for result in results:
		if result[STOCK_LIST_STOCK_NAME][-1] == 'A':
			stock_name = result[STOCK_LIST_STOCK_NAME].replace('A','')
		else:
			stock_name = result[STOCK_LIST_STOCK_NAME]
		stock_id = result[STOCK_LIST_STOCK_ID]
		codelist.append([stock_id,stock_name])

	#print len(codelist)
	for code in codelist:
		if code[1] in text:
			print code[1]
			sql = "SELECT * FROM %s where %s = '%s'"%(TABLE_STOCK_LIST,STOCK_LIST_STOCK_ID,code[0])
			cur.execute(sql)
			result = cur.fetchone()
			stock_name = result[STOCK_LIST_STOCK_NAME]
			stock_id = result[STOCK_LIST_STOCK_ID]
			industry_name = result[STOCK_LIST_INDUSTRY_NAME]
			manipulate_type = 4
			ifend = 1
			marketplate = result[STOCK_LIST_PLATE]
			industry_code = result[STOCK_LIST_INDUSTRY_CODE]

			today = to_tradeday(a,pubtime,1)
			yesterday = last_tradeday(a,today,-1)
			tomorrow = last_tradeday(a,today,1)
			pricesql = "SELECT * FROM %s WHERE %s >= '%s' and %s <= '%s' and %s = '%s'" % (TABLE_MARKET_DAILY,MARKET_DATE,yesterday,MARKET_DATE,tomorrow,MARKET_STOCK_ID,stock_id)
			cur.execute(pricesql)
			priceresults = cur.fetchall()
			#print priceresults
			pricelist = [i[MARKET_PRICE] for i in priceresults]
			ratio1 = pricelist[1] / pricelist[0] - 1
			ratio2 = pricelist[2] / pricelist[1] - 1
			ifratio2 = 1
			ifinput = 0

			if ratio1 >= 0.05:
				start_date = today
				end_date = today
				increase_ratio = ratio1
				ifratio2 = 0
				ifinput = 1

			if ifratio2:
				if ratio2 >= 0.05:
					start_date = today
					end_date = tomorrow
					increase_ratio = ratio2
					ifinput = 1

			
			if ifinput:
				print stock_name,stock_id,start_date,end_date,increase_ratio,industry_name,manipulate_type,industry_code,ifend,marketplate,mid
				order = 'insert into ' + 'manipulate_day' + '(stock_name,stock_id,start_date,end_date,increase_ratio,industry_name,manipulate_type,industry_code,ifend,market_plate,mid)values\
				("%s","%s","%s","%s","%f","%s","%d","%s","%d","%s","%s")' % (stock_name,stock_id,start_date,end_date,increase_ratio,industry_name,manipulate_type,industry_code,ifend,marketplate,mid)
				try:
					cur.execute(order)
					conn.commit()
				except Exception, e:
					print e
					break

	#return text,pubtime
def get_ruman_mid():
	es = Elasticsearch([{'host': '219.224.134.216', 'port': '9201'}])
	query_body = {"size":100,"query": {"match": {"rumor_label" :1}}}
	res = es.search(index='rumor_hot_list', doc_type="2016-11-27",body=query_body, request_timeout=100)
	hits = res['hits']['hits']
	if len(hits):
		midlist = [i['_source']['mid'] for i in hits]
	return midlist

if __name__ == '__main__':
	#mid = 4041291346704466
	#xujia(mid)
	for mid in get_ruman_mid():
		xujia(mid)