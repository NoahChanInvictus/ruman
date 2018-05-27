# -*- coding:utf-8 -*-

import sys
import time
import operator
import json
import numpy as np
#from text_classify.test_topic import topic_classfiy
from elasticsearch import Elasticsearch
from duplicate import duplicate
sys.path.append('./ruman/cron/flow_text/')
from keyword_extraction import get_weibo_single
from ruman.global_utils import es_flow_text as es_text
from ruman.global_utils import es_user_profile as es_profile
from ruman.global_utils import es_user_portrait
from ruman.global_utils import R_SOCIAL_SENSING as r
from ruman.time_utils import ts2datetime, datetime2ts
from ruman.global_utils import flow_text_index_name_pre, flow_text_index_type, profile_index_name, profile_index_type, \
                         portrait_index_name, portrait_index_type
from ruman.parameter import SOCIAL_SENSOR_TIME_INTERVAL as time_interval
from ruman.parameter import SOCIAL_SENSOR_FORWARD_RANGE as time_segment
from ruman.parameter import DETAIL_SOCIAL_SENSING as index_sensing_task
from ruman.parameter import INDEX_MANAGE_SOCIAL_SENSING as index_manage_social_task
from ruman.parameter import DOC_TYPE_MANAGE_SOCIAL_SENSING as task_doc_type
from ruman.parameter import FORWARD_N as forward_n
from ruman.parameter import topic_value_dict
from ruman.parameter import INITIAL_EXIST_COUNT as initial_count
from ruman.parameter import IMPORTANT_USER_NUMBER, IMPORTANT_USER_THRESHOULD, signal_brust, signal_track, signal_count_varition, signal_sentiment_varition,signal_nothing, signal_nothing_variation, \
                      unfinish_signal, finish_signal, AGGRAGATION_KEYWORDS_NUMBER, PRE_AGGREGATION_NUMBER, DAY
from ruman.time_utils import ts2date, datetime2ts, ts2datetime
day_time = 24*3600

# 获得原创微博内容，按时间排序
def get_origin_weibo_detail(ts, user, task_name, size, order, message_type=1):
    _id = user + '-' + task_name
    task_detail = es_user_portrait.get(index=index_sensing_task, doc_type=_id, id=ts)['_source']
    print '37',index_sensing_task,_id
    mid_value = json.loads(task_detail['mid_topic_value'])
    duplicate_dict = json.loads(task_detail['duplicate_dict'])
    tmp_duplicate_dict = dict()
    for k,v in duplicate_dict.iteritems():
        try:
            tmp_duplicate_dict[v].append(k)
        except:
            tmp_duplicate_dict[v] = [k, v]


    if message_type == 1:
        weibo_detail = json.loads(task_detail['origin_weibo_detail'])
    elif message_type == 2:
        weibo_detail = json.loads(task_detail['retweeted_weibo_detail'])
    else:
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
    print len(mid_list)
    results = []
    query_body = {
        "query":{
            "filtered":{
                "filter":{
                    "terms":{"mid": mid_list}
                }
            }
        },
        "size": 1000,
        "sort": {"timestamp": {"order": "desc"}}
    }


    index_list = []
    datetime = ts2datetime(ts)
    datetime_1 = ts2datetime(ts-DAY)
    index_name = flow_text_index_name_pre + datetime
    print es_text
    exist_es = es_text.indices.exists(index_name)
    print exist_es
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
    sort_results = []
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
            sorted_list = sorted(weibo_detail_list, key=lambda x:x[1], reverse=True)[:10]
        elif order == "retweeted":
            sorted_list = sorted(weibo_detail_list, key=lambda x:x[2], reverse=True)[:10]
        elif order == "comment":
            sorted_list = sorted(weibo_detail_list, key=lambda x:x[3], reverse=True)[:10]
        else:
            sorted_list = weibo_detail_list

        count_n = 0
        results_dict = dict()
        mid_index_dict = dict()
        for item in sorted_list: # size
            mid = item[0]
            iter_text = text_dict.get(mid, {})
            temp = []
            # uid, nick_name, photo_url, text, sentiment, timestamp, geo, keywords_string, message_type
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
                if message_type == 1:
                    temp.append(1)
                elif message_type == 2:
                    temp.append(3)
                else:
                    temp.append(iter_text['message_type'])
                #jln 提取关键词
                f_key = get_weibo_single(iter_text['text'])
                temp.append(sorted(f_key.iteritems(),key=lambda x:x[1],reverse=True))
                
                temp.append(item[2])
                temp.append(item[3])
                temp.append(iter_text.get('sensitive', 0))
                temp.append(iter_text['timestamp'])
                temp.append(mid_value[mid])
                temp.append(mid)
                


                results.append(temp)
            count_n += 1


                

        results = sorted(results, key=operator.itemgetter(-4, -2, -6), reverse=True) # -4 -2 -3
        sort_results = []
        count = 0
        for item in results:
            sort_results.append([item])
            mid_index_dict[item[-1]] = count
            count += 1

        
        if tmp_duplicate_dict:
            remove_list = []
            value_list = tmp_duplicate_dict.values() # [[mid, mid], ]
            for item in value_list:
                tmp = []
                for mid in item:
                    if mid_index_dict.get(mid, 0):
                        tmp.append(mid_index_dict[mid])
                if len(tmp) > 1:
                    tmp_min = min(tmp)
                else:
                    continue
                tmp.remove(tmp_min)
                for iter_count in tmp:
                    sort_results[tmp_min].extend(sort_results[iter_count])
                    remove_list.append(sort_results[iter_count])
            if remove_list:
                for item in remove_list:
                    sort_results.remove(item)
        

    return sort_results





