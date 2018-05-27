#-*- coding:utf-8 -*-

import os
import time
import math
import json
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect
from ruman.time_utils import datetime2ts, ts2datetime
from ruman.global_utils import R_SOCIAL_SENSING as r
from ruman.global_utils import es_user_portrait as es
from ruman.global_utils import portrait_index_name, portrait_index_type
from ruman.global_utils import group_index_name as index_group_manage
from ruman.global_utils import group_index_type as doc_type_group
from ruman.parameter import INDEX_MANAGE_SOCIAL_SENSING as index_manage_sensing_task
from ruman.parameter import DOC_TYPE_MANAGE_SOCIAL_SENSING as task_doc_type
from ruman.parameter import DETAIL_SOCIAL_SENSING as index_sensing_task
from ruman.parameter import finish_signal, unfinish_signal, SOCIAL_SENSOR_INFO
from utils import get_warning_detail, get_text_detail, get_sensitive_text_detail
from utils_hot import get_recommend
from delete_es import delete_es
from ruman.parameter import RUN_TYPE

mod = Blueprint('social_sensing', __name__, url_prefix='/social_sensing')


# 前台设置好的参数传入次函数，创建感知任务,放入es, 从es中读取所有任务信息放入redis:sensing_task 任务队列中
# parameters: task_name, create_by, stop_time, remark, social_sensors, keywords
# other parameters: create_at, warning_status,
# warning_status: 0-no, 1-burst, 2-tracking, 3-ever_brusing, now no
# task_type：任务类型：{"0": no keywords and no sensors, "1": no keywords and some sensors, "2": "some keywords and no sensors", "3": "some keywords and some sensors"}
@mod.route('/create_task/')
def ajax_create_task():
    # task_name forbid illegal enter
    task_number = request.args.get('task_number', 1)
    task_name = request.args.get('task_name','') # must
    create_by = request.args.get('create_by', 'admin') # 用户
    stop_time = request.args.get('stop_time', "default") #timestamp, 1234567890
    social_sensors = request.args.get("social_sensors", "") #uid_list, split with ","
    remark = request.args.get("remark", "")
    _id = create_by + "-" + str(task_name)
    exist_es = es.exists(index=index_manage_sensing_task, doc_type=task_doc_type, id=_id)
    if exist_es:
        return json.dumps(["0"]) # 任务名不能重合
    query_body = {
        "query":{
            "filtered":{
                "filter":{
                    "bool":{
                        "must":[
                            {"term":{"processing_status": "1"}},
                            {"term":{"finish":"0"}}
                        ]
                    }
                }
            }
        }
    }
    
    unfinish_number =  es.count(index=index_manage_sensing_task, doc_type=task_doc_type, body=query_body)['count']
    if unfinish_number > (int(task_number)-1):
        return "more than limit"
    if task_name:
        task_detail = dict()
        task_detail["task_name"] = task_name
        task_detail["create_by"] = create_by # 创建任务, user
        task_detail["stop_time"] = stop_time
        task_detail["remark"] = remark
        if social_sensors:
            task_detail["social_sensors"] = json.dumps(list(set(social_sensors.split(','))))
        else:
            return json.dumps(['-1'])
        now_ts = int(time.time())
        task_detail["create_at"] = now_ts # now_ts
        task_detail["warning_status"] = '0'
        task_detail["finish"] = "0" # not end the task
        task_detail["history_status"] = json.dumps([]) # ts, keywords, warning_status
        task_detail['burst_reason'] = ''
        task_detail['processing_status'] = "1" #任务正在进行

    # store task detail into es
    es.index(index=index_manage_sensing_task, doc_type=task_doc_type, id=_id, body=task_detail)


    return json.dumps(["1"])


@mod.route('/delete_task/')
def ajax_delete_task():
    # delete task based on task_name
    task_name = request.args.get('task_name','') # must
    user = request.args.get('user', '')
    print task_name, user
    if task_name and user:
        _id = user + "-" + task_name
        es.delete(index=index_manage_sensing_task, doc_type=task_doc_type, id=_id)
        try:
            delete_es(_id)
        except Exception, r:
            print Exception, r
        return json.dumps(['1'])
    else:
        return json.dumps([])



# 终止任务，即在到达终止时间前就终止任务
@mod.route('/stop_task/')
def ajax_stop_task():
    task_name = request.args.get('task_name','') # must
    user = request.args.get('user', '')
    if task_name and user:
        _id = user + "-" + task_name
        task_detail = es.get(index=index_manage_sensing_task, doc_type=task_doc_type, id=_id)['_source']
        #task_detail["finish"] = finish_signal
        task_detail['processing_status'] = '0'
        es.index(index=index_manage_sensing_task, doc_type=task_doc_type, id=_id, body=task_detail)
        return json.dumps(['1'])
    else:
        return json.dumps([])


