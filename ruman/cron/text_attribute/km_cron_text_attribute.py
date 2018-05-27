#-*- coding: UTF-8 -*-
'''
compute the user attribute about text
data source: weibo api
scene: add user to user portrait
'''
import re
import csv
import sys
import json
import time
from elasticsearch import Elasticsearch
from datetime import datetime
from flow_information import get_flow_information, get_flow_information_v2
from evaluate_index import get_importance, get_activity_time, get_activeness, get_influence
from user_profile import get_profile_information
from save_utils import attr_hash, save_user_results
from config import topic_en2ch_dict, domain_en2ch_dict
from domain_topic_input import get_user_weibo_string, get_user_keywords_dict
from character_input import character_input # use to prepare input for attribute---character
# compute user event
from event.event_user import event_classfiy
# compute user domain
from domain.test_domain_v2 import domain_classfiy
# compute user topic
from topic.test_topic import topic_classfiy
# compute user psy
from psy.new_psy import psychology_classfiy
# compute user character
from character.test_ch_sentiment import classify_sentiment
from character.test_ch_topic import classify_topic

sys.path.append('../../')
from global_utils import es_user_profile, profile_index_name, profile_index_type
from parameter import CHARACTER_TIME_GAP, DAY, WEIBO_API_INPUT_TYPE
from time_utils import ts2datetime, datetime2ts

es_km = Elasticsearch("219.224.134.225:9037", timeout=600)

#abandon in version: 15-12-08
'''
reload(sys)
sys.path.append('../../../../../libsvm-3.17/python/')
from sta_ad import load_scws

cx_dict = ['a', 'n', 'nr', 'ns', 'nz', 'v', '@', 'd']
sw = load_scws()

EXTRA_WORD_WHITE_LIST_PATH = '/home/ubuntu8/libsvm-3.17/python/dict/one_word_white_list.txt'

def load_one_words():
    one_words = [line.strip('\r\n') for line in file(EXTRA_WORD_WHITE_LIST_PATH)]
    return one_words

single_word_whitelist = set(load_one_words())
single_word_whitelist |= set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789')

BLACK_WORDS_PATH = '/home/ubuntu8/huxiaoqian/user_portrait/user_portrait/cron/text_attribute/black.txt'
def load_black_words():
    black_words = set([line.strip('\r\n') for line in file(BLACK_WORDS_PATH)])
    a = list(black_words)[0]
    return black_words

black_words = load_black_words()

def get_emoticon_dict():
    results = dict()
    f = open('/home/ubuntu8/huxiaoqian/user_portrait/user_portrait/cron/text_attribute/emoticons.txt', 'rb')
    for line in f:
        line_list = line.split(':')
        emoticon = line_list[0]
        emo_class = line_list[1]
        try:
            results[emo_class].append(emoticon.decode('utf-8'))
        except:
            results[emo_class] = [emoticon.decode('utf-8')]
    return results

emoticon_dict = get_emoticon_dict()

def get_liwc_dict():
    results = dict()
    f = open('/home/ubuntu8/huxiaoqian/user_portrait/user_portrait/cron/flow2/extract_word.csv', 'rb')
    reader = csv.reader(f)
    for line in reader:
        num = line[0]
        word = line[1]
        try:
            results[num].append(word)
        except:
            results[num] = [word]
    return results

liwc_dict = get_liwc_dict()
'''

# read uid_list from user portrait
'''
def read_uid_list():
    uid_list = []
    return uid_list
'''

#abandon in version: 15-12-08
'''
def attr_text_len(weibo_list):
    len_list = [len(weibo['text']) for weibo in weibo_list]
    ave_len = float(sum(len_list)) / len(len_list)
    return ave_len

def attr_emoticon(weibo_list):
    results = {}
    for weibo in weibo_list:
        text = weibo['text']
        for emo_class in emoticon_dict:
            emoticons = emoticon_dict[emo_class]
            for emoticon in emoticons:
                if isinstance(text, str):
                    text = text.decode('utf-8')
                count = text.count(emoticon)
                if count != 0:
                    try:
                        results[emoticon] += count
                    except:
                        results[emoticon] = count
    
    return results
'''

#abandon in version:15-12-08
''''
# {class_num:{word:count}}
def attr_liwc(weibo_list):
    results = {}
    keyword_results = {}
    for weibo in weibo_list:
        text = weibo['text']
        cut_text = sw.participle(text.encode('utf-8'))
        cut_word_list = [term for term, cx in cut_text if cx in cx_dict]
        for num in liwc_dict:
            for liwc_word in liwc_dict[num]:
                if liwc_word in cut_word_list:
                    if num in results:
                        try:
                            results[num][liwc_word.decode('utf-8')] += 1
                        except:
                            results[num][liwc_word.decode('utf-8')] = 1
                    else:
                        results[num] = {liwc_word.decode('utf-8'): 1}
    return results
'''

