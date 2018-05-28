#-*- coding:utf-8 -*-
from elasticsearch import Elasticsearch
import math
import sys
import datetime
from time_utils import ts2datetime, datetime2ts
from INDEX_TABLE import *
from global_utils import es_user_portrait
from global_utils import es_user_profile
import time as TIME
DAY = 24*3600
USER_INDEX_NAME = 'user_portrait_1222'
USER_INDEX_TYPE = 'user'

WEBUSER_INDEX_NAME = "weibo_user"
WEBUSER_INDEX_TYPE = "user"

# rewrite make_up_user_info
def make_up_user_info(user_list = [] , isall = False, time = 1, sort_norm = "bci" ):
    result_info = []
    today = str(datetime.date.today())
    timestamp = datetime2ts(today)

    if user_list:
        if isall:
            result_info = all_makeup_info(user_list , sort_norm, time)
        else:
            result_info = in_makeup_info(user_list, sort_norm , time)

    return result_info
"""


def make_up_user_info(user_list = [] , isall = False, time = 1, sort_norm = "bci" ):
    result_info = []
    print "sort_norm", sort_norm
    
    today = str(datetime.date.today())
    timestamp = datetime2ts(today)
    if user_list:
        for id in user_list:
            item = {}
            if isall :
                item = all_makeup_info(id , sort_norm , time )
            else:
                item = in_makeup_info(id , sort_norm , time)
            result_info.append(item)
        return result_info
    else:
        return []
"""
# rewrite all_makeup_info
# enter: uid_list
# output result info
def all_makeup_info(uid_list , sort_norm , time):
    es = es_user_profile
    field_bci ,field_sen, field_weibo = get_all_filed(sort_norm , time) 
    search_result = es.mget(index=WEBUSER_INDEX_NAME , doc_type=WEBUSER_INDEX_TYPE, body={"ids":uid_list})["docs"]
    current_ts = datetime2ts(ts2datetime(TIME.time()-DAY))
    bci_result = es.mget(index="bci_history", doc_type="bci", body={"ids":uid_list}, fields=[field_bci, "user_fansnum", field_weibo, "weibo_month_sum"])["docs"]
    sen_result = es.mget(index=SESHIS_INDEX_NAME, doc_type=SESHIS_INDEX_TYPE, body={"ids":uid_list}, fields=[field_sen])["docs"]
    in_portrait = es_user_portrait.mget(index=USER_INDEX_NAME, doc_type=USER_INDEX_TYPE, body={"ids":uid_list}, _source=False)["docs"]
    results = []
    #fans_result = es_user_profile.mget(index="bci_history", doc_type="bci", body={"ids":uid_list}, fields=["user_fansnum"], _source=False)["docs"]
    bci_max = get_max_value(es_user_profile, "bci_history", "bci", field_bci)
    sen_max = get_max_value(es_user_profile, "sensitive_history", "sensitive", field_sen)
    for i in range(len(uid_list)):
        tmp = dict()
        tmp['uid'] = uid_list[i]
        if search_result[i]['found']:
            iter_item = search_result[i]['_source']
            tmp['location'] = iter_item['user_location']
            tmp['uname'] = iter_item['nick_name']
            tmp['photo_url'] = iter_item['photo_url']
        else:
            tmp['location'] = None
            tmp['uname'] = tmp['uid']
            tmp['photo_url'] = 'unknown'
        if in_portrait[i]['found']:
            tmp['is_warehousing'] = True
        else:
            tmp['is_warehousing'] = False
        if bci_result[i]['found']:
            try:
                bci_value = bci_result[i]['fields'][field_bci][0]
                tmp['bci'] = math.log(bci_value/float(bci_max)*9+1,10)*100
            except:
                tmp['bci'] = 0
            try:
                tmp['fans'] = bci_result[i]['fields']["user_fansnum"][0]
            except:
                tmp['fans'] = ''
            try:
                tmp["weibo_count"] = bci_result[i]['fields']["weibo_month_sum"][0]
            except:
                tmp["weibo_count"] = ''
        else:
            tmp['bci'] = None
            tmp['fans'] = None
            tmp["weibo_count"] = None
        if sen_result[i]['found']:
            try:
                sen_value = sen_result[i]['fields'][field_sen][0]
                tmp['sen'] = math.log(sen_value/float(sen_max)*9+1,10)*100
            except:
                tmp['sen'] = 0
        else:
            tmp['sen'] = None

        results.append(tmp)
    return results



