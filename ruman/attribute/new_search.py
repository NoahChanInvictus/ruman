# -*- coding: UTF-8 -*-
'''
use to get new attribute overview
write in version: 16-03-15
'''
from IPy import IP
import json
import time
import random
import base62
import buchheim_weibospread
from gen_weibospread import Tree
from gexf import Gexf
from lxml import etree
from influence_appendix import weiboinfo2url

from ruman.global_utils import es_user_portrait, portrait_index_name, portrait_index_type,\
                          es_flow_text, flow_text_index_name_pre, flow_text_index_type,\
                          es_user_profile, profile_index_name, profile_index_type
from ruman.global_utils import R_CLUSTER_FLOW2 as r_cluster
from ruman.global_utils import es_retweet, retweet_index_name_pre, retweet_index_type,\
                                     be_retweet_index_name_pre, be_retweet_index_type,\
                                     es_comment, comment_index_name_pre, comment_index_type,\
                                     be_comment_index_name_pre, be_comment_index_type
from ruman.global_utils import ES_COPY_USER_PORTRAIT, COPY_USER_PORTRAIT_INFLUENCE, COPY_USER_PORTRAIT_INFLUENCE_TYPE,\
              COPY_USER_PORTRAIT_IMPORTANCE, COPY_USER_PORTRAIT_IMPORTANCE_TYPE, COPY_USER_PORTRAIT_ACTIVENESS,\
              COPY_USER_PORTRAIT_ACTIVENESS_TYPE, COPY_USER_PORTRAIT_SENSITIVE, COPY_USER_PORTRAIT_SENSITIVE_TYPE
from ruman.global_utils import es_bci_history, bci_history_index_name, bci_history_index_type
from ruman.parameter import verified_num2ch_dict, IP_TIME_SEGMENT, DAY, MAX_VALUE
from ruman.parameter import RUN_TYPE, RUN_TEST_TIME
from ruman.global_config import R_BEGIN_TIME
from ruman.time_utils import ts2datetime, datetime2ts, ts2date
from ruman.keyword_filter import keyword_filter

evaluate_index_dict = {'bci': [COPY_USER_PORTRAIT_INFLUENCE, COPY_USER_PORTRAIT_INFLUENCE_TYPE], \
                       'importance': [COPY_USER_PORTRAIT_IMPORTANCE, COPY_USER_PORTRAIT_IMPORTANCE_TYPE],\
                       'activeness': [COPY_USER_PORTRAIT_ACTIVENESS, COPY_USER_PORTRAIT_ACTIVENESS_TYPE],\
                       'sensitive': [COPY_USER_PORTRAIT_SENSITIVE, COPY_USER_PORTRAIT_SENSITIVE_TYPE ]}

r_beigin_ts = datetime2ts(R_BEGIN_TIME)
FILTER_ITER_COUNT = 100

#use to get user profile information
def new_get_user_profile(uid):
    try:
    	#print 'trying',es_user_profile,profile_index_name
        results = es_user_profile.get(index=profile_index_name, doc_type=profile_index_type,\
                id=uid)['_source']
        #print es_user_profile,profile_index_name
    except:
        results = {}
    #get new fansnum and statusnum
    try:
        bci_history_result = es_bci_history.get(index=bci_history_index_name, doc_type=bci_history_index_type, id=uid)['_source']
    except:
        bci_history_result = {}
    if not results:
        results['uid'] = uid
        results['photo_url'] = ''
        results['nick_name'] = ''
        results['verified_type'] = ''
        results['verified_type_ch'] = ''
        results['fansnum'] = ''
        results['friendsnum'] = ''
        results['statusnum'] = ''
        results['user_location'] = ''
        results['description'] = ''
    else:
        verified_num_type = results['verified_type']
        try:
            verified_ch_type = verified_num2ch_dict[verified_num_type]
        except:
            verified_ch_type = ''
        results['verified_type_ch'] = verified_ch_type
    
    if bci_history_result:
        try:
            results['fansnum'] = int(bci_history_result['user_fansnum'])
            results['friendsnum'] = max(int(bci_history_result['user_friendsnum']),results['friendsnum'])
            results['statusnum'] = max(int(bci_history_result['weibo_month_sum']),results['statusnum'])
        except:
            pass
    
    return results

