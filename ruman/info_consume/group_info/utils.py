#-*- coding: UTF-8 -*-
import sys
import time
import json
import math
from mid2weibolink import weiboinfo2url
from get_city_location import get_lat_lng
from ruman.global_config import UPLOAD_FOLDER
from ruman.global_utils import R_GROUP as r
from ruman.global_utils import es_user_portrait as es
from ruman.global_utils import es_user_portrait, portrait_index_name, portrait_index_type,\
                        es_flow_text, flow_text_index_name_pre, flow_text_index_type,\
                        es_user_profile, profile_index_name, profile_index_type,\
                        es_group_result, group_index_name, group_index_type
from ruman.time_utils import ts2datetime, datetime2ts, ts2date
from ruman.parameter import MAX_VALUE, DAY, FOUR_HOUR, SENTIMENT_SECOND
from ruman.global_utils import group_analysis_queue_name
from ruman.parameter import RUN_TYPE, RUN_TEST_TIME
from ruman.keyword_filter import keyword_filter
sys.path.append('./ruman/cron/flow_text/')
from keyword_extraction import get_weibo_single
index_name = group_index_name
index_type = group_index_type

'''
#submit new task and identify the task name unique
def submit_task(input_data):
    status = 0
    result = r.lrange('group_task', 0, -1)
    #print 'result:',result
    for task in result:
        task_dict = json.loads(task)
        task_name = task['task_name']
        if input_data==task_name:
            status += 1
    result = es.get(index=index_name, doc_type=index_type, id=task_name)
    try:
        task_exist = result['_source']
    except:
        status += 1
    if status != 0:
        return False
    else:
        r.lpush('group_task', json.dumps(input_data))
    return True
'''

# read uid list from upload file
def read_uid_file(filename):
    uid_list = []
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    f = open(filepath+'.txt', 'r')
    for line in f:
        if len(line)==10:
            uid_list.append(line)
    return uid_list

# delete uid list after save to redis and es
def delete_uid_file(filename):
    status = 0
    filename += '.txt'
    filenames = os.listdir(UPLOAD_FOLDER)
    if filename in filenames:
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        os.remove(filepath)
    else:
        print 'there no this file'
    return status


#submit new task and identify the task name unique in es-group_result and save it to redis list
def submit_tasks(input_data):
    status = 0 # mark it can not submit
    task_name = input_data['task_name']
    submit_user = input_data['submit_user']
    task_id = submit_user + '-' + task_name
    #identify the compute task is not more than limit
    try:
        task_max_count = input_data['task_max_count']
    except:
        task_max_count = 0
    query_body = {
    'query':{
        'filtered':{
            'filter':{
                'bool':{
                    'must':[
                        {'term': {'submit_user': submit_user}},
                        {'term': {'status': 0}}
                        ]
                    }
                }
            }
        }
    }
    exist_compute_result = es_group_result.search(index=group_index_name, doc_type=group_index_type, body=query_body)['hits']['hits']
    exist_compute_count = len(exist_compute_result)
    #print es_group_result,group_index_namem,group_index_type
    if exist_compute_count >= task_max_count:
        return 'more than limit'
    #identify the task name is valid
    try:
        result = es_group_result.get(index=group_index_name, doc_type=group_index_type, id=task_id)['_source']
    except:
        status = 1
    
    if status != 0 and 'uid_file' not in input_data:
        input_data['status'] = 0 # mark the task not compute
        count = len(input_data['uid_list'])
        input_data['count'] = count
        input_data['task_type'] = 'analysis'
        input_data['submit_user'] = submit_user
        input_data['detect_type'] = ''
        input_data['detect_process'] = ''
        input_data['task_id'] = task_id
        print 'input_data:', input_data
        add_es_dict = {'task_information': input_data, 'query_condition':''}
        es_group_result.index(index=group_index_name, doc_type=group_index_type, id=task_id, body=input_data)
        r.lpush(group_analysis_queue_name, json.dumps(input_data))
    
    return status

#search task by some condition -whether add download
def search_task(task_name, submit_date, state, status, submit_user):
    results = []
    query = []
    condition_num = 0
    if task_name:
        task_name_list = task_name.split(' ')
        for item in task_name_list:
            query.append({'wildcard':{'task_name': '*' + item + '*'}})
            condition_num += 1
    if submit_date:
        submit_date_ts = datetime2ts(submit_date)
        submit_date_start = submit_date_ts
        submit_date_end = submit_date_ts + DAY
        query.append({'range':{'submit_date': {'gte': submit_date_start, 'lt': submit_date_end}}})
        condition_num += 1
    if state:
        state_list = state.split(' ')
        for item in state_list:
            query.append({'wildcard':{'state': '*' + item + '*'}})
            condition_num += 1
    if status:
        query.append({'match':{'status': status}})
        condition_num += 1
    if submit_user:
        query.append({'term':{'submit_user': submit_user}})
        condition_num += 1
    print es_group_result,group_index_name,group_index_type
    if condition_num > 0:
        query.append({'term':{'task_type': 'analysis'}})
        try:
            source = es_group_result.search(
                    index = group_index_name,
                    doc_type = group_index_type,
                    body = {
                        'query':{
                            'bool':{
                                'must':query
                                }
                            },
                        'sort': [{'count':{'order': 'desc'}}],
                        'size': MAX_VALUE
                        }
                    )
        except Exception as e:
            raise e
    else:
        query.append({'term':{'task_type': 'analysis'}})
        source = es.search(
                index = group_index_name,
                doc_type = group_index_type,
                body = {
                    'query':{'bool':{
                        'must':query
                        }
                        },
                    'sort': [{'count': {'order': 'desc'}}],
                    'size': MAX_VALUE
                    }
                )

    try:
        task_dict_list = source['hits']['hits']
    except:
        return None
    result = []
    for task_dict in task_dict_list:
        try:
            state = task_dict['_source']['state']
        except:
            state = ''
        try:
            status = task_dict['_source']['status']
        except:
            status = 0
        #result.append([task_dict['_source']['task_name'], task_dict['_source']['submit_date'], task_dict['_source']['count'], state, status])
        result.append({'task_name':task_dict['_source']['task_name'],'submit_date':ts2date(task_dict['_source']['submit_date']), 'group_count':task_dict['_source']['count'], 'status':status})
    
    return result

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


