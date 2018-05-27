# -*- coding: UTF-8 -*-
'''
acquire the information from flow
input: uid_list and date_ts
output: {uid:{attr:value}}
update: one day
'''
import IP
import sys
import time
import json
reload(sys)
sys.path.append('../../')
from global_utils import R_CLUSTER_FLOW2 as r_cluster
from global_utils import flow_text_index_name_pre, flow_text_index_type, es_flow_text
from global_utils import R_ADMIN as r_sensitive
from parameter import DAY, MAX_VALUE, sensitive_score_dict
from parameter import RUN_TYPE, RUN_TEST_TIME, WEEK
from time_utils import datetime2ts, ts2datetime, ts2date

test_ts = datetime2ts(RUN_TEST_TIME)

WEEK = 7

#use to get hashtag information from flow
#wirte in version:15-12-08
#input:uid_list
#output:{uid:{attr:value}}
def get_flow_information(uid_list):
    results = {}      
    #results = {uid:{'hashtag_dict':{},'hashtag':'', 'keywords_dict':{}, 'keywords_string':'', 'activity_geo':'', 'activity_geo_dict':dict}}
    iter_results = {} # iter_results = {uid:{'hashtag': hashtag_dict, 'geo':geo_dict, 'keywords':keywords_dict}}
    now_ts = time.time()
    now_date_ts = datetime2ts(ts2datetime(now_ts))
    #test
    now_date_ts = test_ts
    for i in range(7,0,-1):
        ts = now_date_ts - DAY*i
        iter_date = ts2datetime(ts)
        flow_text_index_name = flow_text_index_name_pre + iter_date
        uid_day_geo = {}
        #compute hashtag and geo
        hashtag_results = r_cluster.hmget('hashtag_'+str(ts), uid_list)
        ip_results = r_cluster.hmget('new_ip_'+str(ts), uid_list)
        #compute sensitive_words
        sensitive_results = r_cluster.hmget('sensitive_'+str(ts), uid_list)
        count = 0 
        for uid in uid_list:
            #init iter_results[uid]
            if uid not in iter_results:
                iter_results[uid] = {'hashtag':{}, 'geo':{},'geo_track':[],'keywords':{}, 'sensitive':{}}
            #compute hashtag
            hashtag_item = hashtag_results[count]
            if hashtag_item:
                uid_hashtag_dict = json.loads(hashtag_item)
            else:
                uid_hashtag_dict = {}
            for hashtag in uid_hashtag_dict:
                try:
                    iter_results[uid]['hashtag'][hashtag] += uid_hashtag_dict[hashtag]
                except:
                    iter_results[uid]['hashtag'][hashtag] = uid_hashtag_dict[hashtag]
            #compute sensitive
            sensitive_item = sensitive_results[count]
            if sensitive_item:
                uid_sensitive_dict = json.loads(sensitive_item)
            else:
                uid_sensitive_dict = {}
            for sensitive_word in uid_sensitive_dict:
                try:
                    iter_results[uid]['sensitive'][sensitive_word] += uid_sensitive_dict[sensitive_word]
                except:
                    iter_results[uid]['sensitive'][sensitive_word] = uid_sensitive_dict[sensitive_word]
            #compute geo
            uid_day_geo[uid] = {}
            ip_item = ip_results[count]
            if ip_item:
                uid_ip_dict = json.loads(ip_item)
            else:
                uid_ip_dict = {}
            for ip in uid_ip_dict:
                ip_count = len(uid_ip_dict[ip].split('&'))
                geo = ip2city(ip)
                if geo:
                    #print 'geo:', geo
                    try:
                        iter_results[uid]['geo'][geo] += ip_count
                    except:
                        iter_results[uid]['geo'][geo] = ip_count
                    try:
                        uid_day_geo[uid][geo] += ip_count
                    except:
                        uid_day_geo[uid][geo] = ip_count
            iter_results[uid]['geo_track'].append(uid_day_geo[uid])
            count += 1
        
        #compute keywords:        
        try:
            text_results = es_flow_text.search(index=flow_text_index_name, doc_type=flow_text_index_type, \
                                               body={'query':{'filtered':{'filter':{'terms':{'uid': uid_list}}}}, 'size':MAX_VALUE}, _source=True, fields=['uid', 'keywords_dict','text'])['hits']['hits']
        except:
            text_results = {}
        for item in text_results:
            #print 'keywords item:', item
            uid = item['fields']['uid'][0]
            uid_keywords_dict = json.loads(item['fields']['keywords_dict'][0])
            for keywords in uid_keywords_dict:
                try:
                    iter_results[uid]['keywords'][keywords] += uid_keywords_dict[keywords]
                except:
                    iter_results[uid]['keywords'][keywords] = uid_keywords_dict[keywords]

            #jln filter keyword 2016/11/08
            weibo_text = json.loads(item['fields']['text'][0])
            filter_keywords_dict = get_weibo_single(weibo_text)

            for keywords in filter_keywords_dict:
                try:
                    iter_results[uid]['filter_keywords'][keywords] += uid_keywords_dict[keywords]
                except:
                    iter_results[uid]['filter_keywords'][keywords] = uid_keywords_dict[keywords]

        
    #get keywords top
    for uid in uid_list:
        results[uid] = {}
        hashtag_dict = iter_results[uid]['hashtag']
        results[uid]['hashtag_dict'] = json.dumps(hashtag_dict)
        results[uid]['hashtag'] = '&'.join(hashtag_dict.keys())
        #sensitive words
        sensitive_word_dict = iter_results[uid]['sensitive']
        results[uid]['sensitive_dict'] = json.dumps(sensitive_word_dict)
        results[uid]['sensitive_string'] = '&'.join(sensitive_word_dict.keys())
        sensitive_score = 0
        for item in sensitive_word_dict:
            k = item
            v = sensitive_word_dict[k]
            tmp_stage = r_sensitive.hget('sensitive_words', k)
            if tmp_stage:
                sensitive_score += v * sensitive_score_dict[str(tmp_stage)]
        results[uid]['sensitive'] = sensitive_score
        #print 'sensitive_dict:', results[uid]['sensitive_dict']
        #print 'sensitive_string:', results[uid]['sensitive_string']
        #print 'sensitive:', results[uid]['sensitive']
        #geo
        geo_dict = iter_results[uid]['geo']
        geo_track_list = iter_results[uid]['geo_track']
        results[uid]['activity_geo_dict'] = json.dumps(geo_track_list)
        geo_dict_keys = geo_dict.keys()
        #print 'geo_dict_keys:', geo_dict_keys
        results[uid]['activity_geo'] = '&'.join(['&'.join(item.split('\t')) for item in geo_dict_keys])
        #print 'activity_geo:',  results[uid]['activity_geo']

        keywords_dict = iter_results[uid]['keywords']
        keywords_top50 = sorted(keywords_dict.items(), key=lambda x:x[1], reverse=True)[:50]
        keywords_top50_string = '&'.join([keyword_item[0] for keyword_item in keywords_top50])
        
        filter_keywords_dict = iter_results[uid]['filter_keywords']
        f_keywords_top50 = sorted(filter_keywords_dict.items(), key=lambda x:x[1], reverse=True)[:50]
        f_keywords_top50_string = '&'.join([filter_keywords_dict[0] for keyword_item in f_keywords_top50])


        results[uid]['keywords'] = json.dumps(keywords_top50)
        results[uid]['keywords_string'] = keywords_top50_string

        results[uid]['filter_keywords'] = json.dumps(f_keywords_top50)
        results[uid]['filter_keywords_string'] = f_keywords_top50_string
    return results


