# -*- coding: UTF-8 -*-
import csv
import time
import json
from collections import Counter
from cron_text_attribute import test_cron_text_attribute
from user_portrait.parameter import DAY, WEEK,MAX_VALUE
from user_portrait.time_utils import ts2datetime, datetime2ts
from user_portrait.global_utils import es_flow_text, flow_text_index_name_pre, flow_text_index_type

WEEK = 7

#read blacklist user list
def read_black_list():
    f = open('/home/ubuntu8/huxiaoqian/user_portrait/user_portrait/cron/text_attribute/black_list.csv', 'rb')
    reader = csv.reader(f)
    item_list = []
    for item in reader:
        if len(item)!= 10:
            item = item[:10]
        item_list.append(item)
    return iten_list


#test: read user weibo
def read_user_weibo():
    user_weibo_dict = dict()
    csvfile = open('/home/ubuntu8/huxiaoqian/user_portrait/user_portrait/cron/text_attribute/uid_text_0728.csv', 'rb')
    reader = csv.reader(csvfile)
    count = 0
    for line in reader:
        count += 1
        
        if count>=10:
            break
        
        weibo = dict()
        user = line[0]
        weibo['uname'] = 'unknown'
        weibo['text'] = line[1].decode('utf-8')
        weibo['online_pattern'] = 'weibo.com'
        try:
            user_weibo_dict[user].append(weibo)
        except:
            user_weibo_dict[user] = [weibo]
    print 'all count:', len(user_weibo_dict)
    
    iter_count = 0
    iter_weibo_dict = {}
    start_ts = time.time()
    for user in user_weibo_dict:
        iter_count += 1
        iter_weibo_dict[user] = user_weibo_dict[user]
        if iter_count % 100==0:
            status = test_cron_text_attribute(iter_weibo_dict)
            iter_weibo_dict = {}

    if iter_weibo_dict:
        status = test_cron_text_attribute(iter_weibo_dict)
    end_ts = time.time()
    
    print 'all end count:', iter_count
    print 'time_segment:', end_ts - start_ts
    

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
    now_date_ts = datetime2ts(ts2datetime(now_ts))
    now_date_ts = datetime2ts('2013-09-08')
    start_date_ts = now_date_ts - DAY * WEEK
    for i in range(0,WEEK):
        iter_date_ts = start_date_ts + DAY * i
        flow_text_index_date = ts2datetime(iter_date_ts)
        flow_text_index_name = flow_text_index_name_pre + flow_text_index_date
        print flow_text_index_name
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
            
    return  word_dict,weibo_list

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
    now_date_ts = datetime2ts(ts2datetime(now_ts))
    now_date_ts = datetime2ts('2013-09-08')
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
            
    return  word_dict,weibo_list        

if __name__=='__main__':
    read_user_weibo()
    #word_dict,weibo_list = read_flow_text(['2098261223','2991483613'])
    
