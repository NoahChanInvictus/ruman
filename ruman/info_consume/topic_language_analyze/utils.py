# -*- coding: utf-8 -*-
from ruman.global_config import db,es_user_profile,profile_index_name,profile_index_type,\
                            topics_river_index_name,topics_river_index_type,\
                            subopinion_index_name,subopinion_index_type,topic_index_name,topic_index_type
from ruman.global_utils import portrait_index_name,portrait_index_type,bci_history_index_type,bci_history_index_name,es_bci_history,es_user_portrait,portrait_index_name,portrait_index_type
from ruman.global_config import weibo_es,weibo_index_name,weibo_index_type,MAX_FREQUENT_WORDS,MAX_LANGUAGE_WEIBO

from ruman.time_utils import ts2HourlyTime,datetime2ts,full_datetime2ts,ts2datetime

from ruman.parameter import RUN_TYPE,RUN_TEST_TIME
from ruman.info_consume.model import CityTopicCount,CityWeibos
import math,time
import json
import re,sys
from xpinyin import Pinyin
from ruman.global_utils import R_ADMIN as r
from ruman.global_utils import topic_queue_name,es_flow_text,flow_text_index_name_pre,flow_text_index_type
sys.path.append('./ruman/cron/flow_text/')
from keyword_extraction import get_weibo
# from cp_global_config import db,es_user_profile,profile_index_name,profile_index_type,\
#                             topics_river_index_name,topics_river_index_type,\
#                             subopinion_index_name,subopinion_index_type
# from cp_global_config import weibo_es,weibo_index_name,weibo_index_type,MAX_FREQUENT_WORDS,MAX_LANGUAGE_WEIBO

# from cp_time_utils import ts2HourlyTime,datetime2ts,full_datetime2ts

# from cp_model import CityTopicCount,CityWeibos

verified_value={'0':10,'1':5,'2':5,'3':7,'220':3}
#fans_value = {10000000:10,1000000:6,100000:3,10000:1,1:0}

Minute = 60
Fifteenminutes = 15 * Minute
Hour = 3600
SixHour = Hour * 6
Day = Hour * 24
MinInterval = Fifteenminutes
p = Pinyin()

def _json_loads(weibos):
    try:
        return json.loads(weibos)
    except ValueError:
        if isinstance(weibos, unicode):
            return json.loads(json.dumps(weibos))
        else:
            return None


def get_topics(user):
    results = {'recommend':{},'own':{}}
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[{'term':{'comput_status':1}}],
                        'must_not':[{'term':{'submit_user':user}}]
                    }
                }
            }
        },
        'sort':{'submit_ts':{'order':'desc'}},
        'size':1000
        
    }
    topics = weibo_es.search(index=topic_index_name,doc_type=topic_index_type,body=query_body)
    if topics:
        topics = topics['hits']['hits']
        for topic in topics:
            try:
                if topic['_source']['en_name']=='sa-de-1500559853':
                    topic['_source']['en_name']='1478787000_1480255800_sa-de-1500559853_1788911247'
                results['recommend'][topic['_source']['en_name']].append([topic['_source']['name'],topic['_source']['start_ts'],topic['_source']['end_ts'],topic['_source']['comput_status'],topic['_source']['submit_user']])
            except:
                if topic['_source']['en_name']=='sa-de-1500559853':
                    topic['_source']['en_name']='1478787000_1480255800_sa-de-1500559853_1788911247'
                results['recommend'][topic['_source']['en_name']] = [[topic['_source']['name'],topic['_source']['start_ts'],topic['_source']['end_ts'],topic['_source']['comput_status'],topic['_source']['submit_user']]]
    query_own = {
        'query':{
            'filtered':{
                'filter':{
                    'term':{'submit_user':user}
                }
            }
        },
        "size": 1000
    }
    own_topics =  weibo_es.search(index=topic_index_name,doc_type=topic_index_type,body=query_own)
    if own_topics:
        topics = own_topics['hits']['hits']
        for topic in topics:
            try:
                if topic['_source']['en_name']=='sa-de-1500559853':
                    topic['_source']['en_name']='1478787000_1480255800_sa-de-1500559853_1788911247'
                results['own'][topic['_source']['en_name']].append([topic['_source']['name'],topic['_source']['start_ts'],topic['_source']['comput_status'],topic['_source']['end_ts']])
            except:
                if topic['_source']['en_name']=='sa-de-1500559853':
                    topic['_source']['en_name']='1478787000_1480255800_sa-de-1500559853_1788911247'
                results['own'][topic['_source']['en_name']] = [[topic['_source']['name'],topic['_source']['start_ts'],topic['_source']['comput_status'],topic['_source']['end_ts']]]

            #print results
    return json.dumps(results)


    # es.index(index='topics',doc_type='text',id='1467648000_1470900837_aoyunhui_jln',body={'name':'奥运会','en_name':'aoyunhui','end_ts':'1470900837',\
    #                                             'start_ts':'1467648000','submit_user':'jln','comput_status':0})

