# -*- coding: UTF-8 -*-
import json
from elasticsearch import Elasticsearch
from elasticsearch import helpers
#from global_config import es_flow_text as es
from global_config import weibo_es as es
from flow_text_mappings import get_graph_mappings
def write():
	a = {
		"_index": "flow_text_2013-09-02",
		"_type": "text",
		"_id": "3618063561370373",
		"_version": 2,
		"_score": 1,
		"_source": {
			"ip": "111.226.251.248",
			"uid": "1682591580",
			"sentiment": "0",
			"root_uid": "1865583287",
			"text": "转发微博",
			"mid": "3618063561370373",
			"keywords_string": "发微",
			"geo": "中国&河北&廊坊",
			"directed_uid": 1865583287,
			"timestamp": 1378097036,
			"keywords_dict": "{\"aaa\": 1}",
			"directed_uname": "",
			"message_type": 3,
			"root_mid": "3617999674476654",
			"sensitive_words_dict": "{}",
			"sensitive_words_string": "",
		}
	}
	a = json.dumps(a)
	f = open('/home/ubuntu8/jiangln/863/a.txt','w')
	f.write(a)
	f.close()
def gexf2es(indexname, value):
	bulk_action = []
	action = {"index":{"_id":1}}
	#print value
	source = json.dumps(value)
	bulk_action.extend([action,source])
	es.bulk(bulk_action, index=indexname, doc_type='text', timeout=600)
def save_long_gexf(topic, identifyDate, identifyWindow, identifyGexf):
	index_name = topic+'_gexffile'
	
	get_graph_mappings(index_name)
	
	bulk_action = []
	#action = {"index":{"_id":999}}
	source = json.dumps(identifyGexf)
	action = {
    			#"index":{"_id":999},
				#"_source":{
				"name":str(identifyDate)+str(identifyWindow),
				"gexf":source,
				"date":str(identifyDate),
				"window":identifyWindow,
				#}
			}
	bulk_action.extend([action,])
	print bulk_action
	auto_id = [str(i)for i in str(identifyDate)+str(identifyWindow) if i.isdigit()]
	auto_id = ''.join(auto_id)
	#es.bulk(bulk_action, index=index_name, doc_type='text', timeout=600)
	es.index(index=index_name, doc_type='text', id=auto_id, body=action)

def read_long_gexf(topic, identifyDate, identifyWindow):
	name = str(identifyDate)+str(identifyWindow)
	query_body = {
		#"term":{"date":identifyDate}
		"query":{"match_phrase":{"name":name}}
	}
	index_name = topic+'_gexffile'
	try:
		res = es.search(index=index_name, body=query_body)['hits']['hits']	
	except:
		return []
	print es,index_name,query_body
	if len(res) > 0:
		#print '!!!!'
		#print type(json.loads(res[0]['_source']['gexf']))
		return res[0]['_source']['gexf']
	else:
		return []
	#print res
	#res = es.get(index=indexname, doc_type='text',)



def es2gexf(indexname):
	try:
		#result = es.search(index = indexname, doc_type = 'text', body = {})
		res = es.get(index=indexname, doc_type='text', id=1)
	except:
		return []
	#print res
	return res['_source']
	#es_search_weibos = weibo_es.search(index=topic, doc_type=weibo_index_type, body=query_body)['hits']['hits']

def txt2es(filename,name ):
	weibo = []
	f = open(filename,'r')
	i = 0
	bulk_action = []
	for line0 in f:
		line0 = json.loads(line0)
		#print line0[-1]
		count = 0
		for line in line0:
			#weibo.append(line)
			#print line['_source']['mid'],type(line['_source']['mid'])
			action = {"index":{"_id":line['_source']['mid']}}
			source = line['_source']
			count += 1
			bulk_action.extend([action,source])
			if count % 1000 == 0:
				print es.bulk(bulk_action, index=name, doc_type='text', timeout=600)
				bulk_action = []
				print count
				#print len(bulk_action)
			#print len(bulk_action)
		#print bulk_action

	#print es
	#print name,type(name),name.decode('utf-8')
	#print es.bulk(bulk_action, index=name, doc_type='text', timeout=600)

if __name__ == '__main__':
	#write()
	#txt2es('/home/ubuntu2/chenyz/anguancenter/socialconsume/cron/result2.txt','aoyunhui')
	#print es.delete(index='aoyunhui',doc_type='text',id='3995843252444302')
	# es.index(index='topi-cs',doc_type='text',id='14676d48000_1470900837_aoyunhui_jln',body={'name':'奥运会','en_name':'aoyunhui','end_ts':'1470900837',\
	# 											'start_ts':'1467648000','submit_user':'jln','comput_status':0})
	#es.index(index='topics',doc_type='text',id='1467648000_1470900837_laohu_jln',body={'name':'老虎','en_name':'laohu','end_ts':'1470900837',\
												#'start_ts':'1467648000','submit_user':'jln','comput_status':0})
	query_body = {
	    'query':{
	        'filtered':{
	            'filter':{
	                'term':{
	                    'comput_status':0
	                }
	            }
	        }
	    }
	}
	es.delete(index='topics',doc_type='测试',body=query_body)
	#es.delete(index='topics',doc_type='text',id='AVZ4jhDGhhg-Qh1aWtw4')
	#print es.get(index='topics',doc_type='text',id='AVZ4jhC-hhg-Qh1aWtw3',_source=False,fields=['name'])
	# es.update(index='topics',doc_type='text',id='14676d48000_1470900837_aoyunhui_jln',body={'doc':{'comput_status':1}})
	# es.update(index='topics',doc_type='text',id='1467648000_1470900837_laohu_jln',body={'doc':{'comput_status':1}})
	