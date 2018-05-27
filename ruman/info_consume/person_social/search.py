# -*- coding: UTF-8 -*-
'''
search attribute : attention, follower, mention, location, activity
'''
from IPy import IP
import sys
import csv
import time
import json
import math
import redis

from ruman.time_utils import ts2datetime, datetime2ts, ts2date, datetimestr2ts

from ruman.global_utils import R_CLUSTER_FLOW2 as r_cluster
from ruman.global_utils import R_DICT
from ruman.global_utils import es_user_portrait, portrait_index_name, portrait_index_type
from ruman.global_utils import es_user_profile, profile_index_name, profile_index_type
from ruman.global_utils import es_flow_text, flow_text_index_name_pre, flow_text_index_type
from ruman.global_utils import es_retweet,es_fans, es_comment, es_be_comment, es_copy_portrait
from ruman.global_utils import retweet_index_name_pre, retweet_index_type
from ruman.global_utils import be_retweet_index_name_pre, fans_index_type,be_retweet_index_type
from ruman.global_utils import comment_index_name_pre, comment_index_type
from ruman.global_utils import be_comment_index_name_pre,fans_index_name, be_comment_index_type
from ruman.global_utils import copy_portrait_index_name, copy_portrait_index_type
from ruman.global_utils import R_RECOMMENTATION as r_recomment
from ruman.global_utils import es_bci_history, bci_history_index_name, bci_history_index_type
from ruman.global_config import R_BEGIN_TIME
from ruman.parameter import DAY, WEEK, MAX_VALUE, HALF_HOUR, FOUR_HOUR, GEO_COUNT_THRESHOLD, PATTERN_THRESHOLD
from ruman.parameter import PSY_DESCRIPTION_FIELD, psy_en2ch_dict, psy_description_dict
from ruman.search_user_profile import search_uid2uname
from ruman.filter_uid import all_delete_uid
from ruman.parameter import IP_TIME_SEGMENT, IP_TOP, DAY, IP_CONCLUSION_TOP, domain_en2ch_dict, topic_en2ch_dict
from ruman.parameter import INFLUENCE_TREND_SPAN_THRESHOLD, INFLUENCE_TREND_AVE_MIN_THRESHOLD,\
                                    INFLUENCE_TREND_AVE_MAX_THRESHOLD, INFLUENCE_TREND_DESCRIPTION_TEXT
from ruman.parameter import ACTIVENESS_TREND_SPAN_THRESHOLD, ACTIVENESS_TREND_AVE_MIN_THRESHOLD ,\
                                    ACTIVENESS_TREND_AVE_MAX_THRESHOLD, ACTIVENESS_TREND_DESCRIPTION_TEXT
from ruman.parameter import SENTIMENT_DICT,  ACTIVENESS_TREND_TAG_VECTOR
from ruman.parameter import SENTIMENT_SECOND
from ruman.parameter import RUN_TYPE, RUN_TEST_TIME
from ruman.keyword_filter import keyword_filter

r_beigin_ts = datetime2ts(R_BEGIN_TIME)

WEEK = 7

emotion_mark_dict = {'126': 'positive', '127':'negative', '128':'anxiety', '129':'angry'}
link_ratio_threshold = [0, 0.5, 1]

if RUN_TYPE == 0:
    fields = ['bci_week_sum', 'bci_month_ave', 'bci_month_sum','bci_week_ave']
else:
    fields = ['user_fansnum', 'weibo_month_sum', 'user_friendsnum','bci_week_ave']

