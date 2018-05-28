# -*- coding=utf-8 -*-
'''
date: 2015-12-08
operator: hxq
goal: save a week all weibo
'''
import IP
import re
import csv
import sys
import zmq
import time
import json
import math
import redis
from openpyxl import load_workbook
from elasticsearch import Elasticsearch
from datetime import datetime
from triple_sentiment_classifier import triple_classifier
from DFA_filter import createWordTree,searchWord 

reload(sys)
sys.path.append('../../')
from time_utils import ts2datetime, datetime2ts
from global_config import ZMQ_VENT_PORT_FLOW5, ZMQ_CTRL_VENT_PORT_FLOW5,\
                          ZMQ_VENT_HOST_FLOW1, ZMQ_CTRL_HOST_FLOW1
from global_utils import es_user_profile as es_profile
from global_utils import es_flow_text as es
from global_utils import profile_index_name, profile_index_type,\
                         flow_text_index_name_pre, flow_text_index_type
from global_utils import black_words, uname2uid_redis
from global_config import UNAME2UID_HASH as uname2uid_hash
from parameter import RUN_TYPE, RUN_TEST_TIME, DAY,sensitive_score_dict
from flow_text_mappings import get_mappings
from global_config import SENSITIVE_WORDS_PATH
from global_utils import R_CLUSTER_FLOW2 as r_cluster
from global_utils import R_ADMIN as r_sensitive

start_date = '2016-03-03'
DFA = createWordTree()

#ip to city 
#input: ip
#output: 中国&河北&石家庄
def ip2city(ip):
    try:
        city = IP.find(str(ip))
        if city:
            city = city.encode('utf-8')
        else:
            return None
    except Exception, e:
        return None
    city_list = city.split('\t')
    city = '&'.join(city_list)
    return city


#get uid from uname by es_user_profile
#input: uname
#output: uid
def uname2uid(uname):
    try:
        uid = uname2uid_redis.hget(uname2uid_hash, uname)
    except:
        uid = None
    return uid

#abandon
#get uname from uid by es_user_profile
#input: uid
#output：uname
'''
def uid2uname(uid):
    try:
        search_result = es_profile.search(index=profile_index_name, doc_type=profile_index_type, body={'query':{'match':{'uid': uid}}})['hits']['hits']
        search_result = search_result[0]
        uname = search_result['_source']['nick_name']
    except:
        uname = ''
    return uname
'''
#for retweet message: get directed retweet uname and uid
#input: text, root_uid
#output: directed retweet uid and uname
def get_directed_retweet(text, root_uid):
    if isinstance(text, str):
        text = text.decode('utf-8', 'ignore')
    RE = re.compile(u'//@([a-zA-Z-_⺀-⺙⺛-⻳⼀-⿕々〇〡-〩〸-〺〻㐀-䶵一-鿃豈-鶴侮-頻並-龎]+):', re.UNICODE)
    repost_chains = RE.findall(text)
    if repost_chains != []:
        directed_uname = repost_chains[0]
        directed_uid = uname2uid(directed_uname)
        if not directed_uid:
            directed_uid = root_uid
            directed_uname = ''
    else:
        directed_uid = root_uid
        directed_uname = ''

    return directed_uid, directed_uname


#for comment message: get directed comment uname and uid
#input: text, root_uid
#output: directed comment uid and uname
def get_directed_comment(text, root_uid):
    if isinstance(text, str):
        text = text.decode('utf-8', 'ignore')
    RE = re.compile(u'回复@([a-zA-Z-_⺀-⺙⺛-⻳⼀-⿕々〇〡-〩〸-〺〻㐀-䶵一-鿃豈-鶴侮-頻並-龎]+):', re.UNICODE)
    comment_chains = RE.findall(text)
    if comment_chains != []:
        directed_uname = comment_chains[0]
        directed_uid = uname2uid(directed_uname)
        if not directed_uid:
            directed_uid = root_uid
            directed_uname = ''
    else:
        directed_uid = root_uid
        directed_uname = ''

    return directed_uid, directed_uname


#get weibo keywords_dict and keywords_string
#write in version: 15-12-08
#input: keyowrds_list
#output: keywords_dict, keywords_string
def get_weibo_keywords(keywords_list):
    keywords_dict = {}
    keywords_string = ''
    filter_keywords_set = set()
    for word in keywords_list:
        if word not in black_words:
            try:
                keywords_dict[word] += 1
            except:
                keywords_dict[word] = 1
            filter_keywords_set.add(word)
    keywords_string = '&'.join(list(filter_keywords_set))

    return keywords_dict, keywords_string


