# -*- coding: UTF-8 -*-

# 知识图谱人物属性计算入口：
# 需要的用户列表存储在redis的uid_list的队列中；
# 如果人物画像中已有，则将人物属性导入到71的es中
# 如果没有，则需要调用人物属性计算程序，再导入es中

import sys
import time
import json
from elasticsearch import Elasticsearch
from weibo_api_v2 import read_flow_text, read_flow_text_sentiment
from km_cron_text_attribute import test_cron_text_attribute_v2
import redis
reload(sys)
sys.path.append('../../')
#from global_utils import R_RECOMMENTATION as r
from global_utils import es_user_portrait
from parameter import WEIBO_API_INPUT_TYPE
from time_utils import ts2date
r = redis.StrictRedis(host="219.224.134.213", port="7381", db=10)
es_km = Elasticsearch("219.224.134.225:9037", timeout=600)

def scan_compute_redis():
    in_portrait_list = []
    new_portrait_list = []
    non_portrait_list = []

    task_detail = r.rpop("user_portrait_task")
    if not task_detail:
        sys.exit(0)
    task_detail = json.loads(task_detail)
    task_name = task_detail[0]
    task_time = task_detail[1]
    task_uid_list = task_detail[2]
        
    iter_user_list = []
    mapping_dict = dict()
    #test
    count = 0
    for uid in task_uid_list:
        count += 1
        iter_user_list.append(uid)
        if len(iter_user_list) % 100 == 0 and len(iter_user_list) != 0:
            #acquire bulk user weibo data
            in_list, out_list = es_km_storage(iter_uid_list)
            in_portrait_list.extend(in_list)
            if out_list:
                iter_uid_list = out_list
                if WEIBO_API_INPUT_TYPE == 0:
                    user_keywords_dict, user_weibo_dict, online_pattern_dict, character_start_ts = read_flow_text_sentiment(iter_uid_list)
                else:
                    user_keywords_dict, user_weibo_dict, online_pattern_dict, character_start_ts = read_flow_text(iter_uid_list)
                #compute text attribute
                iter_in_list = user_keywords_dict.keys()

                compute_status = test_cron_text_attribute_v2(user_keywords_dict, user_weibo_dict, online_pattern_dict, character_start_ts)
            
                if compute_status==True:
                    new_portrait_list.extend(iter_in_list)
                    print "finish iteration"
                    non_in = list(set(iter_uid_list) - set(iter_in_list))
                    non_portrait_list.extend(non_in)
                else:
                    non_portrait_list.extend(iter_in_list)
            
                #when uid user no weibo at latest week to change compute status to 1
                """
                if len(user_keywords_dict) != len(iter_user_list):
                    change_mapping_dict = dict()
                    change_user_list = set(iter_user_list) - set(user_keywords_dict.keys())
                    for change_user in change_user_list:
                        r.lpush("uid_list",change_user)
                """
            iter_user_list = []
            mapping_dict = {}
            
    if iter_user_list != []:
        #acquire bulk user weibo date
        print 'iter_user_list:', len(iter_user_list)
        in_list, out_list = es_km_storage(iter_user_list)
        in_portrait_list.extend(in_list)
        iter_user_list = out_list
        if iter_user_list:
            print iter_user_list[0][0], type(iter_user_list)
            if WEIBO_API_INPUT_TYPE == 0:
                user_keywords_dict, user_weibo_dict, online_pattern_dict, character_start_ts, filter_keywords_dict = read_flow_text_sentiment(iter_user_list)
            else:
                user_keywords_dict, user_weibo_dict, online_pattern_dict, character_start_ts,filter_keywords_dict = read_flow_text(iter_user_list)
            #compute text attribute
            print 'user_weibo_dict:', len(user_weibo_dict)
            iter_in_list = user_keywords_dict.keys()

            compute_status = test_cron_text_attribute_v2(user_keywords_dict, user_weibo_dict, online_pattern_dict, character_start_ts)
            if compute_status==True:
                new_portrait_list.extend(iter_in_list)
                print "finish iteration"
                non_in = list(set(iter_user_list) - set(iter_in_list))
                non_portrait_list.extend(non_in)
            else:
                non_portrait_list.extend(iter_in_list)
            #when uid user no weibo at latest week to change compute status to 1
            """
            if len(user_keywords_dict) != len(iter_user_list):
                change_mapping_dict = dict()
                change_user_list = set(iter_user_list) - set(user_keywords_dict.keys())
                for change_user in change_user_list:
                    r.lpush("uid_list",change_user)
            """
    results = dict()
    results["task_name"] = task_name
    results["task_time"] = task_time
    results["in_portrait_list"] = json.dumps(in_portrait_list)
    results["new_in_list"] = json.dumps(new_portrait_list)
    results["not_in_list"] = json.dumps(non_portrait_list)

    es_km.index(index="user_portrait_task_results", doc_type="user", id=task_name, body=results)
    try:
        es_km.update(index="user_status", doc_type="user", id=task_name, body={"doc":{"status": "2"}})["_source"]
    except Exception:
        print Exception


def es_km_storage(uid_list):
    es_results = es_user_portrait.mget(index="user_portrait_1222", doc_type="user", body={"ids":uid_list})["docs"]
    in_list = []
    out_list = []
    bulk_action = []
    for item in es_results:
        if item["found"]:
            in_list.append(item["_id"])
            bulk_action.append(item["_source"])
        else:
            out_list.append(item["_id"])

    if bulk_action:
        es_km.bulk(bulk_action, index='user_portrait', doc_type="user", timeout=60) 

    return in_list, out_list
        


if __name__=='__main__':
    log_time_ts = int(time.time())
    print 'cron/text_attribute/scan_compute_redis_imm.py&start&' + str(log_time_ts)
    
    scan_compute_redis()

    log_time_ts = int(time.time())
    print 'cron/text_attribute/scan_compute_redis_imm.py&end&' + str(log_time_ts)
