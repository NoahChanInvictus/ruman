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
from description import active_geo_description, active_time_description, hashtag_description

from ruman.time_utils import ts2datetime, datetime2ts, ts2date, datetimestr2ts


from ruman.global_utils import R_CLUSTER_FLOW2 as r_cluster
from ruman.global_utils import R_DICT
from ruman.global_utils import es_user_portrait, portrait_index_name, portrait_index_type
from ruman.global_utils import es_user_profile, profile_index_name, profile_index_type
from ruman.global_utils import es_flow_text, flow_text_index_name_pre, flow_text_index_type
from ruman.global_utils import es_retweet, es_comment, es_copy_portrait
from ruman.global_utils import retweet_index_name_pre, retweet_index_type
from ruman.global_utils import be_retweet_index_name_pre, be_retweet_index_type
from ruman.global_utils import comment_index_name_pre, comment_index_type
from ruman.global_utils import be_comment_index_name_pre, be_comment_index_type
from ruman.global_utils import copy_portrait_index_name, copy_portrait_index_type
from ruman.global_utils import R_RECOMMENTATION as r_recomment
from ruman.global_utils import es_bci_history, bci_history_index_name, bci_history_index_type
from ruman.global_config import R_BEGIN_TIME
from ruman.parameter import DAY, WEEK, MAX_VALUE,HOUR, HALF_HOUR, FOUR_HOUR, GEO_COUNT_THRESHOLD, PATTERN_THRESHOLD
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

from scws_tools import cut_words_noun

sys.path.append('/home/lcr/ruman/ruman/cron/flow_text/')
from keyword_extraction import get_weibo_single

r_beigin_ts = datetime2ts(R_BEGIN_TIME)

WEEK = 7
emotion_mark_dict = {'126': 'positive', '127':'negative', '128':'anxiety', '129':'angry'}
link_ratio_threshold = [0, 0.5, 1]

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


#use to get user remark
#write in version: 15-12-08
#input: uid
#output: remark
def search_remark(uid):
    try:
        user_portrait_result = es_user_portrait.get(index=portrait_index_name, doc_type=portrait_index_type, id=uid)['_source']
    except:
        user_portrait_result = {}
    try:
        remark_result = user_portrait_result['remark']
    except:
        remark_result = ''

    return remark_result


#use to edit remark
#write in version: 15-12-08
#input: uid, remark
#output: status
def edit_remark(uid, remark):
    status = 'yes'
    try:
        user_portrait_result = es_user_portrait.get(index=portrait_index_name, doc_type=portrait_index_type, id=uid)['_source']
    except:
        return 'no uid'
    es_user_portrait.update(index=portrait_index_name, doc_type=portrait_index_type, id=uid, body={'doc':{'remark': remark}})
    
    return status

#use to search user attention from es: retweet_1 or retweet_2
#write in version: 15-12-08
#input:uid, top_count(0-50)
#output: {'in_portrait_list':[[uid, uname, influence, importance, retweet_count]], \
#         'in_portrait_result':{'topic':{topic1:count,...}, 'domain':{domain1:count}},\
#         'out_portrait_list':[[uid, uname, fansnum]]}
def search_attention(uid, top_count):
    results = {}
    now_ts = time.time()
    evaluate_max_dict = get_evaluate_max()
    db_number = get_db_num(now_ts)
    index_name = retweet_index_name_pre + str(db_number)
    center_uid = uid
    try:
        retweet_result = es_retweet.get(index=index_name, doc_type=retweet_index_type, id=uid)['_source']
    except:
        retweet_result = {}
    if retweet_result:
        retweet_dict = json.loads(retweet_result['uid_retweet'])
    else:
        retweet_dict = {}
    sort_retweet_result = sorted(retweet_dict.items(), key=lambda x:x[1], reverse=True)
    count = 0
    in_portrait_list = []
    out_portrait_list = []
    in_portrait_result = {} # {'topic':{'topic1':count,...}, 'domain':{'domain1':count}}
    in_portrait_topic_list = []
    in_portrait_result['domain'] = {}
    while True:
        uid_list = [item[0] for item in sort_retweet_result[count:count+20]]
        try:
            portrait_result = es_user_portrait.mget(index=portrait_index_name, doc_type=portrait_index_type, body={'ids':uid_list})['docs']
        except:
            portrait_result = []
        for item in portrait_result:
            uid = item['_id']
            if item['found'] == True and uid != center_uid:
                if len(in_portrait_list)<top_count:
                    source = item['_source']
                    uname = source['uname']
                    influence = source['influence']
                    #normal
                    influence = math.log(influence / evaluate_max_dict['influence'] * 9 +1, 10) * 100
                    importance = source['importance']
                    #normal
                    importance = math.log(importance /evaluate_max_dict['importance'] * 9 + 1, 10) * 100
                    activeness = source['activeness']
                    #noraml
                    activeness = math.log(activeness / evaluate_max_dict['activeness'] * 9 + 1, 10) * 100
                    sensitive = source['sensitive']
                    #noraml
                    sensitive = math.log(sensitive / evaluate_max_dict['sensitive'] * 9 + 1, 10) * 100
                    topic_list = source['topic_string'].split('&')
                    domain = source['domain']
                    try:
                        in_portrait_result['domain'][domain] += 1
                    except:
                        in_portrait_result['domain'][domain] = 1
                    in_portrait_topic_list.extend(topic_list)
                    retweet_count = int(retweet_dict[uid])
                    in_portrait_list.append([uid,uname,influence, importance, retweet_count, activeness, sensitive])
            else:
                if len(out_portrait_list)<top_count and uid != center_uid:
                    out_portrait_list.append(uid)
        if len(out_portrait_list)==top_count and len(in_portrait_list)==top_count:
            break
        elif count>= len(sort_retweet_result):
            break
        else:
            count += 20

    in_portrait_result['topic'] = {}
    for topic_item in in_portrait_topic_list:
        try:
            in_portrait_result['topic'][topic_item] += 1
        except:
            in_portrait_result['topic'][topic_item] = 1
    # sort topic and domin stat result
    topic_dict = in_portrait_result['topic']
    sort_topic_dict = sorted(topic_dict.items(), key=lambda x:x[1], reverse=True)
    domain_dict = in_portrait_result['domain']
    sort_domain_dict = sorted(domain_dict.items(), key=lambda x:x[1], reverse=True)
    in_portrait_result['topic'] = sort_topic_dict
    in_portrait_result['domain'] = sort_domain_dict
     
    #use to get user information from user profile
    out_portrait_result = {}
    try:
        out_user_result = es_user_profile.mget(index=profile_index_name, doc_type=profile_index_type, body={'ids':out_portrait_list})['docs']
    except:
        out_user_result = []
    # add bci history index count
    try:
        bci_history_result = es_bci_history.mget(index=bci_history_index_name, doc_type=bci_history_index_type, body={'ids': out_portrait_list}, fields=['user_fansnum', 'weibo_month_sum', 'user_friendsnum'])['docs']
    except:
        bci_history_result = []
    out_portrait_list = [] 
    iter_count = 0
    for out_user_item in out_user_result:
        uid = out_user_item['_id']
        if out_user_item['found'] == True:
            source = out_user_item['_source']
            uname = source['nick_name']
            if uname == '':
                uname = u'未知'
            location = source['user_location']
            friendsnum = source['friendsnum']
        else:
            uname = u'未知'
            location = ''
            friendsnum = ''
        try:
            bci_history_item = bci_history_result[iter_count]
        except:
            bci_history_item = {'found': False}
        if bci_history_item['found'] == True:
            fansnum = bci_history_item['fields']['user_fansnum'][0]
            user_weibo_count = bci_history_item['fields']['weibo_month_sum'][0]
            user_friendsnum = bci_history_item['fields']['user_friendsnum'][0]
        else:
            fansnum = ''
            user_weibo_count = ''
            user_friendsnum = ''

        retweet_count = int(retweet_dict[uid])
        out_portrait_list.append([uid, uname, retweet_count, fansnum, location, user_friendsnum, user_weibo_count])
        iter_count += 1

    return {'in_portrait_list':in_portrait_list, 'in_portrait_result':in_portrait_result, 'out_portrait_list':out_portrait_list}


#abandon in version:15-12-08
'''
#search:'retweet_'+uid return attention {r_uid1:count1, r_uid2:count2...}
#redis:{'retweet_'+uid:{ruid:count}}
#return results: {ruid:[uname,count]}
def search_attention(uid):
    stat_results = dict()
    results = dict()
    for db_num in R_DICT:
        r = R_DICT[db_num]
        ruid_results = r.hgetall('retweet_'+str(uid))
        if ruid_results:
            for ruid in ruid_results:
                if ruid != uid:
                    try:
                        stat_results[ruid] += ruid_results[ruid]
                    except:
                        stat_results[ruid] = ruid_results[ruid]
    # print 'results:', stat_results
    if not stat_results:
        return [None, 0]
    try:
        sort_state_results = sorted(stat_results.items(), key=lambda x:x[1], reverse=True)[:20]
    except:
        return [None, 0]
    uid_list = [item[0] for item in sort_state_results]
    es_profile_results = es_user_profile.mget(index='weibo_user', doc_type='user', body={'ids':uid_list})['docs']
    es_portrait_results = es_user_portrait.mget(index='user_portrait', doc_type='user', body={'ids':uid_list})['docs']
    result_list = []
    for i in range(len(es_profile_results)):
        item = es_profile_results[i]
        uid = item['_id']
        try:
            source = item['_source']
            uname = source['nick_name']
        except:
            uname = u'未知'
        # identify uid is in the user_portrait
        portrait_item = es_portrait_results[i]
        try:
            source = portrait_item[i]
            in_status = 1
        except:
            in_status = 0

        result_list.append([uid,[uname, stat_results[uid], in_status]])
       
    return [result_list[:20], len(stat_results)]
'''