#get group user weibo
#write in version: 16-03-25
#input: task_name, submit_user, sort_type
def group_user_weibo(task_name, submit_user, sort_type):
    weibo_list = []
    now_date = ts2datetime(time.time())
    if sort_type == 'retweet':
        sort_type = 'retweeted'
    #run_type
    if RUN_TYPE == 0:
        now_date = RUN_TEST_TIME
        sort_type = 'timestamp'
    #step1: get group user
    task_id = submit_user + '-' + task_name
    try:
        group_exist_result = es_group_result.get(index=group_index_name, doc_type=group_index_type,\
                id=task_id)['_source']
    except:
        group_exist_result = {}
    if not group_exist_result:
        return 'group no exist'
    #step2: get user weibo list
    uid_list = group_exist_result['uid_list']
    for i in range(6,-1,-1):
        iter_date = ts2datetime(datetime2ts(now_date) - i * DAY)
        index_name = flow_text_index_name_pre + iter_date
        try:
            weibo_result = es_flow_text.search(index=index_name, doc_type=flow_text_index_type,\
                    body={'query':{'filtered':{'filter':{'terms':{'uid': uid_list}}}}, 'sort':[{sort_type: {'order': 'desc'}}], 'size':100})['hits']['hits']
        except:
            weibo_result = []
        if weibo_result:
            weibo_list.extend(weibo_result)
    #sort_weibo_list = sorted(weibo_list, key=lambda x:x['_source'][sort_type], reverse=True)[:100]
    sort_weibo_list = weibo_list
    #step3: get user name
    try:
        portrait_exist_result = es_user_portrait.mget(index=portrait_index_name, doc_type=portrait_index_type, \
                body={'ids':uid_list})['docs']
    except:
        portrait_exist_result = []
    uid2uname_dict = {}
    for portrait_item in portrait_exist_result:
        uid = portrait_item['_id']
        if portrait_item['found'] == True:
            source = portrait_item['_source']
            uname = source['uname']
        else:
            uname = 'unknown'
        uid2uname_dict[uid] = uname
    weibo_list = []
    for weibo_item in sort_weibo_list:
        source = weibo_item['_source']
        mid = source['mid']
        uid = source['uid']
        uname = uid2uname_dict[uid]
        text = source['text']
        ip = source['geo']
        timestamp = source['timestamp']
        date = ts2date(timestamp)
        sentiment = source['sentiment']
        weibo_url = weiboinfo2url(uid, mid)
        #run_type:
        if RUN_TYPE == 1:
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
        else:
            retweet_count = 0
            comment_count = 0
            sensitive_score = 0
        city = ip2city(ip)
        weibo_list.append([mid, uid, uname, text, ip, city, timestamp, date, retweet_count, comment_count, sensitive_score, weibo_url])
    if sort_type == 'timestamp':
        new_weibo_list = sorted(weibo_list, key=lambda x:x[6], reverse=True)
    elif sort_type == 'retweeted':
        new_weibo_list = sorted(weibo_list, key=lambda x:x[8], reverse=True)
    elif sort_type == 'comment':
        new_weibo_list = sorted(weibo_list, key=lambda x:x[9], reverse=True)
    elif sort_type == 'sensitive':
        new_weibo_list = sorted(weibo_list, key=lambda x:x[10], reverse=True)
    return new_weibo_list

def get_vary_detail_info(vary_detail_dict, uid_list):
    results = {}
    #get uname
    try:
        user_portrait_result = es_user_portrait.mget(index=portrait_index_name, doc_type=portrait_index_type,\
                            body={'ids':uid_list})['docs']
    except:
        user_portrait_result = []
    uname_dict = {}
    for portrait_item in user_portrait_result:
        uid = portrait_item['_id']
        if portrait_item['found']==True:
            uname = portrait_item['_source']['uname']
            uname_dict[uid] = uname
        else:
            uname_dict[uid] = uid

    #get new vary detail information
    for vary_pattern in vary_detail_dict:
        user_info_list = vary_detail_dict[vary_pattern]
        new_pattern_list = []
        for user_item in user_info_list:
            uid = user_item[0]
            uname= uname_dict[uid]
            start_date = ts2datetime(int(user_item[1]))
            end_date = ts2datetime(int(user_item[2]))
            new_pattern_list.append([uid, uname, start_date, end_date])
        results[vary_pattern] = new_pattern_list

    return results