def get_key_topics(keyword):
    result = {}
    query_body = {
        'query': {
            'bool': {
                'must': [
                        {'term':{'comput_status':1}},
                        {'wildcard':{'name':'*'+keyword+'*'}}
                        ]
                }
            }
    }
    results = weibo_es.search(index=topic_index_name,doc_type=topic_index_type,body=query_body)
    if results:
        topics = results['hits']['hits']
        for topic in topics:
            try:
                result[topic['_source']['en_name']].append([topic['_source']['name'],topic['_source']['start_ts'],topic['_source']['end_ts'],topic['_source']['comput_status']])
            except:
                result[topic['_source']['en_name']] = [[topic['_source']['name'],topic['_source']['start_ts'],topic['_source']['end_ts'],topic['_source']['comput_status']]]
    return json.dumps(result)


def search_topics(keyword):
    result = []
    query_body = {
        'query': {
            'bool': {
                'should': [
                        {'wildcard':{'en_name':'*'+keyword+'*'}},
                        {'wildcard':{'name':'*'+keyword+'*'}}
                        ]
                }
            }
    }
    results = weibo_es.search(index=topic_index_name,doc_type=topic_index_type,body=query_body)
    if results:
        topics = results['hits']['hits']
        for topic in topics:
            result.append(topic['_source'])
            #try:
            #    result[topic['_source']['en_name']].append([topic['_source']['name'],topic['_source']['start_ts'],topic['_source']['end_ts'],topic['_source']['comput_status']])
            #except:
            #    result[topic['_source']['en_name']] = [[topic['_source']['name'],topic['_source']['start_ts'],topic['_source']['end_ts'],topic['_source']['comput_status']]]
    return json.dumps(result)

def search_topic_by_topic(topic):
    result = []
    query_body = {
        'query': {
            'term': {
                'name':topic
                }
            }
    }
    results = weibo_es.search(index=topic_index_name,doc_type=topic_index_type,body=query_body)
    if results:
        topics = results['hits']['hits']
        for topic in topics:
            result.append(topic['_source'])
            #try:
            #    result[topic['_source']['en_name']].append([topic['_source']['name'],topic['_source']['start_ts'],topic['_source']['end_ts'],topic['_source']['comput_status']])
            #except:
    return json.dumps(result)


def submit(topic,start_ts,end_ts,submit_user):
    # print str(topic.decode('utf-8'))
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'term':{
                        'name':topic 
                    }
                }
            }
        }
    }
    find_topic = weibo_es.search(index=topic_index_name,doc_type=topic_index_type,body=query_body)['hits']['hits']
    if len(find_topic)>0:
        en_name = find_topic[0]['_source']['en_name']
    else:
        en_name = p.get_pinyin(topic)+'-'+str(int(time.time()))

    submit_id = start_ts+'_'+end_ts+'_'+en_name+'_'+submit_user
    query_body={
        'name':topic,
        'en_name':en_name,
        'start_ts':start_ts,
        'end_ts':end_ts,
        'submit_user':submit_user,
        'comput_status':0,
        'submit_ts':int(time.time())
    }
    try:
        # print weibo_es.get(index=topic_index_name, doc_type=topic_index_type, id=submit_id)['_source']
        result = 'already_have'
    except:
        weibo_es.index(index=topic_index_name,doc_type=topic_index_type,id=submit_id,body=query_body)
        result = 'success'
    r.lpush(topic_queue_name,json.dumps(query_body))
    #该push到redis里，然后改status  计算完了再改回来
    return result