def search_follower(uid, top_count):

    results = {}
    now_ts = time.time()
    db_number = get_db_num(now_ts)
    index_name = be_retweet_index_name_pre + str(db_number)
    # return search_user_info(es_retweet,index_name,retweet_index_type,uid,'uid_be_retweet')
    center_uid = uid
    try:
        retweet_result = es_retweet.get(index=index_name, doc_type=be_retweet_index_type, id=uid)['_source']
    except:
        return None
    retweet_dict={}
    if retweet_result:
        retweet_dict_old = json.loads(retweet_result['uid_be_retweet'])
        for key in retweet_dict_old:
            retweet_dict[key]=int(retweet_dict_old[key])
        sorted_list = sorted(retweet_dict.iteritems(),key=lambda x:x[1],reverse=True)[:20]
        uid_list = [i[0] for i in sorted_list if i[0] != uid]
        portrait_result = []
        try:
            user_result = es_user_profile.mget(index=profile_index_name, doc_type=profile_index_type, body={'ids':uid_list})['docs']
        except:
            user_result = []

        try:
            bci_history_result = es_bci_history.mget(index=bci_history_index_name, doc_type=bci_history_index_type, body={'ids':uid_list}, fields=fields)['docs']    
        except:
            bci_history_result = []
        # print bci_history_result
        iter_count = 0
        out_portrait_list = []
        for out_user_item in user_result:
            uid = out_user_item['_id']
            if out_user_item['found'] == True:
                source = out_user_item['_source']
                uname = source['nick_name']
                photo_url = source['photo_url']
                if uname == '':
                    uname = u'未知'
                #location = source['user_location']
                friendsnum = source['friendsnum']

            else:
                uname = u'未知'
                location = ''
                friendsnum = ''
                photo_url = ''

            #add index from bci_history
            try:
                bci_history_item = bci_history_result[iter_count]
            except:
                bci_history_item = {'found': False}
            if bci_history_item['found']==True:
                fansnum = bci_history_item['fields'][fields[0]][0]
                user_weibo_count = bci_history_item['fields'][fields[1]][0]
                user_friendsnum = bci_history_item['fields'][fields[2]][0]
                influence = bci_history_item['fields'][fields[3]][0]
            else:
                fansnum = ''
                user_weibo_count = ''
                user_friendsnum = ''
                influence = ''
            #retweet_count = int(retweet_dict[uid])
            print uid
            count = retweet_dict[uid]
            print count
            out_portrait_list.append({'uid':uid,'photo_url':photo_url,'count':count,'uname':uname,'influence':influence,'fansnum':fansnum, 'friendsnum':user_friendsnum,'weibo_count':user_weibo_count})#location,
            iter_count += 1
        return out_portrait_list
    else:
        return None
    # #sort_retweet_result = sorted(retweet_dict.items(), key=lambda x:x[1], reverse=True)


def search_attention(uid, top_count):

    results = {}
    now_ts = time.time()
    db_number = get_db_num(now_ts)
    index_name = retweet_index_name_pre + str(db_number)
    center_uid = uid
    # print es_retweet,index_name,retweet_index_type,uid
    try:
        retweet_result = es_retweet.get(index=index_name, doc_type=retweet_index_type, id=uid)['_source']
    except:
        return None
    if retweet_result:
        retweet_dict = json.loads(retweet_result['uid_retweet'])
        sorted_list = sorted(retweet_dict.iteritems(),key=lambda x:x[1],reverse=True)[:20]
        uid_list = [i[0] for i in sorted_list if i[0] != uid]
        portrait_result = []
        try:
            user_result = es_user_profile.mget(index=profile_index_name, doc_type=profile_index_type, body={'ids':uid_list})['docs']
        except:
            user_result = []
        try:
            bci_history_result = es_bci_history.mget(index=bci_history_index_name, doc_type=bci_history_index_type, body={'ids':uid_list}, fields=fields)['docs']    
        except:
            bci_history_result = []
        # print bci_history_result
        iter_count = 0
        out_portrait_list = []
        for out_user_item in user_result:
            uid = out_user_item['_id']
            if out_user_item['found'] == True:
                source = out_user_item['_source']
                uname = source['nick_name']
                photo_url = source['photo_url']
                if uname == '':
                    uname = u'未知'
                #location = source['user_location']
                friendsnum = source['friendsnum']
            else:
                uname = u'未知'
                location = ''
                friendsnum = ''
                photo_url = 'unknown'

            #add index from bci_history
            try:
                bci_history_item = bci_history_result[iter_count]
            except:
                bci_history_item = {'found': False}
            if bci_history_item['found']==True:
                fansnum = bci_history_item['fields'][fields[0]][0]
                user_weibo_count = bci_history_item['fields'][fields[1]][0]
                user_friendsnum = bci_history_item['fields'][fields[2]][0]
                influence = bci_history_item['fields'][fields[3]][0]
            else:
                fansnum = ''
                user_weibo_count = ''
                user_friendsnum = ''
                influence = ''
            #retweet_count = int(retweet_dict[uid])
            count = retweet_dict[uid]
            out_portrait_list.append({'uid':uid,'photo_url':photo_url,'count':count,'uname':uname,'influence':influence,'fansnum':fansnum, 'friendsnum':user_friendsnum,'weibo_count':user_weibo_count})#location,
            iter_count += 1
        return out_portrait_list
    else:
        return None
    #sort_retweet_result = sorted(retweet_dict.items(), key=lambda x:x[1], reverse=True)