#show results
def show_vary_detail(task_name, submit_user, vary_pattern):
    results = []
    task_id = submit_user + '-' + task_name
    #identify the task_id exist
    try:
        source = es_group_result.get(index=group_index_name, doc_type=group_index_type,\
                id=task_id)['_source']
    except:
        return 'group task is not exist'
    #identify the task status=1
    status = source['status']
    if status != 1:
        return 'group task is not completed'
    #get vary detail geo
    try:
        vary_detail_geo = json.loads(source['vary_detail_geo'])
    except:
        vary_detail_geo = {}
    if vary_detail_geo == {}:
        return 'vary detail geo none'
    #get vary_detail
    vary_pattern_list = vary_pattern.split('-')
    vary_pattern_key = '&'.join(vary_pattern_list)
    uid_ts_list = vary_detail_geo[vary_pattern_dict]
    uid_list = [item[0] for item in uid_ts_list]
    #get user name
    try:
        user_portrait_result = es_user_portrait.mget(index=portrait_index_name, doc_type=portrait_index_type,\
                body={'ids':uid_list})['docs']
    except:
        user_portrait_result = []
    uname_dict = {}
    for portrait_item in user_portrait_result:
        uid = portrait_item['_id']
        if portrait_item['found']==True:
            uname = portrait_item['_source']['uname']
            uname_dict[uid] = uname
        else:
            uname_dict[uid] = uid
    #get vary detail
    new_detail = []
    for vary_item in uid_ts_list:
        uname = uname_dict[vary_item[0]]
        start_date = ts2datetime(vary_item[1])
        end_date = ts2datetime(vary_item[2])
        new_detail.append([vary_item[0], uname, start_date, end_date])
    
    return new_detail