def delete(en_name,start_ts,end_ts,submit_user):
    task_id = start_ts+'_'+end_ts+'_'+en_name+'_'+submit_user
    # print task_id
    try:
        result = weibo_es.delete(index=topic_index_name,doc_type=topic_index_type,id=task_id)['found']
        # print result
        return result
    except:
        print "not found!"
        return -1

def get_during_keywords(topic,start_ts,end_ts):  #关键词云,unit=MinInterval
    keywords = []
    # if (end_ts-start_ts)>unit:
    #     begin_ts = end_ts-unit
    # else:
    #     begin_ts = start_ts
    # print begin_ts,end_ts
    query_body = {
        'query':{
            'filtered':{
                'filter':{
                    'range':{
                        'timestamp':{'gte': start_ts, 'lt':end_ts} 
                    }
                }
            }
        },
        'size':MAX_LANGUAGE_WEIBO
    }
    keywords_dict = {}
    weibo_text = []
    keyword_weibo = weibo_es.search(index=topic,doc_type=weibo_index_type,body=query_body)['hits']['hits']   
    for key_weibo in keyword_weibo:
        weibo_text.append(key_weibo['_source']['text'].encode('utf-8'))
    keywords_dict = get_weibo(weibo_text,n_gram=2,n_count=100)
    '''
    print keyword_weibo
    for key_weibo in keyword_weibo:
        keywords_dict_list = json.loads(key_weibo['_source']['keywords_dict'])  #
        #print keywords_dict_list,type(keywords_dict_list)
        for k,v in keywords_dict_list.iteritems():
            try:
                keywords_dict[k] += v
            except:
                keywords_dict[k] = v
    '''
    word_results = sorted(keywords_dict.iteritems(),key=lambda x:x[1],reverse=True)[:MAX_FREQUENT_WORDS]   
    return json.dumps(word_results)      

def get_topics_river(topic,start_ts,end_ts,unit=MinInterval):#主题河
    #topic='event'
    # print start_ts,end_ts
    topic_name = topic+'_'+start_ts+'_'+end_ts
    query_body = {
        'query':{
            'bool':{
                'must':[
                    {'term':{'name':topic_name}},
                    {'range':{'start_ts':{'lte':start_ts}}},
                    {'range':{'end_ts':{'gte':end_ts}}}
                ]
            }
        }
    }
    # print '????',query_body
    news_topics = json.loads(weibo_es.search(index=topics_river_index_name,doc_type=topics_river_index_type,body=query_body)['hits']['hits'][0]['_source']['features'])
    zhutihe_results = cul_key_weibo_time_count(topic,news_topics,start_ts,end_ts,unit)
    results = {}
    for k,v in news_topics.iteritems():
        if len(v)>0:
            results[v[0]] = zhutihe_results[k]
    # print results
    return results


