# -*- coding: UTF-8 -*-
'''
update attribute of user portrait one week
update attr: topic, keywords, online_pattern, importance
update freq: one week
'''
import sys
import time
import json
from cron_text_attribute import topic_en2ch, get_fansnum_max
from elasticsearch.helpers import scan
from weibo_api_v2 import read_flow_text_sentiment, read_flow_text
from evaluate_index import get_importance
# compute user topic
from topic.test_topic import topic_classfiy

reload(sys)
sys.path.append('../../')
from global_utils import es_user_portrait as es
from global_utils import es_user_portrait
from global_utils import update_week_redis, UPDATE_WEEK_REDIS_KEY
from parameter import WEIBO_API_INPUT_TYPE, WEEK, RUN_TYPE, RUN_TEST_TIME
from time_utils import ts2datetime


def deal_bulk_action(user_info_list, fansnum_max):
    start_ts = time.time()
    uid_list = user_info_list.keys()
    #acquire bulk user weibo data
    if WEIBO_API_INPUT_TYPE == 0:
        user_keywords_dict, user_weibo_dict, online_pattern_dict, character_start_ts = read_flow_text_sentiment(uid_list)
    else:
        user_keywords_dict, user_weibo_dict, online_pattern_dict, character_start_ts = read_flow_text(uid_list)
    #compute attribute--keywords, topic, online_pattern            
    #get user topic results by bulk action
    topic_results_dict, topic_results_label = topic_classfiy(uid_list, user_keywords_dict)
    #get bulk action
    bulk_action = []
    for uid in uid_list:
        results = {}
        results['uid'] = uid
        #add user topic attribute
        user_topic_dict = topic_results_dict[uid]
        user_label_dict = topic_results_label[uid]
        results['topic'] = json.dumps(user_topic_dict)
        results['topic_string'] = topic_en2ch(user_label_dict)
        #add user keywords attribute
        keywords_dict = user_keywords_dict[uid]
        keywords_top50 = sorted(keywords_dict.items(), key=lambda x:x[1], reverse=True)[:50]
        keywords_top50_string = '&'.join([keyword_item[0] for keyword_item in keywords_top50])
        results['keywords'] = json.dumps(keywords_top50)
        results['keywords_string'] = keywords_top50_string
        #add online_pattern
        user_online_pattern = json.dumps(online_pattern_dict[uid])
        results['online_pattern'] = user_online_pattern
        try:
            results['online_pattern_aggs'] = '&'.join(user_online_pattern.keys())
        except:
            results['online_pattern_aggs'] = ''
        #add user importance
        user_domain = user_info_list[uid]['domain'].encode('utf-8')
        user_fansnum = user_info_list[uid]['fansnum']
        results['importance'] = get_importance(user_domain, results['topic_string'], user_fansnum, fansnum_max)
        #bulk action
        action = {'update':{'_id': uid}}
        bulk_action.extend([action, {'doc': results}])
    es_user_portrait.bulk(bulk_action, index=portrait_index_name, doc_type=portrait_index_type)
    end_ts = time.time()
    #log_should_delete
    #print '%s sec count %s' % (end_ts - start_ts, len(uid_list))
    #log_should_delete
    start_ts = end_ts


#use to update attribute every week for topic, keywords, online_pattern, importance
#write in version: 16-02-28
#this file run after the file: scan_es2redis_week.py function:scan_es2redis_week()
def update_attribute_week_v2():
    bulk_action = []
    count = 0
    user_list = []
    user_info_list = {}
    start_ts = time.time()
    #get fansnum max
    fansnum_max = get_fansnum_max()
    while True:
        r_user_info = update_week_redis.rpop(UPDATE_WEEK_REDIS_KEY)
        if r_user_info:
            r_user_info = json.loads(r_user_info)
            uid = r_user_info.keys()[0]
            count += 1
            user_info_list[uid] = r_user_info[uid]
        else:
            break
        
        if count % 1000 == 0:
            #get bulk action
            deal_bulk_action(user_info_list, fansnum_max)
            user_info_list = {}

    if user_info_list != {}:
        #get bulk action
        deal_bulk_action(user_info_list, fansnum_max)


