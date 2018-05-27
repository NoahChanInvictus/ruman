# -*- coding:utf-8 -*-

# es 使用 Unicode
import sys
import json
import math
import time
from full_text_serach import count_hot_uid, query_hot_mid
from ruman.time_utils import ts2date
from ruman.global_utils import es_user_profile as es_profile
from ruman.global_utils import es_user_portrait as es
from ruman.global_utils import es_flow_text as es_text
from ruman.global_utils import profile_index_name, profile_index_type, portrait_index_name, portrait_index_type, \
                         flow_text_index_name_pre, flow_text_index_type
from ruman.parameter import INDEX_MANAGE_SOCIAL_SENSING as index_manage_sensing_task
from ruman.parameter import DOC_TYPE_MANAGE_SOCIAL_SENSING as task_doc_type
from ruman.parameter import DETAIL_SOCIAL_SENSING as index_sensing_task
from ruman.parameter import SOCIAL_SENSOR_INFO, signal_count_varition, signal_sentiment_varition, CURRENT_WARNING_DICT, IMPORTANT_USER_THRESHOULD, signal_sensitive_variation, DAY
from ruman.time_utils import ts2date_min, datetime2ts, ts2datetime


def get_top_influence(key):
    query_body = {
        "query":{
            "match_all": {}
        },
        "sort":{key:{"order":"desc"}},
        "size": 1
    }

    search_result = es.search(index=portrait_index_name, doc_type=portrait_index_type, body=query_body)['hits']['hits']
    if search_result:
        result = search_result[0]['_source'][key]

    return result

def get_top_all_influence(key, ts):
    query_body = {
        "query":{
            "match_all": {}
        },
        "sort":{key:{"order":"desc"}},
        "size": 1
    }

    index_name = "bci_" + ts2datetime(ts).replace('-','')
    if not es.indices.exists(index=index_name):
        index_name = "bci_" + ts2datetime(ts-DAY).replace('-','')
    exist_es = es.indices.exists(index=index_name)
    if exist_es:
         search_result = es.search(index=index_name, doc_type="bci", body=query_body)['hits']['hits']
    else:
         search_result = {}
    if search_result:
        result = search_result[0]['_source'][key]
    else:
        result = 2000
    return result