def get_symbol_weibo(topic,start_ts,end_ts,unit=MinInterval):  #鱼骨图
    # print topic
    weibos = {}
    # query_body = {
    #     'query':{
    #         'bool':{
    #             'must':[
    #                 {'term':{'name':topic}},
    #                 {'range':{'start_ts':{'lte':start_ts}}},
    #                 {'range':{'end_ts':{'gte':end_ts}}}
    #             ]
    #         }
    #     }
    # }
    query_body = {
        "query": {
          "match_phrase": {
            "name": topic
          }
        }
    }

    try:
        symbol = weibo_es.search(index=topics_river_index_name,doc_type=topics_river_index_type,body=query_body)['hits']['hits'][0]['_source']
    except:
        return 0
    features = json.loads(symbol['features'])
    symbol_weibos = json.loads(symbol['cluster_dump_dict'])
    # print 'dadfhsjdbfsdjdh'
    # print symbol_weibos
    begin_ts = end_ts - unit
    for clusterid,contents in symbol_weibos.iteritems():
        j = 0
        content = set()
        for i in contents:
            ts = full_datetime2ts(i['datetime'])
            # title = re.findall(r'【.*】',i['content'].encode('utf8'))[0]
            title = i['content'][:7]
            if ts >= start_ts and ts <= end_ts and title not in content:  #start_ts应该改成begin_ts，现在近15分钟没数据，所以用所有的
                try:
                    weibos[','.join(features[clusterid][:5])].append(i)
                except:
                    weibos[','.join(features[clusterid][:5])] = [i]
                content.add(title)
                j += 1
            #print content
            if j == 3:
                break
    #print weibos
    return weibos


def get_subopinion(topic,start_ts,end_ts):
    # query_body = {
    #     'query':{
    #         'filtered':{
    #             'filter':{
    #                 'bool':{
    #                     'must':[
    #                         {'match_phrase':{'name':topic}}
    #                     ]
    #                 }
    #             }
    #         }
    #     }
    # }
    query_body = {
        "query": {
          "match_phrase": {
            "name": topic
          }
        }
    }
    # print query_body
    features = weibo_es.search(index=subopinion_index_name,doc_type=subopinion_index_type,body=query_body)['hits']['hits']
    
    # return features
    if features:
        feature = json.loads(features[0]['_source']['features'])
        return feature.values()
    else:
        return 'no results'

def get_subopinion_new(topic,start_ts,end_ts,sort_item='timestamp'):
    # query_body = {
    #     'query':{
    #         'filtered':{
    #             'filter':{
    #                 'bool':{
    #                     'must':[
    #                         {'match_phrase':{'name':topic}}
    #                     ]
    #                 }
    #             }
    #         }
    #     }
    # }
    query_body = {
        "query": {
          "match_phrase": {
            "name": topic
          }
        }
    }
    # print query_body
    results = []
    print topic
    weibos = weibo_es.get(index=subopinion_index_name,id=topic,doc_type="text")['_source']

    print weibos
    for k,weibo in weibos.items():
        if k != 'start_ts' and k !='end_ts':
            result = {}
            weibo_dict ={}
    
            raw_keys=weibo['keys']
            raw_keys = raw_keys.split('_')
            result['keys']=get_mode(raw_keys)
    
            weibos_texts = json.loads(weibo['cluster_dump_dict'])
            for weibo_text in weibos_texts.values():#jln0825
                weibo_text = weibo_text[0]
                weibo_content = {}
                weibo_content['text'] = weibo_text['text'] 
                weibo_content['uid'] = weibo_text['uid']
                weibo_content['timestamp'] = full_datetime2ts(weibo_text['datetime'])
                weibo_content['comment'] = weibo_text['comment']
                weibo_content['retweeted'] = weibo_text['retweeted']
                weibo_content['mid'] = weibo_text['id']
                try:
                    user = es_user_profile.get(index=profile_index_name,doc_type=profile_index_type,id=weibo_content['uid'])['_source']
                    weibo_content['uname'] = user['nick_name']
                    weibo_content['photo_url'] = user['photo_url']
                except:
                    weibo_content['uname'] = 'unknown'
                    weibo_content['photo_url'] = 'unknown'
                weibo_dict[weibo_content['mid']] = weibo_content
    
            result['weibos'] = sorted(weibo_dict.items(),key=lambda x:x[1][sort_item],reverse=True)
            results.append(result)


    return results