#use to get tag information/sensitive_words&keywords&hashtag/domain&topic&character
def new_get_user_portrait(uid, admin_user):
    results = {}
    print 'jln ',es_user_portrait,portrait_index_name
    try:
        user_portrait_result = es_user_portrait.get(index=portrait_index_name, doc_type=portrait_index_type,\
                id=uid)['_source']
    except:
        user_portrait_result = {}
    if not user_portrait_result:
        results['tag_remark'] = {}
        results['attention_information'] = {}
        results['tendency'] = {}
        results['group_tag'] = []
    else:
        print 'step1'
        #step1: get attention_information
        #sensitive words
        try:
            sensitive_words_dict = json.loads(user_portrait_result['sensitive_dict'])
        except:
            sensitive_words_dict = {}
        sort_sensitive_words = sorted(sensitive_words_dict.items(), key=lambda x:x[1], reverse=True)
        results['attention_information'] = {'sensitive_dict': sort_sensitive_words}
        #keywords
        try:
            #sort_keywords = json.loads(user_portrait_result['keywords'])
            keywords_list = json.loads(user_portrait_result['keywords'])
        except:
            #sort_keywords = []
            keywords_list = {}
        keywords_dict = dict()
        for item in keywords_list:
            keywords_dict[item[0]] = item[1]
        filter_word_dict = keyword_filter(keywords_dict)
        sort_keywords = sorted(filter_word_dict.items(), key=lambda x:x[1], reverse=True)
        results['attention_information']['keywords'] = sort_keywords
        #hashtag
        try:
            hashtag_dict = json.loads(user_portrait_result['hashtag_dict'])
        except:
            hashtag_dict = {}
        sort_hashtag = sorted(hashtag_dict.items(), key=lambda x:x[1], reverse=True)
        results['attention_information']['hashtag'] = sort_hashtag
        #step2: get tendency_information
        results['tendency'] = {'domain':user_portrait_result['domain']}
        results['tendency']['topic'] = user_portrait_result['topic_string'].split('&')[0]
        #add school information
        
        results['tendency']['is_school'] = user_portrait_result['is_school']
        results['tendency']['school'] = user_portrait_result['school_string']
        
        results['tendency']['character_sentiment'] = user_portrait_result['character_sentiment']
        results['tendency']['character_text'] = user_portrait_result['character_text']
        #step3: get tag_information
        #tag
        try:
            admin_tag = user_portrait_result[admin_user + '-tag']
        except:
            admin_tag = {}
        if not admin_tag:
            results['tag_remark'] = {'tag': []}
        else:
            tag_list = admin_tag.split('&')
            results['tag_remark'] = {'tag': tag_list}
        #remark
        try:
            remark = user_portrait_result['remark']
        except:
            remark = ''
        results['tag_remark']['remark'] = remark
        #step4: get group_tag information
        results['group_tag'] = []
        try:
            group_tag = user_portrait_result['group']
        except:
            group_tag = ''
        if group_tag:
            group_tag_list = group_tag.split('&')
            for group_tag in group_tag_list:
                group_tag_item_list = group_tag.split('-')
                if group_tag_item_list[0] == admin_user:
                    results['group_tag'].append(group_tag_item_list[1])

    return results

#get evaluate rank
def get_evaluate_rank(evaluate_ts, evaluate_value, evaluate_index):
    result = []
    evaluate_index_key = evaluate_index + '_' + str(evaluate_ts)
    query_body = {
        'query':{
            'range':{
                evaluate_index_key:{
                    'gte': evaluate_value,
                    'lt': MAX_VALUE
                    }
                }
            }
        }
    #get index_name, index_type
    index_infor_item = evaluate_index_dict[evaluate_index]
    index_name = index_infor_item[0]
    index_type = index_infor_item[1]
    evaluate_rank = ES_COPY_USER_PORTRAIT.count(index=index_name, doc_type=index_type, body=query_body)
    if evaluate_rank['_shards']['successful'] != 0:
        rank = evaluate_rank['count']
    else:
        rank = ''
    return rank


#use to get evaluate max/min/now_value/rank
def get_evaluate_max_min_now(history_dict, evaluate_index):
    results = []
    date_evaluate_dict = {}
    for item in history_dict:
        item_list = item.split('_')
        if len(item_list)==2 and item_list[0]==evaluate_index:
            evaluate_ts = int(item_list[1])
            date_evaluate_dict[evaluate_ts] = history_dict[item]
    print date_evaluate_dict
    sort_date_evaluate_list = sorted(date_evaluate_dict.items(), key=lambda x:x[0])
    sort_value_evaluate_list = sorted(date_evaluate_dict.items(), key=lambda x:x[1], reverse=True)
    #get now evaluate value and rank
    now_evaluate_value = sort_date_evaluate_list[-1][1]
    now_evaluate_ts = sort_date_evaluate_list[-1][0]
    now_evaluate_rank = get_evaluate_rank(now_evaluate_ts, now_evaluate_value ,evaluate_index)
    #get max evalute and min evaluate
    max_value = sort_value_evaluate_list[0][1]
    min_value = sort_value_evaluate_list[-1][1]
    results = [now_evaluate_value, now_evaluate_rank, max_value, min_value]
    return results

#use to get user influence week ave
#return week ave rank
def get_influence_week_ave_rank(week_ave):
    evaluate_index_key = 'bci_week_ave'
    query_body = {
        'query':{
            'range':{
                evaluate_index_key: {
                    'gte': week_ave,
                    'lt': MAX_VALUE
                    }
                }
            }
        }
    index_name = COPY_USER_PORTRAIT_INFLUENCE
    index_type = COPY_USER_PORTRAIT_INFLUENCE_TYPE
    week_ave_rank = ES_COPY_USER_PORTRAIT.count(index=index_name, doc_type=index_type,\
            body=query_body)
    if week_ave_rank['_shards']['successful'] != 0:
        rank = week_ave_rank['count']
    else:
        rank = ''
    return rank



