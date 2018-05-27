#-*- coding:utf-8 -*-
from elasticsearch import Elasticsearch
import sys
import json
import time
import datetime
from time_utils import ts2datetime, datetime2ts, ts2date
from parameter import DAY, LOW_INFLUENCE_THRESHOULD
from in_filter import in_sort_filter
from all_filter import all_sort_filter
from Makeup_info import make_up_user_info, get_all_filed
from global_utils import es_user_portrait, es_user_profile
from global_utils import es_flow_text
from global_utils import R_CLUSTER_FLOW3 as redis_task
from influence_appendix import weiboinfo2url

USER_INDEX_NAME = 'user_portrait_1222'
USER_INDEX_TYPE = 'user'


USER_RANK_KEYWORD_TASK_INDEX = 'user_rank_keyword_task'
USER_RANK_KEYWORD_TASK_TYPE = 'user_rank_task'


MAX_ITEMS = 2**28

def key_words_search(task_id, search_type , pre , during , start_time , keyword_list , search_key = '' , sort_norm = '', sort_scope = ''  ,time = 7 , isall = False, number = 100):
    number = int(number)
    should = []
    for key in keyword_list:
        if search_type == "hashtag":
            should.append({"prefix":{"text": "#" +  key + "#"}})
        else:    
            should.append({"wildcard":{"text": "*" +key + "*"}})    
    index_list = []
    date = ts2datetime(start_time)
    index_name = pre + date
    while during:
        if es_flow_text.indices.exists(index=index_name):
            index_list.append(index_name)
            start_time = start_time + DAY
            date = ts2datetime(start_time)
            index_name = pre + date
            during -= 1

    print index_list
    uid_set = set()
    text_results = []
    sorted_text_results = []

    query_body = {
        "query":{
            "bool":{
                "must":should
             }
        },
        "sort":{"user_fansnum":{"order":"desc"}},
        "size":5000
    }
                    
    results = es_flow_text.search(index = index_list , doc_type = 'text' , body = query_body, _source=False, fields=["uid", "user_fansnum","text", "message_type", "sentiment","timestamp", "geo", "retweeted", "comment"])["hits"]["hits"]
    id_index = 0
    index_list = []
    un_uid_list = []
    for item in results :
        if item['fields']['uid'][0] not in uid_set:
            uid_set.add(item['fields']['uid'][0])
            un_uid_list.append(item['fields']['uid'][0])
            index_list.append(id_index)
        id_index += 1
    
    #get_all_filed(sort_norm , time)
    uid_list = []
    print "un_uid_list: ", len(un_uid_list)
    portrait_list = []
    count = 0
    in_index = 0
    if not isall and un_uid_list : # 库内
        portrait_results = es_user_portrait.mget(index=USER_INDEX_NAME, doc_type=USER_INDEX_TYPE, body={"ids":un_uid_list}, _source=False, fields=['uname'])["docs"]
        for item in portrait_results:
            if item["found"]:
                portrait_list.append(item['_id'])    
                nick_name = item['fields']['uname'][0]
                if nick_name == 'unknown':
                    nick_name = item['_id']
                index = index_list[in_index]
                weibo_url = weiboinfo2url(results[index]['fields']['uid'][0], results[index]['_id'])
                text_results.extend([results[index]['fields']['uid'][0], results[index]['fields']['user_fansnum'][0], results[index]['fields']['text'][0], results[index]['fields']['message_type'][0], results[index]['fields']['sentiment'][0], ts2date(results[index]['fields']['timestamp'][0]), results[index]['fields']['geo'][0], results[index]['fields']['retweeted'][0], results[index]['fields']['comment'][0], nick_name, weibo_url])
                count += 1
                if count == number:
                    break
                print "portrait_len, ", len(portrait_list)
            in_index += 1
        if portrait_list:
            uid_list = in_sort_filter(time,sort_norm ,sort_scope ,None , portrait_list , True, number) # sort
            for iter_uid in uid_list:
                iter_index = portrait_list.index(iter_uid)
                sorted_text_results.append(text_results[i])

    elif un_uid_list:
        profile_result = es_user_profile.mget(index="weibo_user", doc_type="user", body={"ids":un_uid_list}, fields=['nick_name'])["docs"]
        for i in range(len(profile_result)):
            index = index_list[i]
            try:
                nick_name = profile_result[i]['fields']['nick_name'][0]
            except:
                nick_name = un_uid_list[i]
            item = results[index]
            weibo_url = weiboinfo2url(item['fields']['uid'][0], results[index]['_id'])
            text_results.append([item['fields']['uid'][0], item['fields']['user_fansnum'][0], item['fields']['text'][0], item['fields']['message_type'][0], item['fields']['sentiment'][0], ts2date(item['fields']['timestamp'][0]), results[index]['fields']['geo'][0], results[index]['fields']['retweeted'][0], results[index]['fields']['comment'][0], nick_name, weibo_url])
            if i == number:
                break
        uid_list = all_sort_filter(un_uid_list[:number] , sort_norm , time ,True, number)
        sorted_text_results = []
        f = open("small.txt", "wb")
        for iter_uid in uid_list:
            iter_index = un_uid_list.index(iter_uid)
            f.write(str(iter_uid)+"\n")
            sorted_text_results.append(text_results[iter_index])
        f.close()
    print "filter_uid_list: ", len(uid_list)
    if uid_list:
        results = make_up_user_info(uid_list,isall,time,sort_norm)
    else:
        results = []
    print "results: ", len(results)
    # 修改状态
    task_detail = es_user_portrait.get(index=USER_RANK_KEYWORD_TASK_INDEX , doc_type=USER_RANK_KEYWORD_TASK_TYPE, id=task_id)
    item = task_detail['_source']
    item['status'] = 1
    item['result'] = json.dumps(results)
    item['text_results'] = json.dumps(sorted_text_results)
    item['number'] = len(results)
    es_user_portrait.index(index = USER_RANK_KEYWORD_TASK_INDEX , doc_type=USER_RANK_KEYWORD_TASK_TYPE , id=task_id,  body=item)

    return "1"



