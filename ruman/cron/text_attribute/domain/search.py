# -*- coding: UTF-8 -*-
'''
search attribute : attention, follower, mention, location, activity
'''
#import IP
import sys
import csv
import time
import json
import redis
from global_utils_do import R_DICT,es_user_profile,es_user_portrait

#search:'be_retweet_' + str(uid) return followers {br_uid1:count1, br_uid2:count2}
#redis:{'be_retweet_'+uid:{br_uid:count}}
#return results:{br_uid:[uname, count]}
def search_follower(uid):
    results = dict()
    stat_results = dict()
    for db_num in R_DICT:
        r = R_DICT[db_num]
        br_uid_results = r.hgetall('be_retweet_'+str(uid))
        #print 'br_uid_results:', br_uid_results
        if br_uid_results:
            for br_uid in br_uid_results:
                try:
                    stat_results[br_uid] += br_uid_results[br_uid]
                except:
                    stat_results[br_uid] = br_uid_results[br_uid]
    # print 'stat_results:', stat_results
    for br_uid in stat_results:
        # search uid
        '''
        uname = search_uid2uname(br_uid)
        if not uname:
        '''
        uname = '未知'
        
        count = stat_results[br_uid]
        results[br_uid] = [uname, count]
    if results:
        return results
    else:
        return None

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
    #print 'sort_state_results:', sort_state_results
    uid_list = [item[0] for item in sort_state_results]
    es_profile_results = es_user_profile.mget(index='weibo_user', doc_type='user', body={'ids':uid_list})['docs']
    es_portrait_results = es_user_portrait.mget(index='user_portrait', doc_type='user', body={'ids':uid_list})['docs']
    result_list = dict()
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

        result_list[uid] = [uid,[uname, stat_results[uid], in_status]]
       
    return [result_list, len(stat_results)]


    