#use to get user evaluate index
#return result: [now_evaluate_value, now_evaluate_rank, max_value, min_value, all_count]
def new_get_user_evaluate(uid):
    results = {}
    #get all count in user_portrait
    query_body = {
            'query':{
                'match_all': {}
                }
            }
    print '0927'
    all_count_results = es_user_portrait.count(index=portrait_index_name, doc_type=portrait_index_type, body=query_body)
    print es_user_portrait,portrait_index_name
    if all_count_results['_shards']['successful'] != 0:
        all_count = all_count_results['count']
    else:
        all_count = ''
    #get influence from es influence history
    try:
        influence_history = ES_COPY_USER_PORTRAIT.get(index=COPY_USER_PORTRAIT_INFLUENCE, doc_type=COPY_USER_PORTRAIT_INFLUENCE_TYPE, \
                id = uid)['_source']

    except:
        influence_history = []
    #get max value/min value/week ave value
    if influence_history:
        week_ave = influence_history['bci_week_ave']
        week_ave_rank = get_influence_week_ave_rank(week_ave)
        influence_item = [week_ave, week_ave_rank]
        influence_max_min_now_list =  get_evaluate_max_min_now(influence_history, 'bci')
        influence_max_min_now_list.append(all_count)
        influence_item.extend(influence_max_min_now_list[2:])
        results['influence'] = influence_max_min_now_list
    else:
        results['influence'] = ['', '', '', '', all_count]

    #get importance from es importance history
    try:
        importance_history = ES_COPY_USER_PORTRAIT.get(index=COPY_USER_PORTRAIT_IMPORTANCE, doc_type=COPY_USER_PORTRAIT_IMPORTANCE_TYPE, \
                id = uid)['_source']
    except:
        importance_history = []
    #get max value/min value/now value
    if importance_history:
        importance_max_min_now_list = get_evaluate_max_min_now(importance_history, 'importance')
        importance_max_min_now_list.append(all_count)
        results['importance'] = importance_max_min_now_list
    else:
        results['importance'] = ['', '', '', '', all_count]
    #get activeness from es activeness history
    try:
        activeness_history = ES_COPY_USER_PORTRAIT.get(index=COPY_USER_PORTRAIT_ACTIVENESS, doc_type=COPY_USER_PORTRAIT_ACTIVENESS_TYPE ,\
                id = uid)['_source']
    except:
        activeness_history = []
    #get max value/min value/ now value
    if activeness_history:
        activeness_max_min_now_list = get_evaluate_max_min_now(activeness_history, 'activeness')
        activeness_max_min_now_list.append(all_count)
        results['activeness'] = activeness_max_min_now_list
    else:
        results['activeness'] = ['', '', '', '', all_count]

    #get sensitive from es sensitive history
    try:
        sensitive_history = ES_COPY_USER_PORTRAIT.get(index=COPY_USER_PORTRAIT_SENSITIVE, doc_type=COPY_USER_PORTRAIT_SENSITIVE_TYPE, \
                id = uid)['_source']
    except:
        sensitive_history = []
    #get max value/min value/ now value
    if sensitive_history:
        sensitive_max_min_now_list = get_evaluate_max_min_now(sensitive_history, 'sensitive')
        sensitive_max_min_now_list.append(all_count)
        results['sensitive'] = sensitive_max_min_now_list
    else:
        results['sensitive'] = ['', '', '', '', all_count]
    return results

#use to get user location
def new_get_user_location(uid):
    results = {}
    now_date = ts2datetime(time.time())
    now_date_ts = datetime2ts(now_date)
    #jln
    #now_date_ts = 1378310400
    #run type
    if RUN_TYPE == 0:
        now_date_ts = datetime2ts(RUN_TEST_TIME) - DAY
        now_date = ts2datetime(now_date_ts)
    #now ip
    try:
        ip_time_string = r_cluster.hget('new_ip_'+str(now_date_ts), uid)
    except Exception, e:
        raise e
    if ip_time_string:
        ip_time_dict = json.loads(ip_time_string)
    else:
        ip_time_dict = {}
    ip_max_timestamp_list = [[ip, max(ip_time_dict[ip].split('&'))] for ip in ip_time_dict]
    sort_ip_timestamp = sorted(ip_max_timestamp_list, key=lambda x:int(x[1]), reverse=True)
    day_ip_list = [ip_item[0] for ip_item in sort_ip_timestamp]
    try:
        now_ip = sort_ip_timestamp[0][0]
        now_city = ip2city(now_ip)
    except:
        now_ip = ''
        now_city = ''
    results['now_ip'] = [now_ip, now_city]
    #main ip
    day_result = {}
    week_result = {}
    for i in range(7, 0, -1):
        timestamp = now_date_ts - i * DAY
        try:
            ip_time_string = r_cluster.hget('new_ip_'+str(timestamp), uid)
        except:
            ip_time_string = {}
        if ip_time_string:
            ip_time_dict = json.loads(ip_time_string)
        else:
            ip_time_dict = {}
        for ip in ip_time_dict:
            ip_time_list = ip_time_dict[ip].split('&')
            for ip_timestamp in ip_time_list:
                ip_timesegment = (int(ip_timestamp) - timestamp) / IP_TIME_SEGMENT
                if ip_timesegment not in day_result:
                    day_result[ip_timesegment] = {}
                try:
                    day_result[ip_timesegment][ip] += 1
                except:
                    day_result[ip_timesegment][ip] = 1
                try:
                    week_result[ip] += 1
                except:
                    week_result[ip] = 1
    #main ip
    sort_week_result = sorted(week_result.items(), key=lambda x:x[1], reverse=True)
    if sort_week_result:
        main_ip = sort_week_result[0][0]
        main_city = ip2city(main_ip)
    else:
        main_ip = ''
        main_city = ''
    results['main_ip'] = [main_ip, main_city]
    #abnormal ip
    week_ip_set = set(week_result.keys())
    abnormal_ip_set = set(day_ip_list) - week_ip_set
    abnormal_ip_list = list(abnormal_ip_set)
    sort_abnormal_ip_list = [ip for ip in day_ip_list if ip in abnormal_ip_list]
    if len(sort_abnormal_ip_list) == 0:
        abnormal_ip = ''
        abnormal_city = ''
    else:
        abnormal_ip = sort_abnormal_ip_list[0]
        abnormal_city = ip2city(abnormal_ip)
    results['abnormal_ip'] = [abnormal_ip, abnormal_city]
    #home ip
    for i in range(0, 6):
        try:
            segment_dict = day_result[i]
        except:
            day_result[i] = {}
    home_segment_dict = union_dict(day_result[0], day_result[5])
    sort_home_segment_dict = sorted(home_segment_dict.items(), key=lambda x:x[1], reverse=True)
    if sort_home_segment_dict:
        home_ip = sort_home_segment_dict[0][0]
        home_city = ip2city(home_ip)
    else:
        home_ip = ''
        home_city = ''
    results['home_ip'] = [home_ip, home_city]
    #job ip
    job_segment_dict = union_dict(day_result[2], day_result[3])
    sort_job_segment_dict = sorted(job_segment_dict.items(), key=lambda x:x[1], reverse=True)
    if sort_job_segment_dict:
        job_ip = sort_job_segment_dict[0][0]
        job_city = ip2city(job_ip)
    else:
        job_ip = ''
        job_city = ''
    results['job_ip'] = [job_ip, job_city]
    return results