#use to get user be_retweet from es: be_retweet_1 or be_retweet_2
#input: uid, top_count
def search_follower(uid, top_count):
    results = {}
    evaluate_max_dict = get_evaluate_max()
    now_ts = time.time()
    db_number = get_db_num(now_ts)
    index_name = be_retweet_index_name_pre + str(db_number)
    center_uid = uid
    try:
        retweet_result = es_retweet.get(index=index_name, doc_type=be_retweet_index_type, id=uid)['_source']
    except:
        retweet_result = {}
    if retweet_result:
        retweet_dict = json.loads(retweet_result['uid_be_retweet'])
    else:
        retweet_dict = {}
    sort_retweet_result = sorted(retweet_dict.items(), key=lambda x:x[1], reverse=True)
    count = 0
    in_portrait_list = []
    out_portrait_list = []
    in_portrait_result = {} # {'topic':{'topic1':count,...}, 'domain':{'domain1':count}}
    in_portrait_topic_list = []
    in_portrait_result['domain'] = {}
    while True:
        uid_list = [item[0] for item in sort_retweet_result[count:count+20]]
        try:
            portrait_result = es_user_portrait.mget(index=portrait_index_name, doc_type=portrait_index_type, body={'ids':uid_list})['docs']
        except:
            portrait_result = {}
        for item in portrait_result:
            uid = item['_id']
            if item['found'] == True and uid != center_uid:
                if len(in_portrait_list)<top_count:
                    source = item['_source']
                    uname = source['uname']
                    influence = source['influence']
                    #normal
                    influence = math.log(influence / evaluate_max_dict['influence'] * 9 + 1, 10) * 100
                    importance = source['importance']
                    #normal
                    importance = math.log(importance / evaluate_max_dict['importance'] * 9 + 1, 10) * 100
                    activeness = source['activeness']
                    #normal
                    activeness = math.log(activeness / evaluate_max_dict['activeness'] * 9 + 1, 10) * 100
                    sensitive = source['sensitive']
                    #normal
                    sensitive = math.log(sensitive / evaluate_max_dict['sensitive'] * 9 + 1, 10) * 100
                    topic_list = source['topic_string'].split('&')
                    domain = source['domain']
                    try:
                        in_portrait_result['domain'][domain] += 1
                    except:
                        in_portrait_result['domain'][domain] = 1
                    in_portrait_topic_list.extend(topic_list)
                    retweet_count = int(retweet_dict[uid])
                    in_portrait_list.append([uid,uname,influence, importance, retweet_count, activeness, sensitive])
            else:
                if len(out_portrait_list)<top_count and uid != center_uid:
                    out_portrait_list.append(uid)
        if len(out_portrait_list)==top_count and len(in_portrait_list)==top_count:
            break
        elif count >= len(sort_retweet_result):
            break
        else:
            count += 20
    in_portrait_result['topic'] = {}
    for topic_item in in_portrait_topic_list:
        try:
            in_portrait_result['topic'][topic_item] += 1
        except:
            in_portrait_result['topic'][topic_item] = 1
    
    #sort in_portrait_result domain and topic
    topic_dict = in_portrait_result['topic']
    sort_topic_dict = sorted(topic_dict.items(), key=lambda x:x[1], reverse=True)
    domain_dict = in_portrait_result['domain']
    sort_domain_dict = sorted(domain_dict.items(), key=lambda x:x[1], reverse=True)
    in_portrait_result['topic'] = sort_topic_dict
    in_portrait_result['domain'] = sort_domain_dict
    
    #use to get user information from user profile
    out_portrait_result = []
    try:
        out_user_result = es_user_profile.mget(index=profile_index_name, doc_type=profile_index_type, body={'ids':out_portrait_list})['docs']
    except:
        out_user_result = []
    #add index from bci_history
    try:
        bci_history_result = es_bci_history.mget(index=bci_history_index_name, doc_type=bci_history_index_type, body={'ids':out_portrait_list}, fields=['user_fansnum', 'weibo_month_sum', 'user_friendsnum'])['docs']    
    except:
        bci_history_result = []
    iter_count = 0
    out_portrait_list = []
    for out_user_item in out_user_result:
        uid = out_user_item['_id']
        if out_user_item['found'] == True:
            source = out_user_item['_source']
            uname = source['nick_name']
            if uname == '':
                uname = u'未知'
            location = source['user_location']
            friendsnum = source['friendsnum']
        else:
            uname = u'未知'
            location = ''
            friendsnum = ''

        #add index from bci_history
        try:
            bci_history_item = bci_history_result[iter_count]
        except:
            bci_history_item = {'found': False}
        if bci_history_item['found']==True:
            fansnum = bci_history_item['fields']['user_fansnum'][0]
            user_weibo_count = bci_history_item['fields']['weibo_month_sum'][0]
            user_friendsnum = bci_history_item['fields']['user_friendsnum'][0]
        else:
            fansnum = ''
            user_weibo_count = ''
            user_friendsnum = ''
        retweet_count = int(retweet_dict[uid])
        out_portrait_list.append([uid, uname, retweet_count, fansnum, location, user_friendsnum, user_weibo_count])
        iter_count += 1

    return {'in_portrait_list':in_portrait_list, 'in_portrait_result':in_portrait_result, 'out_portrait_list':out_portrait_list}



#use to get user comment from es: comment_1, comment_2
#write in version:15-12-08
#input:uid, top_count
#output: in_portrait_list, in_portrait_result, out_portrait_list
def search_comment(uid, top_count):
    results = {}
    evaluate_max_dict = get_evaluate_max()
    now_ts = time.time()
    db_number = get_db_num(now_ts)
    index_name = comment_index_name_pre + str(db_number)
    center_uid = uid
    try:
        retweet_result = es_comment.get(index=index_name, doc_type=comment_index_type, id=uid)['_source']
    except:
        retweet_result = {}
    if retweet_result:
        retweet_dict = json.loads(retweet_result['uid_comment'])
    else:
        retweet_dict = {}
    sort_retweet_result = sorted(retweet_dict.items(), key=lambda x:x[1], reverse=True)
    count = 0
    in_portrait_list = []
    out_portrait_list = []
    in_portrait_result = {} # {'topic':{'topic1':count,...}, 'domain':{'domain1':count}}
    in_portrait_topic_list = []
    in_portrait_result['domain'] = {}
    while True:
        uid_list = [item[0] for item in sort_retweet_result[count:count+20]]
        try:
            portrait_result = es_user_portrait.mget(index=portrait_index_name, doc_type=portrait_index_type, body={'ids':uid_list})['docs']
        except:
            portrait_result = []
        for item in portrait_result:
            uid = item['_id']
            if item['found'] == True and uid != center_uid:
                if len(in_portrait_list)<top_count:
                    source = item['_source']
                    uname = source['uname']
                    influence = source['influence']
                    #normal
                    influence = math.log(influence / evaluate_max_dict['influence'] * 9 + 1 , 10) * 100
                    importance = source['importance']
                    #normal
                    importance = math.log(importance / evaluate_max_dict['importance'] * 9 + 1, 10) * 100
                    activeness = source['activeness']
                    #normal
                    activeness = math.log(activeness / evaluate_max_dict['activeness'] * 9 + 1, 10) * 100
                    sensitive = source['sensitive']
                    #normal
                    sensitive = math.log(sensitive / evaluate_max_dict['sensitive'] * 9 + 1, 10) * 100
                    topic_list = source['topic_string'].split('&')
                    domain = source['domain']
                    try:
                        in_portrait_result['domain'][domain] += 1
                    except:
                        in_portrait_result['domain'][domain] = 1
                    in_portrait_topic_list.extend(topic_list)
                    retweet_count = int(retweet_dict[uid])
                    in_portrait_list.append([uid,uname,influence, importance, retweet_count, activeness, sensitive])
            else:
                if len(out_portrait_list)<top_count and uid != center_uid:
                    out_portrait_list.append(uid)
        if len(out_portrait_list)==top_count and len(in_portrait_list)==top_count:
            break
        elif count >= len(sort_retweet_result):
            break
        else:
            count += 20

    in_portrait_result['topic'] = {}
    for topic_item in in_portrait_topic_list:
        try:
            in_portrait_result['topic'][topic_item] += 1
        except:
            in_portrait_result['topic'][topic_item] = 1
    
    #sort in_portrait_result topic and domain
    topic_dict = in_portrait_result['topic']
    sort_topic_dict = sorted(topic_dict.items(), key=lambda x:x[1], reverse=True)
    domain_dict = in_portrait_result['domain']
    sort_domain_dict = sorted(domain_dict.items(), key=lambda x:x[1], reverse=True)
    in_portrait_result['topic'] = sort_topic_dict
    in_portrait_result['domain'] = sort_domain_dict

    #use to get user information from user profile
    out_portrait_result = {}
    try:
        out_user_result = es_user_profile.mget(index=profile_index_name, doc_type=profile_index_type, body={'ids':out_portrait_list})['docs']
    except:
        out_user_result = {}
    #add index from bci_history
    try:
        bci_history_result = es_bci_history.mget(index=bci_history_index_name, doc_type=bci_history_index_type, body={'ids': out_portrait_list}, fields=['user_fansnum', 'weibo_month_sum', 'user_friendsnum'])['docs']
    except:
        bci_history_result = []
    out_portrait_list = []
    iter_count = 0
    for out_user_item in out_user_result:
        uid = out_user_item['_id']
        if out_user_item['found'] == True:
            source = out_user_item['_source']
            uname = source['nick_name']
            if uname == '':
                uname = u'未知'
            friendsnum = source['friendsnum']
            location = source['user_location']
        else:
            uname = u'未知'
            friendsnum = ''
            location = ''

        #add index from bci_history
        try:
            bci_history_item = bci_history_result[iter_count]
        except:
            bci_history_item = {'found': False}
        if bci_history_item['found'] == True:
            print 'bci_history_item:', bci_history_item
            fansnum = bci_history_item['fields']['user_fansnum'][0]
            user_weibo_count = bci_history_item['fields']['weibo_month_sum'][0]
            user_friendsnum = bci_history_item['fields']['user_friendsnum'][0]
        else:
            fansnum = ''
            user_weibo_count = ''
            user_friendsnum = ''
        retweet_count = int(retweet_dict[uid])
        out_portrait_list.append([uid, uname, retweet_count, fansnum, location, user_friendsnum, user_weibo_count])
        iter_count += 1
    return {'in_portrait_list':in_portrait_list, 'in_portrait_result':in_portrait_result, 'out_portrait_list':out_portrait_list}


