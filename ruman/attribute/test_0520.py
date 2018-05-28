# -*- coding:utf-8 -*-
import csv
import sys
import json
import time
sys.path.append('../')
from global_utils import es_user_portrait, portrait_index_name, portrait_index_type
from global_utils import es_retweet, retweet_index_name_pre, retweet_index_type
from global_utils import be_retweet_index_name_pre, be_retweet_index_type
from global_utils import es_comment, comment_index_name_pre, comment_index_type,\
                         be_comment_index_name_pre, be_comment_index_type
from global_utils import R_CLUSTER_FLOW2 as r_cluster
from global_utils import ES_COPY_USER_PORTRAIT, COPY_USER_PORTRAIT_INFLUENCE, COPY_USER_PORTRAIT_INFLUENCE_TYPE,\
COPY_USER_PORTRAIT_IMPORTANCE, COPY_USER_PORTRAIT_IMPORTANCE_TYPE, COPY_USER_PORTRAIT_ACTIVENESS, COPY_USER_PORTRAIT_ACTIVENESS_TYPE, COPY_USER_PORTRAIT_SENSITIVE, COPY_USER_PORTRAIT_SENSITIVE_TYPE
from global_config import R_BEGIN_TIME
from time_utils import ts2datetime, datetime2ts
from parameter import DAY


r_beigin_ts = datetime2ts(R_BEGIN_TIME)

def get_db_num(timestamp):
    date = ts2datetime(timestamp)
    date_ts = datetime2ts(date)
    db_number = ((date_ts - r_beigin_ts) / (DAY*7)) %2 +1
    return db_number



def search_get_portrait():
    query_body = {
    'query':{
        'wildcard':{'keywords_string': '*' + '文革' + '*'}
        },
    'size': 1000
    }
    #try:
    result = es_user_portrait.search(index=portrait_index_name, doc_type=portrait_index_type,\
           body=query_body)['hits']['hits']
    #except:
    #    result = []
    f = open('/home/user_portrait_0320/revised_user_portrait/user_portrait/user_portrait/attribute/uid_list_0520.txt', 'w')
    for item in result:
        source = item['_source']
        uid = source['uid']
        f.write("%s\n" % uid )
        #print 'source:', source
    f.close()

def get_user_social_data():
    #get uid list
    f_uid_list = open('/home/user_portrait_0320/revised_user_portrait/user_portrait/user_portrait/attribute/uid_list_0520.txt', 'r')
    count = 0
    uid_list = []
    for line in f_uid_list:
        uid = line[:-1]
        count += 1
        uid_list.append(uid)
    f_uid_list.close()
    f_retweet = open('/home/user_portrait_0320/revised_user_portrait/user_portrait/user_portrait/attribute/user_be_comment.txt', 'w')
    db_number = get_db_num(datetime2ts(ts2datetime(time.time())))
    index_name = be_comment_index_name_pre + str(db_number)
    for uid in uid_list:
        #retweet
        try:
            retweet_result  = es_comment.get(index=index_name, doc_type=be_comment_index_type, id=uid)['_source']
        except:
            retweet_result = {}
        if retweet_result:
            f_retweet.write('%s\n' % json.dumps(retweet_result))
    f_retweet.close()
        
def get_uid_list():
    f_uid_list = open('/home/user_portrait_0320/revised_user_portrait/user_portrait/user_portrait/attribute/uid_list_0520.txt', 'r')
    uid_list = []
    for line in f_uid_list:
        uid = line[:-1]
        uid_list.append(uid)
    f_uid_list.close()
    return uid_list

def get_user_at():
    #step1: get_uid_list
    uid_list = get_uid_list()
    date = ts2datetime(time.time())
    ts = datetime2ts(date)
    f = open('/home/user_portrait_0320/revised_user_portrait/user_portrait/user_portrait/attribute/uid_at.txt', 'w')
    for i in range(1, 8):
        ts = ts - DAY
        for uid in uid_list:
            #try:
            result_string = r_cluster.hget('at_' + str(ts), uid)
            #except:
            #    result_string = ''
            if result_string:
                save_dict = {'ts': ts, 'result': result_string}
                f.write('%s\n' % json.dumps(save_dict))
    f.close()

def get_evaluate_trend():
    #get uid list
    uid_list = get_uid_list()
    #save influence trend es result
    f = open('/home/user_portrait_0320/revised_user_portrait/user_portrait/user_portrait/attribute/sensitive_trend.txt', 'w')
    for uid in uid_list:
        #try:
        influence_history = ES_COPY_USER_PORTRAIT.get(index=COPY_USER_PORTRAIT_SENSITIVE, doc_type=COPY_USER_PORTRAIT_SENSITIVE_TYPE, id=uid)['_source']
        #except:
        #    influence_history = {}
        if influence_history:
            f.write('%s\n' % json.dumps(influence_history))
    f.close()
    

if __name__=='__main__':
    #search_get_portrait()
    #get_user_social_data()
    #get_user_at()
    get_evaluate_trend()