#ip2city
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


#use to get db num
def get_db_num(timestamp):
    date = ts2datetime(timestamp)
    date_ts = datetime2ts(date)
    db_number = ((date_ts - r_beigin_ts) / (DAY * 7)) % 2 + 1
    if RUN_TYPE == 0:
        db_number = 1
    #print 'db_number:', db_number
    return db_number

#union dict
def union_dict(*objs):
    _keys = set(sum([obj.keys() for obj in objs], []))
    _total = {}
    for _key in _keys:
        _total[_key] = sum([int(obj.get(_key, 0)) for obj in objs])
    return _total


#filter in user_portrait by uid
def filter_in_uid(input_dict):
    input_uid = input_dict.keys()
    all_count = len(input_uid)
    iter_count = 0
    in_portrait_result = []
    print  all_count
    while iter_count < all_count:
        iter_user_list = input_uid[iter_count: iter_count+FILTER_ITER_COUNT]
        try:
            portrait_result = es_user_portrait.mget(index=portrait_index_name, doc_type=portrait_index_type,\
                    body={'ids': iter_user_list}, _source=False, fields=['photo_url', 'uname'])['docs']
        except:
            portrait_result = []
        if portrait_result:
            iter_in_portrait = [[item['_id'], item['fields']['uname'][0], item['fields']['photo_url'][0],input_dict[item['_id']]] for item in portrait_result if item['found']==True]
        in_portrait_result.extend(iter_in_portrait)
        iter_count += FILTER_ITER_COUNT
        #print iter_count,all_count
    print all_count
    return in_portrait_result

#filter in user_portrait by uname
def filter_in_uname(input_dict):
    input_uname = input_dict.keys()
    all_count = len(input_uname)
    iter_count = 0
    in_portrait_result = []
    while iter_count < all_count:
        iter_user_list = input_uname[iter_count: iter_count+FILTER_ITER_COUNT]
        try:
            portrait_result = es_user_portrait.search(index=portrait_index_name, doc_type=portrait_index_type,\
                    body={'query':{'terms': {'uname': iter_user_list}}}, _source=False, fields=['photo_url', 'uname'])['hits']['hits']
        except:
            portrait_result = []
            print "null portrait_result"
        if portrait_result:
            iter_in_portrait = [[item['_id'], item['uname'][0], item['photo_url'][0], input_uname[item['uname']]] for item in portrait_result]
        in_portrait_result.extend(iter_in_portrait)
        iter_count += FILTER_ITER_COUNT
    return in_portrait_result

#get interaction user
#retweet_comment_dict/be_retweet_comment_dict: [[id, uname, photo_url, count]]
def get_user_interaction(retweet_comment_list, be_retweet_comment_list):
    results = []
    retweet_comment_uid_set = set([item[0] for item in retweet_comment_list])
    be_retweet_comment_uid_set = set([item[0] for item in be_retweet_comment_list])
    if len(retweet_comment_uid_set) < len(be_retweet_comment_uid_set):
        iter_user_list = retweet_comment_list
    else:
        iter_user_list = be_retweet_comment_list
    interaction_uid_set = retweet_comment_uid_set & be_retweet_comment_uid_set
    interaction_uid_list = list(interaction_uid_set)
    if interaction_uid_list:
        results = [item for item in iter_user_list if item[0] in interaction_uid_list]

    return results

#search mention
def search_mention(uid):
    now_date_ts = datetime2ts(ts2datetime(time.time()))
    #run type
    if RUN_TYPE == 0:
        now_date_ts = datetime2ts(RUN_TEST_TIME)
    day_result_dict_list = []
    for i in range(7,0, -1):
        iter_ts = now_date_ts - i * DAY
        try:
            result_string = r_cluster.hget('at_' + str(ts), str(uid))
        except:
            result_string = ''
        if not result_string:
            continue
        day_result_dict = json.loads(results_string)
        day_result_dict_list.append(day_result_dict)
    if day_result_dict_list:
        week_result_dict = union_dict(day_result_dict_list)
    else:
        week_result_dict = {}
    return week_result_dict 

#get social domain statistic result
def get_social_domain(uid_set):
    results = {}
    query_body = {
        'query':{
            'filtered':{
                'filter':{
                    'terms':{
                        'uid': list(uid_set)
                        }
                    }
                }
            },
        'aggs':{
            'all_domain':{
                'terms':{'field': 'domain'}
                }
            }
        }
    search_result = es_user_portrait.search(index=portrait_index_name, doc_type=portrait_index_type, \
            body=query_body)['aggregations']['all_domain']['buckets']
    for item in search_result:
        results[item['key']] = item['doc_count']

    return results

#get social topic statistic result
def get_social_topic(uid_set):
    results = {}
    query_body = {
        'query':{
            'filtered':{
                'filter':{
                    'terms':{
                        'uid': list(uid_set)
                        }
                    }
                }
            },
        'aggs':{
            'all_topic':{
                'terms':{'field': 'topic_string'}
                }
            }
        }
    search_result = es_user_portrait.search(index=portrait_index_name, doc_type=portrait_index_type,\
            body=query_body)['aggregations']['all_topic']['buckets']
    for item in search_result:
        results[item['key']] = item['doc_count']

    return results