#use to get user be_comment from es: be_comment_1, be_comment_2
#write in version: 15-12-08
#input: uid, top_count
#output: in_portrait_list, in_portrait_result, out_portrait_list
def search_be_comment(uid, top_count):
    results = {}
    now_ts = time.time()
    evaluate_max_dict = get_evaluate_max()
    db_number = get_db_num(now_ts)
    index_name = be_comment_index_name_pre + str(db_number)
    center_uid = uid
    try:
        retweet_result = es_comment.get(index=index_name, doc_type=be_comment_index_type, id=uid)['_source']
    except:
        retweet_result = {}
    if retweet_result:
        retweet_dict = json.loads(retweet_result['uid_be_comment'])
    else:
        retweet_dict = {}
    sort_retweet_result = sorted(retweet_dict.items(), key=lambda x:x[1], reverse=True)
    count = 0
    in_portrait_list = []
    out_portrait_list = []
    in_portrait_result = {} # {'topic':{'topic1':count,...}, 'domain':{'domain1':count}}
    in_portrait_topic_list = []
    in_portrait_result['domain'] = {}

    while True:
        uid_list = [item[0] for item in sort_retweet_result[count:count+20]]
        try:
            portrait_result = es_user_portrait.mget(index=portrait_index_name, doc_type=portrait_index_type, body={'ids':uid_list})['docs']
        except:
            portrait_result = []
        for item in portrait_result:
            uid = item['_id']
            if item['found'] == True and uid != center_uid:
                if len(in_portrait_list)<top_count:
                    source = item['_source']
                    uname = source['uname']
                    influence = source['influence']
                    #normal
                    influence = math.log(influence / evaluate_max_dict['influence'] * 9 + 1 , 10) * 100
                    importance = source['importance']
                    #normal
                    importance = math.log(importance / evaluate_max_dict['importance'] * 9 + 1, 10) * 100
                    activeness = source['activeness']
                    #normal
                    activeness = math.log(activeness / evaluate_max_dict['activeness'] * 9 + 1, 10) * 10
                    sensitive = source['sensitive']
                    #normal
                    sensitive = math.log(sensitive / evaluate_max_dict['sensitive'] * 9 + 1, 10) * 100
                    topic_list = source['topic_string'].split('&')
                    domain = source['domain']
                    try:
                        in_portrait_result['domain'][domain] += 1
                    except:
                        in_portrait_result['domain'][domain] = 1
                    in_portrait_topic_list.extend(topic_list)
                    retweet_count = int(retweet_dict[uid])
                    in_portrait_list.append([uid,uname,influence, importance, retweet_count, activeness, sensitive])
            else:
                if len(out_portrait_list)<top_count and uid != center_uid:
                    out_portrait_list.append(uid)
        if len(out_portrait_list)==top_count and len(in_portrait_list)==top_count:
            break
        elif count >= len(sort_retweet_result):
            break
        else:
            count += 20

    in_portrait_result['topic'] = {}
    for topic_item in in_portrait_topic_list:
        try:
            in_portrait_result['topic'][topic_item] += 1
        except:
            in_portrait_result['topic'][topic_item] = 1
    
    #sort in_portrait_result: domain and topic
    topic_dict = in_portrait_result['topic']
    sort_topic_dict = sorted(topic_dict.items(), key=lambda x:x[1], reverse=True)
    domain_dict = in_portrait_result['domain']
    sort_domain_dict = sorted(domain_dict.items(), key=lambda x:x[1], reverse=True)
    in_portrait_result['domain'] = sort_domain_dict
    in_portrait_result['topic'] = sort_topic_dict

    #use to get user information from user profile
    out_portrait_result = {}
    try:
        out_user_result = es_user_profile.mget(index=profile_index_name, doc_type=profile_index_type, body={'ids':out_portrait_list})['docs']
    except:
        out_user_result = []
    #add index from bci
    try:
        bci_history_result = es_bci_history.mget(index=bci_history_index_name, doc_type=bci_history_index_type, body={'ids':out_portrait_list}, fields=['user_fansnum', 'weibo_month_sum', 'user_friendsnum'])['docs']
    except:
        bci_history_result = []
    iter_count = 0
    out_portrait_list = []
    for out_user_item in out_user_result:
        uid = out_user_item['_id']
        if out_user_item['found'] == True:
            source = out_user_item['_source']
            uname = source['nick_name']
            if uname == '':
                uname = u'未知'
            location = source['user_location']
            friendsnum = source['friendsnum']
        else:
            uname = u'未知'
            location = ''
            friendsnum = ''

        #add index from bci_history
        try:
            bci_history_item = bci_history_result[iter_count]
        except:
            bci_history_item = {'found': False}
        if bci_history_item['found'] == True:
            fansnum = bci_history_item['fields']['user_fansnum'][0]
            user_weibo_count = bci_history_item['fields']['weibo_month_sum'][0]
            user_friendsnum = bci_history_item['fields']['user_friendsnum'][0]
        else:
            fansnum = ''
            user_weibo_count = ''
            user_friendsnum = ''
        retweet_count = int(retweet_dict[uid])
        out_portrait_list.append([uid, uname, retweet_count, fansnum, location, user_friendsnum, user_weibo_count])
        iter_count += 1
    return {'in_portrait_list':in_portrait_list, 'in_portrait_result':in_portrait_result, 'out_portrait_list':out_portrait_list}

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
    '''
    if retweet_uid_list:
        try:
            be_retweet_result = es_retweet.mget(index=be_retweet_index_name, doc_type=be_retweet_index_type, body={'ids':retweet_uid_list})['docs']
        except Exception, e:
            raise e
    else:
        be_retweet_result = []
    for be_retweet_item in be_retweet_result:
        be_retweet_uid = be_retweet_item['_id']
        if be_retweet_item['found']==True and be_retweet_uid != uid:
            be_retweet_dict = json.loads(be_retweet_item['_source']['uid_be_retweet'])
            if uid in be_retweet_dict:
                retweet_inter_dict[be_retweet_uid] = be_retweet_dict[uid] + retweet_uid_dict[be_retweet_uid]
    '''
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

    '''
    try:
        be_comment_result = es_comment.mget(index=be_comment_index_name, doc_type=be_comment_index_type, body={'ids':comment_uid_list})['docs']
    except:
        be_comment_result = []
    for be_comment_item in be_comment_result:
        be_comment_uid = be_comment_item['_id']
        if be_comment_item['found']==True and be_comment_uid != uid:
            be_comment_dict = json.loads(be_comment_item['_source']['uid_be_comment'])
            if uid in be_comment_dict:
                comment_inter_dict[be_comment_uid] = be_comment_dict[uid] + comment_uid_dict[be_comment_uid]
    '''
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
    in_portrait_list = []
    in_portrait_result = {}
    in_portrait_topic_list = []
    in_portrait_result['domain'] = {}
    out_portrait_list = []
    count = 0
    evaluate_max_dict = get_evaluate_max()
    while True:
        uid_list = [item for item in all_interaction_uid_list[count: count+20]]
        try:
            portrait_result = es_user_portrait.mget(index=portrait_index_name, doc_type=portrait_index_type, body={'ids':uid_list})['docs']
        except:
            portrait_result = []
        for item in portrait_result:
            uid = item['_id']
            if item['found'] == True:
                if len(in_portrait_list) < top_count:
                    source = item['_source']
                    uname = source['uname']
                    influence = source['influence']
                    #normal
                    influence = math.log(influence / evaluate_max_dict['influence'] * 9 + 1, 10) * 100
                    importance = source['importance']
                    #normal
                    importance = math.log(importance / evaluate_max_dict['importance'] * 9 +1 , 10) * 100
                    activeness = source['activeness']
                    #normal
                    activeness = math.log(activeness / evaluate_max_dict['activeness'] * 9 + 1, 10) * 100
                    sensitive = source['sensitive']
                    #normal
                    sensitive = math.log(sensitive / evaluate_max_dict['sensitive'] * 9 + 1, 10) * 100
                    topic_list = source['topic_string'].split('&')
                    domain = source['domain']
                    try:
                        in_portrait_result['domain'][domain] += 1
                    except:
                        in_portrait_result['domain'][domain] = 1
                    in_portrait_topic_list.extend(topic_list)
                    interaction_count = int(all_interaction_dict[uid])
                    in_portrait_list.append([uid, uname, influence, importance, interaction_count, activeness, sensitive])
            else:
                if len(out_portrait_list)<top_count:
                    out_portrait_list.append(uid)
        if len(out_portrait_list)==top_count and len(in_portrait_list)==top_count:
            break
        elif count >= len(all_interaction_uid_list):
            break
        else:
            count += 20

    in_portrait_result['topic'] = {}
    for topic_item in in_portrait_topic_list:
        try:
            in_portrait_result['topic'][topic_item] += 1
        except:
            in_portrait_result['topic'][topic_item] = 1
    
    #sort in_portrait_result: domain and topic
    topic_dict = in_portrait_result['topic']
    sort_topic_dict = sorted(topic_dict.items(), key=lambda x:x[1], reverse=True)
    domain_dict = in_portrait_result['domain']
    sort_domain_dict = sorted(domain_dict.items(), key=lambda x:x[1], reverse=True)
    in_portrait_result['domain'] = sort_domain_dict
    in_portrait_result['topic'] = sort_topic_dict

    #use to get user information from user profile
    out_portrait_result = {}
    try:
        out_user_result = es_user_profile.mget(index=profile_index_name, doc_type=profile_index_type, body={'ids':out_portrait_list})['docs']
    except:
        out_user_result = []
    #add index from bci_history
    try:
        bci_history_result = es_bci_history.mget(index=bci_history_index_name, doc_type=bci_history_index_type, body={'ids': out_portrait_list}, fields=['user_fansnum', 'weibo_month_sum', 'user_friendsnum'])['docs']
    except:
        bci_history_result = []
    iter_count = 0
    out_portrait_list = []
    for out_user_item in out_user_result:
        uid = out_user_item['_id']
        if out_user_item['found'] == True:
            source = out_user_item['_source']
            uname = source['nick_name']
            if uname == '':
                uname =  u'未知'
            location = source['user_location']
            friendsnum = source['friendsnum']
        else:
            uname = u'未知'
            location = ''
            friendsnum = ''
        #add index from bci_history
        try:
            bci_history_item = bci_history_result[iter_count]
        except:
            bci_history_item = {'found': False}
        if bci_history_item['found'] == True:
            fansnum = bci_history_item['fields']['user_fansnum'][0]
            user_weibo_count = bci_history_item['fields']['weibo_month_sum'][0]
            user_friendsnum = bci_history_item['fields']['user_friendsnum'][0]
        else:
            fansnum = ''
            user_weibo_count = ''
            user_friendsnum = ''

        interaction_count = int(all_interaction_dict[uid])
        out_portrait_list.append([uid, uname, interaction_count, fansnum, location, user_friendsnum, user_weibo_count])
        iter_count += 1

    return {'in_portrait_list':in_portrait_list, 'in_portrait_result': in_portrait_result, 'out_portrait_list': out_portrait_list}

#abandon in version: 15-12-08
'''
#search:'be_retweet_' + str(uid) return followers {br_uid1:count1, br_uid2:count2}
#redis:{'be_retweet_'+uid:{br_uid:count}}
#return results:{br_uid:[uname, count]}
def search_follower(uid):
    results = dict()
    stat_results = dict()
    for db_num in R_DICT:
        r = R_DICT[db_num]
        br_uid_results = r.hgetall('be_retweet_'+str(uid))
        if br_uid_results:
            for br_uid in br_uid_results:
                if br_uid != uid:
                    try:
                        stat_results[br_uid] += br_uid_results[br_uid]
                    except:
                        stat_results[br_uid] = br_uid_results[br_uid]
    if not stat_results:
        return [None, 0]
    try:
        sort_stat_results = sorted(stat_results.items(), key=lambda x:x[1], reverse=True)[:20]
    except:
        return [None, 0]

    uid_list = [item[0] for item in sort_stat_results]
    es_profile_results = es_user_profile.mget(index='weibo_user', doc_type='user', body={'ids':uid_list})['docs']
    es_portrait_results = es_user_portrait.mget(index='user_portrait', doc_type='user', body={'ids':uid_list})['docs']
    result_list = []
    for i in range(len(es_profile_results)):
        item = es_profile_results[i]
        uid = item['_id']
        try:
            source = item['_source']
            uname = source['nick_name']
        except:
            uname = u'未知'

        portrait_item = es_portrait_results[i]
        try:
            source = portrait_item['_source']
            in_status = 1
        except:
            in_status = 0
        result_list.append([uid,[uname, stat_results[uid], in_status]])
    return [result_list[:20], len(stat_results)]
'''


#search:now_ts , uid return 7day at uid list  {uid1:count1, uid2:count2}
#{'at_'+Date:{str(uid):'{at_uid:count}'}}
#return results:{at_uid:[uname,count]}
def search_mention(now_ts, uid, top_count):
    date = ts2datetime(now_ts)
    evaluate_max_dict = get_evaluate_max()
    ts = datetime2ts(date)
    stat_results = dict()
    results = dict()
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
    all_count = len(sort_stat_results) # all mention count
    #select in_portrait and out_portrait
    in_portrait_list = []
    out_portrait_list = []
    count = 0
    in_portrait_result = {'topic':{}, 'domain':{}}
    in_portrait_topic_list = []
    out_list = []
    while True:
        if count>=len(sort_stat_results):
            break
        nest_body_list = [{'match':{'uname':item[0]}} for item in sort_stat_results[count:count+20]]
        query = [{'bool':{'should': nest_body_list}}]
        try:
            portrait_result = es_user_portrait.search(index=portrait_index_name, doc_type=portrait_index_type, body={'query':{'bool':{'must':query}}, 'size':100})['hits']['hits']
        except:
            portrait_result = []
        for item in portrait_result:
            if len(in_portrait_list)<top_count:
                user_dict = item['_source']
                uname = user_dict['uname']
                domain = user_dict['domain']
                influence = user_dict['influence']
                #normal
                influence = math.log(influence / evaluate_max_dict['influence'] * 9 + 1, 10) * 100
                importance = user_dict['importance']
                #normal
                importance = math.log(importance / evaluate_max_dict['importance'] * 9 +1 , 10) * 100
                activeness = user_dict['activeness']
                #noraml
                activeness = math.log(activeness / evaluate_max_dict['activeness'] * 9 + 1, 10) * 100
                sensitive = user_dict['sensitive']
                sensitive = math.log(sensitive / evaluate_max_dic['sensitive'] * 9 + 1, 10) * 100
                try:
                    in_portrait_result['domain'][domain] += 1
                except:
                    in_portrait_result['domain'][domain] = 1
                topic_list = user_dict['topic_string'].split('&')
                in_portrait_topic_list.extend(topic_list)
                mention_count = state_results[uname]
                in_portrait_result.append([uid, uname, influence, importance, mention_count, activeness, sensitive])
        out_item_list = list(set([item[0] for item in sort_stat_results[count:count+20]]) - set([item['_source']['uname'] for item in portrait_result]))
        out_list.extend(out_item_list)
        if len(out_list)>=top_count and len(in_portrait_list)>=top_count:
            break
        else:
            count += 20
    
    in_portrait_result['topic'] = {}
    for topic_item in in_portrait_topic_list:
        try:
            in_portrait_result['topic'][topic_item] += 1
        except:
            in_portrait_result['topic'][topic_item] = 1
    #sort topic and domain stat result
    topic_dict = in_portrait_result['topic']
    sort_topic_dict = sorted(topic_dict.items(), key=lambda x:x[1], reverse=True)
    domain_dict = in_portrait_result['domain']
    sort_domain_dict = sorted(domain_dict.items(), key=lambda x:x[1], reverse=True)
    in_portrait_result['topic'] = sort_topic_dict
    in_portrait_result['domain'] = sort_domain_dict

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
        try:
            bci_history_item = bci_history_result[iter_count]
        except:
            bci_history_item = {}
        new_out_portrait_item = out_portrait_item
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
        new_out_portrait_item[3] = fansnum
        new_out_portrait_item[6] = user_weibo_count
        new_out_portrait_item[-2] = user_friendsnum
        new_out_portrait_list.append(new_out_portrait_item)
        iter_count += 1
    
    return {'in_portrait_list':in_portrait_list, 'out_portrait_list':new_out_portrait_list, 'in_portrait_result':in_portrait_result}