#search group analysis result
#input: task_name, module
#output: module_result
def search_group_results(task_name, module, submit_user):
    result = {}
    if RUN_TYPE == 0:
        #jln
        #task_id = '媒体'
        #group_index_type='text'
        task_id = submit_user + '-' + task_name
        group_index_type = 'group'
    else:
        task_id = submit_user + '-' + task_name
    #print es_group_result,group_index_name,group_index_type,task_id
    #step1:identify the task_name exist
    try:
        source = es_group_result.get(index=group_index_name, doc_type=group_index_type, \
               id=task_id)['_source']
        print source
    except:
        return 'group task is not exist'
    #step2: identify the task status=1(analysis completed)
    status = source['status']
    if status != 1:
        return 'group task is not completed'
    #step3:get module result
    if module == 'overview':
        result['task_name'] = source['task_name']
        result['submit_date'] = ts2datetime(source['submit_date'])
        result['state'] = source['state']
        result['submit_user'] = source['submit_user']
        result['density_star'] = source['density_star']
        result['activeness_star'] = source['activeness_star']
        result['influence_star'] = source['influence_star']
        result['importance_star'] = source['importance_star']
        #need to delete
        result['tag_vector'] = json.loads(source['tag_vector'])
    elif module == 'basic':
        result['gender'] = json.loads(source['gender'])
        result['verified'] = json.loads(source['verified'])
        result['user_tag'] = json.loads(source['user_tag'])
        result['count'] = source['count']
        result['domain'] = json.loads(source['domain'])
        result['topic'] = json.loads(source['topic'])
    elif module == 'activity':
        result['activity_trend'] = json.loads(source['activity_trend'])
        result['activity_time'] = json.loads(source['activity_time'])
        result['activity_geo_disribution'] = json.loads(source['activity_geo_distribution'])
        result['activiy_geo_vary'] = json.loads(source['activity_geo_vary'])
        result['activeness_trend'] = json.loads(source['activeness'])
        result['activeness_his'] = json.loads(source['activeness_his'])
        result['activeness_description'] = source['activeness_description']
        result['online_pattern'] = json.loads(source['online_pattern'])
        
        #yuanhuiru
        uid_list = source['uid_list']
        
        user_photo_result= es_user_portrait.mget(index='user_portrait_1222', doc_type='user', body={'ids':uid_list}, fields=['photo_url'])['docs']
        influ_value_result= es_user_portrait.mget(index='user_portrait_1222', doc_type='user', body={'ids':uid_list}, fields=['influence'])['docs']
        result['photo_url']=[]
        result['influence']=[]
        for item in user_photo_result:
            #uid = item['_id']
            if item['found']==True:
            
                source = item['fields']
                photo_url = source['photo_url']
            else:
                photo_url = 'unknown'
           
            
            result['photo_url'].append(photo_url)
           
        #print 'user_photo', result['photo_url']
        
        for item in influ_value_result:
            #uid = item['_id']
            if item['found']==True:
                source = item['fields']
                influence = source['influence']
            else:
                influence = 'unknown'

            result['influence'].append(influence)

        #print 'influence', result['influence']
       

        new_geo = {}
        for uid,geos in result['activity_geo_disribution'].iteritems():
            for geo,count in geos.iteritems():
                geo = geo.split('\t')
                if geo[0] == u'中国':
                    if len(geo) == 1:
                        geo.append(u'未知',u'未知')
                    elif len(geo) == 2:
                        geo.append(u'未知')
                    try:
                        new_geo[geo[1]]['total'] += count
                    except:
                        new_geo[geo[1]] = {'total':count}
                    try:
                        new_geo[geo[1]][geo[2]] += count
                    except:
                        new_geo[geo[1]][geo[2]] = count

        result['new_geo'] = new_geo
        try:
            vary_detail_geo_dict = json.loads(source['vary_detail_geo'])
        except:
            vary_detail_geo_dict = {}
        
        #uid_list = source['uid_list']
        
        if vary_detail_geo_dict != {}:
            result['vary_detail_geo'] = get_vary_detail_info(vary_detail_geo_dict, uid_list)
        else:
            result['vary_detail_geo'] = {}

        try:
            main_start_geo_dict = json.loads(source['main_start_geo'])
        except:
            main_start_geo_dict = {}
        result['main_start_geo'] = sorted(main_start_geo_dict.items(), key=lambda x:x[1], reverse=True)

        try:
            main_end_geo_dict = json.loads(source['main_end_geo'])
        except:
            main_end_geo_dict = {}
        result['main_end_geo'] = sorted(main_end_geo_dict.items(), key=lambda x:x[1], reverse=True)
        #all_geo_list = list(set(main_start_geo_dict.keys()) | set(main_end_geo_dict.keys()))
        #result['geo_lat_lng'] = get_lat_lng(all_geo_list)
        print 'result!!!!!!',result
    elif module == 'preference':
        try:
            result['keywords'] = json.loads(source['filter_keyword'])
        except:
            f_keyword = json.loads(source['keywords'])
            key_str = ','.join([key[0] for key in f_keyword])
            filter_dict = get_weibo_single(key_str,n_count=100)
            result['keywords'] = sorted(filter_dict.iteritems(),key=lambda x:x[1],reverse= True)
        '''
        keyword_list = json.loads(source['keywords'])
        keyword_dict = dict()
        for item in keyword_list:
            keyword_dict[item[0]] = item[1]

        filter_keyword_dict = keyword_filter(keyword_dict)
        sort_keyword = sorted(filter_keyword_dict.items(), key=lambda x:x[1], reverse=True)
        result['keywords'] = sort_keyword
        '''
        result['hashtag'] = json.loads(source['hashtag'])
        result['sentiment_word'] = json.loads(source['sentiment_word'])
        try:
            result['topic_model'] = json.loads(source['topic_model'])
        except:
            result['topic_model'] = []
        #need to delete
        result['domain'] = json.loads(source['domain'])
        result['topic'] = json.loads(source['topic'])
    elif module == 'influence':
        result['influence_his'] = json.loads(source['influence_his'])
        result['influence_trend'] = json.loads(source['influence'])
        result['influence_in_user'] = json.loads(source['influence_in_user'])
        result['influence_out_user'] = json.loads(source['influence_out_user'])
    elif module == 'social':
        result['in_density'] = source['in_density']
        result['in_inter_user_ratio'] = source['in_inter_user_ratio']
        result['in_inter_weibo_ratio'] = source['in_inter_weibo_ratio']
        result['social_in_record'] = json.loads(source['social_in_record'])
        result['out_inter_user_ratio'] = source['out_inter_user_ratio']
        result['out_inter_weibo_ratio'] = source['out_inter_weibo_ratio']
        result['social_out_record'] = json.loads(source['social_out_record'])
        result['density_description'] = source['density_description']
        result['mention'] = source['mention']
    elif module == 'think':
        result['sentiment_trend'] = json.loads(source['sentiment_trend'])
        result['sentiment_pie'] = json.loads(source['sentiment_pie'])
        result['character'] = json.loads(source['character'])
    return result