#abandon in version:15-12-08
'''
def attr_link(weibo_list):
    count = []
    for weibo in weibo_list:
        text = weibo['text']
        pat = re.compile('http://')
        urls = re.findall(pat, text)
        if len(urls)!=0:
            count.append(len(urls))
    if count:
        all_count = sum(count)    
        ave_count = float(all_count) / len(weibo_list)
        #max_count = max(count)
        #min_count = min(count)
        #return [min_count, max_count, ave_count, all_count]
        return ave_count
    else:
        return 0
'''


#use to get online_pattern attribute
def attr_online_pattern(weibo_list):
    results= {}
    for weibo in weibo_list:
        online_pattern = weibo['online_pattern']
        try:
            results[online_pattern] += 1
        except:
            results[online_pattern] = 1
    return results


#abandon in version:15-12-08
'''
def attr_keywords(weibo_list):
    results = {}
    for weibo in weibo_list:
        text = weibo['text'].encode('utf-8')
        pattern_list = [r'\（分享自 .*\）', r'http://t.cn/\w*']
        for i in pattern_list:
            p = re.compile(i)
            text = p.sub('', text)
        tks = []
        for token in sw.participle(text):
            if 3<len(token[0])<30 or token[0].decode('utf-8') in single_word_whitelist:
                if token[1] in cx_dict:
                    if (token[0] not in black_words):
                        tks.append(token)
                    #else:
                    #    print 'delete:', token[0]

        #print 'tks:', tks[0][0], type(tks[0][0])
        for tk in tks:
            word = tk[0].decode('utf-8')
            try:
                results[word] += 1
            except:
                results[word] = 1
        sort_results = sorted(results.items(), key=lambda x:[1], reverse=True)[:50]
        keywords_results = {}
        for sort_item in sort_results:
            keywords_results[sort_item[0]] = sort_item[1]
    #print 'attr_keyword:', keywords_results
    return keywords_results
'''

#use to compute online_pattern attribute
#write in version:15-12-08
def compute_text_attribute(user, weibo_list):
    result = {}
    '''
    # text attr1: len
    result['text_len'] = attr_text_len(weibo_list)
    # text attr4: web link
    result['link'] = attr_link(weibo_list)
    '''
    # text attr5: online pattern
    result['online_pattern'] = json.dumps(attr_online_pattern(weibo_list))
    
    return result

#make topic_en to topic_ch
def topic_en2ch(topic_label):
    insert_topic_label_list = []
    for en_label in topic_label:
        ch_label = topic_en2ch_dict[en_label]
        insert_topic_label_list.append(ch_label.encode('utf-8'))
    insert_topic_label_string = '&'.join(insert_topic_label_list)
    return insert_topic_label_string

#make domain_en to domain_ch
def domain_en2ch(domain_en_label):
    insert_domain_label = ''
    ch_label = domain_en2ch_dict[domain_en_label]
    ch_label = ch_label.encode('utf-8')
    return ch_label

