#-*- coding:utf-8 -*-

import os
import time
import json
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect
from search import search_be_comment,search_bidirect_interaction,search_follower,search_mention,\
                    search_attention,search_comment,search_weibo,search_yangshi_follower,search_yangshi_attention,search_fans,search_fans_new

'''
from search import delete_action, search_identify_uid, get_activeness_trend
from search import get_activity_weibo, search_comment, search_be_comment
from search import search_bidirect_interaction, search_preference_attribute, search_sentiment_trend, search_tendency_psy
from search import search_sentiment_weibo, get_influence_trend, search_remark, edit_remark
from search import search_character_psy
from search import search_attribute_portrait, search_location, search_ip, search_mention, search_activity,\
                   search_attention, search_follower, search_portrait, get_geo_track, get_geo_track_ip, get_online_pattern
from search_daily_info import search_origin_attribute, search_retweeted_attribute, search_user_index
#use to get new user portrait overview
from new_search import new_get_user_profile, new_get_user_portrait,\
        new_get_user_evaluate, new_get_user_location, new_get_user_social,\
        new_get_user_weibo, new_get_weibo_tree, new_get_activeness_trend, \
        new_get_influence_trend, new_get_sensitive_words
#from search_mid import index_mid
'''
from ruman.search_user_profile import es_get_source
from ruman.global_utils import es_user_portrait as es
from ruman.parameter import SOCIAL_DEFAULT_COUNT, SENTIMENT_TREND_DEFAULT_TYPE
from ruman.parameter import DEFAULT_SENTIMENT, DAY
from ruman.parameter import RUN_TYPE, RUN_TEST_TIME
from ruman.time_utils import ts2datetime, datetime2ts

#from personal_influence import get_user_influence, influenced_detail, influenced_people, influenced_user_detail, statistics_influence_people, tag_vector, comment_on_influence, detail_weibo_influence, influence_summary



# use to test 13-09-08
test_time = datetime2ts(RUN_TEST_TIME)

# custom_attribute
attribute_index_name = 'custom_attribute'
attribute_index_type = 'attribute'

mod = Blueprint('info_person_social', __name__, url_prefix='/info_person_social')






#use to get user be_retweet from es:be_retweet_1 or be_retweet_2
#write in version:15-12-08
#input: uid, top_count
#output: in_portrait_list, in_portrait_result, out_portrait_list
@mod.route('/follower/')
def ajax_follower():
    uid = request.args.get('uid', '')
    uid = str(uid)
    top_count = request.args.get('top_count', SOCIAL_DEFAULT_COUNT)
    top_count = int(top_count)
    results = search_follower(uid, top_count)
    if not results:
        results = {}
    return json.dumps(results)


#央视
@mod.route('/get_follower/')
def ajax_get_follower():
    uid = request.args.get('uid', '')
    uid = str(uid)
    top_count = request.args.get('top_count', SOCIAL_DEFAULT_COUNT)
    top_count = int(top_count)
    results = search_yangshi_follower(uid, top_count)
    if not results:
        results = {}
    return json.dumps(results)

@mod.route('/get_attention/')
def ajax_get_attention():
    uid = request.args.get('uid', '')
    top_count = request.args.get('top_count', SOCIAL_DEFAULT_COUNT)
    uid = str(uid)
    top_count = int(top_count)
    print uid
    results = search_yangshi_attention(uid, top_count)
    if not results:
        results = {}
    return json.dumps(results)

#use to get user mention @ user
#write in version:15-12-08
#input: uid, top_count
#output: result
@mod.route('/mention/')
def ajax_mention():
    uid = request.args.get('uid', '')
    uid = str(uid)
    top_count = request.args.get('top_count', SOCIAL_DEFAULT_COUNT)
    top_count = int(top_count)
    #run_type
    if RUN_TYPE == 1:
        now_ts = time.time()
    else:
        now_ts = test_time
        print test_time
    results = search_mention(now_ts, uid, top_count)

    return json.dumps(results)



#use to get user be_comment from es: be_comment_1 or be_comment_2
#write in version: 15-12-08
#input: uid, top_count
#output: in_portrait_list. in_portrait_result, out_portrait_list
@mod.route('/be_comment/')
def ajax_be_comment():
    uid = request.args.get('uid', '')
    uid =str(uid)
    top_count = request.args.get('top_count', SOCIAL_DEFAULT_COUNT)
    top_count = int(top_count)
    results = search_be_comment(uid, top_count)
    if not results:
        results = {}
    return json.dumps(results)


#use to get user comment from es: comment_1 or comment_2
#write in version: 15-12-08
#input: uid, top_count
#output: in_portrait_list, in_portrait_result, out_portrait_list
@mod.route('/comment/')
def ajax_comment():
    uid = request.args.get('uid', '')
    uid = str(uid)
    top_count = request.args.get('top_count', SOCIAL_DEFAULT_COUNT)
    top_count = int(top_count)
    results = search_comment(uid, top_count)
    if not results:
        results = {}
    return json.dumps(results)



#use to get user interaction from es:retweet_1+be_retweet_1, comment_1+be_comment_1
#write in version: 15-12-08
#input: uid, top_count
#output: retweet_inter_list, comment_inter_list
@mod.route('/bidirect_interaction/')
def ajax_interaction():
    uid = request.args.get('uid', '')
    uid = str(uid)
    top_count = request.args.get('top_count', SOCIAL_DEFAULT_COUNT)
    top_count = int(top_count)
    results = search_bidirect_interaction(uid, top_count)
    if not results:
        results = {}
    return json.dumps(results)

#use to get user retweet from es:retweet_1 or be_retweet_2
#write in version:15-12-08
#input: uid, top_count
#output: in_portrait_list, in_portrait_result, out_portrait_list
@mod.route('/attention/')
def ajax_attention():
    uid = request.args.get('uid', '')
    top_count = request.args.get('top_count', SOCIAL_DEFAULT_COUNT)
    uid = str(uid)
    top_count = int(top_count)
    print uid
    results = search_attention(uid, top_count)
    if not results:
        results = {}
    return json.dumps(results)

@mod.route('/get_weibo/')
def get_weibo():
    root_uid = request.args.get('root_uid','')
    uid = request.args.get('uid','')
    mtype = request.args.get('mtype','')
    results = search_weibo(root_uid,uid,mtype)
    if not results:
        results = []
    return json.dumps(results)

#use to get user fans:set of follower and be_comment
#write in version:16-11-28
#input: uid, top_count
#output: result
@mod.route('/get_fans/')
def ajax_fans():
    uid = request.args.get('uid','')
    uid = str(uid)
    top_count = request.args.get('top_count',SOCIAL_DEFAULT_COUNT)
    top_count = int(top_count)
    results = search_fans_new(uid,top_count)
    if not results:
        results = {}
    return json.dumps(results)