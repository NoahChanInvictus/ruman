#-*- coding:utf-8 -*-

import os
import time
import json
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect
from search import search_attribute_portrait, search_location, search_ip, search_mention, search_activity,\
                   search_attention, search_follower, search_portrait, get_geo_track, get_geo_track_ip, get_online_pattern
from search import delete_action, search_identify_uid, get_activeness_trend
from search import get_activity_weibo, search_comment, search_be_comment,search_yangshi_preference_attribute
from search import search_bidirect_interaction, search_preference_attribute, search_sentiment_trend, search_tendency_psy
from search import search_sentiment_weibo, get_influence_trend, search_remark, edit_remark
from search import search_character_psy
from search_daily_info import search_origin_attribute, search_retweeted_attribute, search_user_index
#use to get new user portrait overview
from new_search import new_get_user_profile, new_get_user_portrait,\
        new_get_user_evaluate, new_get_user_location, new_get_user_social,\
        new_get_user_weibo, new_get_weibo_tree, new_get_activeness_trend, \
        new_get_influence_trend, new_get_sensitive_words
#from search_mid import index_mid
from ruman.search_user_profile import es_get_source
from ruman.global_utils import es_user_portrait as es
from ruman.parameter import SOCIAL_DEFAULT_COUNT, SENTIMENT_TREND_DEFAULT_TYPE
from ruman.parameter import DEFAULT_SENTIMENT, DAY
from ruman.parameter import RUN_TYPE, RUN_TEST_TIME
from ruman.time_utils import ts2datetime, datetime2ts
from personal_influence import get_user_influence, influenced_detail, influenced_people, influenced_user_detail, statistics_influence_people, tag_vector, comment_on_influence, detail_weibo_influence, influence_summary
from description import conclusion_on_influence
from info_new_search import info_new_get_user_social

from personalizedRec import adsRec, personRec, localRec, cctv_video_rec, cctv_item_rec, cctv_live_video_rec

# use to test 13-09-08
test_time = datetime2ts(RUN_TEST_TIME)

# custom_attribute
attribute_index_name = 'custom_attribute'
attribute_index_type = 'attribute'

mod = Blueprint('attribute', __name__, url_prefix='/attribute')



# url for new user_portrait overview
# profile information
# write in version: 16-03-15
@mod.route('/new_user_profile/')
def ajax_new_user_profile():
    uid = request.args.get('uid', '')
    results = new_get_user_profile(uid)
    if not results:
        result = {}
    return json.dumps(results)

# url for new user_portrait overview
# tag information/sensitive_words&keywords&hashtag/domain&topic&character&group_tag
# write in version: 16-03-15
@mod.route('/new_user_portrait/')
def ajax_new_user_portrait():
    admin_user = request.args.get('admin_user', 'admin')
    uid = request.args.get('uid', '')
    results = new_get_user_portrait(uid, admin_user)
    if not results:
        results = {}
    return json.dumps(results)

# url for new user_portrait overview
# evaluate index
# write in version: 16-03-15
@mod.route('/new_user_evaluate/')
def ajax_new_user_evaluate():
    uid = request.args.get('uid', '')
    #print 'evl',uid
    results = new_get_user_evaluate(uid)
    if not results:
        results = {}
    return json.dumps(results)

# url for new user_portrait overview
# location
# write in version: 16-03-15
@mod.route('/new_user_location/')
def ajax_new_user_location():
    uid = request.args.get('uid', '')
    results = new_get_user_location(uid)
    if not results:
        results = {}
    return json.dumps(results)

# url for new user_portrait overview
# social
# write in version: 16-03-15
@mod.route('/new_user_social/')
def ajax_new_user_social():
    uid =request.args.get('uid', '')
    results = new_get_user_social(uid)
    if not results:
        results = {}
    return json.dumps(results)

# url for new user_portrait overview
# social
# jln simple
# write in version: 16-03-15
@mod.route('/info_new_user_social/')
def info_ajax_new_user_social():
    uid =request.args.get('uid', '')
    results = info_new_get_user_social(uid)
    if not results:
        results = {}
    return json.dumps(results)

# url for new user_portrait overview
# weibo
# write in version: 16-03-15
@mod.route('/new_user_weibo/')
def ajax_new_user_weibo():
    uid = request.args.get('uid', '')
    sort_type = request.args.get('sort_type', '')
    results = new_get_user_weibo(uid, sort_type)
    if not results:
        results = []
    return json.dumps(results)