def in_makeup_info(uid_list , sort_norm , time):
    es = es_user_portrait
    search_results = []
    results = []
    ts = datetime2ts(ts2datetime(TIME.time()-DAY))
    field_bci , field_sen ,field_imp ,field_act = get_in_filed(sort_norm,time)
    field_dict = {"uid":"uid","uname":"uname","location":"location","photo_url":"photo_url","topic":"topic_string","domain":"domain","fans":"fansnum", "act":"activeness", "imp":"importance", "bci":"influence"}#
    if uid_list:
        search_results = es_user_portrait.mget(index=USER_INDEX_NAME, doc_type=USER_INDEX_TYPE, body={"ids":uid_list}, _source=False, fields=["uid","uname","location","photo_url","topic_string","domain","fansnum", "influence", "importance", "activeness"])["docs"]#, "sensitive"
        #print '11111',USER_INDEX_NAME,USER_INDEX_TYPE
        bci_results = es.mget(index=BCI_INDEX_NAME, doc_type=BCI_INDEX_TYPE, body={"ids":uid_list}, _source=False, fields=[field_bci,"user_fansnum", "weibo_month_sum"])["docs"]
        imp_results = es.mget(index=IMP_INDEX_NAME, doc_type=IMP_INDEX_TYPE, body={"ids":uid_list}, _source=False, fields=[field_imp])["docs"]
        act_results = es.mget(index=ACT_INDEX_NAME, doc_type=ACT_INDEX_TYPE, body={"ids":uid_list}, _source=False, fields=[field_act])["docs"]
        sen_results = es.mget(index=SES_INDEX_NAME, doc_type=SES_INDEX_TYPE, body={"ids":uid_list}, _source=False, fields=[field_sen])["docs"]
        
        results = []
        for i in range(len(uid_list)):
            item = dict()
            if not search_results[i].get('found', 0):
                continue
            for k,v in field_dict.iteritems():
                item[k] = search_results[i]["fields"][v][0]
                if k == "uname" and not item[k]:
                    item[k] = uid_list[i]


            try:
                act_value = act_results[i]['fields'][field_act][0]
                item['act'] = act_value
            except:
                item['act'] = 0
            try:
                imp_value = imp_results[i]['fields'][field_imp][0]
                item['ipm'] = imp_value
            except:
                item['ipm'] = 0
            try:
                user_fansnum = bci_results[i]['fields']['user_fansnum'][0]
                item['fans'] = user_fansnum
            except:
                item['fans'] = ''
            try:
                bci_value = bci_results[i]['fields'][field_bci][0]
                item['bci'] = bci_value
            except:
                item['bci'] = 0 
            # try:
            #     sen_value = sen_results[i]['fields'][field_sen][0]
            #     tmp['sen'] = sen_value
            # except:
            #     item['sen'] = 0
            
            results.append(item)

    return results
    
  
"""
def in_makeup_info(id , sort_norm , time):
    es = es_user_portrait
    item = {}
    query = {"query":{"bool":{"must":[{"term":{"user.uid":id}}],"must_not":[],"should":[]}},"from":0,"size":10,"sort":[],"facets":{},"fields":["uid","uname","location","topic_string","domain","fansnum"]}
    result = es.search(index=USER_INDEX_NAME , doc_type=USER_INDEX_TYPE , body=query)['hits']
    if result['total'] != 0 :
        item['domain'] = result['hits'][0]['fields']['domain'][0]
        item['uid'] = result['hits'][0]['fields']['uid'][0]
        item['topic'] = result['hits'][0]['fields']['topic_string'][0]
        item['location'] = result['hits'][0]['fields']['location'][0]
        item['uname'] = result['hits'][0]['fields']['uname'][0]
        item['fans'] = result['hits'][0]['fields']['fansnum'][0]
    else :
        item['domain'] = None
        item['uid'] = None
        item['topic'] = None
        item['location'] = None
        item['uname'] = None
        item['fans'] = None

    item['uid'] = id
    field_bci , field_sen ,field_imp ,field_act = get_in_filed(sort_norm,time)
    
    item['bci'] = history_info(BCI_INDEX_NAME,BCI_INDEX_TYPE,id,field_bci)
    item['sen'] = history_info(SES_INDEX_NAME,SES_INDEX_TYPE,id,field_sen)
    item['imp'] = history_info(IMP_INDEX_NAME,IMP_INDEX_TYPE,id,field_imp)
    item['act'] = history_info(ACT_INDEX_NAME,ACT_INDEX_TYPE,id,field_act)
    return item
"""