#use to expand index body to bulk action
#input: weibo_item
#output: action {'index':{'_id': mid}}, xdata {'mid':x, 'text':y,...}
def expand_index_action(item):
    index_body = {}
    index_body['uid'] = str(item['uid'])
    index_body['text'] = item['text']
    index_body['mid'] = str(item['mid'])
    index_body['sentiment'] = str(item['sentiment'])
    index_body['timestamp'] = int(item['timestamp'])
    index_body['message_type'] = item['message_type']
    index_body['keywords_dict'] = item['keywords_dict']
    index_body['keywords_string'] = item['keywords_string']
    index_body['sensitive_words_string'] = item['sensitive_words_string']
    index_body['sensitive_words_dict'] = item['sensitive_words_dict']
    sensitive_words_dict = json.loads(item['sensitive_words_dict'])
    if sensitive_words_dict:
        score = 0
        for k,v in sensitive_words_dict.iteritems():
            tmp_stage = r_sensitive.hget("sensitive_words", k)
            if tmp_stage:
                score += v*sensitive_score_dict[str(tmp_stage)]
        index_body['sensitive'] = score
    if item['message_type'] == 3:
        #for retweet message: get directed retweet uname and uid 
        directed_uid, directed_uname = get_directed_retweet(item['text'], item['root_uid'])
        if directed_uid:
            index_body['directed_uid'] = int(directed_uid)
        else:
            #index_body['directed_uid'] = directed_uid
            index_body['directed_uid'] = 0
        index_body['directed_uname'] = directed_uname
        index_body['root_mid'] = str(item['root_mid'])
        index_body['root_uid'] = str(item['root_uid'])
    elif item['message_type'] == 2:
        #for comment meesage: get directed comment uname and uid
        directed_uid, directed_uname = get_directed_comment(item['text'], item['root_uid'])
        if directed_uid:
            index_body['directed_uid'] = int(directed_uid)
        else:
            #index_body['directed_uid'] = directed_uid
            index_body['directed_uid'] = 0
        index_body['directed_uname'] = directed_uname
        index_body['root_mid'] = str(item['root_mid'])
        index_body['root_uid'] = str(item['root_uid'])

    ip = item['send_ip']
    index_body['ip'] = ip
    index_body['geo'] = ip2city(ip) #output: 中国&河北&石家庄
    
    action = {'index': {'_id': index_body['mid']}}
    xdata = index_body
    return action, xdata


if __name__ == "__main__":
    """
     receive weibo
    """
    context = zmq.Context()

    receiver = context.socket(zmq.PULL)
    receiver.connect('tcp://%s:%s' %(ZMQ_VENT_HOST_FLOW1, ZMQ_VENT_PORT_FLOW5))

    controller = context.socket(zmq.SUB)
    controller.connect("tcp://%s:%s" %(ZMQ_VENT_HOST_FLOW1, ZMQ_CTRL_VENT_PORT_FLOW5))

    count = 0
    read_count = 0
    tb = time.time()
    ts = tb
    bulk_action = []
    now_date = ts2datetime(tb)
    index_name_pre = flow_text_index_name_pre
    index_type = flow_text_index_type
    now_index_name_date = ts2datetime(datetime2ts(start_date) - DAY)
    action = []
    xdata = []
    class_ts = time.time()
    while 1:

        item = receiver.recv_json()
        if not item:
            continue 

        if int(item['sp_type']) == 1:
            read_count += 1
            text = item['text']

            #add sentiment field to weibo
            sentiment, keywords_list  = triple_classifier(item)
            item['sentiment'] = str(sentiment)
            #add key words to weibo
            keywords_dict, keywords_string = get_weibo_keywords(keywords_list)
            item['keywords_dict'] = json.dumps(keywords_dict) # use to compute
            item['keywords_string'] = keywords_string         # use to search

            sensitive_words_dict = searchWord(text.encode('utf-8', 'ignore'), DFA)
            if sensitive_words_dict:
                item['sensitive_words_string'] = "&".join(sensitive_words_dict.keys())
                item['sensitive_words_dict'] = json.dumps(sensitive_words_dict)
            else:
                item['sensitive_words_string'] = ""
                item['sensitive_words_dict'] = json.dumps({})

            timestamp = item['timestamp']
            date = ts2datetime(timestamp)
            ts = datetime2ts(date)
            if sensitive_words_dict:
                print sensitive_words_dict.keys()[0]
                sensitive_count_string = r_cluster.hget('sensitive_'+str(ts), str(uid))
                if sensitive_count_string: #redis取空
                    sensitive_count_dict = json.loads(sensitive_count_string)
                    for word in sensitive_words_dict.keys():
                        if sensitive_count_dict.has_key(word):
                            sensitive_count_dict[word] += sensitive_words_dict[word]
                        else:
                            sensitive_count_dict[word] = sensitive_words_dict[word]
                    r_cluster.hset('sensitive_'+str(ts), str(uid), json.dumps(sensitive_count_dict))
                else:
                    r_cluster.hset('sensitive_'+str(ts), str(uid), json.dumps(sensitive_words_dict))

            #identify whether to mapping new es
            weibo_timestamp = item['timestamp']
            should_index_name_date = ts2datetime(weibo_timestamp)
            if should_index_name_date != now_index_name_date:
                if action != [] and xdata != []:
                    index_name = index_name_pre + now_index_name_date
                    if bulk_action:
                        es.bulk(bulk_action, index=index_name, doc_type=index_type, timeout=60)
                    bulk_action = []
                    count = 0
                    now_index_name_date = should_index_name_date
                    index_name = index_name_pre + now_index_name_date
                    get_mappings(index_name)

            # save
            action, xdata = expand_index_action(item)
            bulk_action.extend([action, xdata])
            count += 1
        
        if count % 1000 == 0 and count != 0:
            index_name = index_name_pre + now_index_name_date
            if bulk_action:
                es.bulk(bulk_action, index=index_name, doc_type=index_type, timeout=60)
            bulk_action = []
            count = 0
            class_te = time.time()
            class_ts = class_te

        #run_type
        if read_count % 10000 == 0 and RUN_TYPE == 0:
            te = time.time()
            print '[%s] cal speed: %s sec/per %s' % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), te - ts, 10000) 
            if read_count % 100000 == 0:
                print '[%s] total cal %s, cost %s sec [avg %s per/sec]' % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), read_count, te - tb, read_count / (te - tb)) 
            ts = te