def scan_offline_task():
    
    query = {"query":{"bool":{"must":[{"term":{"status":0}}]}},"size":1000}
    results = es_user_portrait.search(index = USER_RANK_KEYWORD_TASK_INDEX , doc_type = USER_RANK_KEYWORD_TASK_TYPE,body=query)['hits']['hits']
    if results :
        for item in results:
            task_id = item['_id']
            iter_item = item['_source']
            search_type = iter_item['search_type']          
            pre = iter_item['pre']
            during =  iter_item['during'] 
            start_time =  iter_item['start_time']  
            keyword = json.loads(iter_item['keyword'])
            search_key = iter_item['user_ts']
            number = iter_item['number']
            sort_norm = iter_item['sort_norm']
            sort_scope = iter_item['sort_scope']
            time = iter_item['time']
            isall = iter_item['isall']
            redis_task.lpush("task_user_rank", json.dumps([task_id, search_type , pre , during , start_time , keyword , search_key , sort_norm , sort_scope  ,time , isall, number]))
            iter_item['status'] = -1 
            task_id = item['_id']
            #print item
            es_user_portrait.index(index=USER_RANK_KEYWORD_TASK_INDEX, doc_type=USER_RANK_KEYWORD_TASK_TYPE, id=task_id, body=iter_item)


def cron_task(data):
    key_words_search(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11])
    

if __name__ == "__main__":

    scan_offline_task()
    while 1:
        data = redis_task.rpop("task_user_rank")
        print data
        #"""
        if data:
            try:
                cron_task(json.loads(data))
            except Exception, e:
                print e, '&error&', ts2date(time.time())
        else:
            break
        #"""
            
    