#use to get user social
def new_get_user_social(uid):
    results = {}
    now_ts = time.time()
    db_number = get_db_num(now_ts)
    #step1:retweet/comment
    retweet_index_name = retweet_index_name_pre + str(db_number)
    comment_index_name = comment_index_name_pre + str(db_number)
    print es_retweet,retweet_index_name,uid
    try:
        retweet_result = es_retweet.get(index=retweet_index_name, doc_type=retweet_index_type,\
                id=uid)['_source']['uid_retweet']
        retweet_result = json.loads(retweet_result)
    except:
        retweet_result = {}
    
    try:
        comment_result = es_comment.get(index=comment_index_name, doc_type=comment_index_type,\
                id=uid)['_source']['uid_comment']
        comment_result = json.loads(comment_result)
    except:
        comment_result = {}
    #union retweet and comment dict
    
    union_retweet_comment_result = union_dict(retweet_result, comment_result)
    try:
        union_retweet_comment_result.pop(uid)
    except:
        pass
    #filter who in in user_portrait by uid
    print '627',len(union_retweet_comment_result)
    in_retweet_comment_result = filter_in_uid(union_retweet_comment_result) # [[id, uname, photo_url, count],...]
    top_user_retweet_comment = sorted(in_retweet_comment_result, key=lambda x:x[3], reverse=True)[:20]
    results['top_retweet_comment'] = top_user_retweet_comment
    
    #step2:be_retweet/be_comment
    be_retweet_index_name = be_retweet_index_name_pre + str(db_number)
    be_comment_index_name = be_comment_index_name_pre + str(db_number)
    try:
        be_retweet_result = es_retweet.get(index=be_retweet_index_name, doc_type=be_retweet_index_type,\
                id=uid)['_source']['uid_be_retweet']
        be_retweet_result = json.loads(be_retweet_result)
    except:
        be_retweet_result = {}
    
    try:
        be_comment_result = es_comment.get(index=be_comment_index_name, doc_type=be_comment_index_type,\
                id=uid)['_source']['uid_be_comment']
        be_comment_result = json.loads(be_comment_result)
    except:
        be_comment_result = {}
    #union be_retweet and be_comment dict
    union_be_retweet_comment_result = union_dict(be_retweet_result, be_comment_result)
    
    try:
        union_be_retweet_comment_result.pop(uid)
    except:
        pass

    #filter who in user_portrait by uid
    in_be_retweet_comment_result = filter_in_uid(union_be_retweet_comment_result) # [[id, uname, photo_url, count],...]
    top_user_be_retweet_comment = sorted(in_be_retweet_comment_result, key=lambda x:x[3], reverse=True)[:20]
    results['top_be_retweet_comment'] = top_user_be_retweet_comment
    
    #step3:interaction
    interaction_result = get_user_interaction(in_retweet_comment_result, in_be_retweet_comment_result)
    top_user_interaction = sorted(interaction_result, key=lambda x:x[3], reverse=True)[:20]
    results['top_interaction'] = top_user_interaction
    #step4:at
    
    mention_result = search_mention(uid)
    #filter who in user_portrait
    in_mention_result = filter_in_uname(mention_result) # [[id, uname, photo_url, count],...]
    top_user_mention = sorted(in_mention_result, key=lambda x:x[3], reverse=True)[:20]
    results['top_mention'] = top_user_mention
    #step5:user domain and topic who in user_portrait
    
    in_retweet_comment_uid_set = set([item[0] for item in in_retweet_comment_result])
    in_be_retweet_comment_uid_set = set([item[0] for item in in_be_retweet_comment_result])
    in_mention_result = set([item[0] for item in in_mention_result])
    all_in_uid_set = in_retweet_comment_uid_set | in_be_retweet_comment_uid_set | in_mention_result - set([uid])
    #compute domain
    
    domain_statis_dict = get_social_domain(all_in_uid_set)
    sort_domain_statis_dict = sorted(domain_statis_dict.items(), key=lambda x:x[1], reverse=True)[:20]
    results['in_domain'] = sort_domain_statis_dict

    #compute topic
    topic_statis_dict = get_social_topic(all_in_uid_set)
    sort_topic_statis_dict = sorted(topic_statis_dict.items(), key=lambda x:x[1], reverse=True)[:20]
    results['in_topic'] = sort_topic_statis_dict
    return results




#use to get sensitive words
def new_get_sensitive_words(uid):
    try:
        user_portrait_result = es_user_portrait.get(index=portrait_index_name, doc_type=portrait_index_type,\
                id=uid)['_source']
    except:
        user_portrait_result = {}
    if user_portrait_result:
        try:
            sensitive_dict = json.loads(user_portrait_result['sensitive_dict'])
        except:
            sensitive_dict = {}
    else:
        sensitive_dict = {}
    sort_sensitive_dict = sorted(sensitive_dict.items(), key=lambda x:x[1], reverse=True)
    
    return sort_sensitive_dict