#use to get user activity geo information by day/week/month
#write in version:15-12-08
#input1: time_type=day    output1: now day activity geo
#input2: time_type=week   output2: latest week activity geo track and conclusion
#inout3: time_type=month output3: latest month activity geo track
def search_location(now_ts, uid, time_type):
    results = {}
    now_date = ts2datetime(now_ts)
    now_date_ts = datetime2ts(now_date)
    if time_type == 'day':
        results = search_location_day(uid, now_date_ts)
    elif time_type == 'week':
        results = search_location_week(uid, now_date_ts)
    elif time_type == 'month':
        results = search_location_month(uid, now_date_ts)
    return results

#use to get activity geo information for day
#write inversion:15-12-08
def search_location_day(uid, now_date_ts):
    results = {}
    all_results = {}
    day_ip_set = set()
    try:
        day_ip_string = r_cluster.hget('new_ip_'+str(now_date_ts), uid)
    except Exception, e:
        raise e
    if day_ip_string:
        day_ip_dict = json.loads(day_ip_string)
    else:
        day_ip_dict = {}

    for ip in day_ip_dict:
        ip_weibo_count = len(day_ip_dict[ip].split('&'))
        city = ip2city(ip)
        try:
            results[city] += ip_weibo_count
        except:
            results[city] = ip_weibo_count
        #use to get day ip count
        day_ip_set.add(ip)
    day_ip_count = len(day_ip_set)
    all_results['day_ip_count'] = day_ip_count
    sort_results = sorted(results.items(), key=lambda x:x[1], reverse=True)
    all_results['sort_results'] = sort_results
    try:
        all_results['tag_vector'] = [u'活动城市', sort_results[0][0]]
    except:
        all_results['tag_vector'] = [u'活动城市', []]
    return all_results

#use to get user activity geo information for week from user_portrait
#write in version:15-12-08
#input: uid ,now_ts
#output: geo track week
def search_location_week(uid, now_date_ts):
    results = {}
    #run_type:
    if RUN_TYPE == 0:
        now_date_ts += DAY
    try:
        user_portrait_result = es_user_portrait.get(index=portrait_index_name, doc_type=portrait_index_type, id=uid)['_source']
    except:
        return {}
    
    activity_geo_string = user_portrait_result['activity_geo_dict']
    if activity_geo_string:
        activity_geo_dict_list = json.loads(activity_geo_string)
    activity_geo_week = activity_geo_dict_list[-7:]
    day_count = len(activity_geo_week)
    all_geo_dict = {}
    for i in range(day_count, 0, -1):
        iter_day_ts = ts2datetime(now_date_ts - DAY*i)
        iter_day_date = datetime2ts(iter_day_ts)
        day_geo_dict = activity_geo_week[day_count - i]
        sort_day_geo = sorted(day_geo_dict.items(), key=lambda x:x[1], reverse=True)
        results[iter_day_date] = sort_day_geo
        all_geo_dict = union_dict(all_geo_dict, day_geo_dict)
    
    sort_all_geo_dict = sorted(all_geo_dict.items(), key=lambda x:x[1], reverse=True)

    return {'week_geo_track': results, 'week_top': sort_all_geo_dict}

#use to get user activity geo information for month from user_portrait
#write in version:15-12-08
#input: uid, now_ts
#output: geo track month
def search_location_month(uid, now_date_ts):
    results = {}
    all_results = {}
    #run_type
    if RUN_TYPE == 0:
        now_date_ts += DAY
    
    try:
        user_portrait_result = es_user_portrait.get(index=portrait_index_name, doc_type=portrait_index_type, id=uid)['_source']
    except:
        return None
    activity_geo_string = user_portrait_result['activity_geo_dict']
    if activity_geo_string:
        activity_geo_dict_list = json.loads(activity_geo_string)
    activity_geo_week = activity_geo_dict_list[-30:]
    day_count = len(activity_geo_week)
    for i in range(day_count, 0, -1):
        iter_day_ts = ts2datetime(now_date_ts - DAY*i)
        iter_day_date = datetime2ts(iter_day_ts)
        day_geo_dict = activity_geo_week[day_count - i]
        sort_day_geo = sorted(day_geo_dict.items(), key=lambda x:x[1], reverse=True)
        results[iter_day_date] = sort_day_geo
        for geo in day_geo_dict:
            try:
                all_results[geo] += day_geo_dict[geo]
            except:
                all_results[geo] = day_geo_dict[geo]
    all_top_geo = sorted(all_results.items(), key=lambda x:x[1], reverse=True)
    count = len(all_results)
    if count == 1:
        description_text = u'为该用户的固定活动地'
    elif count >= GEO_COUNT_THRESHOLD:
        description_text = u'为该用户的主要活动地,且经常出差到不同的城市'
    else:
        description_text = u'为该用户的主要活动地，且偶尔会出差到不同的城市'
    description = [all_top_geo[0][0], description_text]
    month_track_result = []
    end_ts = now_date_ts - DAY
    start_ts = end_ts - DAY*len(activity_geo_week)
    for geo_item in activity_geo_week:
        start_ts = start_ts + DAY
        iter_date = ts2datetime(start_ts)
        day_dict = geo_item
        sort_day = sorted(day_dict.items(), key=lambda x:x[1], reverse=True)
        if sort_day:
            month_track_result.append([iter_date, sort_day[0][0]])
        else:
            month_track_result.append([iter_date, ''])
    return {'month_track':month_track_result, 'all_top':all_top_geo, 'description': description}

#abandon in version:15-12-08
'''
#search:now_ts, uid return 7day loaction list {location1:count1, location2:count2}
#{'ip_'+str(Date_ts):{str(uid):'{city:count}'}
# return results: {city:{ip1:count1,ip2:count2}}
def search_location(now_ts, uid):
    date = ts2datetime(now_ts)
    ts = datetime2ts(date)
    stat_results = dict()
    results = dict()
    for i in range(1, 8):
        ts = ts - 24 * 3600
        result_string = r_cluster.hget('ip_' + str(ts), str(uid))
        if not result_string:
            continue
        result_dict = json.loads(result_string)
        for ip in result_dict:
            try:
                stat_results[ip] += result_dict[ip]
            except:
                stat_results[ip] = result_dict[ip]
    for ip in stat_results:
        city = ip2city(ip)
        if city:
            try:
                results[city][ip] = stat_results[ip]
            except:
                results[city] = {ip: stat_results[ip]}
                

    description = active_geo_description(results)
    results['description'] = description
    return results
'''

#make ip to city
#input: [(ip, count), (ip,count)]
#output: [[ip,count,city], [ip,count,city]]
def tupleip2city(tuple_list):
    result = []
    for ip,count in tuple_list:
        city = ip2city(ip)
        result.append([ip, count, city])
    return result

#ip analysis
#write in version:15-12-08
#input:uid
#output:{'day_ip':{}, 'week_ip':{}, 'description':''}
def search_ip(now_ts, uid):
    results = {}
    now_date = ts2datetime(now_ts)
    now_day_ts = datetime2ts(now_date)
    time_segment = IP_TIME_SEGMENT
    #get day ip result
    day_result = dict()
    sort_day_result = dict()
    all_day_result = dict()
    #use to count day ip count and week ip count
    day_ip_set = set()
    week_ip_set = set()
    try:
        ip_time_string = r_cluster.hget('new_ip_'+str(now_day_ts), str(uid))
    except Exception,e:
        raise e
    if ip_time_string:
        ip_time_dict = json.loads(ip_time_string)
    else:
        ip_time_dict = {}
    for ip in ip_time_dict:
        ip_time_list = ip_time_dict[ip].split('&')
        for ip_timestamp in ip_time_list:
            ip_timesegment = (int(ip_timestamp) - now_day_ts) / time_segment
            try:
                day_result[ip_timesegment][ip] += 1
            except:
                day_result[ip_timesegment] = {ip: 1}
            try:
                all_day_result[ip] += 1
            except:
                all_day_result[ip] = 1

    for segment in day_result:
        segment_dict = day_result[segment]
        sort_segment_dict = sorted(segment_dict.items(), key=lambda x:x[1], reverse=True)
        #add geo information for ip
        new_sort_segment_dict = []
        for item in sort_segment_dict[:IP_TOP]:
            ip = item[0]
            geo = ip2city(ip)
            count = item[1]
            new_sort_segment_dict.append([ip, count, geo])
        sort_day_result[segment] = new_sort_segment_dict

    all_day_top = sorted(all_day_result.items(), key=lambda x:x[1], reverse=True)
    #add geo information for ip
    new_all_day_top = []
    for item in all_day_top:
        ip = item[0]
        count = item[1]
        geo = ip2city(ip)
        new_all_day_top.append([ip, count, geo])

    results['day_ip'] = sort_day_result
    results['day_ip_count'] = len(all_day_result)
    results['all_day_top'] = new_all_day_top

    #get week ip result
    week_time_ip_dict = dict()
    sort_week_result = dict()
    all_week_result = dict()
    for i in range(1, 8):
        timestamp = now_day_ts - i*DAY
        try:
            ip_time_string = r_cluster.hget('new_ip_'+str(timestamp), str(uid))
        except Exception, e:
            ip_time_string = {}
        if ip_time_string:
            ip_time_dict = json.loads(ip_time_string)
        else:
            ip_time_dict = {}
        for ip in ip_time_dict:
            ip_time_list = ip_time_dict[ip].split('&')
            for ip_timestamp in ip_time_list:
                ip_timesegment = (int(ip_timestamp) - timestamp) / time_segment
                try:
                    week_time_ip_dict[ip_timesegment][ip] += 1
                except:
                    week_time_ip_dict[ip_timesegment] = {ip: 1}

                try:
                    all_week_result[ip] += 1
                except:
                    all_week_result[ip] = 1
    
    for i in range(0, 6): 
        try:
            segment_dict = week_time_ip_dict[i]
        except:
            week_time_ip_dict[i] = {}
    
    for segment in week_time_ip_dict:
        segment_dict = week_time_ip_dict[segment]
        sort_segment_dict = sorted(segment_dict.items(), key=lambda x:x[1], reverse=True)
        #add geo information to ip
        new_sort_segment_dict = []
        for item in sort_segment_dict[:IP_TOP]:
            ip = item[0]
            geo = ip2city(ip)
            count = item[1]
            new_sort_segment_dict.append([ip, count, geo])
        sort_week_result[segment] = new_sort_segment_dict
    
    sort_all_week_top = sorted(all_week_result.items(), key=lambda x:x[1], reverse=True)
    #add geo information to ip
    new_sort_all_week_top = []
    for item in sort_all_week_top:
        ip = item[0]
        geo = ip2city(ip)
        count = item[1]
        new_sort_all_week_top.append([ip, count, geo])
    results['week_ip'] = sort_week_result
    results['week_ip_count'] = len(all_week_result)
    results['all_week_top'] = new_sort_all_week_top

    #conclusion
    description, home_ip, job_ip = get_ip_description(week_time_ip_dict, all_week_result, all_day_result)
    results['description'] = description
    #tag vector
    if len(home_ip) != 0:
        home_ip_city = ip2city(home_ip[0])
    else:
        home_ip = ['']
        home_ip_city = ''
    if len(job_ip) != 0:
        job_ip_city = ip2city(job_ip[0])
    else:
        job_ip = ['']
        job_ip_city = ''
    results['tag_vector'] = [[u'家庭IP', home_ip[0], home_ip_city], [u'工作IP', job_ip[0], job_ip_city]]
    return results