# get user sensitive words
# sensitive words
# write in version: 16-03-18
@mod.route('/new_sensitive_words/')
def ajax_new_sensitive_words():
    uid = request.args.get('uid', '')
    results = new_get_sensitive_words(uid)
    if not results:
        results = {}
    return json.dumps(results)


# url for new user_portrait overview
# weibo reposts tree
# write in version: 16-03-15
@mod.route('/new_weibo_tree/')
def ajax_new_weibo_tree():
    mid = request.args.get('mid', '')
    weibo_timestamp = request.args.get('timestamp', '')
    results = new_get_weibo_tree(mid, weibo_timestamp)
    if not results:
        results = ''
    return results


@mod.route('/portrait_attribute/')
def ajax_portrait_attribute():
    uid = request.args.get('uid', '')
    uid = str(uid)
    results = search_attribute_portrait(uid)
    if results:
        return json.dumps(results)
    else:
        return None


#get preference attribute
#write in version: 15-12-08
#input: uid
#output: keywords, hashtag, domain, topic
@mod.route('/preference/')
def ajax_preference():
    uid = request.args.get('uid', '')
    uid = str(uid)
    results = search_preference_attribute(uid)
    if not results:
        results = {}
    return json.dumps(results)


#jln yangshi
@mod.route('/get_preference/')
def ajax_get_preference():
    uid = request.args.get('uid', '')
    uid = str(uid)
    results = search_yangshi_preference_attribute(uid)
    if not results:
        results = {}
    return json.dumps(results)


#edit user remark
#write in version: 15-12-08
#input: uid, remark
#output: status
@mod.route('/edit_remark/')
def ajax_edit_remark():
    uid = request.args.get('uid', '')
    uid = str(uid)
    remark = request.args.get('remark', '')
    results = edit_remark(uid, remark) # results = 'yes' or 'no uid'
    return  results

#input remark
#write in version: 15-12-08
#input: uid
#output: remark
@mod.route('/get_remark/')
def ajax_get_remark():
    uid = request.args.get('uid', '')
    uid = str(uid)
    results = search_remark(uid)
    if not results:
        results = ''
    return json.dumps(results)

@mod.route('/portrait_search/')
def ajax_portrait_search():
    stype = request.args.get('stype', '')
    result = {}
    query_data = {}
    query = []
    query_list = []
    condition_num = 0
    submit_user = request.args.get('submit_user', 'admin@qq.com')
    if stype == '1':
        fuzz_item = ['uid', 'uname']
        item_data = request.args.get('term', '')
        for item in fuzz_item:
            if item_data:
                query_list.append({'wildcard':{item:'*'+item_data+'*'}})
                condition_num += 1
        query.append({'bool':{'should':query_list}})
    else:
        query_list = []
        fuzz_item = ['location', 'activity_geo', 'keywords_string', 'hashtag']
        multi_item = ['character_sentiment','character_text','domain','topic_string']
        simple_fuzz_item = ['uid', 'uname']
        item_data = request.args.get('term', '')
        #print 'item_data:', item_data
        for item in simple_fuzz_item:
            if item_data:
                query_list.append({'wildcard':{item: '*'+item_data+'*'}})
                condition_num += 1
        if query_list:
            query.append({'bool': {'should': query_list}}) 
        for item in fuzz_item:
            item_data = request.args.get(item, '')
            if item_data:
                query.append({'wildcard':{item:'*'+item_data+'*'}})
                condition_num += 1
        # custom_attribute
        tag_items = request.args.get('tag', '')
        if tag_items != '':
            tag_item_list = tag_items.split(',')
            for tag_item in tag_item_list:
                attribute_name_value = tag_item.split(':')
                attribute_name = attribute_name_value[0]
                attribute_value = attribute_name_value[1]
                field_key = submit_user + '-tag'
                if attribute_name and attribute_value:
                    query.append({'wildcard':{field_key: '*'+attribute_name + '-' + attribute_value+'*'}})
                    condition_num += 1

        for item in multi_item:
            nest_body = {}
            nest_body_list = []
            item_data = request.args.get(item, '')
            if item_data:
                term_list = item_data.split(',')
                for term in term_list:
                    nest_body_list.append({'wildcard':{item:'*'+term+'*'}})
                condition_num += 1
                query.append({'bool':{'should':nest_body_list}})
        
        
    size = 1000
    sort = '_score'
    #print 'query condition:', query
    result = search_portrait(condition_num, query, sort, size)
    return json.dumps(result)