def get_weibo_content(topic,start_ts,end_ts,opinion,sort_item='timestamp'): #微博内容
    weibo_dict = {}
    #a = json.dumps(opinion)
    #opinion = '圣保罗_班底_巴西_康熙'
    print 'opinion:::::::::',opinion
    print 'topic:::::::;:::',topic
    print type(start_ts),type(end_ts)
    query_body = {
        'query':{
            'bool':{
                'must':[
                    {'wildcard':{'keys':opinion}},
                    {'term':{'name':topic}},
                    {'range':{'start_ts':{'lte':start_ts}}},
                    {'range':{'end_ts':{'gte':end_ts}}}
                ]
            }
        }
    }  #没有查到uid   每次的id不一样   
    print query_body
    weibos = weibo_es.search(index=subopinion_index_name,doc_type=subopinion_index_type,body=query_body)['hits']['hits']
    #print weibo_es,subopinion_index_name,subopinion_index_type,query_body
    print len(weibos)
    if weibos:
        weibos = json.loads(weibos[0]['_source']['cluster_dump_dict'])
        for weibo in weibos.values():#jln0825
            weibo = weibo[0]
            weibo_content = {}
            weibo_content['text'] = weibo['text'] 
            weibo_content['uid'] = weibo['uid']
            weibo_content['timestamp'] = full_datetime2ts(weibo['datetime'])
            weibo_content['comment'] = weibo['comment']
            weibo_content['retweeted'] = weibo['retweeted']
            weibo_content['mid'] = weibo['id']
            try:
                user = es_user_profile.get(index=profile_index_name,doc_type=profile_index_type,id=weibo_content['uid'])['_source']
                weibo_content['uname'] = user['nick_name']
                weibo_content['photo_url'] = user['photo_url']
            except:
                weibo_content['uname'] = 'unknown'
                weibo_content['photo_url'] = 'unknown'
            weibo_dict[weibo_content['mid']] = weibo_content
        results = sorted(weibo_dict.items(),key=lambda x:x[1][sort_item],reverse=True)
        #print results
        return results
    else:
        return 'no results'


def cul_key_weibo_time_count(topic,news_topics,start_ts,over_ts,during):
    key_weibo_time_count = {}
    time_dict = {}
    during = Day
    for clusterid,keywords in news_topics.iteritems(): #{u'd2e97cf7-fc43-4982-8405-2d215b3e1fea': [u'\u77e5\u8bc6', u'\u5e7f\u5dde', u'\u9009\u624b']}
        if len(keywords)>0:
            print len(keywords)
            start_ts = int(start_ts)
            over_ts = int(over_ts)

            over_ts = ts2HourlyTime(over_ts, during)
            interval = (over_ts - start_ts) / during


            for i in range(interval, 0, -1):    #时间段取每900秒的

                begin_ts = over_ts - during * i
                end_ts = begin_ts + during
                must_list=[]
                must_list.append({'range':{'timestamp':{'gte':begin_ts,'lt':end_ts}}})
                temp = []
                
                for word in keywords:
                    word_list=word.split('_', 1)
                    word1=word_list[0]
                    sentence1 =  {'wildcard':{'keywords_string':'*'+word1+'*'}}
                    try:
                        word2=word_list[1]
                        sentence2 =  {'wildcard':{'keywords_string':'*'+word2+'*'}}
                        temp.append(sentence2)
                    except:
                        print "index out of range"
                    temp.append(sentence1)
                must_list.append({'bool':{'should':temp}})

                query_body = {'query':{
                                'bool':{
                                    'must':must_list
                                }
                            }
                        }
                key_weibo = weibo_es.search(index=topic,doc_type=weibo_index_type,body=query_body)
                key_weibo_count = key_weibo['hits']['total']  #分时间段的类的数量
                print key_weibo_count
                time_dict[ts2datetime(end_ts)] = key_weibo_count

            key_weibo_time_count[clusterid] = sorted(time_dict.items(),key=lambda x:x[0])
    return key_weibo_time_count