#get ip information conclusion
#input: sort_week_result, all_week_top, all_day_top
#output:job ip, home ip, abnormal ip 
def get_ip_description(week_result, all_week_top, all_day_top):
    #get job and home ip
    job_ip = []
    home_ip = []
    conclusion = [u'该用户的家庭IP为']
    sort_week_result = sorted(week_result.items(), key=lambda x:x[0])
    #print 'sort_week_result:', sort_week_result
    job_segment_dict = union_dict(sort_week_result[2][1], sort_week_result[3][1]) # 8:00-12:00 and 12:00-16:00
    home_segment_dict = union_dict(sort_week_result[0][1], sort_week_result[5][1]) # 0:00-4:00 and 20:00-24:00
    sort_job_dict = sorted(job_segment_dict.items(), key=lambda x:x[1], reverse=True)[:IP_CONCLUSION_TOP]
    sort_home_dict = sorted(home_segment_dict.items(), key=lambda x:x[1], reverse=True)[:IP_CONCLUSION_TOP]
    
    home_ip_string = ''
    home_ip_list = []
    for item in sort_home_dict:
        '''
        home_ip_string += item[0]
        home_ip_city = ip2city(item[0])
        home_ip_string += home_ip_city
        home_ip_string += ' '
        home_ip.append(item[0])
        '''
        home_ip_list.append(item[0])
        home_ip_city = ip2city(item[0])
        print ''
        home_ip_list.append(home_ip_city)
        home_ip.append(item[0])

    #conclusion.append(home_ip_string)
    conclusion.append(home_ip_list)
    if(conclusion[-1] != []):
        conclusion.append( u',工作IP为')
    else:
        conclusion.append( u'工作IP为')
    
    job_ip_string = ''
    job_ip_list = []
    for item in sort_job_dict:
        '''
        job_ip_string += item[0]
        job_ip_city = ip2city(item[0])
        job_ip_string += job_ip_city
        job_ip_string += ' '
        job_ip.append(item[0])
        '''
        job_ip_list.append(item[0])
        job_ip_city = ip2city(item[0])
        job_ip_list.append(job_ip_city)
        job_ip.append(item[0])

    #conclusion.append(job_ip_string)
    conclusion.append(job_ip_list)

    #get abnormal use IP
    day_ip_set = set(all_day_top.keys())
    week_ip_set = set(all_week_top.keys())
    abnormal_set = day_ip_set - week_ip_set
    if len(abnormal_set)==0:
        #print 'description_conclusion:',conclusion
        return conclusion, home_ip, job_ip
    else:
        if(conclusion[-1] != []):
            conclusion.append(u',异常使用的IP为')
        else:
            conclusion.append(u'异常使用的IP为')
    abnormal_dict = dict()
    for abnormal_ip in list(abnormal_set):
        abnormal_dict[abnormal_ip] = all_day_top[abnormal_ip]
    sort_abnormal_dict = sorted(abnormal_dict.items(), key=lambda x:x[1], reverse=True)[:IP_CONCLUSION_TOP]
    abnormal_ip_string = ''
    abnormal_ip_list = []
    for item in sort_abnormal_dict:
        '''
        abnormal_ip_string += item[0]
        abnormal_ip_string += ' '
        '''
        abnormal_ip_list.append(item[0])
        abnormal_ip_city = ip2city(item[0])
        abnormal_ip_list.append(abnormal_ip_city)

    #conclusion.append(abnormal_ip_string)
    conclusion.append(abnormal_ip_list)

    #print 'conclusion:', conclusion, home_ip, job_ip
    #print 'description_conclusion:', conclusion
    return conclusion, home_ip, job_ip

#abandon in version:15-12-08
'''
#ip analysis
#redis: date_ts:{'uid':{ip1:'timestamp1&timestamp2'}}
#return: top5 ip; day top2 ip; night top2 ip; ip count for mobile or pc type
def search_ip(now_ts, uid):
    date = ts2datetime(now_ts)
    ts = datetime2ts(date)
    all_ip_count_dict = dict()
    day_count_dict = dict() # time range: 8:00-20:00
    night_count_dict = dict() # time range 20:00-8:00
    start_time_seg = 8*3600
    end_time_seg = 20*3600
    day = 3600*24
    for i in range(1,8):
        ts = ts - 24*3600
        ip_time_string = r_cluster.hget('ip_'+str(ts), str(uid))
        if not ip_string:
            next
        ip_time_dict = json.loads(ip_time_string)
        for ip in ip_time_dict:
            time_string = ip_time_dict[ip]
            time_list = time_string.split('&')
            ip_count = len(time_list)
            try:
                all_ip_count_dict[ip] += ip_count
            except:
                all_ip_count_dict[ip] = ip_count
            for ip_time_string in time_list:
                ip_time = int(ip_time_string)
                if ip_time % day > end_time_seg or ip_time % day < start_time_seg:
                    try:
                        day_count_dict[ip] += 1
                    except:
                        dat_count_dict[ip] = 1
                else:
                    try:
                        night_count_dict[ip] += 1
                    except:
                        night_count_dict[ip] = 1
    sort_ip_count = sorted(all_ip_count.items(), key=lambda x:x[1], reverse=True)
    all_top5 = tupleip2city(sort_ip_count[:5]) #input: (ip,count) output: [ip,count,city]
    sort_day_count = sorted(day_count_dict.items(), key=lambda x:x[1], reverse=True)
    day_top2 = tupleip2city(sort_day_count[:2])
    sort_night_count = sorted(night_count_dict.items(), key=lambda x:x[1], reverse=True)
    night_top2 = tupleip2city(sort_night_count[:2])
    all_count = len(all_ip_count.keys())

    return {'all_top5':all_top5, 'day_top2':day_top2, 'night_top2':night_top2, 'all_count':all_count}
'''


#get user day trend, week trend, conclusion
#write in version-15-12-08
#input: now_ts, uid
#output: {'day_trend':[(time_segment, count), (),...], 'week_trend':[(time_segment,count),(),...], 'description':''}
def search_activity(now_ts, uid):
    activity_result = {}
    if RUN_TYPE == 1:
        now_date = ts2datetime(now_ts)
    else:
        now_date = ts2datetime(now_ts - DAY)
    #compute day trend
    day_weibo = dict()
    day_time_count = []
    now_day_ts = datetime2ts(now_date)
    print 'now_day:', now_date
    try:
        day_result = r_cluster.hget('activity_'+str(now_day_ts), str(uid))
    except:
        day_result = ''
    #print 'before if day_result:', day_result
    if day_result:
        #print 'day_result:', day_result
        day_dict = json.loads(day_result)
        for segment in day_dict:
            time_segment = int(segment)/2
            try:
                day_weibo[time_segment*HALF_HOUR] += day_dict[segment]
            except:
                day_weibo[time_segment*HALF_HOUR] = day_dict[segment]
    #run_type
    if RUN_TYPE == 1:
        max_time = int(time.time() - now_day_ts)
    else:
        max_time = DAY
    for time_segment in range(0, max_time, HALF_HOUR):
        if time_segment in day_weibo:
            day_time_count.append((time_segment, day_weibo[time_segment]))
        else:
            day_time_count.append((time_segment, 0))
    #compute week trend
    week_weibo = dict()
    segment_result = dict()
    week_weibo_count = []
    #run_type
    if RUN_TYPE == 1:
        now_day_ts  = now_day_ts - DAY
    for i in range(0, 7):
        ts = now_day_ts - DAY*i
        try:
            week_result = r_cluster.hget('activity_'+str(ts), str(uid))
        except:
            week_result = ''
        if not week_result:
            continue
        week_dict = json.loads(week_result)
        for time_segment in week_dict:
            try:
                week_weibo[int(time_segment)/16*15*60*16+ts] += week_dict[time_segment]
            except:
                week_weibo[int(time_segment)/16*15*60*16+ts] = week_dict[time_segment]

            try:
                segment_result[int(time_segment)/16*15*60*16] += week_dict[time_segment]
            except:
                segment_result[int(time_segment)/16*15*60*16] = week_dict[time_segment]

    for i in range(0,7):
        ts = now_day_ts - i*DAY
        for j in range(0, 6):
            time_seg = ts + j*15*60*16
            if time_seg in week_weibo:
                week_weibo_count.append((time_seg, week_weibo[time_seg]))
            else:
                week_weibo_count.append((time_seg, 0))
    sort_week_weibo_count = sorted(week_weibo_count, key=lambda x:x[0])
    sort_segment_list = sorted(segment_result.items(), key=lambda x:x[1], reverse=True)
    description, active_type = active_time_description(segment_result)
    
    activity_result['day_trend'] = day_time_count
    activity_result['week_trend'] = sort_week_weibo_count
    activity_result['activity_time'] = sort_segment_list[:2]
    #activity_result['description'] = description
    #activity_result['tag_vector'] = [[u'活跃时间', sort_segment_list[:1]], [u'活动类型', active_type]]
    return activity_result


#use to get weibo for day or week
#write in version-15-12-08
#input: uid, time_type, start_ts
#output: weibo_list
def get_activity_weibo(uid, time_type, start_ts):
    weibo_list = []
    if time_type == 'day':
        time_segment = HALF_HOUR
        start_ts = start_ts
    elif time_type == 'week':
        time_segment = FOUR_HOUR

    end_ts = start_ts + time_segment
    time_date = ts2datetime(start_ts)
    flow_text_index_name = flow_text_index_name_pre + time_date # get flow text es index name: flow_text_2013-09-07
    query = []
    query.append({'term': {'uid': uid}})
    query.append({'range': {'timestamp': {'gte': start_ts, 'lt': end_ts}}})
    try:
        flow_text_es_result = es_flow_text.search(index=flow_text_index_name, doc_type=flow_text_index_type, body={'query':{'bool':{'must': query}}, 'sort': 'timestamp', 'size': MAX_VALUE})['hits']['hits']
    except:
        flow_text_es_result = []
    for item in flow_text_es_result:
        weibo = {}
        source = item['_source']
        weibo['timestamp'] = ts2date(source['timestamp'])
        weibo['ip'] = source['ip']
        weibo['text'] = source['text']
        if source['geo']:
            weibo['geo'] = '\t'.join(source['geo'].split('&'))
        else:
            weibo['geo'] = ''
        weibo['ip'] = source['ip']
        weibo_list.append(weibo)
    return weibo_list


#use to get weibo from sentiment trend
#write in version:15-12-08
#input: uid, start_ts, time_type, sentiment_type
#output: weibo_list
def search_sentiment_weibo(uid, start_ts, time_type, sentiment):
    weibo_list = []
    if time_type=='day':
        time_segment = HOUR#HALF_HOUR
    else:
        time_segment = DAY
    end_ts = start_ts + time_segment
    time_date = ts2datetime(start_ts)
    flow_text_index_name = flow_text_index_name_pre + time_date
    print flow_text_index_name
    query = []
    query.append({'term': {'uid': uid}})
    if sentiment != '2':
        query.append({'term': {'sentiment': sentiment}})
    else:
        query.append({'terms':{'sentiment': SENTIMENT_SECOND}})
    query.append({'range':{'timestamp':{'gte':start_ts, 'lte':end_ts}}})
    print query
    try:
        flow_text_es_result = es_flow_text.search(index=flow_text_index_name, doc_type=flow_text_index_type, body={'query':{'bool':{'must': query}}, 'sort':'timestamp', 'size':1000000})['hits']['hits']
    except:
        flow_text_es_result = []
    for item in flow_text_es_result:
        weibo_list.append(item['_source'])
    return weibo_list


#abandon in version: 15-12-08
'''

#search: now_ts, uid return 7day activity trend list {time_segment:weibo_count}
# redis:{'activity_'+Date:{str(uid): '{time_segment: weibo_count}'}}
# return :{time_segment:count}
def search_activity(now_ts, uid):
    date = ts2datetime(now_ts)
    #print 'date:', date
    ts = datetime2ts(date)
    timestamp = ts
    #print 'date-timestamp:', ts
    activity_result = dict()
    results = dict()
    segment_result = dict()
    for i in range(1, 8):
        ts = timestamp - 24 * 3600*i
        #print 'for-ts:', ts
        try:
            result_string = r_cluster.hget('activity_' + str(ts), str(uid))
        except:
            result_string = ''
        #print 'activity:', result_string
        if not result_string:
            continue
        result_dict = json.loads(result_string)
        for time_segment in result_dict:
            try:
                results[int(time_segment)/16*15*60*16+ts] += result_dict[time_segment]
            except:
                
                results[int(time_segment)/16*15*60*16+ts] = result_dict[time_segment]
            try:
                segment_result[int(time_segment)/16*15*60*16] += result_dict[time_segment]
            except:
                segment_result[int(time_segment)/16*15*60*16] = result_dict[time_segment]


    trend_list = []
    for i in range(1,8):
        ts = timestamp - i*24*3600
        for j in range(0, 6):
            time_seg = ts + j*15*60*16
            if time_seg in results:
                trend_list.append((time_seg, results[time_seg]))
            else:
                trend_list.append((time_seg, 0))
    sort_trend_list = sorted(trend_list, key=lambda x:x[0], reverse=False)
    #print 'sort_trend_list:', sort_trend_list
    activity_result['activity_trend'] = sort_trend_list
    sort_segment_list = sorted(segment_result.items(), key=lambda x:x[1], reverse=True)
    activity_result['activity_time'] = sort_segment_list[:2]
    #print segment_result
    description = active_time_description(segment_result)
    activity_result['description'] = description
    return activity_result
'''