# 特别适用于doc_type=2的事件
def get_task_detail_2(task_name, ts, user):
    results = dict()
    index_name = task_name
    _id = user + "-" + task_name
    task_detail = es.get(index=index_manage_sensing_task, doc_type=task_doc_type, id=_id)["_source"]
    task_name = task_detail['task_name']
    social_sensors = json.loads(task_detail['social_sensors'])
    history_status = json.loads(task_detail['history_status'])
    start_time = task_detail['create_at']
    create_by = task_detail['create_by']
    stop_time = task_detail['stop_time']
    remark = task_detail.get('remark', '')
    portrait_detail = []
    count = 0 # 计数

    top_influence = get_top_influence("influence")
    top_activeness = get_top_influence("activeness")
    top_importance = get_top_influence("importance")

    if social_sensors:
        search_results = es.mget(index=portrait_index_name, doc_type=portrait_index_type, body={"ids":social_sensors}, fields=SOCIAL_SENSOR_INFO)['docs']
        for item in search_results:
            temp = []
            if item['found']:
                for iter_item in SOCIAL_SENSOR_INFO:
                    if iter_item == "topic_string":
                        temp.append(item["fields"][iter_item][0].split('&'))
                    elif iter_item == "activeness":
                        temp.append(math.log(item['fields']['activeness'][0]/float(top_activeness)*9+1, 10)*100)
                    elif iter_item == "importance":
                        temp.append(math.log(item['fields']['importance'][0]/float(top_importance)*9+1, 10)*100)
                    elif iter_item == "influence":
                        temp.append(math.log(item['fields']['influence'][0]/float(top_influence)*9+1, 10)*100)
                    else:
                        temp.append(item["fields"][iter_item][0])
                portrait_detail.append(temp)
        portrait_detail = sorted(portrait_detail, key=lambda x:x[5], reverse=True)

    time_series = [] # 时间
    #positive_sentiment_list = [] # 情绪列表
    #neutral_sentiment_list = []
    #negetive_sentiment_list = []
    all_weibo_list = []
    origin_weibo_list = [] # 微博列表
    retweeted_weibo_list = []
    #retweeted_weibo_count = [] # 别人转发他的数量
    #comment_weibo_count = []
    #total_number_count = []
    #burst_time_list = [] # 爆发时间列表
    important_user_set = set() # 重要人物列表
    out_portrait_users = set() # 未入库

    ts = int(ts)
    time_series = history_status
    #for item in history_status:
    #    if int(item[0]) <= ts:
    #        time_series.append(item[0]) # 到目前为止的所有的时间戳

    # get detail task information from es
    if time_series:
        flow_detail = es.mget(index=index_sensing_task, doc_type=_id, body={"ids": time_series})['docs']
    else:
        flow_detail = {}
    if flow_detail:
        for item in flow_detail:
            item = item['_source']
            timestamp = item['timestamp']
            #sentiment_distribution = json.loads(item["sentiment_distribution"])
            #positive_sentiment_list.append(int(sentiment_distribution['1']))
            #negetive_sentiment_list.append(int(sentiment_distribution['2'])+int(sentiment_distribution['3']) \
            #        +int(sentiment_distribution['4'])+int(sentiment_distribution['5'])+int(sentiment_distribution['6']))
            #neutral_sentiment_list.append(int(sentiment_distribution['0']))
            origin_weibo_list.append(item["origin_weibo_number"]) # real
            retweeted_weibo_list.append(item['retweeted_weibo_number']) # real
            all_weibo_list.append(item["origin_weibo_number"]+item['retweeted_weibo_number'])
            #retweeted_weibo_count.append(item['retweeted_weibo_count'])
            #comment_weibo_count.append(item['comment_weibo_count'])
            #total_number_count.append(item['weibo_total_number'])
            temp_important_user_list = json.loads(item['important_users'])
            unfiltered_users = json.loads(item['unfilter_users'])
            temp_out_portrait_users = set(unfiltered_users) - set(temp_important_user_list) # 未入库
            important_user_set = important_user_set | set(temp_important_user_list)
            out_portrait_users = out_portrait_users | set(temp_out_portrait_users)

            #burst_reason = item.get("burst_reason", "")
            #if burst_reason:
            #    burst_time_list.append([timestamp, count, burst_reason])
            count += 1

    ####################################################################################
    # 统计爆发原因，下相应的结论
    """
    weibo_variation_count = 0
    weibo_variation_time = []
    sentiment_variation_count = 0
    sentiment_variation_time = []
    sensitive_variation_count = 0 # sensitive
    sensitive_variation_time = [] # sensitive
    common_variation_count = 0
    common_variation_time = []
    if burst_time_list:
        for item in burst_time_list:
            tmp_common = 0
            x1 = 0
            x2 = 0
            x3 = 0
            if signal_count_varition in item[2]:
                weibo_variation_count += 1
                weibo_variation_time.append([ts2date_min(item[0]), total_number_count[item[1]]])
                x1 = total_number_count[item[1]]
                tmp_common += 1
            if signal_sentiment_varition in item[2]:
                tmp_common += 1
                sentiment_variation_count += 1
                x2 = negetive_sentiment_list[item[1]]
                sentiment_variation_time.append([ts2date_min(item[0]), negetive_sentiment_list[item[1]]])
            if signal_sensitive_variation in item[2]:
                tmp_common += 1
                sensitive_variation_count += 1
                x3 = sensitive_total_number_list[item[1]]
                sensitive_variation_time.append([ts2date_min(item[0]), all_weibo_list[item[1]]])
            if tmp_common >= 2:
                common_variation_count += 1
                common_variation_time.append([ts2date_min(item[0]), x1, x2, x3])

    warning_conclusion = remark
    variation_distribution = []
    if weibo_variation_count:
        variation_distribution.append(weibo_variation_time)
    else:
        variation_distribution.append([])

    if sentiment_variation_count:
        variation_distribution.append(sentiment_variation_time)
    else:
        variation_distribution.append([])

    if sensitive_variation_count:
        variation_distribution.append(sensitive_variation_time)
    else:
        variation_distribution.append([])

    if common_variation_count:
        variation_distribution.append(common_variation_time)
    else:
        variation_distribution.append([])

    results['warning_conclusion'] = warning_conclusion
    results['variation_distribution'] = variation_distribution

    # 每个用户的热度
    """

    # 获取重要用户的个人信息
    important_uid_list = list(important_user_set)
    out_portrait_users_list = list(out_portrait_users)
    social_sensor_set = set(social_sensors)
    user_detail_info = [] #
    out_user_detail_info = []
    if important_uid_list:
        user_results = es.mget(index=portrait_index_name, doc_type=portrait_index_type, body={"ids":important_uid_list}, fields=['uid', 'uname', 'domain', 'topic_string', "photo_url", 'importance', 'influence', 'activeness'])['docs']
        for item in user_results:
            if item['found']:
                temp = []
                #if int(item['fields']['importance'][0]) < IMPORTANT_USER_THRESHOULD:
                #    continue
                temp.append(item['fields']['uid'][0])
                uname = item['fields']['uname'][0]
                if not uname or uname == "未知":
                    uname = item['fields']['uid'][0]
                temp.append(uname)
                temp.append(item['fields']['photo_url'][0])
                temp.append(item['fields']['domain'][0])
                temp.append(item['fields']['topic_string'][0].split('&'))
                #hot_count = count_hot_uid(item['fields']['uid'][0], start_time, stop_time)
                #temp.append(hot_count)
                temp.append(math.log(item['fields']['importance'][0]/float(top_importance)*9+1, 10)*100)
                temp.append(math.log(item['fields']['influence'][0]/float(top_influence)*9+1, 10)*100)
                temp.append(math.log(item['fields']['activeness'][0]/float(top_activeness)*9+1, 10)*100)
                if item['fields']['uid'][0] in social_sensor_set:
                    temp.append(1)
                else:
                    temp.append(0)
                user_detail_info.append(temp)
    # 排序
    if user_detail_info:
        user_detail_info = sorted(user_detail_info, key=lambda x:x[6], reverse=True)
    else:
        user_detail_info = []

    if out_portrait_users_list:
        profile_results = es_profile.mget(index=profile_index_name, doc_type=profile_index_type, body={"ids":out_portrait_users_list})["docs"]
        bci_index = "bci_" + ts2datetime(ts-DAY).replace('-','')
        influence_results = es.mget(index=bci_index, doc_type="bci", body={"ids":out_portrait_users_list}, fields=["user_index"])['docs']
        bci_results = es_profile.mget(index="bci_history", doc_type="bci", body={"ids":out_portrait_users_list}, fields=['user_fansnum'])['docs']
        top_influence = get_top_all_influence("user_index", ts)
        count = 0
        if profile_results:
            for item in profile_results:
                temp = []
                if item['found']:
                    temp.append(item['_source']['uid'])
                    if item['_source']['nick_name']:
                        temp.append(item['_source']['nick_name'])
                    else:
                        temp.append(item['_source']['uid'])
                    temp.append(item['_source']['user_location'])
                    #temp.append(item['_source']['fansnum'])
                else:
                    temp.append(item['_id'])
                    temp.append(item['_id'])
                    temp.extend([''])
                try:
                    user_fansnum = bci_results[count]["fields"]["user_fansnum"][0]
                except:
                    user_fansnum = 0
                temp.append(user_fansnum)
                temp_influ = influence_results[count]
                if temp_influ.get('found', 0):
                    user_index = temp_influ['fields']['user_index'][0]
                    temp.append(math.log(user_index/float(top_influence)*9+1, 10)*100)
                else:
                    temp.append(0)
                count += 1
                out_user_detail_info.append(temp)
    print len(out_user_detail_info)
    if len(out_user_detail_info):
        print "sort"
        out_user_detail_info = sorted(out_user_detail_info, key=lambda x:x[4], reverse=True)


    revise_time_series = []
    for item in time_series:
        revise_time_series.append(ts2date_min(item))

    results['important_user_detail'] = user_detail_info
    results['out_portrait_user_detail'] = out_user_detail_info
    #results['burst_time'] = burst_time_list # 爆发时间点，以及爆发原因
    results['time_series'] = revise_time_series
    #results['positive_sentiment_list'] = positive_sentiment_list
    #esults['negetive_sentiment_list'] = negetive_sentiment_list
    #results['neutral_sentiment_list'] = neutral_sentiment_list
    results['all_weibo_list'] = all_weibo_list
    results['origin_weibo_list'] = origin_weibo_list
    results['retweeted_weibo_list'] = retweeted_weibo_list
    #results['comment_weibo_count'] = comment_weibo_count
    #results['retweeted_weibo_count'] = retweeted_weibo_count
    #results['total_number_list'] = total_number_count
    results['social_sensors_detail'] = portrait_detail

    return results


if __name__ == "__main__":
    print get_task_detail_2('监督维权律师', "keywords", "1378323000")