#start-up by scan_compute_redis and compute user attribute for who need to be added to user_portrait
#write in version:15-12-08
#input: uid_list and user_weibo_dict
#output: save user attribute to user_portrait
#attention: this function cannot be used to update user_portrait
def compute2in(uid_list, user_weibo_dict):
    #get user flow information: hashtag, activity_geo, keywords
    flow_result = get_flow_information(uid_list)
    #get user topic information
    topic_results_dict, topic_results_label = topic_classfiy(user_weibo_list)
    #get user domain information
    domain_results = domain_classfiy(user_weibo_dict)
    domain_results_dict = domain_results[0]
    domain_results_label = domain_results[1]
    #get user psy information
    psy_results_dict = psychology_classfiy(user_weibo_dict)
    #get user profile information
    register_result = get_profile_information(uid_list)
    #get user fansnum max
    fansnum_max = get_fansnum_max()
    #get user activeness by bulk_action
    activeness_results = get_activity_time(uid_list)
    #get user inlfuence by bulk action
    influence_results = get_influence(uid_list)
    #deal bulk action
    for user in user_weibo_dict:
        weibo_list = user_weibo_dict[user]
        uname = weibo_list[0]['uname']
        #compute text attribute: online_pattern
        results = compute_text_attribute(user, weibo_list)
        results['uname'] = uname
        results['uid'] = str(user)
        #add flow information: hashtag, activity_geo, keywords
        flow_dict = flow_result[str(user)]
        results = dict(results, **flow_dict)
        #add topic attribute
        topic_dict = topic_results_dict[user]
        results['topic'] = json.dumps(topic_dic)                   #{topic1_en:pro1, topic2_en:pro, ...}
        topic_label = topic_results_label[user] 
        results['topic_string'] = topic_en2ch(topic_label)         #topic1_ch&topic2_ch&topic3_ch
        #add domain attribute
        user_domain_dict = domain_results_dict[user]
        user_domain_label = domain_results_label[user]
        results['domain_v3'] = json.dumps(user_domain_dict)        #[domain_en1, domain_en2, domain_en3]
        results['domain_string'] = domain_en2ch(user_domain_label) #domain_ch
        #add psy attribute
        user_psy_dict = psy_results_dict[user]
        results['psycho_status'] = json.dumps(user_psy_dict)
        #add user profile attribute
        register_dict = register_result[str(user)]
        results = dict(results, **register_dict)
        #add user_evaluate attribute---importance
        results['importance'] = get_importance(results['domain'], results['topic_string'], results['fansnum'], fansnum)
        #add user_evaluate attribute---activeness
        user_activeness_time = activeness_results[user]
        user_activeness_geo = json.loads(results['activity_geo_dict'])[-1]
        results['activeness'] = get_activeness(user_activeness_geo, user_activeness_time)
        #add user_evaluate attribute---influence
        results['influence'] = influence_results[user]
        #bulk_action
        action = {'index':{'_id':str(user)}}
        bulk_action.extend([action, results])
    status = save_user_results(bulk_action)
    return True

#get user fansnum max from es_user_profile to compute evaluate index--importance
def get_fansnum_max():
    query_body = {
        'query':{
            'match_all':{}
            },
        'size': 1,
        'sort': [{'fansnum': {'order': 'desc'}}]
        }
    try:
        fansnum_max_results = es_user_profile.search(index=profile_index_name, doc_type=profile_index_type, body=query_body)['hits']['hits']
    except Exception, e:
        raise e
    fansnum_max = fansnum_max_results[0]['_source']['fansnum']

    return fansnum_max

#use to compute new user attribute by scan_compute_redis.py
#version: write in 2016-02-28
def test_cron_text_attribute_v2(user_keywords_dict, user_weibo_dict, online_pattern_dict, character_start_ts):
    status = False
    print 'start cron_text_attribute'
    uid_list = user_keywords_dict.keys()
    
    #get user flow information: hashtag, activity_geo, keywords
    print 'get flow result'
    flow_result = get_flow_information_v2(uid_list, user_keywords_dict)
    print 'flow result len:', len(flow_result)
    
    #get user profile information
    print 'get register result'
    register_result = get_profile_information(uid_list)
    print 'register result len:', len(register_result)
    
    #get user topic and domain by bulk action
    print 'get topic and domain'
    topic_results_dict, topic_results_label = topic_classfiy(uid_list, user_keywords_dict)
    domain_results = domain_classfiy(uid_list, user_keywords_dict)
    domain_results_dict = domain_results[0]
    domain_results_label = domain_results[1]
    print 'topic result len:', len(topic_results_dict)
    print 'domain result len:', len(domain_results_dict)
    
    #get user character attribute
    print 'get character result'
    #type_mark = 0/1 for identify the task input status---just sentiment or text
    character_start_time = ts2datetime(character_start_ts)
    character_end_time = ts2datetime(character_start_ts + DAY * CHARACTER_TIME_GAP - DAY)
    print 'character_start_time:', character_start_time
    print 'character_end_time:', character_end_time
    character_sentiment_result_dict = classify_sentiment(uid_list, user_weibo_dict, character_start_time, character_end_time, WEIBO_API_INPUT_TYPE)
    character_text_result_dict = classify_topic(uid_list, user_keywords_dict)
    print 'character result len:', len(character_sentiment_result_dict), len(character_text_result_dict)
    
    #get user fansnum max
    fansnum_max = get_fansnum_max()
    #get user activeness by bulk_action
    print 'get activeness results'
    activeness_results = get_activity_time(uid_list)
    print 'activeness result len:', len(activeness_results)
    #get user inlfuence by bulk action
    print 'get influence'
    influence_results = get_influence(uid_list)
    print 'influence results len:', len(influence_results)
    
    # compute text attribute
    bulk_action = []
    count = 0
    for user in uid_list:
        count += 1
        results = {}       
        #get user text attribute: online_pattern
        results['online_pattern'] = json.dumps(online_pattern_dict[user])
        try:
            results['online_pattern_aggs'] = '&'.join(online_pattern_dict[user].keys())
        except:
            results['online_pattern_aggs'] = ''
        results['uid'] = str(user)
        #add user flow information: hashtag, activity_geo, keywords
        flow_dict = flow_result[str(user)]
        results = dict(results, **flow_dict)
        
        #add user topic attribute
        user_topic_dict = topic_results_dict[user]
        user_label_dict = topic_results_label[user]
        results['topic'] = json.dumps(user_topic_dict)         # {'topic1_en':pro1, 'topic2_en':pro2...}
        results['topic_string'] = topic_en2ch(user_label_dict) # 'topic1_ch&topic2_ch&topic3_ch'
        
        #add user domain attribute
        user_domain_dict = domain_results_dict[user]
        user_label_dict = domain_results_label[user]
        results['domain_v3'] = json.dumps(user_domain_dict) # [label1_en, label2_en, label3_en]
        results['domain'] = domain_en2ch(user_label_dict)      # label_ch
        
        #add user character_sentiment attribute
        character_sentiment = character_sentiment_result_dict[user]
        results['character_sentiment'] = character_sentiment
        #add user character_text attribtue
        character_text = character_text_result_dict[user]
        results['character_text'] = character_text
        
        #add user profile attribute
        register_dict = register_result[str(user)]
        results = dict(results, **register_dict)
        #add user_evaluate attribute---importance
        results['importance'] = get_importance(results['domain'], results['topic_string'], results['fansnum'], fansnum_max)
        #add user_evaluate attribute---activeness
        user_activeness_time = activeness_results[user]
        user_activeness_geo = json.loads(results['activity_geo_dict'])[-1]
        results['activeness'] = get_activeness(user_activeness_geo, user_activeness_time)
        #add user_evaluate attribute---influence
        results['influence'] = influence_results[user]
        
        #bulk_action
        action = {'index':{'_id': str(user)}}
        bulk_action.extend([action, results])
        
    #status = save_user_results(bulk_action)
    status = es_km.bulk(bulk_action, index='user_portrait', doc_type="user", timeout=60)
    
    return True