#abandon in version: 15-12-08
'''
# get user activity trend by es:flow_text_2013-09-01
def search_activity_flow_text(uid):
    activity_result = {}
    activity_trend = []
    activity_time = {}
    now_ts = int(time.time())
    now_datets = datetime2ts(ts2datetime(now_ts))
    mod_value = (now_ts - now_datets) % (3600*4)
    if mod_value != 0:
        now_timesegment = int((now_ts - now_datets) / (3600*4)) + 1
    else:
        now_timesegment = int((now_ts - now_datets) / (3600*4))

    range_end_ts = now_timesegment * 3600 + now_datets
    range_start_ts = range_end_ts - 3600*24*7
    index_name_pre = 'flow_text_'
    index_type = 'text'
    for i in range(range_start_ts, range_end_ts, 4*3600):
        iter_date = ts2datetime(range_start_ts)
        index_name = index_name_pre + iter_date
        query_body = {
                'query':{
                    'term': {'uid': uid},
                    'range':{
                        'timestamp':{
                        'gte': i,
                        'lt': i + 3600*4
                        }
                    }
                }
            }
        try:
            text_count = es_user_profile.count(index=index_name, doc_type=index_type, body=query_body)
        except:
            text_count = 0
        activity_trend.append((i, text_count))
        
        segment_ts = i - datetime2ts(iter_date)
        try:
            activity_time[segment_ts] += text_count
        except:
            activity_time[segment_ts] = text_count

    activity_result['activity_trend'] = activity_trend
    sort_activity_time = sorted(activity_time.items(), key=lambda x:x[1], reverse=True)
    activity_result['activity_time'] = sort_activity_time[:2]
    #print 'segment_result:', segment_result
    description = active_time_description(activity_time)
    activity_result['description'] = description

    return activity_result
'''

# ip to city
def ip2city(ip):
    try:
        city = IP.find(str(ip))
        if city:
            city = city.encode('utf-8')
        else:
            return None
        city_list = city.split('\t')
        if len(city_list)==4:
            city = '\t'.join(city_list[:3])
    except Exception,e:
        return None
    return city

# show user geo track
def get_geo_track(uid):
    date_results = [] # {'2013-09-01':[(geo1, count1),(geo2, count2)], '2013-09-02'...}
    now_ts = time.time()
    now_date = ts2datetime(now_ts)
    #test
    now_date = '2013-09-08'
    ts = datetime2ts(now_date)
    city_list = []
    city_set = set()
    for i in range(7, 0, -1):
        timestamp = ts - i*24*3600
        #print 'timestamp:', ts2datetime(timestamp)
        ip_dict = dict()
        results = r_cluster.hget('ip_'+str(timestamp), uid)
        ip_dict = dict()
        date = ts2datetime(timestamp)
        date_key = '-'.join(date.split('-')[1:])
        if results:
            ip_dict = json.loads(results)
            geo_dict = ip_dict2geo(ip_dict)
            city_list.extend(geo_dict.keys())
            sort_geo_dict = sorted(geo_dict.items(), key=lambda x:x[1], reverse=True)
            date_results.append([date_key, sort_geo_dict[:2]])
        else:
            date_results.append([date_key, []])

    #print 'results:', date_results
    city_set = set(city_list)
    geo_conclusion = get_geo_conclusion(uid, city_set)
    return [date_results, geo_conclusion]

# get geo track from es about one month by ip-timestamp
def get_geo_track_ip(uid):
    result = []
    index_name = 'user_portrait'
    index_type = 'user'
    try:
        results = es_user_portrait.get(index=index_name, doc_type=index_type, id=uid)['_source']
    except:
        results = None
        return None
    day_activity_geo_list = json.loads(results['activity_geo_dict'])
    now_ts = time.time()
    now_date = ts2datetime(now_ts)
    date_ts = datetime2ts(now_date)
    city_list = []
    if day_activity_geo_list:
        week_activity_geo_list = day_activity_geo_list
        day_count = len(week_activity_geo_list)
        for i in range(0, day_count):
            ts = date_ts - (day_count-i)*24*3600
            date = ts2datetime(ts)
            day_geo_dict = week_activity_geo_list[i]
            city_list.extend(day_geo_dict.keys())
            sort_day_geo_dict = sorted(day_geo_dict.items(), key=lambda x:x[1], reverse=True)
            result.append([date, sort_day_geo_dict])
    city_set = set(city_list)
    geo_conclusion = get_geo_conclusion(uid, city_set)
    return [result, geo_conclusion]

def get_geo_conclusion(uid, city_set):
    conclusion = ''
    mark = 0
    user_portrait_result = es_user_portrait.get(index='user_portrait', doc_type='user', id=uid)
    try:
        source = user_portrait_result['_source']
        location = source['location']
        location_city_list = location.split('\t')
        #print 'location_city:', location_city_list
        for location_city in location_city_list:
            if location_city in city_set:
                mark += 1
        if mark==0:
            conclusion = u'该用户注册地与活跃地区不一致'
        else:
            conclusion = u'该用户注册地包括在活跃地区范围内'
    except:
        conclusion = ''
    #print 'conclusion:', conclusion
    return conclusion

def ip_dict2geo(ip_dict):
    city_set = set()
    geo_dict = dict()
    for ip in ip_dict:
        try:
            city = IP.find(str(ip))
            if city:
                city.encode('utf-8')
            else:
                city = ''
        except Exception, e:
            city = ''
        if city:
            len_city = len(city.split('\t'))
            if len_city==4:
                city = '\t'.join(city.split('\t')[:3])
            new_len_city = len(city.split('\t'))
            city = city.split('\t')[new_len_city-1]
            try:
                geo_dict[city] += ip_dict[ip]
            except:
                geo_dict[city] = ip_dict[ip]
    return geo_dict

# get importance max & activeness max & influence max
def get_evaluate_max():
    max_result = {}
    index_name = 'user_portrait_1222'
    index_type = 'user'
    evaluate_index = ['activeness', 'importance', 'influence', 'sensitive']
    for evaluate in evaluate_index:
        query_body = {
            'query':{
                'match_all':{}
                },
            'size':1,
            'sort':[{evaluate: {'order': 'desc'}}]
            }
        try:
            result = es_user_portrait.search(index=index_name, doc_type=index_type, body=query_body)['hits']['hits']
        except Exception, e:
            raise e
        max_evaluate = result[0]['_source'][evaluate]
        if max_evaluate != 0:
            max_result[evaluate] = max_evaluate
        else:
            max_result[evaluate] = MAX_VALUE
    return max_result

# use to merge dict
def union_dict(*objs):
    _keys = set(sum([obj.keys() for obj in objs],[]))
    _total = {}
    for _key in _keys:
        _total[_key] = sum([int(obj.get(_key, 0)) for obj in objs])
    #print '_total:', _total
    return _total

# use to show user online pattern by week
# input: {'online_'+str(ts):{uid:{online_pattern1:count1, online_pattern2:count2}}}
'''
def get_online_pattern(now_ts, uid):
    now_date = ts2datetime(now_ts)
    ts = datetime2ts(now_date)
    online_pattern_dict_list = []
    for i in range(7,0,-1):
        timestamp = ts - i * 24 *3600
        try:
            result_string = r_cluster.get('online_'+str(ts), uid)
        except:
            result_string = ''
        if result_string:
            result_dict = json.loads(result_string)
            online_pattern_dict_list.append(online_pattern_dict)
    union_online_pattern_dict = union_dict(online_pattern_dict_list)
    sort_online_pattern = sorted(union_online_pattern_dict.items(), key=lambda x:x[1], reverse=True)
    
    return sort_online_pattern
'''

#use to show user online pattern by week from es_user_portrait
#write in version:15-12-08
#input: uid, now_ts
#output: {pattern1:count, pattern2:count...}
def get_online_pattern(now_ts, uid):
    result = {}
    try:
        portrait_result = es_user_portrait.get(index=portrait_index_name, doc_type=portrait_index_type, id=uid)['_source']
    except:
        return None
    print 'portrait_result:', portrait_result
    online_pattern_string = portrait_result['online_pattern']
    if online_pattern_string:
        try:
            result = json.loads(online_pattern_string)
        except:
            result = {}
    sort_result = sorted(result.items(), key=lambda x:x[1], reverse=True)
    count = len(result)
    '''
    if count == 1:
        description_text = u'为用户固定的上网方式'
    elif count >= PATTERN_THRESHOLD:
        description_text = u'为用户主要的上网方式, 但该用户有多种上网方式'
    else:
        description_text = u'为用户主要的上网方式'
    description = [sort_result[0][0], description_text]
    '''
    return {'sort_result': sort_result}

#get user in portrait preference_attribute
#write in version: 15-12-08
#input: uid
#output: keywords, hashtag, domain, topic
def search_preference_attribute(uid):
    results = {}
    try:
        #print '???',es_user_portrait,portrait_index_name
        portrait_result = es_user_portrait.get(index=portrait_index_name, doc_type=portrait_index_type, id=uid)['_source']
        print portrait_result
    except:
        return None
    try:
        filter_keywords_dict  = json.loads(portrait_result['filter_keywords'])
    except:
        keywords_item_dict = portrait_result['keywords_string']
        filter_keywords_dict = get_weibo_single(keywords_item_dict,n_count=40)
    print "filter_keywords_dict"

    new_filter_keywords_dict={}

    for key in filter_keywords_dict:
        key=key.encode('utf-8')
        print type(key)
        if_noun=cut_words_noun(key)
        if if_noun:
            print key
            key=key.decode('utf-8')
            new_filter_keywords_dict[key]=filter_keywords_dict[key]
        else:   
            print "非名词"+key


    #keywords
    # keywords_item_dict = json.loads(portrait_result['keywords'])
    # keywords_dict = dict()
    # for item in keywords_item_dict:
    #     keywords_dict[item[0]] = item[1]    
    #调用cut 方法，保留名词，判断null或者名词自身

    #cut_words_noun();
    '''分词, 加入黑名单过滤单个词，保留名词
       input
           texts: 输入text的list，utf-8
       output:
           terms: 关键词list
    '''


    # filter_keywords_dict = keyword_filter(keywords_dict)
    sort_keywords = sorted(new_filter_keywords_dict.items(), key=lambda x:x[1], reverse=True)

    #sort_keywords = sorted(keywords_item_dict, key=lambda x:x[1], reverse=True)[:50]
    results['keywords'] = sort_keywords
    #hashtag
    if portrait_result['hashtag_dict']:
        hashtag_dict = json.loads(portrait_result['hashtag_dict'])
    else:
        hashtag_dict = {}
    sort_hashtag = sorted(hashtag_dict.items(), key=lambda x:x[1], reverse=True)[:50]
    results['hashtag'] = sort_hashtag
    #domain
    domain_v3 = json.loads(portrait_result['domain_v3'])
    domain_v3_list = [domain_en2ch_dict[item] for item in domain_v3]
    domain = portrait_result['domain']
    results['domain'] = [domain_v3_list, domain]
    #topic
    topic_en_dict = json.loads(portrait_result['topic'])
    topic_ch_dict = {}
    for topic_en in topic_en_dict:
        # if topic_en != 'life':
        topic_ch = topic_en2ch_dict[topic_en]
        topic_ch_dict[topic_ch] = topic_en_dict[topic_en]
    sort_topic_ch_dict = sorted(topic_ch_dict.items(), key=lambda x:x[1], reverse=True)
    sort_topic_en_dict = sorted(topic_en_dict.items(), key=lambda x:x[1], reverse=True)
   
    #results['topic'] = topic_ch_dict
    results['topic'] = sort_topic_ch_dict
    results['topic_en'] = sort_topic_en_dict

    #add school information
    
    # is_school = portrait_result['is_school']
    # school_string= portrait_result['school_string']
    # results['is_school'] = is_school
    # results['school_string'] = school_string
    
    description_text1 = u'该用户所属领域为'
    description_text2 = u'偏好参与的话题为'
    description = [description_text1, domain, description_text2, sort_topic_ch_dict[0][0]]
    try:
        top_hashtag = sort_hashtag[0][0]
    except:
        top_hashtag = ''
    try:
        top_topic = sort_topic_ch_dict[0][0]
    except:
        top_topic = ''
    tag_vector_list = [[u'hashtag',top_hashtag], [u'领域',domain], [u'话题', top_topic]]
    print 'yes_pr'
    return {'results': results, 'description':description, 'tag_vector': tag_vector_list}


