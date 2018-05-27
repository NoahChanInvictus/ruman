#-*- coding:utf-8 -*-
import datetime
import json
import time as TIME
from elasticsearch import Elasticsearch
from time_utils import ts2datetime, datetime2ts,ts2date
from global_utils import es_user_portrait as es



USER_RANK_KEYWORD_TASK_INDEX = 'user_rank_keyword_task'
USER_RANK_KEYWORD_TASK_TYPE = 'user_rank_task'

MAX_ITEMS = 2 ** 10

def add_task( user_name ,type = "keyword",range = "all"  ,pre ='flow_text_' , during = '1' , start_time ='2013-09-07' ,end_time ='2013-09-07', keyword = 'hello,world' , sort_norm = 'bci' , sort_scope  = 'in_limit_keyword', time = 7, isall = False, number=100 ):
    time_now = int(TIME.time())
    task_id = user_name + "-" + str(time_now)
    tmp_list = keyword.split(',')
    keyword_list = []
    for item in tmp_list:
        if item:
            keyword_list.append(item)
       
    body_json = {
                'submit_user' : user_name ,
                'keyword' : json.dumps(keyword_list),
                'keyword_string': "&".join(keyword_list),
                'submit_time' : ts2datetime(time_now),
                'create_time': time_now,
                'end_time' : datetime2ts(end_time),
                'search_type' : type,
                'status':0,
                'range' : range , 
                'user_ts' : user_name + '-'+ str(time_now),
                'pre' : pre,
                'during' : during ,
                'start_time' : datetime2ts(start_time) ,
                'sort_norm' : sort_norm ,
                'sort_scope' : sort_scope,
                'time' : time ,
                'isall' : isall,
                'number': number
            }
    es.index(index = USER_RANK_KEYWORD_TASK_INDEX , doc_type=USER_RANK_KEYWORD_TASK_TYPE , id=task_id, body=body_json)
    return body_json["user_ts"]

def search_user_task(user_name):
    c_result = {}
    query = {"query":{"bool":{"must":[{"term":{"submit_user":str(user_name)}}]}},"size":MAX_ITEMS,"sort":[{"create_time":{"order":"desc"}}],"fields":["status","search_type","keyword","submit_user","sort_scope","sort_norm","start_time","user_ts","end_time","create_time",'number']}#"sort":[{"create_time":{"order":"desc"}}],;;field:"create_time", 'number'
    if 1:
        return_list = []
        result = es.search(index=USER_RANK_KEYWORD_TASK_INDEX , doc_type=USER_RANK_KEYWORD_TASK_TYPE , body=query)['hits']
        c_result['flag'] = True
        for item in result['hits']:
            result_temp = {}
            result_temp['submit_user'] = item['fields']['submit_user'][0]
            result_temp['search_type'] = item['fields']['search_type'][0]
            #jln
            #result_temp['keyword'] = json.loads(item['fields']['keyword'][0])
            result_temp['keyword'] = json.loads(item['fields']['keyword'][0])
            result_temp['sort_scope'] = item['fields']['sort_scope'][0]
            result_temp['sort_norm'] = item['fields']['sort_norm'][0]
            # result_temp['start_time'] = ts2datetime(item['fields']['start_time'][0])
            # result_temp['end_time'] = ts2datetime(item['fields']['end_time'][0])
            result_temp['start_time'] = item['fields']['start_time'][0]
            result_temp['end_time'] = item['fields']['end_time'][0]

            result_temp['status'] = item['fields']['status'][0]
            result_temp['create_time'] = ts2date(item['fields']['create_time'][0])
            result_temp['search_id'] = item['fields']['user_ts'][0]
            tmp = item['fields'].get('number', 0)
            if tmp:
                result_temp['number'] = int(tmp[0])
            else:
                result_temp['number'] = 100
            return_list.append(result_temp)
        c_result['data'] = return_list
        return c_result

def getResult(search_id):
    item = es.get(index=USER_RANK_KEYWORD_TASK_INDEX , doc_type=USER_RANK_KEYWORD_TASK_TYPE , id=search_id)
    try:
        # result_obj = {}
        # result_obj['keyword'] = json.loads(item['_source']['keyword'])
        # result_obj['sort_scope'] = item['_source']['sort_scope']
        # result_obj['sort_norm'] = item['_source']['sort_norm']
        # result_obj['start_time'] = ts2datetime(item['_source']['start_time'])
        # result_obj['end_time'] =ts2datetime(item['_source']['end_time'])
        # result_obj['result'] = json.loads(item['_source']['result'])
        # # with open("social_sensors.txt", "wb") as f:
        # #     for item in result_obj['result']:
        # #         f.write(str(item)+"\n")
        # result_obj['text_results'] = json.loads(item['_source']['text_results'])
        # result_obj['number'] = item['_source']['number']
        return json.loads(item['_source']['result'])
    except :
        return []    

def delOfflineTask(search_id):
    es.delete(index=USER_RANK_KEYWORD_TASK_INDEX , doc_type=USER_RANK_KEYWORD_TASK_TYPE , id = search_id )
    return True


def sort_task(user, keyword, status, start_time, end_time, submit_time):
    query_body = {
        "query":{
            "filtered":{
                "filter":{
                    "bool":{
                        "must":[
                            {"term":{"submit_user": user}}
                        ]
                    }
                }
            }
        },
        "size": 10000,
        "sort":{"submit_time":{"order":"desc"}}
    }

    query_list = []
    if keyword:
        keyword_list = keyword.split(',')
        query_list.append({"terms":{"keyword_string":keyword_list}})
    if status != 2:
        query_list.append({"term":{"status": status}})
    if start_time and end_time:
        start_ts = datetime2ts(start_time)
        end_ts = datetime2ts(end_time)
        query_list.append({"range":{"start_time":{"gte":start_ts, "lte":end_ts}}})
        query_list.append({"range":{"end_time":{"gte":start_ts, "lte":end_ts}}})
    if submit_time:
        query_list.append({"term":{"submit_time": submit_time}})

    if query_list:
        query_body["query"]["filtered"]["filter"]["bool"]["must"].extend(query_list)

    #print query_body
    search_results = es.search(index=USER_RANK_KEYWORD_TASK_INDEX, doc_type=USER_RANK_KEYWORD_TASK_TYPE, body=query_body)["hits"]["hits"]
    results = []
    if search_results:
        for item in search_results:
            iter_item = item['_source']
            tmp = []
            tmp.append(iter_item['search_type'])
            tmp.append(json.loads(iter_item['keyword']))
            tmp.append(ts2datetime(iter_item['start_time']))
            tmp.append(ts2datetime(iter_item['end_time']))
            tmp.append(iter_item['range'])
            tmp.append(ts2date(iter_item['create_time']))
            tmp.append(iter_item['status'])
            tmp.append(iter_item['sort_norm'])
            tmp.append(iter_item['sort_scope'])
            tmp.append(item['_id']) # task_name
            results.append(tmp)

    return results
 
if __name__ == "__main__":
    print search_task("admin@qq.com", [], 0, '', '', '2016-04-12')        