# use to compute flow information for new user attribute compute
# write in version: 2016-02-28
# input: uid_list, keywords_dict
def get_flow_information_v2(uid_list, all_user_keywords_dict):
    results = {}      
    #results = {uid:{'hashtag_dict':{},'hashtag':'', 'keywords_dict':{}, 'keywords_string':'', 'activity_geo':'', 'activity_geo_dict':dict, 'activity_geo_aggs':''}}
    iter_results = {} # iter_results = {uid:{'hashtag': hashtag_dict, 'geo':geo_dict, 'keywords':keywords_dict}}
    now_ts = time.time()
    #run_type
    if RUN_TYPE == 1:
        now_date_ts = datetime2ts(ts2datetime(now_ts))
    else:
        now_date_ts = test_ts
    for i in range(WEEK,0,-1):
        ts = now_date_ts - DAY*i
        print ts
        uid_day_geo = {}
        #compute hashtag and geo
        hashtag_results = r_cluster.hmget('hashtag_'+str(ts), uid_list)
        ip_results = r_cluster.hmget('new_ip_'+str(ts), uid_list)
        #compute sensitive_words
        sensitive_results = r_cluster.hmget('sensitive_'+str(ts), uid_list)
        count = 0 
        for uid in uid_list:
            #init iter_results[uid]
            if uid not in iter_results:
                iter_results[uid] = {'hashtag':{}, 'geo':{},'geo_track':[],'keywords':{}, 'sensitive':{}}
            #compute hashtag
            hashtag_item = hashtag_results[count]
            if hashtag_item:
                uid_hashtag_dict = json.loads(hashtag_item)
            else:
                uid_hashtag_dict = {}
            for hashtag in uid_hashtag_dict:
                try:
                    iter_results[uid]['hashtag'][hashtag] += uid_hashtag_dict[hashtag]
                except:
                    iter_results[uid]['hashtag'][hashtag] = uid_hashtag_dict[hashtag]
            #compute sensitive
            sensitive_item = sensitive_results[count]
            if sensitive_item:
                uid_sensitive_dict = json.loads(sensitive_item)
            else:
                uid_sensitive_dict = {}
            for sensitive_word in uid_sensitive_dict:
                try:
                    iter_results[uid]['sensitive'][sensitive_word] += uid_sensitive_dict[sensitive_word]
                except:
                    iter_results[uid]['sensitive'][sensitive_word] = uid_sensitive_dict[sensitive_word]
            #compute geo
            uid_day_geo[uid] = {}
            ip_item = ip_results[count]
            if ip_item:
                uid_ip_dict = json.loads(ip_item)
            else:
                uid_ip_dict = {}
            for ip in uid_ip_dict:
                ip_count = len(uid_ip_dict[ip].split('&'))
                geo = ip2city(ip)
                if geo:
                    try:
                        iter_results[uid]['geo'][geo] += ip_count
                    except:
                        iter_results[uid]['geo'][geo] = ip_count
                    try:
                        uid_day_geo[uid][geo] += ip_count
                    except:
                        uid_day_geo[uid][geo] = ip_count
            iter_results[uid]['geo_track'].append(uid_day_geo[uid])
            count += 1
               
    #get keywords top
    for uid in uid_list:
        results[uid] = {}
        #hashtag
        hashtag_dict = iter_results[uid]['hashtag']
        results[uid]['hashtag_dict'] = json.dumps(hashtag_dict)
        results[uid]['hashtag'] = '&'.join(hashtag_dict.keys())
        #sensitive words
        sensitive_word_dict = iter_results[uid]['sensitive']
        results[uid]['sensitive_dict'] = json.dumps(sensitive_word_dict)
        results[uid]['sensitive_string'] = '&'.join(sensitive_word_dict.keys())
        sensitive_score = 0
        for sensitive_item in sensitive_word_dict:
            k = sensitive_item
            v = sensitive_word_dict[sensitive_item]
            tmp_stage = r_sensitive.hget('sensitive_words', k)
            if tmp_stage:
                sensitive_score += v * sensitive_score_dict[str(tmp_stage)]
        results[uid]['sensitive'] = sensitive_score
        #print 'sensitive_dict:', results[uid]['sensitive_dict']
        #print 'sensitive_string:', results[uid]['sensitive_string']
        #print 'sensitive:', results[uid]['sensitive']
        #geo
        geo_dict = iter_results[uid]['geo']
        geo_track_list = iter_results[uid]['geo_track']
        results[uid]['activity_geo_dict'] = json.dumps(geo_track_list)
        geo_dict_keys = geo_dict.keys()
        results[uid]['activity_geo'] = '&'.join(['&'.join(item.split('\t')) for item in geo_dict_keys])
        try:
            results[uid]['activity_geo_aggs'] = '&'.join([item.split('\t')[-1] for item in geo_dict_keys])
        except:
            results[uid]['activity_geo_aggs'] = ''

        keywords_dict = all_user_keywords_dict[uid]
        keywords_top50 = sorted(keywords_dict.items(), key=lambda x:x[1], reverse=True)[:50]
        keywords_top50_string = '&'.join([keyword_item[0] for keyword_item in keywords_top50])
        results[uid]['keywords'] = json.dumps(keywords_top50)
        results[uid]['keywords_string'] = keywords_top50_string
        
    return results



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