#央视 jln
def search_yangshi_preference_attribute(uid):
    results = {}
    try:
        #print '???',es_user_portrait,portrait_index_name
        portrait_result = es_user_portrait.get(index=portrait_index_name, doc_type=portrait_index_type, id=uid)['_source']
        
    except:
        return None
    try:
        filter_keywords_dict  = json.loads(portrait_result['filter_keywords'])
    except:
        keywords_item_dict = portrait_result['keywords_string']
        filter_keywords_dict = get_weibo_single(keywords_item_dict,n_count=40)
    #keywords
    # keywords_item_dict = json.loads(portrait_result['keywords'])
    # keywords_dict = dict()
    # for item in keywords_item_dict:
    #     keywords_dict[item[0]] = item[1]

    # filter_keywords_dict = keyword_filter(keywords_dict)
    sort_keywords = sorted(filter_keywords_dict.items(), key=lambda x:x[1], reverse=True)

    #sort_keywords = sorted(keywords_item_dict, key=lambda x:x[1], reverse=True)[:50]
    results['keywords'] = sort_keywords
    #hashtag
    if portrait_result['hashtag_dict']:
        hashtag_dict = json.loads(portrait_result['hashtag_dict'])
    else:
        hashtag_dict = {}
    sort_hashtag = sorted(hashtag_dict.items(), key=lambda x:x[1], reverse=True)[:50]
    results['hashtag'] = sort_hashtag
    #domain
    domain_v3 = json.loads(portrait_result['domain_v3'])
    domain_v3_list = [domain_en2ch_dict[item] for item in domain_v3]
    domain = portrait_result['domain']
    results['domain'] = [domain_v3_list, domain]
    #topic
    topic_en_dict = json.loads(portrait_result['topic'])
    topic_ch_dict = {}
    for topic_en in topic_en_dict:
        if topic_en != 'life':
            topic_ch = topic_en2ch_dict[topic_en]
            topic_ch_dict[topic_ch] = topic_en_dict[topic_en]
    sort_topic_ch_dict = sorted(topic_ch_dict.items(), key=lambda x:x[1], reverse=True)
    #results['topic'] = topic_ch_dict
    results['topic'] = sort_topic_ch_dict

    #add school information
    
    # is_school = portrait_result['is_school']
    # school_string= portrait_result['school_string']
    # results['is_school'] = is_school
    # results['school_string'] = school_string
    
    try:
        top_hashtag = sort_hashtag[0][0]
    except:
        top_hashtag = ''
    try:
        top_topic = sort_topic_ch_dict[0][0]
    except:
        top_topic = ''
    tag_vector_list = [[u'hashtag',top_hashtag], [u'领域',domain], [u'话题', top_topic]]
    print 'yes_pr'
    return {'results': results, 'tag_vector': tag_vector_list}



#use to get user sentiment trend by time_type: day or week
#write in version: 15-12-08
#input: uid, time_type
#output: sentiment_trend
def search_sentiment_trend(uid, time_type, now_ts):
    results = {'1':{}, '2':{}, '0':{}, 'time_list':[]}
    trend_results = {'1':[], '2':[], '0':[]}
    sentiment_list = ['1', '2', '0']
    now_date = ts2datetime(now_ts)
    now_date_ts = datetime2ts(now_date)

    if time_type=='day':
        flow_text_index_name = flow_text_index_name_pre + now_date
        try:
            print 'trying',es_flow_text,flow_text_index_name
            flow_text_count = es_flow_text.search(index=flow_text_index_name, doc_type=flow_text_index_type, body={'query':{'term':{'uid': uid}}, 'sort': 'timestamp', 'size':MAX_VALUE})['hits']['hits']
            print es_flow_text,flow_text_index_name
        except:
            flow_text_count = []
        for flow_text_item in flow_text_count:
            source = flow_text_item['_source']
            timestamp = source['timestamp']
            #time_segment = int((timestamp - now_date_ts) / HALF_HOUR) * HALF_HOUR + now_date_ts
            time_segment = int((timestamp - now_date_ts) / HOUR) * HOUR + now_date_ts
            
            sentiment = str(source['sentiment'])
            print sentiment
            if sentiment != '0' and sentiment != '1':
                sentiment = '2'
            try:
                results[str(sentiment)][time_segment] += 1
            except:
                results[str(sentiment)][time_segment] = 1
        if RUN_TYPE==1:
            max_end_time = int(time.time())
        else:
            max_end_time = now_date_ts+DAY
        time_list = [item for item in range(now_date_ts, max_end_time, HOUR)]
        results['time_list'] = time_list
        for time_segment in time_list:
            for sentiment in sentiment_list:
                try:
                    trend_results[sentiment].append(results[sentiment][time_segment])
                except:
                    trend_results[sentiment].append(0)
        #add description
        description_result = {}
        for sentiment in trend_results:
            description_result[sentiment] = sum(trend_results[sentiment])
        sort_description_result = sorted(description_result.items(), key=lambda x:x[1], reverse=True)
        max_sentiment = SENTIMENT_DICT[sort_description_result[0][0]]
        description_text = u'该用户今日主要情绪为'
        description = [description_text, max_sentiment]
        new_time_list = [ts2date(item) for item in time_list]
        return {'trend_result':trend_results, 'description':description, 'time_list':new_time_list}
    elif time_type=='week':
        #run_type
        print '222'
        if RUN_TYPE == 0:
            now_date_ts += DAY
        for i in range(7,0,-1):
            iter_date_ts = now_date_ts - i*DAY
            iter_date = ts2datetime(iter_date_ts)
            flow_text_index_name = flow_text_index_name_pre + iter_date
            try:
                print 'try2',es_flow_text,flow_text_index_name
                flow_text_count = es_flow_text.search(index=flow_text_index_name, doc_type=flow_text_index_type, body={'query':{'term':{'uid':uid}}, 'sort':'timestamp', 'size': MAX_VALUE})['hits']['hits']
                print es_flow_text,flow_text_index_name
            except:
                flow_text_count = []
            for flow_text_item in flow_text_count:
                source = flow_text_item['_source']
                time_segment = iter_date_ts
                sentiment = str(source['sentiment'])
                if sentiment != '0' and sentiment != '1':
                    sentiment = '2'
                try:
                    results[sentiment][time_segment] += 1
                except:
                    results[sentiment][time_segment] = 1
            
            results['time_list'].append(iter_date_ts)
        for time_segment in results['time_list']:
            for sentiment in sentiment_list:
                try:
                    trend_results[sentiment].append(results[sentiment][time_segment])
                except:
                    trend_results[sentiment].append(0)
        #add description
        description_result = {}
        for sentiment in trend_results:
            description_result[sentiment] = sum(trend_results[sentiment])
        sort_description_result = sorted(description_result.items(), key=lambda x:x[1], reverse=True)
        max_sentiment = SENTIMENT_DICT[sort_description_result[0][0]]
        description_text = u'该用户今日主要情绪为'
        description = [description_text, max_sentiment]

        time_list = [ts2datetime(item) for item in results['time_list']]

        return {'trend_result':trend_results, 'time_list':time_list, 'description':description}



#use to get character and psycho_status
#input: uid
#output: character, psycho_status
def search_character_psy(uid):
    results = {}
    #get user_portrait_result
    try:
        portrait_result = es_user_portrait.get(index=portrait_index_name, doc_type=portrait_index_type, \
                id=uid)['_source']
    except:
        return None
    #get character_sentiment
    results['character_sentiment'] = portrait_result['character_sentiment']
    results['character_text'] = portrait_result['character_text']
    
    #get psycho_status
    uid_sentiment_dict = {}
    #run_type
    if RUN_TYPE == 1:
        now_ts = time.time()
    else:
        now_ts = datetime2ts(RUN_TEST_TIME)
    now_date_ts = datetime2ts(ts2datetime(now_ts))
    start_date_ts = now_date_ts - DAY * WEEK
    for i in range(0, WEEK):
        iter_date_ts = start_date_ts + DAY * i
        flow_text_index_date = ts2datetime(iter_date_ts)
        flow_text_index_name = flow_text_index_name_pre + flow_text_index_date
        try:
            flow_text_result = es_flow_text.search(index=flow_text_index_name, doc_type=flow_text_index_type, \
                body={'query':{'filtered':{'filter':{'bool':{'must':[{'term':{'uid': uid}}, {'terms':{'sentiment':['0','1','2','3','4','5','6']}}]}}}}, 'aggs':{'all_sentiment':{'terms':{'field': 'sentiment'}}}}, _source=False, fields=['uid', 'sentiment'])['aggregations']['all_sentiment']['buckets']
        except:
            flow_text_result = []
        for item in flow_text_result:
            sentiment = item['key']
            try:
                uid_sentiment_dict[sentiment] += item['doc_count']
            except:
                uid_sentiment_dict[sentiment] = item['doc_count']
    results['sentiment_pie'] = uid_sentiment_dict
    return results


#get psy all ave dict from overview es
#write in version: 15-12-08
#remark!! there should be adjust
def get_all_ave_psy():
    results= {}
    hash_name = 'overview'
    overview_result = r_recomment.getall(hash_name)
    results = json.loads(overview_result['ave_psy'])

    return results



#use to get tendency and psy
#write in version: 15-12-08
#input: uid
#output: tendency and psy
def search_tendency_psy(uid):
    #test
    portrait_index_name = 'user_portrait_1222'
    portrait_index_type = 'user'
    results = {}
    try:
        portrait_result = es_user_portrait.get(index=portrait_index_name, doc_type=portrait_index_type, id=uid)['_source']
    except:
        return None
    #test
    #print 'portrait_result:', portrait_result
    results['tendency'] = portrait_result['tendency']
    
    psy_dict_list = json.loads(portrait_result['psycho_status'])
    psy_change_dict = dict()
    #get history all other ave psy level
    #all_ave_psy_dict = get_all_ave_psy()  #this value should be computed in overview every day
    #test
    all_ave_psy_dict = {'anger':0, 'other':0.8, 'anx':0, 'sad':0.2, 'posemo':0.4, 'negemo':0.2, 'middle':0.4}
    #end test
    
    if len(psy_dict_list) == 2:
        old_psy_dict = psy_dict_list[0]
        old_psy = dict(old_psy_dict['first'], **old_psy_dict['second'])
        new_psy_dict = psy_dict_list[1]
        new_psy = dict(new_psy_dict['first'], **new_psy_dict['second'])
        for item in new_psy:
            iter_list = []
            #add compare with old self
            if new_psy_[item] > old_psy[item]:
                iter_list.append(1)
            elif new_psy[item] < old_psy[item]:
                iter_list.append(-1)
            else:
                iter_list.append(0)
            #add compare with all other ave level
            if new_psy[item] > all_ave_psy_dict[item]:
                iter_list.append(1)
            elif new_psy[item] < all_ave_psy_dict[item]:
                iter_list.append(-1)
            else:
                iter_list.append(0)
            psy_change_dict[item] = iter_list
    elif len(psy_dict_list) == 1:
        new_psy_dict = psy_dict_list[0]
        new_psy = dict(new_psy_dict['first'], **new_psy_dict['second'])
        for item in new_psy:
            #add compare with all other ave level
            if new_psy[item] > all_ave_psy_dict[item]:
                psy_change_dict[item] = [0, 1]
            elif new_psy[item] < all_ave_psy_dict[item]:
                psy_change_dict[item] = [0, -1]
            else:
                psy_change_dict[item] = [0, 0]
    
    description = [u'该用户']
    for field in PSY_DESCRIPTION_FIELD:
        if psy_change_dict[field] == [0, 1]:
            description.append(psy_en2ch_dict[field])
            description.append(psy_description_dict['0'])
            #u'与个人历史水平持平,但是高于全库平均水平'
        elif psy_change_dict[field] == [1, 0]:
            description.append(psy_en2ch_dict[field])
            description.append(psy_description_dict['1'])
            #u'高于个人历史水平, 但与全库平均水平持平'
        elif psy_change_dict[field] == [1, 1]:
            description.append(psy_en2ch_dict[field])
            description.append(psy_description_dict['2'])
            #u'高于个人历史水平及全库平均水平'
    if len(description) == 1:
        description.append(psy_description_dict['3'])
        #u'心理状态平稳正常'

    results['psy_change'] = psy_change_dict
    results['psy_first'] = new_psy_dict['first']
    results['psy_second'] = new_psy_dict['second']
    results['description'] = description
    return results