def get_sen_ratio(topic,start_ts,end_ts):
    query_body = {
        'query':{
            'bool':{
                'must':[
                    {'wildcard':{'text':'*'+topic+'*'}},
                    {'range':{'timestamp':{'lte':end_ts,'gte':start_ts}}}
                ]
            }
        },
        'aggs':{
            'all_interests':{
                'terms':{
                    'field': 'sentiment',
                }
            }
        }
    } 
    if RUN_TYPE == 0 :
        date = '2013-09-07'
    else:
        date = ts2datetime(time.time())
    result = es_flow_text.search(index = flow_text_index_name_pre+date,doc_type=flow_text_index_type,body=query_body)\
            ['aggregations']['all_interests']['buckets']
    return result

def get_person_value(uid):
    #认证类型
    #print es_user_profile,profile_index_name,profile_index_type,uid
    try:
        value_static = es_bci_history.get(index = bci_history_index_name,doc_type = bci_history_index_type,id=uid)
        value_inf = es_user_portrait.get(index = portrait_index_name,doc_type = portrait_index_type,id=uid)
        static = es_user_profile.get(index = profile_index_name,doc_type = profile_index_type,id=uid)
    except:
        return 'no'
    fans_max = es_bci_history.search(index = bci_history_index_name,doc_type = bci_history_index_type,body={'query':{'match_all':{}},'sort':{'user_fansnum':{'order':'desc'}},'size':1})['hits']['hits'][0]['_source']['user_fansnum']
    print 'max:',fans_max
    #print static['found']
    if static['found']==False:
        return 'no'
    else:
        static = static['_source']
    #print "static",static
    try:
        ver_calue = verified_value[static['verified_type']]
    except:
        ver_calue = 0
    #账号创建时间
    times = math.ceil((time.time()-int(static['create_at']))/31536000)
    #粉丝数
    #person = es_user_profile.get(index = profile_index_name,doc_type = profile_index_type,id=uid)['_source']
    fans_value = math.log(float(value_static['_source']['user_fansnum'])/float(fans_max)*9+1,10)
    #fans_value = (math.log(static['fansnum']+1000000,100000000)-0.75)*4
    #if fans_value>1:
    #    fans_value=1.0
    influence_max = es_user_portrait.search(index = portrait_index_name,doc_type = portrait_index_type,body={'query':{'match_all':{}},'sort':{'influence':{'order':'desc'}},'size':1})['hits']['hits'][0]['_source']['influence']
    influence_value = float(value_inf['_source']['influence'])/float(influence_max)
    final= (ver_calue*0.1+times*0.05+fans_value+influence_value*1.2)*30
    print ver_calue,times,fans_value,influence_value
    return final
    
def get_mode(arr):  
    mode = [];  
    arr_appear = dict((a, arr.count(a)) for a in arr);  # 统计各个元素出现的次数  
    if max(arr_appear.values()) == 1:  # 如果最大的出现为1  
        return;  # 则没有众数  
    else: 
        sort_arr = sorted(arr_appear.iteritems(), key=lambda d:d[1], reverse = True)
        for i in range(0,4):  # 否则，出现次数最大的数字，就是众数  
            mode.append(sort_arr[i][0]);  
    return mode


if __name__ == '__main__':
	#all_weibo_count('aoyunhui',1468166400,1468170900)
    #get_symbol_weibo('aoyunhui',1468944000,1471622400,Day)
    # opinion=['姐姐', '综艺节目', '网络']
    #get_weibo_content('aoyunhui',1468944000,1471622400,opinion)
    # get_during_keywords('aoyunhui',1468944000,1469707652)
    topic='te-lang-pu-ji-xin-ge-1492166854'
    start_ts = 1478736000
    end_ts=1480176000
    query_body = {
        'query':{
            'bool':{
                'must':[
                    {'term':{'name':topic}},
                    {'range':{'start_ts':{'lte':start_ts}}},
                    {'range':{'end_ts':{'gte':end_ts}}}
                ]
            }
        }
    }
    
    symbol = weibo_es.search(index=topics_river_index_name,doc_type=topics_river_index_type,body=query_body)['hits']['hits'][0]['_source']
    print symbol