def search_yangshi_follower(uid, top_count):
    results = {}
    now_ts = time.time()
    db_number = get_db_num(now_ts)
    index_name = be_retweet_index_name_pre + str(db_number)
    center_uid = uid
    try:
        retweet_result = es_retweet.get(index=index_name, doc_type=be_retweet_index_type, id=uid)['_source']
    except:
        return None
    # print retweet_result
    if retweet_result:
        retweet_dict = json.loads(retweet_result['uid_be_retweet'])
        sorted_list = sorted(retweet_dict.iteritems(),key=lambda x:x[1],reverse=True)[:20]
        uid_list = [i[0] for i in sorted_list if i[0] != uid]
        portrait_result = []
        try:
            user_result = es_user_profile.mget(index=profile_index_name, doc_type=profile_index_type, body={'ids':uid_list})['docs']
        except:
            user_result = []

        iter_count = 0
        out_portrait_list = []
        for out_user_item in user_result:
            uid = out_user_item['_id']
            if out_user_item['found'] == True:
                source = out_user_item['_source']
                uname = source['nick_name']
                if uname == '':
                    uname = u'未知'

            else:
                uname = u'未知'


            #retweet_count = int(retweet_dict[uid])
            count = retweet_dict[uid]
            out_portrait_list.append({'uid':uid,'count':count,'uname':uname})#location,
            iter_count += 1
        return out_portrait_list
    else:
        return None
    #sort_retweet_result = sorted(retweet_dict.items(), key=lambda x:x[1], reverse=True)


def search_yangshi_attention(uid, top_count):

    results = {}
    now_ts = time.time()
    db_number = get_db_num(now_ts)
    index_name = retweet_index_name_pre + str(db_number)
    center_uid = uid
    # print es_retweet,index_name,retweet_index_type,uid
    try:
        retweet_result = es_retweet.get(index=index_name, doc_type=retweet_index_type, id=uid)['_source']
    except:
        return None
    if retweet_result:
        retweet_dict = json.loads(retweet_result['uid_retweet'])
        sorted_list = sorted(retweet_dict.iteritems(),key=lambda x:x[1],reverse=True)[:20]
        uid_list = [i[0] for i in sorted_list if i[0] != uid]
        portrait_result = []
        try:
            user_result = es_user_profile.mget(index=profile_index_name, doc_type=profile_index_type, body={'ids':uid_list})['docs']
        except:
            user_result = []

        iter_count = 0
        out_portrait_list = []
        for out_user_item in user_result:
            uid = out_user_item['_id']
            if out_user_item['found'] == True:
                source = out_user_item['_source']
                uname = source['nick_name']
                if uname == '':
                    uname = u'未知'

            else:
                uname = u'未知'

            count = retweet_dict[uid]
            out_portrait_list.append({'uid':uid,'count':count,'uname':uname,})#location,
            iter_count += 1
        return out_portrait_list
    else:
        return None
    #sort_retweet_result = sorted(retweet_dict.items(), key=lambda x:x[1], reverse=True)