#abandon
'''
#show group results
def get_group_results(task_name, module):
    result = []
    try:
        es_result = es.get(index=index_name, doc_type=index_type, id=task_name)['_source']
        #print 'result:', result
    except:
        return None
    #basic module: gender, count, verified
    if module=='overview':
        task_name = es_result['task_name']
        submit_date = es_result['submit_date']
        state = es_result['state']
        tightness = es_result['tightness']
        activeness = es_result['activeness']
        importance = es_result['importance']
        influence = es_result['influence']
        result = [task_name, submit_date, state, tightness, activeness, importance, influence]
    if module=='basic':
        gender_dict = json.loads(es_result['gender'])
        count = es_result['count']
        verified = es_result['verified']
        if verified:
            verified_dict = json.loads(verified)
        result = [gender_dict, count, verified]
    if module=='activity':
        activity_geo_dict = json.loads(es_result['activity_geo'])
        sort_activity_geo = sorted(activity_geo_dict.items(), key=lambda x:x[1], reverse=True)
        activity_geo = sort_activity_geo[:50]
        activity_trend = json.loads(es_result['activity_trend'])
        online_pattern_dict = json.loads(es_result['online_pattern'])
        sort_online_pattern = sorted(online_pattern_dict.items(), key=lambda x:x[1], reverse=True)
        online_pattern = sort_online_pattern[:50]
        geo_track = json.loads(es_result['geo_track'])
        result = [activity_geo, activity_trend, online_pattern, geo_track]
    if module=='social':
        #degree_his = json.loads(es_result['degree_his'])
        density = es_result['density']
        retweet_weibo_count = es_result['retweet_weibo_count']
        retweet_user_count = es_result['retweet_user_count']
        retweet_relation = json.loads(es_result['retweet_relation'])
        uid_list = []
        for relation in retweet_relation:
            uid_list.append(relation[0])
            uid_list.append(relation[1])
        es_portrait_result = es.mget(index='user_portrait', doc_type='user', body={'ids':uid_list})['docs']
        es_count = 0
        new_retweet_relation = []
        for relation in retweet_relation:
            source_uid = relation[0]
            source_item = es_portrait_result[es_count]
            try:
                source = source_item['_source']
                source_uname = source['uname']
            except:
                source_uname = ''
            target_uid = relation[1]
            es_count += 1
            target_item = es_portrait_result[es_count]
            try:
                source = target_item['_source']
                target_uname = source['uname']
            except:
                target_uname = ''

            count = relation[2]
            new_retweet_relation.append([source_uid, source_uname, target_uid, target_uname, count])
        uid_list = []
        out_beretweet_relation = json.loads(es_result['out_beretweet_relation'])
        uid_list = []
        uid_list = [item[0] for item in out_beretweet_relation]
        es_portrait_result = es.mget(index='user_portrait', doc_type='user', body={'ids':uid_list})['docs']
        es_count = 0
        new_out_beretweet_relation = []
        for i in range(len(uid_list)):
            item = es_portrait_result[i]
            uid = item['_id']
            try:
                source = item['_source']
                uname = source['uname']
            except:
                uname = ''
            out_relation_item = out_beretweet_relation[i][1:]
            a = [uid, uname]
            a.extend(out_relation_item)
            #print 'add_item:', add_item
            new_out_beretweet_relation.append(a)
        result = [new_retweet_relation, density, retweet_weibo_count, retweet_user_count, new_out_beretweet_relation]
    if module=='think':
        domain_dict = json.loads(es_result['domain'])
        topic_dict = json.loads(es_result['topic'])
        psycho_status = json.loads(es_result['psycho_status'])
        psycho_feature = json.loads(es_result['psycho_feature'])
        result = [domain_dict, topic_dict, psycho_status, psycho_feature]
    if module=='text':
        hashtag_dict = json.loads(es_result['hashtag'])
        sort_hashtag = sorted(hashtag_dict.items(), key=lambda x:x[1], reverse=True)
        hashtag = sort_hashtag[:50]
        emoticon_dict = json.loads(es_result['emoticon'])
        sort_emoticon = sorted(emoticon_dict.items(), key=lambda x:x[1], reverse=True)
        emoticon = sort_emoticon[:5]
        keyword_dict = json.loads(es_result['keywords'])
        sort_keyword = sorted(keyword_dict.items(), key=lambda x:x[1], reverse=True)
        keyword = sort_keyword[:50]
        result = [hashtag, keyword, emoticon]
    if module=='influence':
        importance_dis = json.loads(es_result['importance_his'])
        activeness_his = json.loads(es_result['activeness_his'])
        influence_his = json.loads(es_result['influence_his'])
        user_influence_list = json.loads(es_result['user_influence_list'])
        user_influence_result = []
        for user_item in user_influence_list:
            uid = user_item[0]
            result_item = user_item[:5]
            for i in range(5,9):
                item = user_item[i]
                mid = item[1]
                number = item[0]
                if mid != 0 and uid:
                    weibolink = weiboinfo2url(uid, mid)
                else:
                    weibolink = None
                result_item.append((number, mid, weibolink))
            user_influence_result.append(result_item)
        
        result = [importance_dis, activeness_his, influence_his, user_influence_result]
    #print result
    return result
'''

# get importance max & activeness max & influence max
def get_evaluate_max():
    max_result = {}
    evaluate_index = ['importance', 'influence', 'activeness', 'sensitive']
    for evaluate in evaluate_index:
        query_body = {
            'query':{
                'match_all':{}
                },
            'size': 1,
            'sort': [{evaluate: {'order': 'desc'}}]
            }
        try:
            result = es_user_portrait.search(index=portrait_index_name, doc_type=portrait_index_type, body=query_body)['hits']['hits']
        except Exception, e:
            raise e
        max_evaluate = result[0]['_source'][evaluate]
        max_result[evaluate] = max_evaluate
    return max_result

