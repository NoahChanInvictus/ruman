# -*- coding: UTF-8 -*-
'''
search attribute : attention, follower, mention, location, activity
'''
import sys
import csv
import time
import json
import redis
from global_utils_ch import es_user_portrait,es_flow_text,portrait_index_name,portrait_index_type,\
                         flow_text_index_name_pre,flow_text_index_type,MAX_VALUE

#根据uid查询用户属性
def search_profile(uid_list):
    '''
    输入：uid列表
    '''
    es_profile_results = es_user_portrait.mget(index=portrait_index_name, doc_type=portrait_index_type, body={'ids':uid_list})['docs']

    result_list = dict()
    for i in range(len(es_profile_results)):
        item = es_profile_results[i]
        uid = item['_id'].encode('utf-8')
        if item['found']:#有数据
            source = item['_source']
            topic = source['topic_string']
        else:
            topic = ''        

        result_list[uid] = topic
       
    return result_list

#根据uid和date查询用户发布的文本，此接口表示每条微博的情绪已经计算完成
def search_text_sentiment(uid_list, date, result):
    '''
    输入：uid列表、时间
    输出：情绪list、文本list
    '''
    nest_body_list = [{'match':{'uid':k}} for k in uid_list]
    query = [{'bool':{'should': nest_body_list}}]
    try:
        portrait_result = es_flow_text.search(index=flow_text_index_name_pre+date, doc_type=flow_text_index_type, body={'query':{'bool':{'must':query}}, 'size':MAX_VALUE})['hits']['hits']
    except:
        portrait_result = []

    for item in portrait_result:
        source = item['_source']
        uid = source['uid'].encode('utf-8')
        text = source['text'].encode('utf-8')
        sentiment = source['sentiment']
        timestamp = source['timestamp']
        result.append([uid,text,sentiment,timestamp])
       
    return result  

#根据uid和date查询用户发布的文本，此接口表示没有计算每条微博的情绪或者情绪计算不准确
def search_text(uid_list, date, result):
    '''
    输入：uid列表、时间
    输出：情绪list、文本list
    '''
    nest_body_list = [{'match':{'uid':k}} for k in uid_list]
    query = [{'bool':{'should': nest_body_list}}]
    try:
        portrait_result = es_flow_text.search(index=flow_text_index_name_pre+date, doc_type=flow_text_index_type, body={'query':{'bool':{'must':query}}, 'size':MAX_VALUE})['hits']['hits']
    except:
        portrait_result = []

    for item in portrait_result:
        source = item['_source']
        uid = source['uid'].encode('utf-8')
        text = source['text'].encode('utf-8')
        timestamp = source['timestamp']
        result.append([uid,text,timestamp])
       
    return result 