#test manual instruction
def test_cron_text_attribute(user_weibo_dict):
    #get user weibo 7day {user:[weibos]}
    print 'start cron_text_attribute'
    uid_list = user_weibo_dict.keys()
    print 'user count:', len(uid_list)
    
    #get user flow information: hashtag, activity_geo, keywords
    print 'get flow result'
    flow_result = get_flow_information(uid_list)
    print 'flow result len:', len(flow_result)
    
    #get user profile information
    print 'get register result'
    register_result = get_profile_information(uid_list)
    print 'register result len:', len(register_result)
    #get topic and domain input data
    user_weibo_string_dict = get_user_weibo_string(user_weibo_dict) # use as the tendency input data
    user_keywords_dict = get_user_keywords_dict(user_weibo_string_dict)
    #get user event results by bulk action
    event_results_dict = event_classfiy(user_weibo_string_dict)
    print 'event_result len:', len(event_results_dict)
    
    #get user topic and domain by bulk action
    print 'get topic and domain'
    topic_results_dict, topic_results_label = topic_classfiy(user_keywords_dict)
    domain_results = domain_classfiy(user_keywords_dict)
    domain_results_dict = domain_results[0]
    domain_results_label = domain_results[1]
    print 'topic result len:', len(topic_results_dict)
    print 'domain result len:', len(domain_results_dict)
    
    #get user psy attribute
    #print 'get psy result'
    #psy_results_dict = psychology_classfiy(user_weibo_dict)
    #print 'psy result len:', len(psy_results_dict)
    
    #get user character attribute
    print 'get character result'
    #type_mark = 0/1 for identify the task input status---just sentiment or text
    now_ts = time.time()
    #test
    now_ts = datetime2ts('2013-09-08')
    character_end_time = ts2datetime(now_ts - DAY)
    character_start_time = ts2datetime(now_ts - DAY * CHARACTER_TIME_GAP)
    character_type_mark = 1
    character_sentiment_result_dict = classify_sentiment(uid_list, character_start_time, character_end_time, character_type_mark)
    character_type_mark = 1
    character_text_result_dict = classify_topic(uid_list, character_start_time, character_end_time, character_type_mark)
    print 'character result len:', len(character_sentiment_result_dict), len(character_text_result_dict)
    print 'character_sentiment_result:', character_sentiment_result_dict
    print 'character_text_result:', character_text_result_dict
    
    #get user fansnum max
    fansnum_max = get_fansnum_max()
    #get user activeness by bulk_action
    print 'get activeness results'
    activeness_results = get_activity_time(uid_list)
    print 'activeness result len:', len(activeness_results)
    #get user inlfuence by bulk action
    print 'get influence'
    influence_results = get_influence(uid_list)
    print 'influence results len:', len(influence_results)
    
    # compute text attribute
    user_set = set()
    bulk_action = []
    count = 0
    for user in user_weibo_dict:
        count += 1
        results = {}       
        user_set.add(user)
        weibo_list = user_weibo_dict[user]
        uname = weibo_list[0]['uname']
        #get user text attribute: online_pattern
        results = compute_text_attribute(user, weibo_list)
        results['uid'] = str(user)
        #add user flow information: hashtag, activity_geo, keywords
        flow_dict = flow_result[str(user)]
        results = dict(results, **flow_dict)
        
        #add user topic attribute
        user_topic_dict = topic_results_dict[user]
        user_label_dict = topic_results_label[user]
        results['topic'] = json.dumps(user_topic_dict)         # {'topic1_en':pro1, 'topic2_en':pro2...}
        results['topic_string'] = topic_en2ch(user_label_dict) # 'topic1_ch&topic2_ch&topic3_ch'
        #add user event attribute
        results['tendency'] = event_results_dict[user]
        
        #add user domain attribute
        user_domain_dict = domain_results_dict[user]
        user_label_dict = domain_results_label[user]
        results['domain_v3'] = json.dumps(user_domain_dict) # [label1_en, label2_en, label3_en]
        results['domain'] = domain_en2ch(user_label_dict)      # label_ch
        
        #add user character_sentiment attribute
        character_sentiment = character_sentiment_result_dict[user]
        results['character_sentiment'] = character_sentiment
        #add user character_text attribtue
        character_text = character_text_result_dict[user]
        results['character_text'] = character_text
        
        #add user psy attribute
        user_psy_dict = [psy_results_dict[user]]
        results['psycho_status'] = json.dumps(user_psy_dict)
        
        #add user profile attribute
        register_dict = register_result[str(user)]
        results = dict(results, **register_dict)
        #add user_evaluate attribute---importance
        results['importance'] = get_importance(results['domain'], results['topic_string'], results['fansnum'], fansnum_max)
        #add user_evaluate attribute---activeness
        user_activeness_time = activeness_results[user]
        user_activeness_geo = json.loads(results['activity_geo_dict'])[-1]
        results['activeness'] = get_activeness(user_activeness_geo, user_activeness_time)
        #add user_evaluate attribute---influence
        results['influence'] = influence_results[user]
        
        #bulk_action
        action = {'index':{'_id': str(user)}}
        bulk_action.extend([action, results])
        if count >= 20:
            mark = save_user_results(bulk_action)
            print 'bulk_action:', bulk_action
            bulk_action = []
            count = 0
    
    end_ts = time.time()
    
    print 'user_set len:', len(user_set)
    print 'count:', count
    print 'bulk_action count:', len(bulk_action)
    
    print 'bulk_action:', bulk_action
    
    if bulk_action:
        status = save_user_results(bulk_action)
    
    #status = False
    return status # save by bulk