#use to get activity geo from user_portrait for week and month
#write in version:15-12-08
#input:uid and time type--day or week or month
#output:day geo or week geo track+conclusion(about activity geo module) or month geo track+month top 
@mod.route('/location/')
def ajax_location():
    uid = request.args.get('uid', '')
    uid = str(uid)
    time_type = request.args.get('time_type', '') # type = day; week; month
    #run_type
    if RUN_TYPE == 1:
        now_ts = time.time()
    else:
        now_ts = test_time - DAY
    results = search_location(now_ts, uid, time_type)
    
    return json.dumps(results)


#use to get ip information for day and week
#write in version-15-12-08
#input: now_ts, uid
#output:{'day_ip':{}, 'week_ip':{}, 'description':''}
@mod.route('/ip/')
def ajax_ip():
    uid = request.args.get('uid', '')
    #run_type
    if RUN_TYPE == 1:
        now_ts = time.time()
    else:
        now_ts = test_time - DAY
    result = search_ip(now_ts, uid)
    if not result:
        result = {}
    return json.dumps(result)


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
    results = search_mention(now_ts, uid, top_count)

    return json.dumps(results)

#use to get now day activity trend ,week activity trend and conclusion
#write in version:15-12-08
#output: {'day_trend':[], 'week_trend':[], 'description':[]}
@mod.route('/activity/')
def ajax_activity_day():
    results = {}
    uid = str(request.args.get('uid', ''))
    #run_type
    if RUN_TYPE == 1:
        now_ts = time.time()
    else:
        now_ts = test_time
    results = search_activity(now_ts, uid)
    if not results:
        results = {}
    return json.dumps(results)

#use to get weibo for activity trend in day or week
#write in version:15-12-08
#input: uid, time_type, start_ts
#output: weibo_list
@mod.route('/activity_weibo/')
def ajax_activity_weibo():
    results = {}
    uid = str(request.args.get('uid', ''))
    time_type = str(request.args.get('type', '')) # type = day or week
    start_ts = int(request.args.get('start_ts', ''))
    results = get_activity_weibo(uid, time_type, start_ts)
    if not results:
        results = []
    return json.dumps(results)

#abandon in version-15-12-08
'''
@mod.route('/activity/')
def ajax_activity():
    uid = request.args.get('uid', '')
    uid = str(uid)
    now_ts = time.time()
    # test
    now_ts = test_time
    results = search_activity(now_ts, uid)
    if results:
        return json.dumps(results)
    else:
        return None
'''

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
    results = search_attention(uid, top_count)
    if not results:
        results = {}
    return json.dumps(results)

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


#use to get user sentiment trend
#write in version： 15-12-08
#input: uid, time_type
#output: sentiment_trend
@mod.route('/sentiment_trend/')
def ajax_sentiment_trend():
    uid = request.args.get('uid', '')
    uid = str(uid)
    time_type = request.args.get('time_type', SENTIMENT_TREND_DEFAULT_TYPE)
    #run_type
    if RUN_TYPE == 1:
        now_ts = time.time()
    else:
        now_ts = test_time - DAY
    #print '1'
    results = search_sentiment_trend(uid, time_type, now_ts)
    #print '3'
    if not results:
        results = {}
    return json.dumps(results)


#use to get user weibo from sentiment trend
#write in version: 15-12-08
#input: uid, start_time, time_type, sentiment_type
#output: weibo_list
@mod.route('/sentiment_weibo/')
def ajax_sentiment_weibo():
    uid = request.args.get('uid', '')
    uid = str(uid)
    start_ts = request.args.get('start_ts', '')
    start_ts = int(start_ts)
    time_type = request.args.get('time_type', SENTIMENT_TREND_DEFAULT_TYPE)
    sentiment_type = request.args.get('sentiment', DEFAULT_SENTIMENT)
    results = search_sentiment_weibo(uid, start_ts, time_type, sentiment_type)
    if not results:
        results = ''
    return json.dumps(results)


#use to get user tendency and psy
#write in version: 15-12-08
#input: uid
#output: tendency, psy(first level and second level)
@mod.route('/tendency_psy/')
def ajax_tendency_psy():
    uid = request.args.get('uid', '')
    uid = str(uid)
    results = search_tendency_psy(uid)
    if not results:
        results = {}
    return json.dumps(results)