def history_info(index_name , index_type , uid , fields):
    if index_name == BCIHIS_INDEX_NAME or index_name == SESHIS_INDEX_NAME:
        es = es_user_profile
    else:
        es = es_user_portrait
    
    length = len(fields)
    print '-----'
    print fields
    
    query = {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "term": {
                                    "uid": uid
                                }
                            }
                        ]
                    }
                },
                "fields": fields
            }
    result = es.search(index = index_name , doc_type = index_type , body = query)
    print result
    results = es.get(index=index_name, doc_type = index_type, id=uid, fields=[fields])
    print results
    if result['timed_out'] == False and result['hits']['total'] != 0 :
        item = result['hits']['hits'][0]['fields']
        return item[fields][0]
    else :
        return None


def get_all_filed(sort_norm , time):
    ts = datetime2ts(ts2datetime(TIME.time() - DAY))
    field_bci = 'bci_day_last'
    field_weibo = "weibo_month_sum"
    field_sen = 'sensitive_score_%s'%ts
    if sort_norm == "weibo_num":
        if time == 1:
            field_weibo = 'weibo_day_last'
        if time == 7:
            field_weibo = "weibo_week_sum"
        elif time == 30:
            field_weibo = "weibo_month_sum"
        else:
            pass
    if sort_norm == 'bci':
        if time == 1:
            field_bci = 'bci_day_last'
        elif time == 7:
            field_bci = 'bci_week_ave'
        else:
            field_bci = 'bci_month_ave'
    elif sort_norm == 'bci_change':
        if time == 1:
            field_bci = 'bci_day_change'
        elif time == 7:
            field_bci = 'bci_week_change'
        else:
            field_bci = 'bci_month_change'
    elif sort_norm == 'ses':
        if time == 1:
            field_sen = 'sensitive_score_%s'%ts
        elif time == 7:
            field_sen = 'sensitive_week_ave'
        else:
            field_sen = 'senstiive_month_ave'
    elif sort_norm == 'ses_change':
        if time == 1:
            field_sen = 'sensitive_day_change'
        elif time == 7:
            field_sen = 'sensitive_week_change'
        else:
            field_sen = 'sensitive_month_change'
    return  field_bci, field_sen, field_weibo


def get_in_filed(sort_norm , time):

    field_bci = 'bci_week_ave'
    field_sen = 'sensitive_week_ave'
    field_imp = 'importance_week_ave'
    field_act = 'activeness_week_ave'
    ts = datetime2ts(ts2datetime(TIME.time() - DAY))

    if sort_norm == 'bci':
        if int(time) == 1:
            field_bci = 'bci_day_last'
        elif int(time) == 7:
            field_bci = 'bci_week_ave'
        else:
            field_bci = 'bci_month_ave'
    elif sort_norm == 'bci_change':
        if int(time) == 1:
            field_bci = 'bci_day_change'
        elif int(time) == 7:
            field_bci = 'bci_week_change'
        else:
            field_bci = 'bci_month_change'
    elif sort_norm == 'ses':
        if int(time) == 1:
            field_sen = 'sensitive_score_%s'%ts
        elif int(time) == 7:
            field_sen = 'sensitive_week_ave'
        else:
            field_sen = 'sensitive_month_ave'
    elif sort_norm == 'ses_change':
        if int(time) == 1:
            field_sen = 'sensitive_day_change'
        elif int(time) == 7:
            field_sen = 'sensitive_week_change'
        else:
            field_sen = 'sensitive_month_change'
    elif sort_norm == 'imp':
        if int(time) == 1:
            field_imp = 'importance_day_change'
        elif int(time) == 7:
            field_imp = 'importance_week_ave'
        else:
            field_imp = 'importance_month_ave'
    elif sort_norm == 'imp_change':
        if int(time) == 1:
            field_imp = 'importance_day_change'
        elif int(time) == 7:
            field_imp = 'importance_week_change'
        else:
            field_imp = 'importance_month_change'
    elif sort_norm == 'act':
        if int(time) == 1:
            field_act = 'activeness_day_change'
        elif int(time) == 7:
            field_act = 'activeness_week_ave'
        else:
            field_act = 'activeness_month_ave'
    elif sort_norm == 'act_change':
        if int(time) == 1:
            field_act = 'activeness_day_change'
        elif int(time) == 7:
            field_act = 'activeness_week_change'
        else:
            field_act = 'activeness_month_change'
    return  field_bci, field_sen, field_imp,field_act
 

def get_max_value(es, index_name, _type, key):
    query_body = {
        "query":{
            "match_all": {}
        },
        "sort":{key:{"order":"desc"}},
        "size": 1
    }

    max_value = 1
    try:
        result = es.search(index=index_name, doc_type=_type, body=query_body)['hits']['hits']
    except:
        result = []
    if result:
        max_value = result[0]['_source'][key]

    return max_value