#abandon in version: 16-02-28
#use to update attribute every month for domain, topic, psy, tendency
#write in version: 15-12-08
#this file run after the file: scan_es2redis.py function:scan_es2redis_week()
'''
def update_attribute_week_v1():
    bulk_action = []
    count = 0
    user_info_list = {}
    start_ts = time.time()
    while True:
        r_user_info = update_week_redis.rpop(UPDATE_WEEK_REDIS_KEY)
        if r_user_info:
            r_user_info = json.loads(r_user_info)
            uid = r_user_info.keys()[0]
            user_info_list[uid] = r_user_info[uid]
            count += 1
        else:
            break

        if count % 1000 == 0:
            uid_list = user_info_list.keys()
            #get user_list weibo dict (7 days): {uid1: [weibo1, weibo2,..], uid2:[weibo1, weibo2,...]}
            user_weibo_dict = read_user_weibo(user_list)
            #deal input data structure
            #get tendency input data
            user_weibo_string = get_user_weibo_string(user_weibo_dict)
            #get domain and topic input data
            user_keywords_dict = get_user_keywords_dict(user_weibo_string_dict)
            #get user event results by bulk action
            event_results_dict = event_classfiy(user_weibo_string_dict)
            #get user topic results by bulk action
            topic_results_dict, topic_results_label = topic_classfiy(user_keywords_dict)
            #get user domain results by bulk action
            domain_results_dict = domain_classfiy(user_keywords_dict)
            #get user psy results by bulk action
            psy_results_dict = psychology_clssfiy(user_weibo_dict)
            
            bulk_action = []
            results = {}
            for uid in uid_list:
                results['uid'] = uid
                #add user topic attribute
                user_topic_dict = topic_results_dict[uid]
                user_label_dict = topic_results_label[uid]
                results['topic'] = json.dumps(user_topic_dict)
                results['topic_string'] = topic_en2ch(user_label_dict)
                #add user domain attribute
                user_domain_dict = domain_results_dict[uid]
                user_label_dict = domain_results_label[uid]
                results['domain_v3'] = json.dumps(user_label_dict)
                results['domain'] = domain_en2ch(user_label_dict)
                #add user event attribute
                results['tendency'] = event_results_dict[uid]
                #add user psy attribute
                new_user_psy_dict = psy_results_dict[uid]
                old_user_psy_list = json.loads(user_info_list[uid]['psycho_status'])
                user_psy_list = old_user_psy_list[-1:].add(new_user_psy_dict)
                results['psycho_status'] = json.dumps(user_psy_list)
                action = {'update':{'_id': uid}}
                bulk_action.extend([action, {'doc': results}])
            es_user_portrait.bulk(bulk_action, index=portrait_index_name, doc_type=portrait_index_type)
            user_info_list = {}
            end_ts = time.time()
            print '%s sec count 1000' % (end_ts - start_ts)
            start_ts = end_ts
    
    print 'count:', count
'''

#abandon in version: 15-12-08
'''
def update_atttribute_week():
    # scan the user_portrait and bulk action to update
    status = False
    results = {}
    count = 0
    index_name = 'user_portriat'
    index_type = 'user'
    s_re = scan(es, query={'query':{'match_all':{}}, 'size':1000}, index=index_name, doc_type=index_type)
    while True:
        bulk_action = []
        uid_list = []
        while True:
            try:
                scan_re = s_re.next()['_source']
                count += 1
            except StopIteration:
                print 'all done'
                sys.exit(0)
            except Exception, r:
                print Exception, r
                sys.exit(0)
            uid = scan_re['uid']
            uid_list.append(uid)
            if count%1000==0:
                break
        if uid_list:
            # get user list weibo dict from weibo api
            user_weibo_dict = read_user_weibo(uid_list)
            status = compute2in(uid_list, user_weibo_dict, status='update')
            print 'status:', status
    return status
'''

if __name__=='__main__':
    log_time_ts = time.time()
    log_time_date = ts2datetime(log_time_ts)
    print 'cron/text_attribute/update_week.py&start&' + log_time_date

    update_attribute_week_v2()
    
    log_time_ts = time.time()
    log_time_date = ts2datetime(log_time_ts)
    print 'cron/text_attribute/update_week.py&start&' + log_time_date