# 获得转发或者评论微博所对应的文本
# 是一般性的转发或者评论文本，非root_mid

def get_retweet_weibo_detail(ts, user, task_name, size, text_type, type_value):
    _id = user + '-' + task_name
    task_detail = es_user_portrait.get(index=index_sensing_task, doc_type=_id, id=ts)['_source']
    origin_weibo_detail = json.loads(task_detail['origin_weibo_detail'])
    retweeted_weibo_detail = json.loads(task_detail['retweeted_weibo_detail'])

    mid_list = []
    mid_list.extend(origin_weibo_detail.keys())
    mid_list.extend(retweeted_weibo_detail.keys())

    query_body = {
        "query":{
            "filtered":{
                "filter":{
                    "bool":{
                        "must":[
                            {"range":{
                                "timestamp":{
                                    "gte": ts - time_interval,
                                    "lt": ts
                                }
                            }},
                            {"terms": {"root_mid": mid_list}}
                        ]
                    }
                }
            }
        },
        "sort": {"timestamp": {"order": "desc"}},
        "size": 100
    }

    if text_type == "message_type":
        query_body['query']['filtered']['filter']['bool']['must'].append({"term":{text_type: type_value}})
    if text_type == "sentiment":
        #if isinstance(type_value, str):
        if len(type_value) == 1:
            query_body['query']['filtered']['filter']['bool']['must'].append({"term":{text_type: type_value}})
        else:
            query_body['query']['filtered']['filter']['bool']['must'].append({"terms":{text_type: type_value}})

    datetime = ts2datetime(ts)
    datetime_1 = ts2datetime(ts-time_interval)
    index_name = flow_text_index_name_pre + datetime
    exist_es = es_text.indices.exists(index_name)
    index_name_1 = flow_text_index_name_pre + datetime_1
    exist_es_1 = es_text.indices.exists(index_name_1)

    # 1. 查询微博
    if datetime == datetime_1 and exist_es:
        search_results = es_text.search(index=index_name, doc_type=flow_text_index_type, body=query_body)["hits"]["hits"]
    elif datetime != datetime_1 and exist_es_1:
        search_results = es_text.search(index=index_name_1, doc_type=flow_text_index_type, body=query_body)["hits"]["hits"]
    else:
        search_results = []
    #print search_results
    # 2. 获取微博相关信息
    results = []
    uid_list = []
    if search_results:
        for item in search_results:
            uid_list.append(item["_source"]['uid'])
        if uid_list:
            portrait_result = es_profile.mget(index=profile_index_name, doc_type=profile_index_type, body={"ids":uid_list}, fields=['nick_name', 'photo_url'])["docs"]

        for i in range(len(uid_list)):
            item = search_results[i]['_source']
            temp = []
            # uid, nick_name, photo_url, text, sentiment, timestamp, geo, common_keywords, message_type
            temp.append(item['uid'])
            if portrait_result[i]['found']:
                temp.append(portrait_result[i]["fields"]["nick_name"][0])
                temp.append(portrait_result[i]["fields"]["photo_url"][0])
            else:
                temp.append(item['uid'])
                temp.append("")
            temp.append(item["text"])
            #print item['text']
            temp.append(item["sentiment"])
            temp.append(ts2date(item['timestamp']))
            temp.append(item['geo'])
            temp.append(item["message_type"])
            results.append(temp)

    return results