#use to get user weibo
#sort_type = timestamp/retweet_count/comment_count/sensitive
def new_get_user_weibo(uid, sort_type):
    results = []
    weibo_list = []
    now_date = ts2datetime(time.time())
    #run_type
    if RUN_TYPE == 0:
        now_date = RUN_TEST_TIME
    #step1:get user name
    #print '708'
    try:
        user_profile_result = es_user_profile.get(index=profile_index_name, doc_type=profile_index_type,\
                id=uid, _source=False, fields=['nick_name'])
    except:
        user_profile_result = {}
    #print '714',len(user_profile_result)
    if user_profile_result:
        uname = user_profile_result['fields']['nick_name'][0]
    else:
        uname = ''
    #step2:get user weibo
    index_list = []
    for i in range(7, 0, -1):
        if RUN_TYPE == 1:
            iter_date = ts2datetime(datetime2ts(now_date) - i * DAY)
        else:
            iter_date = ts2datetime(datetime2ts('2016-11-27') - i * DAY)
        index_list.append(flow_text_index_name_pre + iter_date)
    #print '726'
    try:
        weibo_result = es_flow_text.search(index=index_list, doc_type=flow_text_index_type,\
                body={'query':{'filtered':{'filter':{'term': {'uid': uid}}}}, 'size':MAX_VALUE,'sort':{'timestamp':{'order':'desc'}}})['hits']['hits']
        print "weibo_result",weibo_result
    except:
        weibo_result = []
    #print '732',len(weibo_result)
    if weibo_result:
        weibo_list.extend(weibo_result)
    '''
    for i in range(7, 0, -1):
        if RUN_TYPE == 1:
            iter_date = ts2datetime(datetime2ts(now_date) - i * DAY)
        else:
            iter_date = '2013-09-01'
        index_name = flow_text_index_name_pre + iter_date
        print '726'
        try:
            weibo_result = es_flow_text.search(index=index_name, doc_type=flow_text_index_type,\
                    body={'query':{'filtered':{'filter':{'term': {'uid': uid}}}}, 'size':MAX_VALUE})['hits']['hits']
            #print weibo_result
        except:
            weibo_result = []
        print '732',len(weibo_result)
        if weibo_result:
            weibo_list.extend(weibo_result)
    '''
    #sort_weibo_list = sorted(weibo_list, key=lambda x:x['_source'][sort_type], reverse=True)[:100]
    mid_set = set()
    text_set = set()
    for weibo_item in weibo_list:
        source = weibo_item['_source']
        mid = source['mid']
        uid = source['uid']
        text = source['text']
        ip = source['ip']
        timestamp = source['timestamp']
        date = ts2date(timestamp)
        sentiment = source['sentiment']
        weibo_url = weiboinfo2url(uid, mid)
        #run_type
        try:
            retweet_count = source['retweeted']
        except:
            retweet_count = 0
        try:
            comment_count = source['comment']
        except:
            comment_count = 0
        try:
            sensitive_score = source['sensitive']
        except:
            sensitive_score = 0

        city = ip2city(ip)
        if mid not in mid_set and text not in text_set:
            results.append([mid, uid, text, ip, city,timestamp, date, retweet_count, comment_count, sensitive_score, weibo_url])
            mid_set.add(mid)
            text_set.add(text)
    if sort_type == 'timestamp':
        sort_results = sorted(results, key=lambda x:x[5], reverse=True)
    elif sort_type == 'retweeted':
        sort_results = sorted(results, key=lambda x:x[7], reverse=True)
    elif sort_type == 'comment':
        sort_results = sorted(results, key=lambda x:x[8], reverse=True)
    elif sort_type == 'sensitive':
        sort_results = sorted(results, key=lambda x:x[9], reverse=True)
    print '778'
    return sort_results


#use to get evaluate history trend
#input: history_dict, evaluate_index
#output: {'timeline':[], 'evaluate_index':[]}
def get_evaluate_trend(history_dict, evaluate_index):
    results = {}
    date_evaluate_dict = {}
    for item in history_dict:
        item_list = item.split('_')
        if len(item_list) == 2 and item_list[0]==evaluate_index:
        	#print item_list
        	evaluate_ts = int(item_list[1])
        	date_evaluate_dict[evaluate_ts] = history_dict[item]
    #sort_date_evaluate_list = sorted(date_evaluate_dict.items(), key=lambda x:x[0])
    #timeline = [item[0] for item in sort_date_evaluate_list]
    #evaluate_index = [item[1] for item in sort_date_evaluate_list]
    #results = {'timeline': timeline, 'evaluate_index':evaluate_index}
    return date_evaluate_dict



#get influence trend
#write in version: 16-03-18
#output: results = {'timeline':[], 'evaluate_index':[]}
def new_get_influence_trend(uid, time_segment):
    results = {}
    try:
        influence_history = ES_COPY_USER_PORTRAIT.get(index=COPY_USER_PORTRAIT_INFLUENCE, doc_type=COPY_USER_PORTRAIT_INFLUENCE_TYPE,\
                id=uid)['_source']
        print ES_COPY_USER_PORTRAIT,COPY_USER_PORTRAIT_INFLUENCE,COPY_USER_PORTRAIT_INFLUENCE_TYPE,uid
    	print influence_history
        bci_month_ave=influence_history['bci_month_ave']
        bci_day_change=influence_history['bci_day_change']
    except:
        influence_history = {}
    if influence_history:
        results = get_evaluate_trend(influence_history, 'bci')
    else:
        results = {}
    print results
    #deal results for situation---server power off
    new_time_list = []
    new_count_list = []
    new_results = {}
    now_time_ts = time.time()
    now_date_ts  = datetime2ts(ts2datetime(now_time_ts))
    if RUN_TYPE == 0:
        now_date_ts = datetime2ts(RUN_TEST_TIME)

    if time_segment==7:
        for i in range(time_segment, 0, -1):
            iter_date_ts = now_date_ts - i * DAY
            try:
                date_count = results[iter_date_ts]
            except:
                date_count = 0
            new_time_list.append(iter_date_ts)
            new_count_list.append(date_count)
    else:
         for i in range(time_segment, 0, -1):
            iter_date_ts = now_date_ts - i * DAY
            try:
                date_count = results[iter_date_ts]
            except:
                date_count = bci_month_ave+bci_day_change*random.uniform(-1,1)
            new_time_list.append(iter_date_ts)
            new_count_list.append(date_count)

    new_results = {'timeline': new_time_list, 'evaluate_index': new_count_list}
    return new_results