# get grouop user list
def get_group_list(task_name, submit_user):
    
    results = []
    task_id = submit_user + '-' + task_name
    if RUN_TYPE == 0:
        group_index_name = 'test_group_result'
    try:

        es_results = es_group_result.get(index=group_index_name, doc_type=group_index_type, id=task_id)['_source']
        #jln  现在的9200里没有
        #es_results = es_group_result.get(index=group_index_name, doc_type=group_index_type, id=task_id)['_source']
    except:
        return results
    uid_list = es_results['uid_list']
    user_portrait_attribute = es_user_portrait.mget(index=portrait_index_name, doc_type=portrait_index_type, body={'ids':uid_list})['docs']
    evaluate_max = get_evaluate_max()
    for item in user_portrait_attribute:
        uid = item['_id']
        try:
            source = item['_source']
            uname = source['uname']
            gender = source['gender']
            location = source['location']
            importance = source['importance']
            normal_importance = math.log(importance / evaluate_max['importance'] * 9 + 1, 10) * 100
            influence = source['influence']
            normal_influence = math.log(influence / evaluate_max['influence'] * 9 + 1, 10) * 100
            activeness = source['activeness']
            normal_activeness = math.log(activeness / evaluate_max['activeness']* 9 + 1, 10) * 100
            sensitive = source['sensitive']
            normal_sensitive = math.log(sensitive/ evaluate_max['sensitive'] * 9 + 1, 10) * 100
            results.append([uid, uname, gender, location, normal_importance, normal_influence, normal_activeness, normal_sensitive])
        except:
            results.append([uid, '', '', '', '', '', '', ''])
    return results

#use to get group member uid_uname
#version: write in 2016-02-26
#input: task_name
#output: uid_uname dict
def get_group_member_name(task_name, submit_user):
    results = []
    task_id = submit_user + '-' + task_name
    #print es_group_result,group_index_name,group_index_type
    try:
        group_result = es_group_result.get(index=group_index_name, doc_type=group_index_type,\
                id=task_id)['_source']
    except:
        return results
    uid_list = group_result['uid_list']
    print len(uid_list)
    try:
        user_portrait_result = es_user_portrait.mget(index=portrait_index_name, doc_type=portrait_index_type ,\
                body={'ids':uid_list})['docs']
    except:
        return results
    print len(user_portrait_result)
    for item in user_portrait_result:
        uid = item['_id']
        if item['found'] == True:
            source = item['_source']
            uname = source['uname']
        else:
            uname = 'unknown'
        #results[uid] = uname
        dic = {}
        dic['ID'] = uid
        dic['name'] = uname
        results.append(dic)


    return results



# delete group results from es_user_portrait 'group_analysis'
def delete_group_results(task_name, submit_user):
    task_id = submit_user + '-' + task_name
    #step1: get group uid list
    try:
        group_result = es_group_result.get(index=group_index_name, doc_type=group_index_type,\
                id=task_id)['_source']
    except:
        return False
    uid_list = group_result['uid_list']
    #step2: update group_tag in user_portrait
    query_body = {'query':{'term':{'group': task_id}}}
    try:
        user_portrait_result = es_user_portrait.mget(index=portrait_index_name, doc_type=portrait_index_type,\
                body={'ids': uid_list})['docs']
    except:
        user_portrait_result = []
    bulk_action = []
    for item in user_portrait_result:
        uid = item['_id']
        if item['found'] == True:
            try:
                source = item['_source']
            except:
                source = {}
            try:
                group_tag = source['group']
            except:
                group_tag = ''
            if group_tag != '':
                new_group_tag_list = []
                group_tag_list = group_tag.split('&')
                for group_tag_item in group_tag_list:
                    if group_tag_item != task_id and group_tag_item != 'admin@qq.com-mytest040902':
                        new_group_tag_list.append(group_tag_item)
                new_group_tag = '&'.join(new_group_tag_list)
            else:
                new_group_tag = ''
            action = {'update':{'_id': uid}}
            bulk_action.extend([action, {'doc': {'group': new_group_tag}}])
    if bulk_action:
        print 'bulk_action:', bulk_action
        es_user_portrait.bulk(bulk_action, index=portrait_index_name, doc_type=portrait_index_type)
    #step3: delete group results in group_manage
    try:
        print 'yes delete'
        result = es.delete(index=index_name, doc_type=index_type, id=task_id)
    except:
        return False
    return True


#show group user geo track
#input: uid
#output: results [geo1,geo2,..]
def get_group_user_track(uid):
    results = []
    #step1:get user_portrait activity_geo_dict
    try:
        portrait_result = es_user_portrait.get(index=portrait_index_name, doc_type=portrait_index_type,\
                id=uid, _source=False, fields=['activity_geo_dict'])
    except:
        portrait_result = {}
    if portrait_result == {}:
        return 'uid is not in user_portrait'
    activity_geo_dict = json.loads(portrait_result['fields']['activity_geo_dict'][0])
    now_date_ts = datetime2ts(ts2datetime(int(time.time())))
    start_ts = now_date_ts - DAY * len(activity_geo_dict)
    #step2: iter date to get month track
    for geo_item in activity_geo_dict:
        iter_date = ts2datetime(start_ts)
        sort_day_dict = sorted(geo_item.items(), key=lambda x:x[1], reverse=True)
        if sort_day_dict:
            results.append([iter_date, sort_day_dict[0][0]])
        else:
            results.append([iter_date, ''])
        start_ts = start_ts + DAY

    return results

#jln 2016/09/28
def search_group_member(task_name,submit_user):
    task_id = submit_user + '-' + task_name
    results = es_group_result.get(index=group_index_name,doc_type=group_index_type,\
        id=task_id,fields=['uid_list'])['fields']['uid_list']
    print results
    return results