# 获得积极情绪的微博
def get_positive_weibo_detail(ts, social_sensors, keywords_list, size, sentiment_type=1):
    former_mid_list = query_mid_list(ts-time_interval, keywords_list, time_segment, social_sensors) # 前一段时间内的微博mid list
    current_mid_list = query_mid_list(ts, keywords_list, time_interval,  social_sensors)
    mid_list = []
    mid_list.extend(former_mid_list)
    mid_list.extend(current_mid_list)

    query_body = {
        "query":{
            "filtered":{
                "filter":{
                    "bool":{
                        "must":[
                            {"range":{
                                "timestamp":{
                                    "gte": ts - time_interval,
                                    "lt": ts
                                }
                            }},
                        ],
                        "should":[
                            {"terms": {"root_mid": mid_list}},
                            {"terms": {"mid": mid_list}},
                            {"terms":{"keywords_string": keywords_list}}
                        ]
                    }
                }
            }
        },
        "sort": {"timestamp": {"order": "desc"}},
        "size": 100
    }



    #if social_sensors and int(sentiment_type) == 1:
    #    query_body["query"]["filtered"]["filter"]["bool"]["must"].append({"terms":{"uid": social_sensors}})

    if int(sentiment_type) == 1 or int(sentiment_type) == 0:
        query_body["query"]["filtered"]["filter"]["bool"]["must"].append({"term":{"sentiment":sentiment_type}})
    else:
        query_body["query"]["filtered"]["filter"]["bool"]["must"] = [{"terms":{"sentiment": ["2", "3"]}}]

    # 判断当前ts和ts-time_interval是否属于同一天，确定查询哪个es
    datetime = ts2datetime(ts)
    datetime_1 = ts2datetime(ts-time_interval)
    index_name = flow_text_index_name_pre + datetime
    exist_es = es_text.indices.exists(index_name)
    index_name_1 = flow_text_index_name_pre + datetime_1
    exist_es_1 = es_text.indices.exists(index_name_1)

    # 1. 聚合原创微博mid list
    if datetime == datetime_1 and exist_es:
        search_results = es_text.search(index=index_name, doc_type=flow_text_index_type, body=query_body)["hits"]["hits"]
    elif datetime != datetime_1 and exist_es_1:
        search_results = es_text.search(index=index_name_1, doc_type=flow_text_index_type, body=query_body)["hits"]["hits"]
    else:
        search_results = []

    uid_list = []
    results = []
    if search_results:
        for item in search_results:
            uid_list.append(item["_source"]['uid'])
        if uid_list:
            portrait_result = es_profile.mget(index=profile_index_name, doc_type=profile_index_type, body={"ids":uid_list}, fields=['nick_name', 'photo_url'])["docs"]

        for i in range(len(uid_list)):
            item = search_results[i]['_source']
            temp = []
            # uid, nick_name, photo_url, text, sentiment, timestamp, geo, common_keywords, message_type
            temp.append(item['uid'])
            if portrait_result[i]['found']:
                temp.append(portrait_result[i]["fields"]["nick_name"][0])
                temp.append(portrait_result[i]["fields"]["photo_url"][0])
            else:
                temp.append("unknown")
                temp.append("")
            temp.append(item["text"])
            temp.append(item["sentiment"])
            temp.append(ts2date(item['timestamp']))
            temp.append(item['geo'])
            keywords_set = set(item['keywords_string'].split('&'))
            common_keywords = set(keywords_list) & keywords_set
            temp.append(list(common_keywords))
            temp.append(item['message_type'])
            results.append(temp)

    return results





