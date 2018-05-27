# -*-coding:utf-8-*-

import json
from elasticsearch import Elasticsearch

es_text = Elasticsearch("10.128.55.75")
es_bci = Elasticsearch("10.128.55.70")

def query_body(message_type, uid):
    query_body = {
	"query":{
	    "filtered":{
		"filter":{
		    "bool":{
			"must":[
			    {"term":{"message_type":message_type}},
			    {"term":{"uid": uid}}
			]
		    }
		}
	    }
	},
        "size": 1000
    }

    return query_body

def bci_detail(date, uid):
    bci_index = "bci_" + date.replace('-','')
    try:
        bci_result = es_bci.get(index=bci_index, doc_type="bci", id=uid)['_source']
    except:
        bci_result = dict()

    try:
        origin_retweeted = json.loads(bci_result.get("origin_weibo_retweeted_detail", []))
    except:
        origin_retweeted = []
    origin_weibo_retweeted_brust_average = bci_result.get("origin_weibo_retweeted_brust_average", 0) # 爆发数
    try:
        origin_comment = json.loads(bci_result.get("origin_weibo_comment_detail", []))
    except:
	    origin_comment = []
    origin_weibo_comment_brust_average = bci_result.get("origin_weibo_comment_brust_average", 0)
    try:
        retweeted_retweeted = json.loads(bci_result.get("retweeted_weibo_retweeted_detail", []))
    except:
	    retweeted_retweeted = []
    retweeted_weibo_retweeted_brust_average = bci_result.get('retweeted_weibo_retweeted_brust_average', 0)
    try:
        retweeted_comment = json.loads(bci_result.get("retweeted_weibo_comment_detail", []))
    except:
        retweeted_comment = []
    retweeted_weibo_comment_brust_average = bci_result.get('retweeted_weibo_comment_brust_average', 0)


    origin_query = query_body(1, uid)
    text_index = "flow_text_" + date
    origin_text = es_text.search(index=text_index, doc_type="text", body=origin_query)["hits"]["hits"]
    #print origin_text
    retweeted_query = query_body(3, uid)
    retweeted_text = es_text.search(index=text_index, doc_type="text", body=retweeted_query)["hits"]["hits"]

    origin_weibo_number = len(origin_text) # 1
    retweeted_weibo_number = len(retweeted_text) #2
 
    retweet_total_number = 0 # 转发总数
    comment_total_number = 0 # 评论总数
    origin_retweet_total_number = 0 # 原创被转发总数
    origin_comment_total_number = 0 # 原创被评论总数
    retweet_retweet_total_number = 0 # 转发被转发总数
    retweet_comment_total_number = 0 # 转发被评论总数
    origin_retweet_average_number = 0 # 原创被转发平均数
    origin_comment_average_number = 0 # 原创被评论平均数
    retweet_retweet_average_number = 0 # 转发被转发平均数
    retweet_comment_average_number = 0 # 转发被评论平均数
    origin_retweet_top_number = 0 # 原创被转发最高
    origin_comment_top_number = 0 # 原创被评论最高
    retweet_retweet_top_number = 0 # 转发被转发最高
    retweet_comment_top_number = 0 # 转发被评论最高
    for item in origin_text:
        retweet_total_number += item['_source'].get('retweeted', 0)
        comment_total_number += item['_source'].get('comment', 0)
        origin_retweet_total_number += item['_source'].get('retweeted', 0)
        origin_comment_total_number += item['_source'].get('comment', 0)
        if origin_retweet_top_number < item['_source'].get('retweeted', 0):
	        origin_retweet_top_number = item['_source'].get('retweeted', 0)
        if origin_comment_top_number < item['_source'].get('comment', 0):
            origin_comment_top_number = item['_source'].get('comment', 0)
    for item in retweeted_text:
        retweet_total_number += item['_source'].get('retweeted', 0)
        comment_total_number += item['_source'].get('comment', 0)
        retweet_retweet_total_number += item['_source'].get('retweeted', 0)
        retweet_comment_total_number += item['_source'].get('comment', 0)
        if retweet_retweet_top_number < item['_source'].get('retweeted', 0):
            retweeet_retweet_top_number = item['_source'].get('retweeted', 0)
        if retweet_comment_top_number < item['_source'].get('comment', 0):
            retweet_comment_top_number = item['_source'].get('comment', 0)
    try:
        average_retweet_number = retweet_total_number/(origin_weibo_number+retweeted_weibo_number) # 平均转发数
    except:
        average_retweet_number = 0
    try:
	average_comment_number = comment_total_number/(origin_weibo_number+retweeted_weibo_number) # 平均评论数
    except:
	average_comment_number = 0

    try:
        origin_retweet_average_number = origin_retweet_total_number/origin_weibo_number
    except:
	    origin_retweet_average_number = 0	
    try:
        origin_comment_average_number = origin_comment_total_number/origin_weibo_number
    except:
	    origin_comment_average_number = 0	
    try:
        retweet_retweet_average_number = retweet_retweet_total_number/retweeted_weibo_number
    except:
	    retweet_retweet_average_number = 0	
    try:
        retweet_comment_average_number = retweet_comment_total_number/retweeted_weibo_number
    except:
	    retweet_comment_average_number = 0

    result = dict()
    result["origin_weibo_number"] = origin_weibo_number	
    result["retweeted_weibo_number"] = retweeted_weibo_number
    result["origin_weibo_retweeted_total_number"] = origin_retweet_total_number
    result["origin_weibo_comment_total_number"] = origin_comment_total_number
    result["retweeted_weibo_retweeted_total_number"] = retweet_retweet_total_number
    result["retweeted_weibo_comment_total_number"] = retweet_comment_total_number
    result["origin_weibo_retweeted_average_number"] = origin_retweet_average_number
    result["origin_weibo_comment_average_number"] = origin_comment_average_number
    result["retweeted_weibo_retweeted_average_number"] = retweet_retweet_average_number
    result["retweeted_weibo_comment_average_number"] = retweet_comment_average_number
    result["origin_weibo_retweeted_top_number"] = origin_retweet_top_number
    result["origin_weibo_comment_top_number"] = origin_comment_top_number
    result["retweeted_weibo_retweeted_top_number"] = retweet_retweet_top_number
    result["retweeted_weibo_comment_top_number"] = retweet_comment_top_number
    result["origin_weibo_comment_brust_average"] = origin_weibo_comment_brust_average
    result["origin_weibo_retweeted_brust_average"] = origin_weibo_retweeted_brust_average
    result["retweeted_weibo_comment_brust_average"] = retweeted_weibo_comment_brust_average
    result["retweeted_weibo_retweeted_brust_average"] = retweeted_weibo_retweeted_brust_average
    result['user_index'] = bci_result.get('user_index', 0)

    return result

if __name__ == "__main__":
    print bci_detail("2016-03-28", "1742566624")