#search:now_ts , uid return 7day at uid list  {uid1:count1, uid2:count2}
#{'at_'+Date:{str(uid):'{at_uid:count}'}}
#return results:{at_uid:[uname,count]}
def search_mention(now_ts, uid, top_count):
    date = ts2datetime(now_ts)
    #evaluate_max_dict = get_evaluate_max()
    ts = datetime2ts(date)
    stat_results = dict()
    results = dict()
    uid_dict = {}
    for i in range(1,8):
        ts = ts - DAY
        try:
            result_string = r_cluster.hget('at_' + str(ts), str(uid))
        except:
            result_string = ''
        if not result_string:
            continue
        result_dict = json.loads(result_string)
        for at_uname in result_dict:
            try:
                stat_results[at_uname] += result_dict[at_uname]
            except:
                stat_results[at_uname] = result_dict[at_uname]
    sort_stat_results = sorted(stat_results.items(), key=lambda x:x[1], reverse=True)
    # print sort_stat_results

    out_portrait_list = []
    out_list = stat_results.keys()

    #use to get user information from user profile
    out_query_list = [{'match':{'uname':item}} for item in out_list]
    if len(out_query_list) != 0:
        query = [{'bool':{'should': out_query_list}}]
        try:
            out_profile_result = es_user_profile.search(index=profile_index_name, doc_type=profile_index_type, body={'query':{'bool':{'must':query}}, 'size':100})['hits']['hits']
        except:
            out_profile_result = []
    else:
        out_profile_result = []
    out_in_profile_list = []
    bci_search_id_list = []

    for out_item in out_profile_result:
        source = out_item['_source']
        uname = source['nick_name']
        uid = source['uid']
        location = source['location']
        friendsnum = source['friendsnum']
        out_portrait_list.append([uid, uname, stat_results[uname], '', location, friendsnum, ''])
        out_in_profile_list.append(uname)
        #use to search bci history
        bci_search_id_list.append(uid)
    out_out_profile_list = list(set(out_list) - set(out_in_profile_list))
    for out_out_item in out_out_profile_list:
        out_portrait_list.append(['', out_out_item, stat_results[out_out_item],'', '', '', ''])
    
    #add index from bci_history
    new_out_portrait_list = []
    try:
        bci_history_result = es_bci_history.mget(index=bci_history_index_name, doc_type=bci_history_index_type, body={'ids': bci_search_id_list}, fields=['user_fansnum', 'weibo_month_sum', 'user_friendsnum'])['docs']
    except:
        bci_history_result = []
    iter_count = 0
    for out_portrait_item in out_portrait_list:
        append_dict = {}
        try:
            bci_history_item = bci_history_result[iter_count]
        except:
            bci_history_item = {}
        new_out_portrait_item = out_portrait_item
        append_dict['uid'] = out_portrait_item[0]
        append_dict['uname'] = out_portrait_item[1]
        append_dict['count'] = out_portrait_item[2]
        if bci_history_item:
            if bci_history_item['found'] == True:
                fansnum = bci_history_item['fields']['user_fansnum'][0]
                user_weibo_count = bci_history_item['fields']['weibo_month_sum'][0]
                user_friendsnum = bci_history_item['fields']['user_friendsnum'][0]
            else:
                fansnum = ''
                user_weibo_count = ''
                user_friendsnum = ''
        else:
            fansnum = ''
            user_weibo_count = ''
            user_friendsnum = ''
        append_dict['fansnum'] = fansnum
        append_dict['weibo_count'] = user_weibo_count
        append_dict['friendsnum'] = user_friendsnum
        # new_out_portrait_item[3] = fansnum
        # new_out_portrait_item[6] = user_weibo_count
        # new_out_portrait_item[-2] = user_friendsnum
        #new_out_portrait_list.append(new_out_portrait_item)
        new_out_portrait_list.append(append_dict)
        iter_count += 1
        #print append_dict
    return new_out_portrait_list  #  uid，名字，提及次数,粉丝数，注册地，关注数，微博数



#use to get user be_comment from es: be_comment_1, be_comment_2
#write in version: 15-12-08
#input: uid, top_count
#output: in_portrait_list, in_portrait_result, out_portrait_list
def search_be_comment(uid, top_count):
    results = {}
    #evaluate_max_dict = get_evaluate_max()
    now_ts = time.time()
    db_number = get_db_num(now_ts)
    index_name = be_comment_index_name_pre + str(db_number)
    # print es_comment
    return search_user_info(es_comment,index_name,be_comment_index_type,uid,'uid_be_comment')


def search_comment(uid, top_count):
    results = {}
    #evaluate_max_dict = get_evaluate_max()
    now_ts = time.time()
    db_number = get_db_num(now_ts)
    index_name = comment_index_name_pre + str(db_number)
    center_uid = uid
    return search_user_info(es_comment,index_name,comment_index_type,uid,'uid_comment')

'''
def search_be_comment(uid, top_count):
    results = {}
    now_ts = time.time()
    
    #evaluate_max_dict = get_evaluate_max()
    db_number = get_db_num(now_ts)
    index_name = be_comment_index_name_pre + str(db_number)
    center_uid = uid
    try:
        retweet_result = es_comment.get(index=index_name, doc_type=be_comment_index_type, id=uid)['_source']
    except:
        return None

    content = json.loads(retweet_result['uid_be_comment'])
    return_list = []
    for uid,count in content.iteritems():
        try:
            uname = es_user_portrait.get(index=profile_index_name,doc_type=profile_index_type,id=uid)['_source']['nick_name']
        except:
            uname = u'未知'
        return_list.append({'uid':uid,'uname':uname,'count':count})
    return return_list
'''
 