# 修改任务终止时间
# 修改finish=0代表重启任务
# 修改终止时间，当任务停止后即使延迟终止时间，仍需要设置finish=0代表重新启动
# if finish == 1:
#    finish
# else:
#    if processing_status == 0:
#        print "stop"
#    else:
#        print "working"
@mod.route('/revise_task/')
def ajax_revise_task():
    task_name = request.args.get('task_name','') # must
    finish = request.args.get("finish", "10")
    stop_time = request.args.get('stop_time', '') # timestamp
    user = request.args.get('user', '')

    #now_ts = datetime2ts("2013-09-06")
    _id = user + '-' + task_name
    now_ts = time.time()
    if stop_time and stop_time < now_ts:
        return json.dumps([])

    if task_name and user:
        task_detail = es.get(index=index_manage_sensing_task, doc_type=task_doc_type, id=_id)['_source']
        if stop_time:
            task_detail['stop_time'] = stop_time
        if int(finish) == 0:
            task_detail['finish'] = finish
            task_detail['processing_status'] = "1" # 重启时将处理状态改为
        if stop_time or int(finish) == 0:
            es.index(index=index_manage_sensing_task, doc_type=task_doc_type, id=_id, body=task_detail)
            return json.dumps(['1'])
    return json.dumps([])



@mod.route('/show_task/')
def ajax_show_task():
    # show all working task
    # "0": unfinish working task
    # "1": finish working task
    status = request.args.get("finish", "01")
    user = request.args.get('user', '')
    length = len(status)
    query_body = {
        "query":{
            "filtered":{
                "filter":{
                    "bool":{
                        "must":[
                            {"term":{"create_by": user}}
                        ]
                    }
                }
            }
        },
        "sort": {"create_at": {"order": "desc"}},
        "size": 10000
    }
    #if length == 2:
    #    category_list = [status[0], status[1]]
    #    query_body['query']['filtered']['filter']["bool"]["must"].append({"term":{"finish": category_list}})
    if length == 1:
        query_body['query']['filtered']['filter']['bool']['must'].append({"term":{"finish": status}})
    #else:
    #    print "error"

    try:
        search_results = es.search(index=index_manage_sensing_task, doc_type=task_doc_type, body=query_body)['hits']['hits']
    except:
        search_results = []
    results = []
    if search_results:
        for item in search_results:
            item = item['_source']
            history_status = json.loads(item['history_status'])
            if history_status:
                item['history_status'] = sorted(history_status, key=lambda x:x, reverse=True)
            else:
                item['history_status'] = []
            results.append(item)
    return json.dumps(results)


@mod.route('/get_task_detail_info/')
def ajax_get_task_detail_info():
    task_name = request.args.get('task_name','') # task_name
    user = request.args.get('user', 'admin')
    _id = user + "-" + task_name
    task_detail = es.get(index=index_manage_sensing_task, doc_type=task_doc_type, id=_id)['_source']
    task_detail["social_sensors"] = json.loads(task_detail["social_sensors"])
    #task_detail['keywords'] = json.loads(task_detail['keywords'])
    #task_detail["sensitive_words"]= json.loads(task_detail["sensitive_words"])
    history_status = json.loads(task_detail['history_status'])
    if history_status:
        temp_list = []
        """
        temp_list.append(history_status[-1])
        print history_status
        for item in history_status[:-1]:
            temp_list.append(item)
        """
        sorted_list = sorted(history_status, key=lambda x:x, reverse=True)
        task_detail['history_status'] = sorted_list
    else:
        task_detail['history_status'] = []
    task_detail['social_sensors_portrait'] = []
    portrait_detail = []

    if task_detail["social_sensors"]:
        search_results = es.mget(index=portrait_index_name, doc_type=portrait_index_type, body={"ids": task_detail["social_sensors"]})['docs']
        if search_results:
            for item in search_results:
                temp = []
                if item['found']:
                    for iter_item in SOCIAL_SENSOR_INFO:
                        if iter_item == "topic_string":
                            temp.append(item["_source"][iter_item].split('&'))
                        else:
                            temp.append(item["_source"][iter_item])
                    portrait_detail.append(temp)
        if portrait_detail:
            portrait_detail = sorted(portrait_detail, key=lambda x:x[5], reverse=True)
    task_detail['social_sensors_portrait'] = portrait_detail

    return json.dumps(task_detail)