#abadon in version:15-12-08
'''
def get_flow_information(uid_list):
    results_dict = {}
    now_ts = time.time()
    now_date = ts2datetime(now_ts)
    ts = datetime2ts(now_date)
    #test
    hashtag_results = {}
    geo_results = {}
    timestamp = datetime2ts('2013-09-08')
    user_hashtag_result = dict()
    user_online_result = dict()
    user_ip_result = dict()
    user_ip_list_dict = dict() # {uid:[{ip1:count1, ip2:count2}, {ip3:count3,ip4:count4}]} list index by date
    for i in range(7,0,-1):
        ts = timstamp - 3600*24*i  
        #attr: hashtag
        results = r_cluster.hmget('hashtag_'+str(ts), uid_list)
        #attr: ip
        ip_results = r_cluster.hmget('ip_'+str(ts), uid_list)
        for j in range(0,len(uid_list)):
            uid = uid_list[j]
            #attr: hashtag
            if results[j]:
                hashtag_dict = json.loads(results[j])
                for hashtag in hashtag_dict:
                    if uid in user_hashtag_result:
                        try:
                            user_hashtag_result[uid][hashtag] += hashtag_dict[hashtag]
                        except:
                            user_hashtag_result[uid][hashtag] = hashtag_dict[hashtag]
                    else:
                        user_hashtag_result[uid] = {hashtag: hashtag_dict[hashtag]}
            #attr: ip
            if ip_results[j]:
                ip_dict = json.loads(ip_results[j])
                for ip in ip_dict:
                    if uid in user_ip_result:
                        try:
                            user_ip_result[uid][ip] += ip_dict[ip]
                        except:
                            user_ip_result[uid][ip] = ip_dict[ip]
                    else:
                        user_ip_result[uid] = {ip: ip_dict[ip]}

            #geo from ip-timestamp
            
            day_ip_dict = dict()
            if ip_results[j]:
                ip_timestamp_dict = json.loads(ip_results[j])
                for ip in ip_timestamp_dict:
                    ip_count = len(ip_timestamp_dict[ip].split('&'))
                    day_ip_dict[ip] = ip_count
                    if uid in user_ip_result:
                        try:
                            user_ip_result[uid][ip] += ip_count
                        except:
                            user_ip_result[uid][ip] = ip_count
                    else:
                        user_ip_result[uid] = {ip: ip_count}
            if user in user_ip_list_dict:
                user_ip_list_dict[user].append(day_ip_dict)
            else:
                user_ip_list_dict[user] = [day_ip_dict]
            

    for uid in uid_list:
        #attr: hashtag
        try:
             hashtag_dict = user_hashtag_result[uid]
             hashtag_string = json.dumps(hashtag_dict)
             hashtag_list = '&'.join(hashtag_dict.keys())
        except KeyError:
            hashtag_string = ''
            hashtag_list = ''
        #geo from geo
        try:
            ip_dict = user_ip_result[uid]
            geo_dict = ip2geo(ip_dict)
            geo_string = json.dumps(geo_dict)
            geo_dict_keys = geo_dict.keys()
            geo_one_list = []
            for key in geo_dict_keys:
                key_list = key.split('\t')
                n = len(key_list)
                geo_one_list.append(key_list[n-1])
            geo_list = '&'.join(geo_one_list)
        except KeyError:
            geo_string = ''
            geo_list = ''
        #geo from ip-timestamp
        
        try:
            ip_dict = user_ip_result[uid]
            geo_dict = ip2geo(ip_dict)
            geo_dict_keys = geo_dict.keys()
            geo_one_list = []
            for key in geo_dict_keys:
                key_string = '&'.join(key.split('\t'))
                geo_one_list.append(key_string)
            geo_list = '&'.join(geo_one_list)
        except KeyError:
            geo_list = ''
        try:
            user_ip_list = user_ip_list_dict[uid]
            day_geo_list = []
            for day_ip_dict in user_ip_list:
                geo_dict = ip2geo(day_ip_dict)
                day_geo_list.append(geo_dict)
            geo_string = json.dumps(day_geo_list)
        except KeyError:
            geo_string = ''
        
        results_dict[uid] = {'hashtag_dict':hashtag_string, 'activity_geo_dict':geo_string, \
                             'hashtag':hashtag_list, 'activity_geo':geo_list}
        
        results_dict[uid] = {'hashtag_dict':hashtag_string, 'activity_geo_dict':geo_string, \
                             'hashtag':hashtag_list, 'activity_geo':geo_list, \
                             'online_pattern_dict':online_pattern_string, 'online_pattern': online_pattern_list}
        
    #print 'results_dict:', results_dict
    return results_dict
'''