#use to get user bidirect interaction from es:retweet/be_retweet/comment/be_comment
#write in version: 15-12-08
#input: uid, top_count
#output: retweet_interaction, comment_interaction
def search_bidirect_interaction(uid, top_count):

    now_ts = time.time()
    now_date_ts = datetime2ts(ts2datetime(now_ts))
    db_number = get_db_num(now_date_ts)
    retweet_index_name = retweet_index_name_pre + str(db_number)
    be_retweet_index_name = be_retweet_index_name_pre + str(db_number)
    comment_index_name = comment_index_name_pre + str(db_number)
    be_comment_index_name = be_comment_index_name_pre + str(db_number)
    results = {}
    retweet_inter_dict = {}
    comment_inter_dict = {}
    center_uid = uid
    #bidirect interaction in retweet and be_retweet
    try:
        retweet_result = es_retweet.get(index=retweet_index_name, doc_type=retweet_index_type, id=uid)['_source']
    except:
        retweet_result = {}
    if retweet_result:
        retweet_uid_dict = json.loads(retweet_result['uid_retweet'])
    else:
        retweet_uid_dict = {}
    retweet_uid_list = retweet_uid_dict.keys()
    try:
        be_retweet_result = es_retweet.get(index=be_retweet_index_name, doc_type=be_retweet_index_type, id=uid)['_source']
    except:
        be_retweet_result = {}
    if be_retweet_result:
        be_retweet_uid_dict = json.loads(be_retweet_result['uid_be_retweet'])
    else:
        be_retweet_uid_dict = {}

    #bidirect interaction in comment and be_comment
    try:
        comment_result = es_comment.get(index=comment_index_name, doc_type=comment_index_type, id=uid)['_source']
    except:
        comment_result = {}
    if comment_result:
        comment_uid_dict = json.loads(comment_result['uid_comment'])
    else:
        comment_uid_dict = {}
    comment_uid_list = comment_uid_dict.keys()
    try:
        be_comment_result = es_comment.get(index=be_coment_index_name, doc_type=be_comment_index_type, id=uid)['_source']
    except:
        be_comment_result = {}
    if be_comment_result:
        be_comment_uid_dict = json.loads(be_comment_result['uid_be_comment'])
    else:
        be_comment_uid_dict = {}
    #get bidirect_interaction dict
    #all_interaction_dict = union_dict(retweet_inter_dict, comment_inter_dict)
    retweet_comment_result = union_dict(retweet_uid_dict, comment_uid_dict)
    be_retweet_comment_result = union_dict(be_retweet_uid_dict, be_comment_uid_dict)
    interaction_user_set = set(retweet_comment_result.keys()) & set(be_retweet_comment_result.keys())
    interaction_user_list = list(interaction_user_set)
    all_interaction_dict = {}
    for interaction_user in interaction_user_list:
        if interaction_user != center_uid:
            all_interaction_dict[interaction_user] = retweet_comment_result[interaction_user] + be_retweet_comment_result[interaction_user]
            
    sort_all_interaction_dict = sorted(all_interaction_dict.items(), key=lambda x:x[1], reverse=True)
    #get in_portrait_list, in_portrait_results and out_portrait_list
    all_interaction_uid_list = [item[0] for item in sort_all_interaction_dict]
    #print all_interaction_uid_list

    # if RUN_TYPE == 0:
        # all_interaction_dict = {'2029036025':3,'1282005885':2,'2549228714':2,'1809833450':1}
        # all_interaction_uid_list = ['2029036025', '1282005885', '2549228714', '1809833450']

    out_portrait_list = all_interaction_uid_list
    #use to get user information from user profile
    out_portrait_result = {}
    try:
        out_user_result = es_user_profile.mget(index=profile_index_name, doc_type=profile_index_type, body={'ids':out_portrait_list})['docs']
    except:
        out_user_result = []
    #add index from bci_history
    try:
        bci_history_result = es_bci_history.mget(index=bci_history_index_name, doc_type=bci_history_index_type, body={'ids': out_portrait_list}, fields=fields)['docs']
    except:
        bci_history_result = []
    iter_count = 0
    out_portrait_list = []
    for out_user_item in out_user_result:
        uid = out_user_item['_id']
        if out_user_item['found'] == True:
            source = out_user_item['_source']
            uname = source['nick_name']
            photo_url = source['photo_url']
            if uname == '':
                uname =  u'未知'
            location = source['user_location']
            friendsnum = source['friendsnum']
        else:
            uname = u'未知'
            location = ''
            friendsnum = ''
            photo_url = 'unknown'
        #add index from bci_history
        try:
            bci_history_item = bci_history_result[iter_count]
        except:
            bci_history_item = {'found': False}
        # print bci_history_item
        if bci_history_item['found'] == True:
            fansnum = bci_history_item['fields'][fields[0]][0]
            user_weibo_count = bci_history_item['fields'][fields[1]][0]
            user_friendsnum = bci_history_item['fields'][fields[2]][0]
            influence = bci_history_item['fields'][fields[3]][0]
        else:
            fansnum = ''
            user_weibo_count = ''
            user_friendsnum = ''

        interaction_count = int(all_interaction_dict[uid])
        out_portrait_list.append({'uid':uid,'photo_url':photo_url,'uname':uname, 'count':interaction_count, 'fansnum':fansnum,'friendsnum': user_friendsnum,'weibo_count': user_weibo_count})
        iter_count += 1

    return out_portrait_list