#use to get user character and psy
#write in version: 16-02-25
#input: uid
#ouput: character, psy(first level and second level)
@mod.route('/character_psy/')
def ajax_chracter_psy():
    uid = request.args.get('uid', '')
    uid = str(uid)
    results = search_character_psy(uid)
    if not results:
        results = {}
    return json.dumps(results)


#abandon in version: 15-12-08
'''
# get user geo track
@mod.route('/geo_track/')
def ajax_geo_track():
    uid = request.args.get('uid', '')
    uid = str(uid)
    results = get_geo_track(uid)
    #geo track by ip-timestamp
    #results = get_geo_track_ip(uid)
    if results:
        return json.dumps(results)
    else:
        return None
'''


#get user online pattern by week
#write in version: 15-12-08
#input: uid
#output: [(pattern1:count1), (pattern2:count2),...]
@mod.route('/online_pattern/')
def ajax_online_pattern():
    uid = request.args.get('uid', '')
    uid = str(uid)
    #run_type
    if RUN_TYPE == 1:
        now_ts = time.time()
    else:
        now_ts = test_time
    results = get_online_pattern(now_ts, uid)
    if not results:
        results = {}
    return json.dumps(results)


#get user evaluate_index: activeness trend
#write in version: 15-12-08
#input: uid
#output: {'time_line':[], 'activeness':[]}
@mod.route('/activeness_trend/')
def ajax_activeness_trend():
    uid = request.args.get('uid', '')
    time_segment = request.args.get('time_segment', '30')
    uid = str(uid)
    time_segment = int(time_segment)
    #results = get_activeness_trend(uid)
    results = new_get_activeness_trend(uid, time_segment)
    if not results:
        results = {}
    return json.dumps(results)

#get user influence trend
#write in version: 15-12-08
#input: uid
#output: {'time_line':[], 'influence':[]}
@mod.route('/influence_trend/')
def ajax_influence_trend():
    uid = request.args.get('uid', '')
    uid = str(uid)
    time_segment = request.args.get('time_segment', '20') #time_segment=7/30
    time_segment = int(time_segment)
    #results = get_influence_trend(uid, time_segment)
    results = new_get_influence_trend(uid, time_segment)
    if not results:
        results = {}
    return json.dumps(results)

@mod.route('/identify_uid/')
def ajax_identify_uid():
    uid = request.args.get('uid', '')
    results = search_identify_uid(uid)
    return json.dumps(results)


@mod.route('/delete/')
def ajax_delete():
    uid_list = request.args.get('uids', '') # uids = [uid1, uid2]
    if uid_list:
        uid_list = json.loads(uid_list)
        status = delete_action(uid_list)
    return json.dumps(status)
        

"""
attention: the format of date from request must be vertified
format : '2015/07/04'

"""

@mod.route('/origin_weibo/')
def ajax_origin_weibo():
    uid = request.args.get('uid', '')
    date = request.args.get('date', '') # which day you want to see
    uid = str(uid)

    # test
    date = '2013/09/01'
    uid = '1713926427'

    date = str(date).replace('/', '')

    results = search_origin_attribute(date, uid)

    """
    results['origin_weibo_top_retweeted_comtent'] = index_mid(results["origin_weibo_top_retweeted_id"])
    results['origin_weibo_top_comment_content'] = index_mid(results["origin_weibo_top_comment_id"])
    """

    return json.dumps(results)

@mod.route('/retweeted_weibo/')
def ajax_retweetd_weibo():
    uid = request.args.get('uid', '')
    date = request.args.get('date', '')
    uid = str(uid)

    # test
    #date = '2013/09/01'
    #uid = '1713926427'

    date = str(date).replace('/', '')

    results = search_retweeted_attribute(date, uid)

    """
    returm mid content

    results['retweeted_weibo_top_retweeted_content'] = index_mid(results['retweeted_weibo_top_retweeted_id'])
    results['retweeted_weibo_top_comment_content'] = index_mid(results['retweeted_weibo_top_comment_id'])
    """

    return json.dumps(results)

@mod.route('/basic_info/')
def ajax_basic_info():
    uid = request.args.get('uid', '')
    uid = str(uid)

    # test 
    uid = '1713926427'


    results = es_get_source(uid)

    return json.dumps(results)