def query_hot_mid(ts, keywords_list, text_type,size=100):
    query_body = {
        "query":{
            "filtered":{
                "filter":{
                    "bool":{
                        "must":[
                            {"range":{
                                "timestamp":{
                                    "gte":ts - time_interval,
                                    "lt": ts
                                }
                            }},
                            {"terms": {"keywords_string": keywords_list}},
                            {"term": {"message_type": "0"}}
                        ]
                    }
                }
            }
        },
        "aggs":{
            "all_interests":{
                "terms":{"field": "root_mid", "size": size}
            }
        }
    }

    datetime = ts2datetime(ts)
    datetime_1 = ts2datetime(ts-time_interval)
    index_name = flow_text_index_name_pre + datetime
    exist_es = es_text.indices.exists(index_name)
    index_name_1 = flow_text_index_name_pre + datetime_1
    exist_bool_1 = es_text.indices.exists(index_name_1)
    print datetime, datetime_1
    if datetime == datetime_1 and exist_es:
        search_results = es_text.search(index=index_name, doc_type=flow_text_index_type, body=query_body)["aggregations"]["all_interests"]["buckets"]
    elif datetime != datetime_1 and exist_bool_1:
        search_results = es_text.search(index=index_name_1, doc_type=flow_text_index_type, body=query_body)["aggregations"]["all_interests"]["buckets"]
    else:
        search_results = []

    hot_mid_list = []
    if search_results:
        for item in search_results:
            print item
            temp = []
            temp.append(item['key'])
            temp.append(item['doc_count'])
            hot_mid_list.append(temp)

    #print hot_mid_list

    return hot_mid_list


def count_hot_uid(uid, start_time, stop_time):
    query_body = {
        "query":{
            "filtered":{
                "filter":{
                    "bool":{
                        "must":[
                            {"range":{
                                "timestamp":{
                                    "gte":start_time,
                                    "lt": stop_time
                                }
                            }},
                            {"term": {"root_uid": uid}}
                        ]
                    }
                }
#                "query":{
#                    "bool":{
#                        "should":[
#                        ]
#                    }
#                }
            }
        }
    }


    count = 0
    datetime = ts2datetime(float(stop_time))
    index_name = flow_text_index_name_pre + datetime
    exist_es = es_text.indices.exists(index_name)
    if exist_es:
        count = es_text.count(index=index_name, doc_type=flow_text_index_type, body=query_body)["count"]
    else:
        count = 0

    datetime_1 = ts2datetime(float(start_time))
    if datetime_1 == datetime:
        pass
    else:
        ts = float(stop_time)
        while 1:
            ts = ts-day_time
            datetime = ts2datetime(ts)
            index_name = flow_text_index_name_pre + datetime
            exist_es = es_text.indices.exists(index_name)
            if exist_es:
                count = es_text.count(index=index_name, doc_type=flow_text_index_type, body=query_body)["count"]
            else:
                count += 0
            if datetime_1 == datetime:
                break

    return count



def aggregation_hot_keywords(start_time, stop_time, keywords_list):
    start_time = int(start_time)
    stop_time = int(stop_time)
    query_body = {
        "query":{
            "filtered":{
                "filter":{
                    "bool":{
                        "must":[
                            {"terms": {"keywords_string": keywords_list}},
                            {"range":{
                                "timestamp":{
                                    "gte":start_time,
                                    "lt": stop_time
                                }
                            }}
                        ]
                    }
                }
            }
        },
        "aggs":{
            "all_keywords":{
                "terms": {"field": "keywords_string", "size": PRE_AGGREGATION_NUMBER}
            }
        }
    }


    keywords_dict = dict()
    datetime = ts2datetime(float(stop_time))
    index_name = flow_text_index_name_pre + datetime
    exist_es = es_text.indices.exists(index_name)
    if exist_es:
        search_results = es_text.search(index=index_name, doc_type=flow_text_index_type, body=query_body)["aggregations"]['all_keywords']['buckets']
        if search_results:
            for item in search_results:
                keywords_dict[item['key']] = item['doc_count']

    datetime_1 = ts2datetime(float(start_time))
    if datetime_1 == datetime:
        pass
    else:
        ts = float(stop_time)
        while 1:
            keywords_dict_1 = dict()
            ts = ts-day_time
            datetime = ts2datetime(ts)
            index_name = flow_text_index_name_pre + datetime
            exist_es = es_text.indices.exists(index_name)
            if exist_es:
                search_results_1 = es_text.search(index=index_name, doc_type=flow_text_index_type, body=query_body)["aggregations"]['all_keywords']['buckets']
                if search_results_1:
                    print search_results_1
                    for item in search_results_1:
                        keywords_dict_1[item['key']] = item['doc_count']
                for iter_key in keywords_dict_1.keys():
                    if keywords_dict.has_key(iter_key):
                        keywords_dict[iter_key] += keywords_dict_1[iter_key]
                    else:
                        keywords_dict[iter_key] = keywords_dict_1[iter_key]
            if datetime_1 == datetime:
                break
    print keywords_dict
    return_dict = sorted(keywords_dict.items(), key=lambda x:x[1], reverse=True)[:AGGRAGATION_KEYWORDS_NUMBER]
    return return_dict