def search_identify_uid(uid):
    result = 0
    try:
        user_dict = es_user_portrait.get(index=portrait_index_name, doc_type=portrait_index_type, id=uid)
        result = 1
    except:
        result = 0
    return result

#use to get retweet/be_retweet/comment/be_comment db_number
def get_db_num(timestamp):
    date = ts2datetime(timestamp)
    date_ts = datetime2ts(date)
    db_number = ((date_ts - r_beigin_ts) / (DAY*7)) %2 +1
    #run_type
    if RUN_TYPE == 0:
        db_number = 1
    return db_number


# use to merge dict
def union_dict(*objs):
    _keys = set(sum([obj.keys() for obj in objs],[]))
    _total = {}
    for _key in _keys:
        _total[_key] = sum([int(obj.get(_key, 0)) for obj in objs])
    #print '_total:', _total
    return _total


#use to search user_portrait by lots of condition 
def search_portrait(condition_num, query, sort, size):
    user_result = []
    index_name = portrait_index_name
    index_type = portrait_index_type
    if condition_num > 0:
        #try:
        result = es_user_portrait.search(index=index_name, doc_type=index_type, \
                    body={'query':{'bool':{'must':query}}, 'sort':[{sort:{'order':'desc'}}], 'size':size})['hits']['hits']
        #except Exception,e:
        #    raise e
        #print 'result:', result
    else:
        try:
            result = es_user_portrait.search(index=index_name, doc_type=index_type, \
                    body={'query':{'match_all':{}}, 'sort':[{sort:{"order":"desc"}}], 'size':size})['hits']['hits']
        except Exception, e:
            raise e
    if result:
        search_result_max = get_evaluate_max()
        
        filter_set = all_delete_uid() # filter_uids_set
        for item in result:
            user_dict = item['_source']
            score = item['_score']

            if not user_dict['uid'] in filter_set:
                result_normal_activeness = math.log(user_dict['activeness'] / search_result_max['activeness'] * 9 + 1, 10)
                result_normal_importance = math.log(user_dict['importance'] / search_result_max['importance'] * 9 + 1, 10)
                result_normal_influence = math.log(user_dict['influence'] / search_result_max['influence'] * 9 + 1, 10)
                result_normal_sensitive = math.log(user_dict['sensitive'] / search_result_max['sensitive'] * 9 + 1, 10)
                user_dict['activeness'] = result_normal_activeness*100
                user_dict['importance'] = result_normal_importance*100
                user_dict['influence'] = result_normal_influence*100
                user_dict['sensitive'] = result_normal_sensitive*100
                uname = user_dict['uname']
                if user_dict['uid']=='1935084477':
                    uname = '迟夙生律师'
                user_result.append([user_dict['uid'], uname, user_dict['location'], user_dict['activeness'], user_dict['importance'], user_dict['influence'], score, user_dict['sensitive']])

    return user_result


def search_user_info(es,index_name,doc_type,uid,result_name):
    try:
        retweet_result = es.get(index=index_name, doc_type=doc_type, id=uid)['_source']
    except:
        return None
    if retweet_result:
        retweet_dict = json.loads(retweet_result[result_name])
        sorted_list = sorted(retweet_dict.iteritems(),key=lambda x:x[1],reverse=True)[:20]
        uid_list = [i[0] for i in sorted_list if i[0] != uid]
        portrait_result = []
        try:
            user_result = es_user_profile.mget(index=profile_index_name, doc_type=profile_index_type, body={'ids':uid_list})['docs']
        except:
            user_result = []
        try:
            bci_history_result = es_bci_history.mget(index=bci_history_index_name, doc_type=bci_history_index_type, body={'ids':uid_list}, fields=fields)['docs']    
        except:
            bci_history_result = []
        #print bci_history_result
        iter_count = 0
        out_portrait_list = []
        for out_user_item in user_result:
            uid = out_user_item['_id']
            if out_user_item['found'] == True:
                source = out_user_item['_source']
                uname = source['nick_name']
                photo_url = source['photo_url']
                if uname == '':
                    uname = u'未知'
                #location = source['user_location']
                friendsnum = source['friendsnum']
            else:
                uname = u'未知'
                location = ''
                friendsnum = ''
                photo_url = 'unknown'
            #add index from bci_history
            try:
                bci_history_item = bci_history_result[iter_count]
            except:
                bci_history_item = {'found': False}
            if bci_history_item['found']==True:
                fansnum = bci_history_item['fields'][fields[0]][0]
                user_weibo_count = bci_history_item['fields'][fields[1]][0]
                user_friendsnum = bci_history_item['fields'][fields[2]][0]
                influence = bci_history_item['fields'][fields[3]][0]
            else:
                fansnum = ''
                user_weibo_count = ''
                user_friendsnum = ''
                influence = ''
            #retweet_count = int(retweet_dict[uid])
            count = retweet_dict[uid]
            out_portrait_list.append({'uid':uid,'photo_url':photo_url,'count':count,'uname':uname,'influence':influence,'fansnum':fansnum, 'friendsnum':user_friendsnum,'weibo_count':user_weibo_count})#location,
            iter_count += 1
        return out_portrait_list
    else:
        return None


