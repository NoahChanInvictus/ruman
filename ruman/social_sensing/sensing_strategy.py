# -*- coding:utf-8 -*-

import sys
import time
import json
import numpy as np
from elasticsearch import Elasticsearch
from  mappings_social_sensing import mappings_sensing_task
from aggregation_weibo import get_forward_numerical_info, query_mid_list, query_related_weibo, aggregation_sentiment_related_weibo
from clustering import kmeans, tfidf, text_classify, cluster_evaluation, freq_word
reload(sys)
sys.path.append("./../")
from global_utils import es_flow_text as es_text
from global_utils import es_user_profile as es_profile
from global_utils import es_user_portrait
from global_utils import R_SOCIAL_SENSING as r
from global_utils import flow_text_index_name_pre, flow_text_index_type, profile_index_name, profile_index_type, \
                         portrait_index_name, portrait_index_type
from parameter import SOCIAL_SENSOR_TIME_INTERVAL as time_interval
from parameter import SOCIAL_SENSOR_FORWARD_RANGE as forward_time_range
from parameter import DETAIL_SOCIAL_SENSING as index_sensing_task
from parameter import INDEX_MANAGE_SOCIAL_SENSING as index_manage_social_task
from parameter import DOC_TYPE_MANAGE_SOCIAL_SENSING as task_doc_type
from parameter import FORWARD_N as forward_n
from parameter import INITIAL_EXIST_COUNT as initial_count
from parameter import IMPORTANT_USER_NUMBER, IMPORTANT_USER_THRESHOULD, signal_brust, signal_track, signal_count_varition,signal_sentiment_varition, signal_nothing, signal_nothing_variation, \
                      unfinish_signal, finish_signal, signal_sensitive_variation

from time_utils import ts2datetime, datetime2ts