#use to search user_portrait to show the attribute saved in es_user_portrait
def search_attribute_portrait(uid):
    results = dict()
    try:
        results = es_user_portrait.get(index=portrait_index_name, doc_type=portrait_index_type, id=uid)['_source']
    except:
        results = None
        return None
    keyword_list = []
    
    #state
    if results['uid']:
        uid = results['uid']
        try:
            profile_result = es_user_profile.get(index='weibo_user', doc_type='user', id=uid)
        except:
            profile_result = None
        try:
            user_state = profile_result['_source']['description']
            results['description'] = user_state
        except:
            results['description'] = ''
    else:
        results['uid'] = ''
        results['description'] = ''
    
    # get importance value
    if results['importance']:
        query_body = {
                'query':{
                    "range":{
                        "importance":{
                        "gte": results['importance'],
                        "lt": 1000000
                        }
                        }
                    }
                }
        importance_rank = es_user_portrait.count(index=portrait_index_name, doc_type=portrait_index_type, body=query_body)
        if importance_rank['_shards']['successful'] != 0:
            results['importance_rank'] = importance_rank['count']
        else:
            print 'es_importance_rank error'
            results['importance_rank'] = 0
    else:
        results['importance_rank'] = 0
    if results['activeness']:
        query_body = {
                'query':{
                    "range":{
                        "activeness":{
                            "gte":results['activeness'],
                            "lt": 1000000
                            }
                        }
                    }
                }
        activeness_rank = es_user_portrait.count(index=portrait_index_name, doc_type=portrait_index_type, body=query_body)
        if activeness_rank['_shards']['successful'] != 0:
            results['activeness_rank'] = activeness_rank['count']
        else:
            print 'es_activess_rank error'
            results['activeness_rank'] = 0
    if results['influence']:
        query_body = {
                'query':{
                    'range':{
                        'influence':{
                            'gte':results['influence'],
                            'lt': 1000000
                            }
                        }
                    }
                }
        influence_rank = es_user_portrait.count(index=portrait_index_name, doc_type=portrait_index_type, body=query_body)
        if influence_rank['_shards']['successful'] != 0:
            results['influence_rank'] = influence_rank['count']
        else:
            print 'es_influence_rank error'
            results['influence_rank'] = 0
    #total count in user_portrait
    query_body ={
            'query':{
                'match_all':{}
                }
            }
    all_count_results = es_user_portrait.count(index=portrait_index_name, doc_type=portrait_index_type, body=query_body)
    if all_count_results['_shards']['successful'] != 0:
        results['all_count'] = all_count_results['count']
    else:
        print 'es_user_portrait error'
        results['all_count'] = 0
    # activeness normalized to 0-100
    evaluate_max = get_evaluate_max()
    normal_activeness = math.log(results['activeness'] / evaluate_max['activeness'] * 9 + 1, 10)
    results['activeness'] = int(normal_activeness * 100)
    normal_importance = math.log(results['importance'] / evaluate_max['importance'] * 9 + 1, 10)
    results['importance'] = int(normal_importance * 100)
    normal_influence = math.log(results['influence'] / evaluate_max['influence'] * 9 + 1, 10)
    results['influence'] = int(normal_influence * 100)
    return results

#get emotion conclusion
def get_emotion_conclusion(emotion_dict):
    positive_key = '126'
    negative_key = '127'
    emotion_conclusion = ''
    if positive_key in emotion_dict:
        positive_word_count = sum(emotion_dict[positive_key].values())
    else:
        positive_word_count = 0
    if negative_key in emotion_dict:
        negative_word_count = sum(emotion_dict[negative_key].values())
    else:
        negative_word_count = 0
    if positive_word_count > negative_word_count:
        emotion_conclusion = u'该用户发布微博中偏好使用正向情感词'
    elif positive_word_count < negative_word_count:
        emotion_conclusion = u'该用户发布微博中偏好使用负向情感词'
    else:
        emotion_conclusion = u'该用户发布微博中正向情感词和负向情感词使用均衡'
    return emotion_conclusion

#get link conclusion
def get_link_conclusion(link_ratio):
    conclusion = ''
    if link_ratio >= link_ratio_threshold[2]: 
        conclusion = u'该用户极易于将外部信息引入微博平台'
    elif link_ratio < link_ratio_threshold[2] and link_ratio >= link_ratio_threshold[1]:
        conclusion = u'该用户一般易于将外部信息引入微博平台'
    elif link_ratio < link_ratio_threshold[1]:
        conclusion = u'该用户不易于将外部信息引入微博平台'
    return conclusion


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


def delete_action(uid_list):
    index_name = portrait_index_name
    index_type = portrait_index_type
    bulk_action = []
    for uid in uid_list:
        action = {'delete':{'_id': uid}}
        bulk_action.append(action)
    es.bulk(bulk_action, index=index_name, doc_type=index_type)
    time.sleep(1)
    return True

#use to get activeness_trend
#write in version: 15-12-08
#input: uid
#output: {'time_line':[], 'activeness':[]}
def get_activeness_trend(uid):
    results = {}
    try:
        es_result = es_copy_portrait.get(index=copy_portrait_index_name, doc_type=copy_portrait_index_type, id=uid)['_source']
    except:
        return None
    value_list = []
    for item in es_result:
        item_list = item.split('_')
        if len(item_list)==2 and '-' in item_list[1]:
            value = es_result[item]
            value_list.append(value)
            
            if '-' in item_list[1]:
                results[item_list[1]] = value
    sort_results = sorted(results.items(), key=lambda x:datetime2ts(x[0]))
    time_list = [item[0] for item in sort_results]
    activeness_list = [item[1] for item in sort_results]

    #get activeness description
    max_activeness = max(value_list)
    min_activeness = min(value_list)
    ave_activeness = sum(value_list) / float(len(value_list))
    
    if max_activeness - min_activeness <= ACTIVENESS_TREND_SPAN_THRESHOLD and ave_activeness >= ACTIVENESS_TREND_AVE_MAX_THRESHOLD:
        mark = ACTIVENESS_TREND_DESCRIPTION_TEXT['0']
        tag_vector =  ACTIVENESS_TREND_TAG_VECTOR['0']
        #u'活跃度较高, 且保持平稳'
    elif max_activeness - min_activeness > ACTIVENESS_TREND_SPAN_THRESHOLD and ave_activeness >= ACTIVENESS_TREND_AVE_MAX_THRESHOLD:
        mark = ACTIVENESS_TREND_DESCRIPTION_TEXT['1']
        tag_vector =  ACTIVENESS_TREND_TAG_VECTOR['1']
        #u'活跃度较高, 且波动性较大'
    elif max_activeness - min_activeness <= ACTIVENESS_TREND_SPAN_THRESHOLD and ave_activeness < ACTIVENESS_TREND_AVE_MAX_THRESHOLD and ave_activeness >= ACTIVENESS_TREND_AVE_MIN_THRESHOLD:
        mark = ACTIVENESS_TREND_DESCRIPTION_TEXT['2']
        tag_vector =  ACTIVENESS_TREND_TAG_VECTOR['2']
        #u'活跃度一般, 且保持平稳'
    elif max_activeness - min_activeness > ACTIVENESS_TREND_SPAN_THRESHOLD and ave_activeness < ACTIVENESS_TREND_AVE_MAX_THRESHOLD and ave_activeness >= ACTIVENESS_TREND_AVE_MIN_THRESHOLD:
        mark = ACTIVENESS_TREND_DESCRIPTION_TEXT['3']
        tag_vector =  ACTIVENESS_TREND_TAG_VECTOR['3']
        #u'活跃度一般, 且波动性较大'
    elif max_activeness - min_activeness <= ACTIVENESS_TREND_SPAN_THRESHOLD and ave_activeness < ACTIVENESS_TREND_AVE_MIN_THRESHOLD:
        mark = ACTIVENESS_TREND_DESCRIPTION_TEXT['4']
        tag_vector =  ACTIVENESS_TREND_TAG_VECTOR['4']
        #u'活跃度较低, 且保持平稳'
    else:
        mark = ACTIVENESS_TREND_DESCRIPTION_TEXT['5']
        tag_vector =  ACTIVENESS_TREND_TAG_VECTOR['5']
        #u'活跃度较低, 且波动性较大'

    description = [u'该用户', mark]

    return {'time_line':time_list, 'activeness':activeness_list, 'description':description, 'tag_vector': tag_vector}

#use to get influence_trend
#write in version: 15-12-08
#input: uid, day_count(7/30)
#output: {'time_line':[], 'influence':[]}
def get_influence_trend(uid, day_count):
    results = {}
    try:
        es_result = es_copy_portrait.get(index=copy_portrait_index_name, doc_type=copy_portrait_index_type, id=uid)['_source']
    except:
        return None
    influence_value_list = []
    for item in es_result:
        item_list = item.split('_')
        if len(item_list)==1 and item_list[0] != 'uid':
            value = es_result[item]
            influence_value_list.append(value)
            
            query_key = item
            query_body = {
                    'query':{
                        'match_all':{}
                    },
                    'size': 1,
                    'sort': [{query_key: {'order': 'desc'}}]
                }
            try:
                iter_max_value = es_user_portrait.search(index=copy_portrait_index_name, doc_type=copy_portrait_index_type, body=query_body)['hits']['hits']
            except Exception, e:
                raise e
            iter_max = iter_max_value[0]['_source'][query_key]
            
            if '-' not in item_list[0]:
                #run_type
                if RUN_TYPE == 0:
                    normal_value = math.log((value / iter_max) * 9 + 1 , 10) * 100
                    results[item_list[0]] = normal_value
                else:
                    results[item_list[0]] = value
    sort_results = sorted(results.items(), key=lambda x:datetimestr2ts(x[0]))[0-day_count:]
    time_list = [ts2datetime(datetimestr2ts(item[0])) for item in sort_results]
    influence_list = [item[1] for item in sort_results]
    
    max_influence = max(influence_value_list)
    ave_influence = sum(influence_value_list) / float(len(influence_value_list))
    min_influence = min(influence_value_list)
    if max_influence - min_influence <= INFLUENCE_TREND_SPAN_THRESHOLD and ave_influence >= INFLUENCE_TREND_AVE_MAX_THRESHOLD:
        mark = INFLUENCE_TREND_DESCRIPTION_TEXT['0']
        #u'影响力较高,且保持平稳'
    elif max_influence - min_influence > INFLUENCE_TREND_SPAN_THRESHOLD and ave_influence >= INFLUENCE_TREND_AVE_MAX_THRESHOLD:
        mark = INFLUENCE_TREND_DESCRIPTION_TEXT['1']
        #u'影响力较高,且波动性较大'
    elif max_influence - min_influence <= INFLUENCE_TREND_SPAN_THRESHOLD and ave_influence < INFLUENCE_TREND_AVE_MAX_THRESHOLD and ave_influence >= INFLUENCE_TREND_AVE_MIN_THRESHOLD:
        mark = INFLUENCE_TREND_DESCRIPTION_TEXT['2']
        #u'影响力一般,且保持平稳'
    elif max_influence - min_influence > INFLUENCE_TREND_SPAN_THRESHOLD and ave_influence < INFLUENCE_TREND_AVE_MAX_THRESHOLD and ave_influence >= INFLUENCE_TREND_AVE_MIN_THRESHOLD:
        mark = INFLUENCE_TREND_DESCRIPTION_TEXT['3']
        #u'影响力一般,且波动性较大'
    elif max_influence - min_influence <= INFLUENCE_TREND_SPAN_THRESHOLD and ave_influence < INFLUENCE_TREND_AVE_MIN_THRESHOLD:
        mark = INFLUENCE_TREND_DESCRIPTION_TEXT['4']
        #u'影响力较低,且保持平稳'
    else:
        mark = INFLUENCE_TREND_DESCRIPTION_TEXT['5']
        #u'影响力较低,且波动性较大'
    description = [u'该用户', mark]

    return {'time_line':time_list, 'influence':influence_list, 'description':description}

if __name__=='__main__':
    uid = '1843990885'
    now_ts = 1377964800 + 3600 * 24 * 4
    #search_attribute_portrait(uid)
    #result = get_evaluate_max()
    
    results1 = search_attention(uid)
    print 'attention:', results1
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
    