def search_weibo(root_uid,uid,mtype):
    query_body = {
        #'query':{
            'filter':{
                'bool':{
                    'must':[{'term':{'uid':uid}},
                            {'term':{'message_type':mtype}}],
                    'should':[{'term':{'root_uid':root_uid}},
                              {'term':{'directed_uid':root_uid}}],
                }
            }
        #}
    }
    index_list = []
    for i in range(7, 0, -1):
        if RUN_TYPE == 1:
            iter_date = ts2datetime(datetime2ts(now_date) - i * DAY)
        else:
            iter_date = ts2datetime(datetime2ts(RUN_TEST_TIME) - i * DAY) 
        index_list.append(flow_text_index_name_pre + iter_date)
    results = es_flow_text.search(index=index_list,doc_type=flow_text_index_type,body=query_body)['hits']['hits']
    weibo = {}
    f_result = []

    if len(results) > 0:
        for result in results:
            #print type(result),result
            weibo['last_text'] = [result['_source']['text'],result['_source']['text'],result['_source']['timestamp']]
            mid = result['_source']['root_mid']
            # print mid
            len_pre = len(flow_text_index_name_pre)
            index = result['_index'][len_pre:]
            root_index = []
            for j in range(0,7):   #一周的，一个月的话就0,30
                iter_date = ts2datetime(datetime2ts(index) - j * DAY) 
                root_index.append(flow_text_index_name_pre + iter_date)
            results0 = es_flow_text.search(index=root_index,doc_type=flow_text_index_type,body={'query':{'term':{'mid':mid}}})['hits']['hits']
            if len(results0)>0:
                for result0 in results0:
                    weibo['ori_text'] = [result0['_source']['text'],result0['_source']['timestamp']]
                    f_result.append(weibo)
                    weibo={}
    return f_result

def search_fans_new(uid,top_count):
    results = {}
    now_ts = time.time()
    now_date_ts = datetime2ts(ts2datetime(now_ts))
    db_number = get_db_num(now_date_ts)

    fan_result_new=es_fans.get(index = fans_index_name,doc_type=fans_index_type,id=uid)['_source']
    
    fan_result_new = json.loads(fan_result_new['uid_be_retweet'])

    out_portrait_list=[]
    # print fan_result_new
    i=1
    for key in fan_result_new:
        # print key
        fansnum=0
        user_friendsnum=0
        user_weibo_count=0
        fans_count=0

        uid=fan_result_new[key]['uid']

        if fan_result_new[key]['photo_url']:
            photo_url = fan_result_new[key]['photo_url']
        else:
            photo_url="http://tp2.sinaimg.cn/1878376757/50/0/1"
        
        if fan_result_new[key]['nick_name']:
            uname=fan_result_new[key]['nick_name']
        else:
            uname=uid

        if fan_result_new[key]['times']:
            fans_count=fan_result_new[key]['times']
        else:
            fans_count=0
        
        if fan_result_new[key]['fansnum']:
            fansnum=fan_result_new[key]['fansnum']
        else:
            fansnum=0

        if fan_result_new[key]['friendsnum']:
            user_friendsnum=fan_result_new[key]['friendsnum']
        else:
            user_friendsnum=0

        if fan_result_new[key]['statusnum']:
            user_weibo_count=fan_result_new[key]['statusnum']
        else:
            user_weibo_count=0

        out_portrait_list.append({'uid':uid,'photo_url':photo_url,'uname':uname, 'count':fans_count, 'fansnum':fansnum,'friendsnum': user_friendsnum,'weibo_count': user_weibo_count})
        
        if i>100:
            break
        i=i+1
    return out_portrait_list