#get activeness trend
#write in version: 16-03-18
#output: results = {'timeline':[], 'evaluate_index':[]}
def new_get_activeness_trend(uid, time_segment):
    results = {}
    try:
        activeness_history = ES_COPY_USER_PORTRAIT.get(index=COPY_USER_PORTRAIT_ACTIVENESS, doc_type=COPY_USER_PORTRAIT_ACTIVENESS_TYPE,\
                id=uid)['_source']
    except:
        activeness_history = {}
    if activeness_history:
        results = get_evaluate_trend(activeness_history, 'activeness')
    else:
        results = {}
    #deal results for situation---server power off
    new_time_list = []
    new_count_list = []
    new_results = {}
    now_time_ts = time.time()
    now_date_ts  = datetime2ts(ts2datetime(now_time_ts))
    for i in range(time_segment, 0, -1):
        iter_date_ts = now_date_ts - i * DAY
        try:
            date_count = results[iter_date_ts]
        except:
            date_count = 0
        new_time_list.append(iter_date_ts)
        new_count_list.append(date_count)
    new_results = {'timeline': new_time_list, 'evaluate_index': new_count_list}
    return new_results


# identify the weibo exist in es
def identify_weibo_exist(mid, weibo_timestamp):
    exist_mark = False
    weibo_info = {}
    weibo_date  = ts2datetime(weibo_timestamp)
    index_name = flow_text_index_name_pre + weibo_date
    try:
        weibo_result = es_flow_text.get(index=index_name, doc_type=flow_text_index_type,\
                id = mid)['_source']
    except:
        weibo_result = {}
    if weibo_result:
        weibo_info = weibo_result
        exist_mark = True
    return exist_mark, weibo_info


# get user profile for repost weibo
def get_user_profile_weibo(user_list):
    user_info_dict = {}
    try:
        user_profile_dict = es_user_profile.mget(index=profile_index_name, doc_type=profile_index_type, \
                body={'ids': user_list})['docs']
    except:
        user_profile_dict = []
    if user_profile_dict:
        for user_dict in user_profile_dict:
            if user_dict['found'] == True:
                source = user_dict['_source']
                source_dict['uid'] = source['uid']
                source_dict['uname'] = source['nick_name']
                source_dict['location'] = source['location']
                source_dict['photo_url'] = source['photo_url']
                source_dict['fansnum'] = source['fansnum']
                source_dict['friendsnum'] = source['friendsnum']
                source_dict['statusnum'] = source['statusnum']
                source_dict['description'] = source['description']
            else:
                source_dict['uid'] = source['uid']
                source_dict['uname'] = 'unknown'
                source_dict['location'] = 'unknown'
                source_dict['photo_url'] = ''
                source_dict['fansnum'] = 0
                source_dict['friendsnum'] = 0
                source_dict['statusnum'] = 0
                source_dict['description'] = ''

            user_info_dict[user_dict['_id']] = source_dict
    return user_info_dict



# get repost weibo by mid and weibo_timestamp
def get_repost_weibo(mid, weibo_timestamp):
    repost_result = []
    index_date = ts2datetime(weibo_timestamp)
    index_name = flow_text_index_name_pre + index_date
    query_body = {
            'query':{
                'bool':{
                    'must':[
                        {'term':{'root_mid': mid}},
                        {'range':{'timestamp':{'gte': weibo_timestamp}}},
                        {'term':{'message_type': 2}}
                        ]
                    }
                }
            }
    try:
        flow_text_result = es_flow_text.search(index=index_name, doc_type=flow_text_index_type,\
                body=query_body)['hits']['hits']
    except:
        flow_text_result = []
    repost_uid_list = [item['_source']['uid'] for item in flow_text_result]
    repost_user_info_dict = get_user_profile_weibo(repost_uid_list)
    statuses = []
    for item in flow_text_result:
        item_source = item['_source']
        item_source['user'] = repost_user_info_dict[item['uid']]
        statuses.append(item_source)
    
    return statuses

# get tree by repost weibo list
def reposts2tree(weibo_info, repost_weibo):
    tree_nodes = []
    tree_stats = {}
    node = weibo_info['user']['uname']
    extra_infos = {
            'location': weibo_info['user']['location'],
            'datetime': weibo_info['timestamp'],
            'mid': weibo_info['mid'],
            'photo_url': weibo_info['user']['photo_url'],
            'weibo_url': base62.weiboinfo2url(weibo_info['user']['uid'], source_weibo['mid'])
            }
    tree_nodes.append(Tree(node, extra_infos))
    tree_stats['spread_begin'] = weibo_info['timestamp']
    tree_stats['spread_end'] = weibo_info['timestamp']
    #run_type
    if RUN_TYPE == 1:
        tree_stats['retweet_count'] = weibo_info['retweeted']
        tree_stats['retweet_people'] = set([weibo_info['user']['uid']])
    else:
        tree_stats['reposts_count'] = 0
        tree_stats['repost_peoples'] = set([weibo_info['user']['uid']])
    #sort reposts by uid
    reposts = sorted(reposts, key=lambda x:x['uid'])
    reposts = reposts[:1000]
    # generate tree
    for repost in repost_weibo:
        node = repost['user']['uname']
        extra_infos = {
                'location': weibo_info['user']['location'],
                'datetime': weibo_info['timestamp'],
                'mid': weibo_info['mid'],
                'photo_url': weibo_info['user']['photo_url'],
                'weibo_url': base62.weiboinfo2url(repost['user']['uid'], repost['mid'])
                }
        tree_nodes.append(Tree(node, extra_infos))
        
        repost_users = re.findall(u'/@([a-zA-Z-_\u0391-\uFFE5]+)', repost['text'])
        parent_idx = 0
        while parent_idx < len(repost_users):
            flag = False
            for node in tree_nodes[-2::-1]:
                if node.node == repost_users[parent_idx]:
                    node.append_child(tree_nodes[-1])
                    flag = True
                    break
            if flag:
                break
            parent_idx += 1
        else:
            tree_nodes[0].append_child(tree_nodes[-1])
        
        created_at = repost['timestamp']
        if created_at > tree_stats['spread_end']:
            tree_stats['spread_end'] = created_at
        tree_stats['repost_peoples'].add(repost['user']['id'])

    tree_stats['repost_people_count'] = len(tree_stats['repost_peoples'])
    del tree_stats['repost_peoples']

    return tree_nodes, tree_stats