def sensors_keywords_detection(task_detail):
    task_name = task_detail[0]
    social_sensors = task_detail[1]
    keywords_list = task_detail[2]
    sensitive_words = task_detail[3]
    stop_time = task_detail[4]
    forward_warning_status = task_detail[5]
    ts = task_detail[7]

    forward_result = get_forward_numerical_info(task_name, ts, keywords_list)
    # 1. 聚合前12个小时内传感人物发布的所有与关键词相关的原创微博
    forward_origin_weibo_list = query_mid_list(ts-time_interval, keywords_list, forward_time_range, 1, social_sensors)
    # 2. 聚合当前阶段内的原创微博
    current_mid_list = query_mid_list(ts, keywords_list, time_interval, 1, social_sensors)
    all_mid_list = []
    all_mid_list.extend(current_mid_list)
    all_mid_list.extend(forward_origin_weibo_list)
    all_mid_list = list(set(all_mid_list))
    print all_mid_list
    # 3. 查询当前的原创微博和之前12个小时的原创微博在当前时间内的转发和评论数, 聚合按照message_type
    statistics_count = query_related_weibo(ts, all_mid_list, time_interval, keywords_list, 1, social_sensors)
    current_total_count = statistics_count['total_count']
    # 当前阶段内所有微博总数
    print "current all weibo: ", statistics_count
    current_origin_count = statistics_count['origin']
    current_retweeted_count = statistics_count['retweeted']
    current_comment_count = statistics_count['comment']

    # 4. 聚合当前时间内积极、中性、悲伤、愤怒情绪分布
    sentiment_count = {"0": 0, "1": 0, "2": 0, "3": 0}
    datetime = ts2datetime(ts)
    datetime_1 = ts2datetime(ts-time_interval)
    if datetime == datetime_1:
        index_name = flow_text_index_name_pre + datetime
    else:
        index_name = flow_text_index_name_pre + datetime_1
    exist_es = es_text.indices.exists(index_name)
    if exist_es:
        search_results = aggregation_sentiment_related_weibo(ts, all_mid_list, time_interval, keywords_list, 1)
        sentiment_count = search_results
        print "sentiment_count: ", sentiment_count
    negetive_count = sentiment_count['2'] + sentiment_count['3']

    # 5. 那些社会传感器参与事件讨论
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
                            {"terms":{"uid": social_sensors}}
                        ],
                        "should":[
                            {"terms": {"root_mid": all_mid_list}},
                            {"terms": {"mid": all_mid_list}}
                        ]
                    }
                }
            }
        },
        "size": 10000
    }

    datetime = ts2datetime(ts)
    datetime_1 = ts2datetime(ts - time_interval)
    if datetime == datetime_1:
        index_name = flow_text_index_name_pre + datetime
    else:
        index_name = flow_text_index_name_pre + datetime_1

    search_results = es_text.search(index=index_name, doc_type=flow_text_index_type, body=query_body)['hits']['hits']
    attend_users = []
    if search_results:
        for item in search_results:
            attend_users.append(item['_source']['uid'])

    important_users = list(set(attend_users))
    print "important users", important_users


    # 6. 敏感词识别，如果传感器的微博中出现这么一个敏感词，那么就会预警------PS.敏感词是一个危险的设置
    sensitive_origin_weibo_number = 0
    sensitive_retweeted_weibo_number = 0
    sensitive_comment_weibo_number = 0
    sensitive_total_weibo_number = 0

    if sensitive_words:
        query_sensitive_body = {
            "query":{
                "filtered":{
                    "filter":{
                        "bool":{
                            "must":[
                                {"range":{
                                    "timestamp":{
                                        "gte": ts - time_interval,
                                        "lt": ts
                                    }}
                                },
                                {"terms": {"keywords_string": sensitive_words}},
                                {"terms": {"uid": social_sensors}}
                            ]
                        }
                    }
                }
            },
            "aggs":{
                "all_list":{
                    "terms":{"field": "message_type"}
                }
            }
        }

        sensitive_results = es_text.search(index=index_name, doc_type=flow_text_index_type, body=query_sensitive_body)['aggregations']['all_list']["buckets"]
        if sensitive_results:
            for item in sensitive_results:
                if int(item["key"]) == 1:
                    sensitive_origin_weibo_number = item['doc_count']
                elif int(item["key"]) == 2:
                    sensitive_comment_weibo_number = item['doc_count']
                elif int(item["key"]) == 3:
                    sensitive_retweeted_weibo_number = item["doc_count"]
                else:
                    pass

            sensitive_total_weibo_number = sensitive_origin_weibo_number + sensitive_comment_weibo_number + sensitive_retweeted_weibo_number


    burst_reason = signal_nothing_variation
    warning_status = signal_nothing
    finish = unfinish_signal # "0"

    if sensitive_total_weibo_number: # 敏感微博的数量异常
        print "======================"
        if forward_warning_status == signal_brust: # 已有事件发生，改为事件追踪
            warning_status = signal_track
        else:
            warning_status = signal_brust
        burst_reason = signal_sensitive_variation

    if forward_result[0]:
        # 根据移动平均判断是否有时间发生
        mean_count = forward_result[1]
        std_count = forward_result[2]
        mean_sentiment = forward_result[3]
        std_sentiment = forward_result[4]
        if current_total_count > mean_count+1.96*std_count: # 异常点发生
            print "====================================================="
            if forward_warning_status == signal_brust: # 已有事件发生，改为事件追踪
                warning_status = signal_track
            else:
                warning_status = signal_brust
            burst_reason += signal_count_varition # 数量异常
        if negetive_count > mean_sentiment+1.96*std_sentiment:
            warning_status = signal_brust
            burst_reason += signal_sentiment_varition # 负面情感异常, "12"表示两者均异常
            if forward_warning_status == signal_brust: # 已有事件发生，改为事件追踪
                warning_status = signal_track

    if int(stop_time) <= ts: # 检查任务是否已经完成
        finish = finish_signal

    # 7. 感知到的事, all_mid_list
    if burst_reason: # 有事情发生
        text_list = []
        if signal_sensitive_variation in burst_reason:
            query_sensitive_body = {
                "query":{
                    "filtered":{
                        "filter":{
                            "bool":{
                                "must":[
                                    {"range":{
                                        "timestamp":{
                                            "gte": ts - time_interval,
                                            "lt": ts
                                        }}
                                    },
                                    {"terms": {"keywords_string": sensitive_words}}
                                ]
                            }
                        }
                    }
                },
                "size": 10000
            }
            if social_sensors:
                query_sensitive_body['query']['filtered']['filter']['bool']['must'].append({"terms":{"uid": social_sensors}})

            sensitive_results = es_text.search(index=index_name, doc_type=flow_text_index_type, body=query_sensitive_body)['hits']["hits"]
            if sensitive_results:
                for item in sensitive_results:
                    iter_mid = item['_source']['mid']
                    iter_text = item['_source']['text']
                    temp_dict = dict()
                    temp_dict["mid"] = iter_mid
                    temp_dict["text"] = iter_text
                    text_list.append(temp_dict) # 整理后的文本，mid，text
            burst_reason.replace(signal_sensitive_variation, "")


        if burst_reason and all_mid_list:
            sensing_text = es_text.mget(index=index_name, doc_type=flow_text_index_type, body={"ids": all_mid_list}, fields=["mid", "text"])["docs"]
            if sensing_text:
                for item in sensing_text:
                    if item['found']:
                        iter_mid = item["fields"]["mid"][0]
                        iter_text = item["fields"]["text"][0]
                        temp_dict = dict()
                        temp_dict["mid"] = iter_mid
                        temp_dict["text"] = iter_text
                        text_list.append(temp_dict)

        if len(text_list) == 1:
            top_word = freq_word(text_list)
            topic_list = top_word.keys()
        elif len(text_list) == 0:
            topic_list = []
            burst_reason = "" #没有相关微博，归零
            print "***********************************"
        else:
            feature_words, input_word_dict = tfidf(text_list) #生成特征词和输入数据
            word_label, evaluation_results = kmeans(feature_words, text_list) #聚类
            inputs = text_classify(text_list, word_label, feature_words)
            clustering_topic = cluster_evaluation(inputs)
            sorted_dict = sorted(clustering_topic.items(), key=lambda x:x[1], reverse=True)[0:5]
            topic_list = []
            if sorted_dict:
                for item in sorted_dict:
                    topic_list.append(word_label[item[0]])
            print topic_list


    results = dict()
    results['sensitive_origin_weibo_number'] = sensitive_origin_weibo_number
    results['sensitive_retweeted_weibo_number'] = sensitive_retweeted_weibo_number
    results['sensitive_comment_weibo_number'] = sensitive_comment_weibo_number
    results['sensitive_weibo_total_number'] = sensitive_total_weibo_number
    results['origin_weibo_number'] = current_origin_count
    results['retweeted_weibo_number'] = current_retweeted_count
    results['comment_weibo_number'] = current_comment_count
    results['weibo_total_number'] = current_total_count
    results['sentiment_distribution'] = json.dumps(sentiment_count)
    results['important_users'] = json.dumps(important_users)
    results['burst_reason'] = burst_reason
    results['timestamp'] = ts
    if burst_reason:
        results["clustering_topic"] = json.dumps(topic_list)

    # es存储当前时段的信息
    doctype = task_name
    es_user_portrait.index(index=index_sensing_task, doc_type=doctype, id=ts, body=results)

    # 更新manage social sensing的es信息
    temporal_result = es_user_portrait.get(index=index_manage_social_task, doc_type=task_doc_type, id=task_name)['_source']
    temporal_result['warning_status'] = warning_status
    temporal_result['burst_reason'] = burst_reason
    temporal_result['finish'] = finish
    history_status = json.loads(temporal_result['history_status'])
    history_status.append([ts, ' '.join(keywords_list), warning_status])
    temporal_result['history_status'] = json.dumps(history_status)
    es_user_portrait.index(index=index_manage_social_task, doc_type=task_doc_type, id=task_name, body=temporal_result)

    return "1"




