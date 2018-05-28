# -*- coding: UTF-8 -*-
import csv
import sys
import time
import json
from collections import Counter

sys.path.append('../../')
from parameter import DAY, WEEK,MAX_VALUE
from parameter import RUN_TYPE, RUN_TEST_TIME
from time_utils import ts2datetime, datetime2ts
from global_utils import es_flow_text, flow_text_index_name_pre, flow_text_index_type
WEEK = 7
def read_flow_text_sentiment(uid_list):
    '''
        读取用户微博（返回结果有微博情绪标签）:
        输入数据：uid_list（字符串型列表）
        输出数据：word_dict（用户分词结果字典）,weibo_list（用户微博列表）
        word_dict示例：{uid1:{'w1':f1,'w2':f2...}...}
        weibo_list示例：[[uid1,text1,s1,ts1],[uid2,text2,s2,ts2],...]（每一条记录对应四个值：uid、text、sentiment、timestamp）
    '''
    word_dict = dict()#词频字典
    weibo_list = []#微博列表
    now_ts = time.time()
    #run_type
    if RUN_TYPE == 1:
        now_date_ts = datetime2ts(ts2datetime(now_ts))
    else:
        now_date_ts = datetime2ts(RUN_TEST_TIME)
    start_date_ts = now_date_ts - DAY * WEEK
    for i in range(0,WEEK):
        iter_date_ts = start_date_ts + DAY * i
        flow_text_index_date = ts2datetime(iter_date_ts)
        flow_text_index_name = flow_text_index_name_pre + flow_text_index_date
        try:
            flow_text_exist = es_flow_text.search(index=flow_text_index_name, doc_type=flow_text_index_type,\
                    body={'query':{'filtered':{'filter':{'terms':{'uid': uid_list}}}}, 'size': MAX_VALUE}, _source=False,  fields=['text','uid','sentiment','keywords_dict','timestamp'])['hits']['hits']
        except:
            flow_text_exist = []

        for flow_text_item in flow_text_exist:
            uid = flow_text_item['fields']['uid'][0].encode('utf-8')
            text = flow_text_item['fields']['text'][0].encode('utf-8')
            sentiment = int(flow_text_item['fields']['sentiment'][0])
            ts = flow_text_item['fields']['timestamp'][0]
            keywords_dict = json.loads(flow_text_item['fields']['keywords_dict'][0])
            keywords_dict = json.dumps(keywords_dict, encoding="UTF-8", ensure_ascii=False)
            keywords_dict = eval(keywords_dict)

            if word_dict.has_key(uid):
                item_dict = Counter(word_dict[uid])
                keywords_dict = Counter(keywords_dict)
                item_dict = dict(item_dict + keywords_dict)
                word_dict[uid] = item_dict
            else:
                word_dict[uid] = keywords_dict

            weibo_list.append([uid,text,sentiment,ts])
            
    return  word_dict,weibo_list, start_date_ts

def read_flow_text(uid_list):
    '''
        读取用户微博（返回结果没有微博情绪标签）:
        输入数据：uid_list（字符串型列表）
        输出数据：word_dict（用户分词结果字典）,weibo_list（用户微博列表）
        word_dict示例：{uid1:{'w1':f1,'w2':f2...}...}
        weibo_list示例：[[uid1,text1,ts1],[uid2,text2,ts2],...]（每一条记录对应三个值：uid、text、timestamp）
    '''
    word_dict = dict()#词频字典
    weibo_list = []#微博列表
    now_ts = time.time()
    #run_type
    if RUN_TYPE = 1:
        now_date_ts = datetime2ts(ts2datetime(now_ts))
    else:
        now_date_ts = datetime2ts(RUN_TEST_TIME)

    start_date_ts = now_date_ts - DAY * WEEK
    for i in range(0,WEEK):
        iter_date_ts = start_date_ts + DAY * i
        flow_text_index_date = ts2datetime(iter_date_ts)
        flow_text_index_name = flow_text_index_name_pre + flow_text_index_date
        print flow_text_index_name
        try:
            flow_text_exist = es_flow_text.search(index=flow_text_index_name, doc_type=flow_text_index_type,\
                    body={'query':{'filtered':{'filter':{'terms':{'uid': uid_list}}}}, 'size': MAX_VALUE}, _source=False,  fields=['text','uid','keywords_dict','timestamp'])['hits']['hits']
        except:
            flow_text_exist = []

        for flow_text_item in flow_text_exist:
            uid = flow_text_item['fields']['uid'][0].encode('utf-8')
            text = flow_text_item['fields']['text'][0].encode('utf-8')
            ts = flow_text_item['fields']['timestamp'][0]
            keywords_dict = json.loads(flow_text_item['fields']['keywords_dict'][0])
            keywords_dict = json.dumps(keywords_dict, encoding="UTF-8", ensure_ascii=False)
            keywords_dict = eval(keywords_dict)

            if word_dict.has_key(uid):
                item_dict = Counter(word_dict[uid])
                keywords_dict = Counter(keywords_dict)
                item_dict = dict(item_dict + keywords_dict)
                word_dict[uid] = item_dict
            else:
                word_dict[uid] = keywords_dict

            weibo_list.append([uid,text,ts])
            
    return  word_dict,weibo_list, start_date_ts

if __name__=='__main__':
    word_dict,weibo_list = read_flow_text(['2098261223','2991483613'])
    