@mod.route('/user_index/')
def ajax_user_index():
    uid = request.args.get('uid', '')
    date = request.args.get('date', '')
    uid = str(uid)
    date = str(date).replace('/', '')

    results = search_user_index(date, uid)

    return json.dumps(results)


@mod.route('/user_influence_detail/')
def ajax_user_influence_detail():
    uid = request.args.get('uid', '')
    date = request.args.get('date', '')
    uid = str(uid)

    results = get_user_influence(uid, date)

    return json.dumps(results)


# get top 3 weibo
# date: 2013-09-01 (must be)
@mod.route('/get_top_weibo/')
def ajax_get_top_weibo():
    uid = request.args.get('uid', '')
    date = request.args.get('date', '')
    style = request.args.get("style", 0)
    uid = str(uid)
    date = str(date).replace('/', '-')

    results = influenced_detail(uid, date, style)

    return json.dumps(results)

# date: 2013-09-01
# all influenced user by a weibo
@mod.route('/influenced_users/')
def ajax_influenced_users():
    uid = request.args.get('uid', '')
    date = request.args.get('date', '')
    mid = request.args.get('mid', '')
    style = request.args.get('style', '')
    count = request.args.get('count', 0)
    number = request.args.get("number", 20)
    uid = str(uid)
    #date = str(date).replace('/', '-')
    mid = str(mid)
    style = int(style)
    number = int(number)

    results = detail_weibo_influence(uid, mid, style, date, number)

    return json.dumps(results)


# style: 0: all retweeted users, 1: all comment users
@mod.route('/all_influenced_users/')
def ajax_all_influenced_users():
    uid = request.args.get('uid', '')
    date = request.args.get('date', '')
    style = request.args.get("style", 0)
    count = request.args.get("count", 0)
    uid = str(uid)
    date = str(date).replace('/', '-')
    style = int(style)

    results = statistics_influence_people(uid, date, style)

    return json.dumps(results)



# date: 2013-09-01
@mod.route('/current_influence_comment/')
def ajax_current_influence_comment():
    uid = request.args.get('uid', '')
    date = request.args.get("date", '')
    uid = str(uid)
    date = str(date)

    results = comment_on_influence(uid, date)

    return json.dumps(results)



# date: 2013-09-01
@mod.route('/current_tag_vector/')
def ajax_current_tag_vector():
    uid = request.args.get('uid', '')
    date = request.args.get("date", '')
    uid = str(uid)
    date = str(date)

    results = tag_vector(uid, date)

    return json.dumps(results)


@mod.route('/history_activeness_influence/')
def ajax_history_activeness_influence():
    uid = request.args.get('uid', '')
    uid = str(uid)

    results = []
    results = conclusion_on_influence(uid)

    return json.dumps(results)

# 影响力总评价，大小，类型，领域和话题
@mod.route("/summary_influence/")
def ajax_summary_influence():
    uid = request.args.get('uid', '')
    date = request.args.get('date', '')

    result = influence_summary(uid, date)

    return json.dumps(result)



# 给用户推荐相应的判定为广告的微博
@mod.route("/adsRec/")
def ajax_adsRec():
    uid = request.args.get('uid', '')
    #sort_type = request.args.get('sort_type', 'timestamp')
    results = adsRec(uid)
    if results is None:
        results = []
    return json.dumps(results)

# 附近的微博推荐
@mod.route("/localRec/")
def ajax_localRec():
    uid = request.args.get('uid', '')
    results = localRec(uid)
    if results is None:
        results = []
    return json.dumps(results)


# 推荐关注用户
@mod.route("/personRec/")
def ajax_personRec():
    uid = request.args.get('uid','')
    results = personRec(uid)
    if results is None:
        results = []
    return json.dumps(results)


# 央视video推荐，video id
@mod.route("/cctv_video_rec/")
def ajax_cctv_video_rec():
    uid = request.args.get('uid','')
    results = cctv_video_rec(uid)
    if results is None:
        results = []
    return json.dumps(results)


@mod.route("/cctv_live_video_rec")
def ajax_cctv_live_video_rec():
    uid = request.args.get("uid","")
    results = cctv_live_video_rec(uid)
    if results is None:
        results = []
    return json.dumps(results)


# 央视item推荐，item概念名字
@mod.route("/cctv_item_rec/")
def ajax_cctv_item_rec():
    uid = request.args.get('uid','')
    results = cctv_item_rec(uid)
    if results is None:
        results = []
    return json.dumps(results)
