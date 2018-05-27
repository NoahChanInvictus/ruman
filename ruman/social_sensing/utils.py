# -*- coding:utf-8 -*-

import sys
import json
import math
import time
from get_task_detail import get_task_detail_2
from full_text_serach import get_origin_weibo_detail, get_retweet_weibo_detail, get_positive_weibo_detail
from ruman.global_utils import es_user_profile as es_profile
from ruman.global_utils import es_user_portrait as es
from ruman.global_utils import es_flow_text as es_text
from ruman.global_utils import profile_index_name, profile_index_type, portrait_index_name, portrait_index_type, \
                         flow_text_index_name_pre, flow_text_index_type
from ruman.parameter import INDEX_MANAGE_SOCIAL_SENSING as index_manage_sensing_task
from ruman.parameter import DOC_TYPE_MANAGE_SOCIAL_SENSING as task_doc_type
from ruman.parameter import DETAIL_SOCIAL_SENSING as index_sensing_task
from ruman.parameter import DAY
from ruman.time_utils import ts2datetime, datetime2ts

def get_warning_detail(task_name, ts, user):
    results = dict()
    index_name = task_name # 可能的index-name

    results = get_task_detail_2(task_name, ts, user)


    return results

# 获得一段时间内的文本，按序排列
def get_text_detail(task_name, ts, text_type, user, order, size=100):
    results = []
    _id = user + '-' + task_name
    task_detail = es.get(index=index_manage_sensing_task, doc_type=task_doc_type, id=_id)["_source"]
    social_sensors = json.loads(task_detail["social_sensors"])
    
    #print social_sensors
    if int(text_type) == 0: # 热门原创微博
        results = get_origin_weibo_detail(ts, user, task_name, size, order, 1)

    elif int(text_type) == 1: # 热门转发微博
        results = get_origin_weibo_detail(ts, user, task_name, size, order, 2)

    elif int(text_type) == 2: # 普通转发微博
        results = get_retweet_weibo_detail(ts, user, task_name, size, "message_type", 3)

    elif int(text_type) == 3: # 普通评论微博
        results = get_retweet_weibo_detail(ts, user, task_name, size, "message_type", 2)

    elif int(text_type) == 4: # 积极微博
        results = get_retweet_weibo_detail(ts, user, task_name, size, "sentiment", "1")

    elif int(text_type) == 5: # 中性微博
        results = get_retweet_weibo_detail(ts, user, task_name, size, "sentiment", "0")

    elif int(text_type) == 6: # 消极微博
        results = get_retweet_weibo_detail(ts, user, task_name, size, "sentiment", ["2", "3", "4", "5", "6"])
    elif int(text_type) == 7: # 敏感微博
        results = get_origin_weibo_detail(ts, user, task_name, size, order, 3)

    else:
        print "error"
    print '******************'
    #print results
    return results

def get_sensitive_text_detail(task_name, ts, user, order):
    _id = user + '-' + task_name
    task_detail = es.get(index=index_sensing_task, doc_type=_id, id=ts)['_source']
    weibo_detail = json.loads(task_detail['sensitive_weibo_detail'])

    weibo_detail_list = []
    if weibo_detail:
        for iter_mid, item in weibo_detail.iteritems():
            tmp = []
            tmp.append(iter_mid)
            tmp.append(item[iter_mid])
            tmp.append(item['retweeted'])
            tmp.append(item['comment'])
            weibo_detail_list.append(tmp)
    mid_list = weibo_detail.keys()

    results = []
    query_body = {
        "query":{
            "filtered":{
                "filter":{
                    "terms":{"mid": mid_list}
                }
            }
        }
    }

    index_list = []
    datetime = ts2datetime(ts)
    datetime_1 = ts2datetime(ts-DAY)
    index_name = flow_text_index_name_pre + datetime
    exist_es = es_text.indices.exists(index_name)
    if exist_es:
        index_list.append(index_name)
    index_name_1 = flow_text_index_name_pre + datetime_1
    exist_es_1 = es_text.indices.exists(index_name_1)
    if exist_es_1:
        index_list.append(index_name_1)

    if index_list and mid_list:
        search_results = es_text.search(index=index_list, doc_type=flow_text_index_type, body=query_body)["hits"]["hits"]
    else:
        search_results = []

    uid_list = []
    text_dict = dict() # 文本信息
    portrait_dict = dict() # 背景信息
    if search_results:
        for item in search_results:
            uid_list.append(item["_source"]['uid'])
            text_dict[item['_id']] = item['_source'] # _id是mid
        if uid_list:
            portrait_result = es_profile.mget(index=profile_index_name, doc_type=profile_index_type, body={"ids":uid_list}, fields=['nick_name', 'photo_url'])["docs"]
            for item in portrait_result:
                if item['found']:
                    portrait_dict[item['_id']] = {"nick_name": item["fields"]["nick_name"][0], "photo_url": item["fields"]["photo_url"][0]}
                else:
                    portrait_dict[item['_id']] = {"nick_name": item['_id'], "photo_url":""}

        if order == "total":
            sorted_list = sorted(weibo_detail_list, key=lambda x:x[1], reverse=True)
        elif order == "retweeted":
            sorted_list = sorted(weibo_detail_list, key=lambda x:x[2], reverse=True)
        elif order == "comment":
            sorted_list = sorted(weibo_detail_list, key=lambda x:x[3], reverse=True)
        else:
            sorted_list = weibo_detail_list

        count_n = 0
        for item in sorted_list:
            mid = item[0]
            iter_text = text_dict.get(mid, {})
            temp = []
            # uid, nick_name, photo_url, text, sentiment, timestamp, geo, common_keywords, message_type
            if iter_text:
                uid = iter_text['uid']
                temp.append(uid)
                iter_portrait = portrait_dict.get(uid, {})
                if iter_portrait:
                    temp.append(iter_portrait['nick_name'])
                    temp.append(iter_portrait['photo_url'])
                else:
                    temp.extend([uid,''])
                temp.append(iter_text["text"])
                temp.append(iter_text["sentiment"])
                temp.append(ts2date(iter_text['timestamp']))
                temp.append(iter_text['geo'])
                temp.append(iter_text['message_type'])
                temp.append(item[2])
                temp.append(item[3])
                temp.append(iter_text.get('sensitive', 0))
                count_n += 1
                results.append(temp)

        if results and order == "ts":
            results = sorted(results, key=lambda x:x[5], reverse=True)

        if results and order == "sensitive":
            results = sorted(results, key=lambda x:x[-1], reverse=True)

    return results
    