def search_fans(uid,top_count):
    results = {}
    now_ts = time.time()
    now_date_ts = datetime2ts(ts2datetime(now_ts))
    db_number = get_db_num(now_date_ts)

    be_comment_index_name = be_comment_index_name_pre + str(db_number)
    be_retweet_index_name = be_retweet_index_name_pre + str(db_number)
    result = {}
    be_retweet_inter_dict = {}
    be_comment_inter_dict = {}
    center_uid = uid
    try:
        be_retweet_result = es_retweet.get(index = be_retweet_index_name,doc_type=be_retweet_index_type,id=uid)['_source']
    except:
        be_retweet_result = {}

    if be_retweet_result:
        be_retweet_uid_dict = json.loads(be_retweet_result['uid_be_retweet'])
    else:
        be_retweet_uid_dict = {}
    # print "be_retweet_uid_dict", be_retweet_uid_dict
    try:
        be_comment_result = es_be_comment.get(index=be_comment_index_name, doc_type=be_comment_index_type, id=uid)['_source']
    except:
        be_comment_result = {}

    if be_comment_result:
        be_comment_uid_dict = json.loads(be_comment_result['uid_be_comment'])
    else:
        be_comment_uid_dict = {}
    # print "be_comment_uid_dict", be_comment_uid_dict

    fans_result = union_dict(be_retweet_uid_dict,be_comment_uid_dict)
    fans_user_set = set(fans_result.keys())
    fans_list = list(fans_user_set)
    # print "fans_list", fans_list
    all_fans_dict = {}

    for fans_user in fans_list:
        if fans_user != center_uid:
            all_fans_dict[fans_user] = fans_result[fans_user]
    sort_all_fans_dict = sorted(all_fans_dict.items(), key=lambda x:x[1], reverse=True)
    all_fans_uid_list=[]
    all_fans_uid_list_all = [item[0] for item in sort_all_fans_dict]

    count = 0
    for i in all_fans_uid_list_all:
        count += 1
        all_fans_uid_list.append(i)
        if count == 1000:
            break
    # print all_fans_uid_list

    out_portrait_list = all_fans_uid_list
    #use to get user information from user profile
    out_portrait_result = {}
    try:
        out_user_result = es_user_profile.mget(index=profile_index_name, doc_type=profile_index_type, body={'ids':out_portrait_list})['docs']
    except:
        out_user_result = []
    #add index from bci_history
    try:
        bci_history_result = es_bci_history.mget(index=bci_history_index_name, doc_type=bci_history_index_type, body={'ids': out_portrait_list}, fields=fields)['docs']
    except:
        bci_history_result = []
    iter_count = 0
    out_portrait_list = []
    for out_user_item in out_user_result:
        uid = out_user_item['_id']
        if out_user_item['found'] == True:
            source = out_user_item['_source']
            uname = source['nick_name']
            photo_url = source['photo_url']
            if uname == '':
                uname =  u'未知'
            location = source['user_location']
            friendsnum = source['friendsnum']
        else:
            uname = u'未知'
            location = ''
            friendsnum = ''
            photo_url = 'unknown'
        #add index from bci_history
        try:
            bci_history_item = bci_history_result[iter_count]
        except:
            bci_history_item = {'found': False}
        # print bci_history_item
        if bci_history_item['found'] == True:
            fansnum = bci_history_item['fields'][fields[0]][0]
            user_weibo_count = bci_history_item['fields'][fields[1]][0]
            user_friendsnum = bci_history_item['fields'][fields[2]][0]
            influence = bci_history_item['fields'][fields[3]][0]
        else:
            fansnum = ''
            user_weibo_count = ''
            user_friendsnum = ''

        fans_count = int(all_fans_dict[uid])
        out_portrait_list.append({'uid':uid,'photo_url':photo_url,'uname':uname, 'count':fans_count, 'fansnum':fansnum,'friendsnum': user_friendsnum,'weibo_count': user_weibo_count})
        iter_count += 1

    return out_portrait_list


if __name__=='__main__':
    uid = '1843990885'
    now_ts = 1377964800 + 3600 * 24 * 4
    #search_attribute_portrait(uid)
    #result = get_evaluate_max()
    
    results1 = search_attention(uid)
    # print 'attention:', results1
    '''
    results2 = search_follower(uid)
    print 'follow:', results2
    results3 = search_mention(now_ts, uid)
    print 'at_user:', results3 
    results4 = search_location(now_ts, uid)
    print 'location:', results4
    results5 = search_activity(now_ts, uid)
    print 'activity:', results5
    '''
    