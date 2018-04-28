#!/usr/bin/env python
# encoding: utf-8
import sys
reload(sys)
sys.path.append('../')
from config import ES_HOST,ES_PORT
import requests
import json
import time
import elasticsearch
from elasticsearch import Elasticsearch

es = Elasticsearch([{'host':ES_HOST,'port':ES_PORT}])

def eastMoney(theday):
	#today = time.strftime("%Y-%m-%d",time.localtime(int(time.time())))
	today = theday
	# today="2018-03-19"
	todayUrl = "http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get?type=DZJYXQ&token=70f12f2f4f091e459a279469fe49eca5&st=SECUCODE&p=%s&ps=5000&filter=(Stype='EQA')(TDATE=^{}^)".format(today)

	for offset in range(1,11):
		# print(todayUrl%offset)
		r = requests.get(todayUrl%offset)
		# print(r.text)
		j = json.loads(r.text)
		if j:
			for each in j:
				date = each['TDATE'].replace('T00:00:00','')
				stock_id = each['SECUCODE']
				stock_name = each['SNAME']
				increase = each['RCHANGE']
				closing_price_today = each['CPRICE']
				transaction_price = each['PRICE']
				Discount_ratio = each['Zyl']
				transaction_number = each['TVOL']
				transaction_amount = each['TVAL']
				Buyer = each['BUYERNAME']
				Seller = each['SALESNAME']

				dict = {'date':date, 'stock_id':stock_id, 'increase':increase,\
						 'closing_price_today':closing_price_today, 'transaction_price':transaction_price,\
						  'Discount_ratio':Discount_ratio, 'transaction_number':transaction_number,\
						   'transaction_amount':transaction_amount, 'Buyer':Buyer, 'Seller':Seller}
				es.index(index='east_money',doc_type='type1',body=dict)

				# with open(today + '.json','a+') as f:
				# 	f.write(json.dumps(dict,ensure_ascii=False) + '\n')
		else:
			break
