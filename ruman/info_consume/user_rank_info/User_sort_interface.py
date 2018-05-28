#-*- coding:utf-8 -*-
from in_filter import in_sort_filter
from Offline_task import add_task
from all_filter import all_sort_filter
from Keyword_task import key_words_search
from time_utils import ts2datetime, datetime2ts
from ruman.parameter import DAY, LOW_INFLUENCE_THRESHOULD
from Makeup_info import make_up_user_info
import json
#from global_utils import es_user_portrait
from ruman.global_utils import es_user_portrait

def query_task_number(user_name):
    query_body = {
        "query":{
            "filtered":{
                "filter":{
                    "bool":{
                        "must":[
                            {"terms":{
                                "status": [0,-1]
                            }},
                            {"term":{
                                'submit_user' : user_name
                            }}      
                        ]
                    }
                }
            }
        }
    }

    return query_body

def user_sort_interface(username , time ,sort_scope , sort_norm , arg = None, st = None, et = None, isall = False, task_number=0, number=100):

    task_number = int(task_number)
    # print "user_interface:", number
    user_list = []
    if isall:
        #deal with the situation of all net user
        if sort_scope == 'all_limit_keyword':
            #offline job
            #add job to es index
            during = ( datetime2ts(et) - datetime2ts(st) ) / DAY + 1
            time = 7
            if during > 3:
                time = 7
            elif during > 16:
                time = 30
            running_number = es_user_portrait.count(index='user_rank_keyword_task', doc_type='user_rank_task', body=query_task_number(username))['count']
            # print 'running',running_number
            if running_number > task_number-1:
                return "more than limit"
            search_id = add_task( username ,"keyword" , "all" ,'flow_text_' , during , st ,et, arg , sort_norm , sort_scope, time, isall, number)
            #deal with the offline task   
            return {"flag":True , "search_id" : search_id }
        elif sort_scope == 'all_nolimit':
            #online job
            # print "all_sort, ", number,sort_norm
            user_list = all_sort_filter(None,sort_norm,time,False,number)
    else:
        if sort_scope == 'in_limit_keyword':
            #offline job
            #deal with the offline task
            during = ( datetime2ts(et) - datetime2ts(st) ) / DAY + 1
            time = 1
            if during > 3:
                time = 7
            elif during > 16:
                time = 30
            running_number = es_user_portrait.count(index='user_rank_keyword_task', doc_type='user_rank_task', body=query_task_number(username))['count']
            if running_number > task_number-1:
                return "more than limit"
            search_id = add_task( username ,"keyword" , "in" ,'flow_text_' , during , st ,et , arg , sort_norm , sort_scope, time, isall, number)
            return {"flag":True , "search_id" : search_id }
        elif sort_scope == 'in_limit_hashtag':
            during = ( datetime2ts(et) - datetime2ts(st) ) / DAY + 1
            time = 7
            if during > 3:
                time = 7
            elif during > 16:
                time = 30
            running_number = es_user_portrait.count(index='user_rank_keyword_task', doc_type='user_rank_task', body=query_task_number(username))['count']
            if running_number > task_number-1:
                return "more than limit"
            search_id = add_task( username ,"hashtag" , "in" ,'flow_text_' , during , st ,et, arg , sort_norm , sort_scope, time, isall,  number)
            return {"flag":True , "search_id" : search_id }
        else:
            #find the scope
            #in_limit_topic
            user_list = in_sort_filter(time , sort_norm,sort_scope , arg,[], False, number)
            #print user_list
    result = make_up_user_info(user_list,isall , time , sort_norm)
    # print "user_list:", len(user_list)
    return result
    
if __name__ == "__main__":    
    print json.dumps(user_sort_interface(username = "kanon", time = 1, sort_scope =  "all_limit_keyword", sort_norm = "bci" , arg = 'hello' , st = "2016-11-21"  ,et =  "2016-11-21" , isall = True) )
            
            