def add_domain():
    #read user weibo
    user_weibo_dict = read_user_weibo()
    uid_list = user_weibo_dict.keys()
    #get topic and domain input data
    user_keywords_dict = get_user_keywords_dict(user_weibo_dict)
    print 'user_keywords_dict:',user_keywords_dict
    
    print 'len(uid_list):', len(uid_list)
    start_ts = time.time()
    print 'start_ts:', start_ts
    '''
    psy_results = psychology_classfiy(user_weibo_dict)
    print 'psy_result:', psy_results
    
    domain_results = domain_classfiy(user_weibo_dict)
    domain_dict = domain_results[0]
    domain_label = domain_results[1]
    print 'domain_dict:', domain_dict
    print 'domain_label:', domain_label
    topic_dict , topic_label = topic_classfiy(user_weibo_dict)
    print 'topic_dict:', topic_dict
    print 'topic_label:', topic_label
    '''
    end_ts = time.time()
    print 'end_ts:', end_ts
    print 'end_ts - start_ts' , (end_ts - start_ts)
    print '[%s] cal speed: %s sec/per %s' % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'),end_ts - start_ts, len(uid_list))


if __name__=='__main__':
    print 'test'
    bulk_action = test_cron_text_attribute()
    #print 'bulk_action:', bulk_action
    #add_domain()