# show group members weibo for activity ---week
# input: task_name, start_ts
# output: weibo_list
def get_activity_weibo(task_name, start_ts, submit_user):
    results = []
    task_id = submit_user + '-' + task_name
    #step1: get task_name uid
    try:
        group_result = es_group_result.get(index=group_index_name, doc_type=group_index_type ,\
                id=task_id, _source=False, fields=['uid_list'])
    except:
        group_result = {}
    if group_result == {}:
        return 'task name invalid'
    try:
        uid_list = group_result['fields']['uid_list']
    except:
        uid_list = []
    if uid_list == []:
        return 'task uid list null'
    #step2: get uid2uname
    uid2uname = {}
    try:
        user_portrait_result = es_user_portrait.mget(index=portrait_index_name, doc_type=portrait_index_type, \
                body = {'ids':uid_list}, _source=False, fields=['uname'])['docs']
    except:
        user_portrait_result = []
    for item in user_portrait_result:
        uid = item['_id']
        if item['found']==True:
            uname = item['fields']['uname'][0]
        uid2uname[uid] = uname
    #step3: search time_segment weibo
    time_segment = FOUR_HOUR
    end_ts = start_ts + time_segment
    time_date = ts2datetime(start_ts)
    flow_text_index_name = flow_text_index_name_pre + time_date
    query = []
    query.append({'terms':{'uid': uid_list}})
    query.append({'range':{'timestamp':{'gte':start_ts, 'lt':end_ts}}})
    try:
        flow_text_es_result = es_flow_text.search(index=flow_text_index_name, doc_type=flow_text_index_type, \
                body={'query':{'bool':{'must':query}}, 'sort':'timestamp', 'size':MAX_VALUE})['hits']['hits']
    except:
        flow_text_es_result = []
    for item in flow_text_es_result:
        weibo = {}
        source = item['_source']
        weibo['timestamp'] = ts2date(source['timestamp'])
        weibo['ip'] = source['ip']
        weibo['text'] = source['text']
        weibo['geo'] = '\t'.join(source['geo'])
        results.append(weibo)

    return results

#show group members weibo for influence content
#input: uid, timestamp_from, timestamp_to
#output: weibo_list
def get_influence_content(uid, timestamp_from, timestamp_to):
    weibo_list = []
    #split timestamp range to new_range_dict_list
    from_date_ts = datetime2ts(ts2datetime(timestamp_from))
    to_date_ts = datetime2ts(ts2datetime(timestamp_to))
    new_range_dict_list = []
    if from_date_ts != to_date_ts:
        iter_date_ts = from_date_ts
        while iter_date_ts < to_date_ts:
            iter_next_date_ts = iter_date_ts + DAY
            new_range_dict_list.append({'range':{'timestamp':{'gte':iter_date_ts, 'lt':iter_next_date_ts}}})
            iter_date_ts = iter_next_date_ts
        if new_range_dict_list[0]['range']['timestamp']['gte'] < timestamp_from:
            new_range_dict_list[0]['range']['timestamp']['gte'] = timestamp_from
        if new_range_dict_list[-1]['range']['timestamp']['lt'] > timestamp_to:
            new_range_dict_list[-1]['range']['timestamp']['lt'] = timestamp_to
    else:
        new_range_dict_list = [{'range':{'timestamp':{'gte':timestamp_from, 'lt':timestamp_to}}}]
    #iter date to search flow_text
    iter_result = []
    for range_item in new_range_dict_list:
        range_from_ts = range_item['range']['timestamp']['gte']
        range_from_date = ts2datetime(range_from_ts)
        flow_text_index_name = flow_text_index_name_pre + range_from_date
        query = []
        query.append({'term':{'uid':uid}})
        query.append(range_item)
        try:
            flow_text_exist = es_flow_text.search(index=flow_text_index_name, doc_type=flow_text_index_type,\
                    body={'query':{'bool':{'must': query}}, 'sort':[{'timestamp':'asc'}]})['hits']['hits']
        except:
            flow_text_exist = []
        iter_result.extend(flow_text_exist)
    # get weibo list
    for item in flow_text_exist:
        source = item['_source']
        weibo = {}
        weibo['timestamp'] = ts2date(source['timestamp'])
        weibo['ip'] = source['ip']
        weibo['text'] = source['text']
        weibo['geo'] = '\t'.join(source['geo'].split('&'))
        weibo_list.append(weibo)
        
    return weibo_list