def ip2geo(ip_dict):
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
            try:
                geo_dict[city] += ip_dict[ip]
            except:
                geo_dict[city] = ip_dict[ip]
    return geo_dict

# use to update flow_information by day
def update_flow_information(user_info):
    results = {} # results ={uid: {'activity_geo_dict':'', 'activity_geo':'', 'hashtag_dict':'', 'hashtag':'', 'online_pattern_dict':'', 'online_pattern':''}}
    uid_list = user_info.keys()
    now_ts = time.time()
    now_date = ts2datetime(now_ts)
    timestamp = datetime2ts(now_date)
    #test
    timestamp = datetime2ts('2013-09-08')
    user_hashtag_dict = dict()
    user_online_dict = dict()
    ip_user_count_dict = {}
    new_day_ip_dict = dict()
    for i in range(7,0,-1):
        ts = timestamp - 24*3600*i
        print 'iter date:', ts2date(ts)
        results = r_cluster.hmget('hashtag_'+str(ts), uid_list)
        online_pattern_results = r_cluster.hmget('online_'+str(ts), uid_list)

        if i==0:
            ip_result = r_cluater.hmget('hashtag_'+str(ts), uid_list)

        for j in range(0, len(uid_list)):
            uid = uid_list[j]
            #attr: hashtag
            if results[j]:
                hashtag_dict = json.loads(results[j])
                for hashtag in hashtag_dict:
                    if uid in user_hashtag_dict:
                        try:
                            user_hashtag_dict[uid][hashtag] += hashtag_dict[hashtag]
                        except:
                            user_hashtag_dict[uid][hashtag] = hashtag_dict[hashtag]
                    else:
                        user_hashtag_dict[uid] = {hashtag: hashtag_dict[hashtag]}
            '''
            #attr: online_pattern
            if online_pattern_results[j]:
                online_pattern_dict = json.loads(online_pattern_results[j])
                for online_pattern in online_pattern_dict:
                    if uid in user_online_dict:
                        try:
                            user_online_dict[uid][online_pattern] += online_pattern_dict[online_pattern]
                        except:
                            user_online_dict[uid][online_pattern] = online_pattern_dict[online_pattern]
                    else:
                        user_online_dict[uid] = {online_pattern: online_pattern_dict[online_pattern]}
            '''
            
            #attr: activity_geo by ip-timestamp
            if i==0 and ip_result[j]:
                ip_timestamp_dict = json.loads(ip_result[j])
                old_flow_information = user_info[uid]
                old_day_geo_list = json.loads(old_flow_information['activity_geo_dict'])
                for ip in ip_timestamp_dict:
                    ip_count = len(ip_timestamp_dict[ip].split('&'))
                    new_day_ip_dict[uid][ip] = ip_count
                geo_dict = ip2city(new_day_ip_dict[uid])
                if len(old_day_geo_list)>=30:
                    new_day_geo_list = old_day_geo_list[1:].append(geo_dict)
                else:
                    new_day_geo_list = old_day_geo_list.append(geo_dict)
                week_geo_list = []
                week_day_geo_list = new_day_geo[-7:]
                for day_geo_dict in week_day_geo_list:
                    week_geo_list.extend(day_geo_dict.keys())
                week_geo_list = list(set(week_geo_list))
                activity_geo_string = ''
                new_week_geo_list = []
                for geo_string in week_geo_list:
                    day_geo_string = '&'.join(geo_string.split('\t'))
                    new_week_geo_list.append(day_geo_string)
                activity_geo_string = '&'.join(new_week_geo_list)
                print 'activity_geo_string:', activity_geo_string
                

    for uid in uid_list:
        #attr: hashtag
        try:
            hashtag_dict = user_hashtag_dict[uid]
            hashtag_string = json.dumps(hashtag_dict)
            hashtag_list = '&'.join(hashtag_dict.keys())
        except KeyError:
            hashtag_string = ''
            hashtag_list = ''
        '''
        #attr: online_pattern
        try:
            online_dict = user_online_dict[uid]
            online_string = json.dumps(online_dict)
            online_list = '&'.join(online_dict.keys())
        except KeyError:
            online_string = ''
            online_list = ''
        '''
        result[uid] = {'hashtag_dict':hashtag_string, 'hashtag':hashtag_list, \
                       'activity_geo_dict': json.loads(new_day_geo_list), 'activity_geo': activity_geo_string, \
                       'online_pattern_dict': online_pattern_string, 'online_pattern': online_pattern_list}
    return result

if __name__=='__main__':
    test_uid = ['1640601392', '2294854302']
    result_dict = get_flow_information_v2(test_uid, dict())
    print 'result_dict:', result_dict