# unfinished
@mod.route('/get_group_list/')
def ajax_get_group_list():
    user = request.args.get('user', '')
    # get all group list from group manage
    results = [] #
    query_body = {
        "query":{
            "filtered":{
                "filter":{
                    "bool":{
                        "should":[
                            {"term": {"task_type": "analysis"}},
                            {"bool":{
                                "must":[
                                    {"term": {"task_type": "detect"}},
                                    {"term": {"detect_process":100}}
                                ]
                            }}
                        ],
                        "must":{"term": {"submit_user": user}}
                    }
                }
            }
        },
        "sort": {"submit_date": {"order": "desc"}},
        "size": 10000
    }

    search_results = es.search(index=index_group_manage, doc_type=doc_type_group, body=query_body, timeout=600)['hits']['hits']
    if search_results:
        for item in search_results:
            item = item['_source']
            temp = []
            temp.append(item['task_name'])
            temp.append(item['submit_user'])
            temp.append(item['submit_date'])
            temp.append(0)
            temp.append(item.get('state', ""))
            try:
                temp.append(json.loads(item['uid_list']))
                count = len(json.loads(item['uid_list']))
                temp[3] = count
            except:
                temp.append(item['uid_list'])
                temp[3] = len(item['uid_list'])
            results.append(temp)

    return json.dumps(results)

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

@mod.route('/get_group_detail/')
def ajax_get_group_detail():
    task_name = request.args.get('task_name','') # task_name
    user = request.args.get('user', '')
    _id = user + '-' + task_name
    portrait_detail = []
    top_activeness = get_top_influence("activeness")
    top_influence = get_top_influence("influence")
    top_importance = get_top_influence("importance")
    search_result = es.get(index=index_group_manage, doc_type=doc_type_group, id=_id).get('_source', {})
    if search_result:
        try:
            uid_list = json.loads(search_result['uid_list'])
        except:
            uid_list = search_result['uid_list']
        if uid_list:
            search_results = es.mget(index=portrait_index_name, doc_type=portrait_index_type, body={"ids":uid_list}, fields=SOCIAL_SENSOR_INFO)['docs']
            for item in search_results:
                temp = []
                if item['found']:
                    for iter_item in SOCIAL_SENSOR_INFO:
                        if iter_item == "topic_string":
                            temp.append(item["fields"][iter_item][0].split('&'))
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

    return json.dumps(portrait_detail)


# 返回某个预警事件的详细信息，包括微博量、情感和参与的人
@mod.route('/get_warning_detail/')
def ajax_get_warning_detail():
    task_name = request.args.get('task_name','') # task_name
    ts = request.args.get('ts', '') # timestamp: 123456789
    user = request.args.get('user', '')
    _id = user + '-' + task_name

    results = get_warning_detail(task_name, ts, user)

    return json.dumps(results)


# 返回某个时间段特定的文本，按照热度排序
@mod.route('/get_text_detail/')
def ajax_get_text_detail():
    task_name = request.args.get('task_name','media') # task_name
    user = request.args.get('user', '')
    order = request.args.get('order', 'total') # total, retweeted, comment
    ts = int(request.args.get('ts', '1480176000')) # timestamp: 123456789
    text_type = request.args.get('text_type', 0) # which line

    results = get_text_detail(task_name, ts, text_type, user, order)

    return json.dumps(results)

# 返回敏感微博
@mod.route('/get_sensitive_text_detail/')
def ajax_get_sensitive_text_detail():
    task_name = request.args.get('task_name','') # task_name
    user = request.args.get('user', '')
    order = request.args.get('order', 'sensitive') # total, retweeted, comment
    ts = int(request.args.get('ts', '')) # timestamp: 123456789

    results = get_sensitive_text_detail(task_name, ts, user, order)

    return json.dumps(results)
# 返回某个预警点的微博主题, 没有则为空
@mod.route('/get_clustering_topic/')
def ajax_get_clustering_topic():
    task_name = request.args.get('task_name','') # task_name
    user = request.args.get('user', '')
    ts = int(request.args.get('ts', '')) # timestamp: 123456789
    topic_list = []
    _id = user + '-' + task_name
    task_detail = es.get(index=index_sensing_task, doc_type=_id, id=ts)['_source']
    #burst_reason = task_detail['burst_reason']
    burst_reason = 1
    filter_list = []
    if burst_reason:
        topic_list = task_detail.get("clustering_topic", [])
        if topic_list:
            topic_list = json.loads(topic_list)
            for item in topic_list:
                tmp = []
                for word in item:
                    if len(word) > 1:
                        tmp.append(word)
                filter_list.append(tmp)

    return json.dumps(filter_list[:5])


@mod.route('/get_rub_hotspots/')
def ajax_get_hotspots():
    uid = request.args.get('uid','')
    results=get_recommend(uid)
    return results