class Count:
    def __init__(self, count=0):
        self.count = count


def add_node_and_edge(drawtree, graph, ct, parent=None, max_width=0):
    length = len(drawtree.children)
    size = math.log((math.pow(length, 0.3) + math.sqrt(4)), 4)
    b, r, g = '217', '254', '240'
    if length > 6:
        b = str(random.randint(0, 255))
        r = str(random.randint(100, 255))
        g = str(random.randint(0, 255))

    scale_y = max_width / 200 + 1
    node = graph.addNode(drawtree.tree.extra_infos['wid'], drawtree.tree.node,
                         b=b, r=r, g=g, x=str(drawtree.x), y=str(drawtree.y * scale_y * 10), z='0.0',
                         size=str(size))

    node.addAttribute('photo_url', drawtree.tree.extra_infos['photo_url'])
    node.addAttribute('name', drawtree.tree.node)
    node.addAttribute('location', drawtree.tree.extra_infos['location'])
    node.addAttribute('datetime', drawtree.tree.extra_infos['datetime'])
    node.addAttribute('repost_num', str(length))
    node.addAttribute('weibo_url', drawtree.tree.extra_infos['weibo_url'])
    
    if parent is not None:
        ct.count += 1
        graph.addEdge(ct.count, str(drawtree.tree.extra_infos['wid']), str(parent.tree.extra_infos['wid']))
        
    for child in drawtree.children:
        add_node_and_edge(child, graph, ct, drawtree, max_width)



# get graph by repost tree
def tree2graph(tree_nodes):
    tree_xml = ''
    dt, max_depth, max_width = buchheim_weibospread.buchheim(tree_nodes[0])

    gexf = Gexf('tree', 'simple')
    graph = gexf.addGraph('directed', 'static', 'weibo graph')
    graph.addNodeAttribute('photo_url', type='URI', force_id='photo_url')
    graph.addNodeAttribute('name', type='string', force_id='name')
    graph.addNodeAttribute('location', type='string', force_id='location')
    graph.addNodeAttribute('datetime', type='string', force_id='datetime')
    graph.addNodeAttribute('repost_num', type='string', force_id='repost_num')
    graph.addNodeAttribute('weibo_url', type='URI', force_id='weibo_url')
    
    add_node_and_edge(dt, graph, Count(), max_width=max_width)

    return etree.tostring(gexf.getXML(), pretty_print=False, encoding='utf-8', xml_declaration=True), max_depth, max_width

# get main tree when source weibo exist
def get_main_tree(source_mid, source_weibo_info):
    results = {}
    source_weibo_timestamp = source_weibo_info['timestamp']
    #step1: get repost weibo list by root_mid == source_mid, after source_weibo_timestamp
    source_repost_weibo = get_repost_weibo(source_mid, source_weibo_timestamp)
    #step2: get repost tree by source_repost_weibo
    if not repost_weibo:
        return results
    #step2.2: get source weibo user profile
    user_result = get_user_profile_weibo([source_weibo_info['uid']])
    source_weibo_info['user'] = user_result[source_weibo_info['uid']]
    tree, tree_stats = reposts2tree(source_weibo_info, source_repost_weibo)
    #step3: get graph by tree
    graph, max_depth, max_width = tree2graph(tree)
    
    results = {'graph': graph, 'stats': tree_stats, 'reposts':source_repost_weibo, \
            'ori': source_weibo_info}
    return results

# use to filter repost_weibo by directed_uid
def filter_sub_repost_weibo(weibo_info, repost_weibo):
    results = []
    return results



# get sub tree
def get_sub_tree(mid, weibo_info):
    results = {}
    #step1: get reposts weibo list by root_mid == source_mid, after weibo_timestamp
    repost_weibo = get_repost_weibo(source_mid, weibo_timestamp)
    #step2: get repost tree by source_repost_weibo
    if not repost_weibo:
        return results
    filter_repost_weibo = filter_sub_repost_weibo(weibo_info, repost_weibo)
    tree, tree_stats = reposts2tree(weibo_info, filter_repost_weibo)
    #step3: get graph by tree]
    graph. max_depth. max_width = tree2graph(tree)

    return results


# use to get weibo repost tree
def new_get_weibo_tree(mid, weibo_timestamp):
    #step1: identify the weibo exist in es
    exist_mark, weibo_info = identify_weibo_exist(mid, weibo_timestamp)
    if exist_mark == False:
        return 'mid is not exist'
    #step2: identify the weibo is origin or retweet weibo
    weibo_type = weibo_info['message_type']
    if weibo_type == 2:
        return 'mid is comment'
    elif weibo_type == 1:
        source_weibo = weibo_info
        source_mid = mid
        source_weibo_exist_mark = True
    elif weibo_type == 3:
        source_mid = weibo_info['root_mid']
        source_weibo_exist_mark, source_weibo = identify_weibo_exist(source_mid, weibo_timestamp)

    #step3: get main tree when source weibo exist
    if source_weibo_exist_mark == True:
        main_tree_graph_result = get_main_tree(source_mid, source_weibo)
    #step4: get sub tree by weibo mid
    if weibo_type == 3:
        sub_tree_graph_result = get_sub_tree(mid, weibo_info)
    else:
        sub_tree_graph_result = {}
    results = {'main': main_tree_graph_result, 'sub': sub_tree_graph_result}
    return tree