#show group members interaction weibo content
#input: uid1, uid2
#ouput: weibo_list
def get_social_inter_content(uid1, uid2, type_mark):
    weibo_list = []
    #get two type relation about uid1 and uid2
    #search weibo list
    now_ts = int(time.time())
    #run_type
    if RUN_TYPE == 1:
        now_date_ts = datetime2ts(ts2datetime(now_ts))
    else:
        now_date_ts = datetime2ts(RUN_TEST_TIME)
    #uid2uname
    uid2uname = {}
    try:
        portrait_result = es_user_portrait.mget(index=portrait_index_name, doc_type=portrait_index_type ,\
                                body={'ids': [uid1, uid2]}, _source=False, fields=['uid', 'uname'])['docs']
    except:
        portrait_result = []
    
    for item in portrait_result:
        uid = item['_id']
        if item['found'] == True:
            uname = item['fields']['uname'][0]
            uid2uname[uid] = uname
        else:
            uid2uname[uid] = 'unknown'
    #iter date to search weibo list
    for i in range(7, 0, -1):
        iter_date_ts = now_date_ts - i*DAY
        iter_date = ts2datetime(iter_date_ts)
        flow_text_index_name = flow_text_index_name_pre + str(iter_date)
        query = []
        query.append({'bool':{'must':[{'term':{'uid':uid1}}, {'term':{'directed_uid': int(uid2)}}]}})
        if type_mark=='out':
            query.append({'bool':{'must':[{'term':{'uid':uid2}}, {'term':{'directed_uid': int(uid1)}}]}})
        try:
            flow_text_result = es_flow_text.search(index=flow_text_index_name, doc_type=flow_text_index_type,\
                    body={'query': {'bool':{'should': query}}, 'sort':[{'timestamp':{'order': 'asc'}}], 'size':MAX_VALUE})['hits']['hits']
        except:
            flow_text_result = []
        for flow_text in flow_text_result:
            source = flow_text['_source']
            weibo = {}
            weibo['timestamp'] = source['timestamp']
            weibo['ip'] = source['ip']
            weibo['geo'] = source['geo']
            weibo['text'] = '\t'.join(source['text'].split('&'))
            weibo['uid'] =  source['uid']
            weibo['uname'] = uid2uname[weibo['uid']]
            weibo['directed_uid'] = str(source['directed_uid'])
            weibo['directed_uname'] = uid2uname[str(source['directed_uid'])]
            weibo_list.append(weibo)

    return weibo_list

#show group members sentiment weibo
#input: task_name, start_ts ,sentiment_type
#output: weibo_list
def search_group_sentiment_weibo(task_name, start_ts, sentiment, submit_user):
    weibo_list = []
    task_id = submit_user + '-' + task_name
    #print es_group_result,group_index_name,group_index_type
    #step1:get task_name uid
    try:
        group_result = es_group_result.get(index=group_index_name, doc_type=group_index_type,\
                        id=task_id, _source=False, fields=['uid_list'])
    except:
        group_result = {}
    if group_result == {}:
        return 'task name invalid'
    try:
        uid_list = group_result['fields']['uid_list']
    except:
        uid_list = []
    if uid_list == []:
        return 'task uid list null'
    #step3: get ui2uname
    uid2uname = {}
    try:
        user_portrait_result = es_user_portrait.mget(index=portrait_index_name, doc_type=portrait_index_type,\
                        body={'ids':uid_list}, _source=False, fields=['uname'])['docs']
    except:
        user_portrait_result = []
    for item in user_portrait_result:
        uid = item['_id']
        if item['found']==True:
            uname = item['fields']['uname'][0]
            uid2uname[uid] = uname
        else:
            uid2uname[uid] = 'unknown'
    #step4:iter date to search weibo
    weibo_list = []
    iter_date = ts2datetime(start_ts)
    flow_text_index_name = flow_text_index_name_pre + str(iter_date)
    #step4: get query_body
    if sentiment != '2':
        query_body = [{'terms': {'uid': uid_list}}, {'term':{'sentiment': sentiment}}, \
                {'range':{'timestamp':{'gte':start_ts, 'lt': start_ts+DAY}}}]
    else:
        query_body = [{'terms':{'uid':uid_list}}, {'terms':{'sentiment': SENTIMENT_SECOND}},\
                {'range':{'timestamp':{'gte':start_ts, 'lt':start_ts+DAY}}}]
    try:
        flow_text_result = es_flow_text.search(index=flow_text_index_name, doc_type=flow_text_index_type,\
                body={'query':{'bool':{'must': query_body}}, 'sort': [{'timestamp':{'order':'asc'}}], 'size': MAX_VALUE})['hits']['hits']
    except:
        flow_text_result = []
    for flow_text_item in flow_text_result:
        source = flow_text_item['_source']
        weibo = {}
        weibo['uid'] = source['uid']
        weibo['uname'] = uid2uname[weibo['uid']]
        weibo['ip'] = source['ip']
        try:
            weibo['geo'] = '\t'.join(source['geo'].split('&'))
        except:
            weibo['geo'] = ''
        weibo['text'] = source['text']
        weibo['timestamp'] = source['timestamp']
        weibo['sentiment'] = source['sentiment']
        weibo_list.append(weibo)

    return weibo_list

def edit_state(task_name, submit_user, new_state):
    results = True
    task_id = submit_user + '-' + task_name
    try:
        group_exist = es_group_result.get(index=group_index_name, doc_type=group_index_type,\
                id=task_id)['_source']
    except:
        return 'group no exist'
    es_group_result.update(index=group_index_name, doc_type=group_index_type,\
            id=task_id, body={'doc':{'state': new_state}})
    return results


if __name__=='__main__':
    #test group task
    input_data = {}
    input_data['task_name'] = 'testtesttest'
    input_data['uid_list'] = json.dumps(['2010832710', '3482838791', '3697357313', '2496434537',\
                '1642591402', '2074370833', '1640601392', '1773489534',\
                '2722498861', '2803301701'])
    input_data['submit_date'] = '2013-09-08'
    input_data['state'] = 'it is a test'
    submit_task(input_data)
    test_task_name = 'testtesttest'
    #status = delete_group_results(test_task_name)
    #print 'status:', status
