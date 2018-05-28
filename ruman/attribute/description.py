# -*- coding:utf-8 -*-
import time
import sys
from influence_appendix import level

from ruman.global_utils import es_user_portrait as es
from ruman.global_utils import copy_portrait_index_name, copy_portrait_index_type
from ruman.time_utils import datetime2ts, ts2datetime
from ruman.parameter import INFLUENCE_CONCLUSION as conclusion_dict
from ruman.parameter import ACTIVENESS_CONCLUSION as activeness_conclusion_dict
from ruman.parameter import INFLUENCE_LENTH as N
from ruman.parameter import PRE_ACTIVENESS as pre_activeness
from ruman.parameter import INFLUENCE_LEVEL as influence_level
from ruman.parameter import INFLUENCE_LEVEL as activeness_level

def active_geo_description(result):
    active_city = {}
    active_ip = {}

    for city,value in result.items():
        count = 0
        for ip, ip_value in value.items():
            count += ip_value
            active_ip[ip] = ip_value
        active_city[city] = count

    city_count = len(active_city)
    ip_count = len(active_ip)

    active_city = sorted(active_city.iteritems(), key=lambda asd:asd[1], reverse=True)
    city = active_city[0][0]

    if city_count == 1 and ip_count <= 4:
        description_text = '为该用户的主要活动地，且较为固定在同一个地方登陆微博'
        city_list = city.split('\t')
        city = city_list[len(city_list)-1]
        description = [city, description_text]
    elif city_count >1 and ip_count <= 4:
        description_text1 = '多为该用户的主要活动地，且经常出差，较为固定在'
        description_text2 = '个城市登陆微博'
        city_list = city.split('\t')
        city = city_list[len(city_list)-1]
        description = [city, description_text1, city_count, description_text2]
    elif city_count == 1 and ip_count > 4:
        description_text = '为该用户的主要活动地，且经常在该城市不同的地方登陆微博'
        city_list = city.split('\t')
        city = city_list[len(city_list)-1]
        description = [city, description_text]
    else:
        description_text = '多为该用户的主要活动地，且经常出差，在不同的城市登陆微博'
        city_list = city.split('\t')
        city = city_list[len(city_list)-1]
        description = [city, description_text]
    return description


def active_time_description(result):
    count = 0
    for v in result.values():
        count += v
    average = count / 6.0
    active_time_order = sorted(result.iteritems(), key=lambda asd:asd[1], reverse=True)
    active_time = {0:'0:00-4:00', 14400:'4:00-8:00',28800:'8:00-12:00',43200:'12:00-16:00',57600:'16:00-20:00',72000:'20:00-24:00'}
    timestamp = active_time_order[0][0]
    segment = str(int(timestamp)/4/3600)
    definition = active_time[int(timestamp)]
    pd = {'0':'夜猫子','1':'早起刷微博','2':'工作时间刷微博','3':'午休时间刷微博','4':'上班时间刷微博','5':'下班途中刷微博','6':'晚间休息刷微博'}
 
    #description = '用户属于%s类型，活跃时间主要集中在%s' % (pd[segment], definition)
    description = ['用户属于', pd[segment], '类型，活跃时间主要集中在', definition]

    return description, pd[segment]


def hashtag_description(result):
    order_hashtag = sorted(result.iteritems(), key=lambda asd:asd[1], reverse=True)
    count_hashtag = len(result)

    count = 0 
    if result:
        for v in result.values():
            count += v
        average = count / len(result)

        v_list = []
        like = order_hashtag[0][0]
        for k,v in result.items():
            if v >= average:
                v_list.append(k)
        definition = ','.join(v_list)

    if count_hashtag == 0:
        description = u'该用户不喜欢参与话题讨论，讨论数为0'
    elif count_hashtag >3:
        description = u'该用户热衷于参与话题讨论,热衷的话题是%s' % definition
    else:
        description = u'该用户不太热衷于参与话题讨论, 参与的话题是%s' % definition

    return description


# version: 2015-12-22
# conclusion of a user based on history influence info
def conclusion_on_influence(uid):
    # test
    index_name = copy_portrait_index_name
    index_type = copy_portrait_index_type
    total_number = es.count(index=copy_portrait_index_name, doc_type=copy_portrait_index_type)["count"]

    try:
        influ_result = es.get(index=index_name, doc_type=index_type, id=uid)['_source']
    except:
        influ_result = {}
        result = [0, 0, 0, 0, 0, 0, total_number] # aver_activeness, sorted, aver_influence, sorted
        return result

    aver_activeness = influ_result.get("aver_activeness", 0)
    aver_influence = influ_result.get("aver_influence", 0)
    aver_importance = influ_result.get('aver_importance', 0)
    influence_query_body = {
        "query":{
            "match_all": {}
        },
        "sort": {"aver_influence": {"order": "desc"}},
        "size": 1
    }
    top_influence = es.search(index=copy_portrait_index_name, doc_type=copy_portrait_index_type, body=influence_query_body)['hits']['hits'][0]['sort'][0]

    importance_query_body = {
        "query":{
            "match_all": {}
        },
        "sort": {"aver_importance": {"order": "desc"}},
        "size": 1
    }
    top_importance = es.search(index=copy_portrait_index_name, doc_type=copy_portrait_index_type, body=importance_query_body)['hits']['hits'][0]['sort'][0]

    activeness_query_body = {
        "query":{
            "match_all": {}
        },
        "sort": {"aver_activeness": {"order": "desc"}},
        "size": 1
    }
    top_activeness = es.search(index=copy_portrait_index_name, doc_type=copy_portrait_index_type, body=activeness_query_body)['hits']['hits'][0]['sort'][0]

    influence_query_body = {
        "query": {
            "filtered":{
                "filter": {
                    "range": {
                        "aver_influence": {
                            "gt": aver_influence
                        }
                    }
                }
            }
        }
    }

    activeness_query_body = {
        "query": {
            "filtered":{
                "filter": {
                    "range": {
                        "aver_activeness": {
                            "gt": aver_activeness
                        }
                    }
                }
            }
        }
    }

    importance_query_body = {
        "query": {
            "filtered":{
                "filter": {
                    "range": {
                        "aver_importance": {
                            "gt": aver_importance
                        }
                    }
                }
            }
        }
    }

    influence_count = es.count(index=copy_portrait_index_name, doc_type=copy_portrait_index_type, body=influence_query_body)['count']
    activeness_count = es.count(index=copy_portrait_index_name, doc_type=copy_portrait_index_type, body=activeness_query_body)['count']
    importance_count = es.count(index=copy_portrait_index_name, doc_type=copy_portrait_index_type, body=importance_query_body)['count']

    result = [int(aver_activeness*100.0/top_activeness), activeness_count, int(aver_influence*100.0/top_influence), influence_count, int(aver_importance*100.0/top_importance), importance_count, total_number]
    return result

# version: 2015-12-22
# conclusion of a user based on history influence info
def conclusion_on_activeness(uid):
    # test
    index_name = copy_portrait_index_name
    index_type = copy_portrait_index_type
    try:
        influ_result = es.get(index=index_name, doc_type=index_type, id=uid)['_source']
    except:
        influ_result = {}
        result = activeness_conclusion_dict['0']
        return result

    # generate time series---keys
    now_ts = time.time()
    now_ts = datetime2ts('2013-09-12')
    activeness_set = set()
    for i in range(N):
        ts = ts2datetime(now_ts - i*3600*24)
        activeness_set.add(pre_activeness+ts)

    # 区分影响力和活跃度的keys
    keys_set = set(influ_result.keys())
    activeness_keys = keys_set & activeness_set

    if activeness_keys:
        activeness_value = []
        for key in activeness_keys:
            activeness_value.append(influ_result[key])
        mean, std_var = level(activeness_value)
        if mean < activeness_level[0]:
            result = activeness_conclusion_dict['1']
        elif mean >= activeness_level[0] and mean < activeness_level[1]:
            result = activeness_conclusion_dict['2']
        elif mean >= activeness_level[1] and mean < activeness_level[2]:
            result = activeness_conclusion_dict["3"]
        elif mean >= activeness_level[2] and mean < activeness_level[3]:
            result = activeness_conclusion_dict["4"]
        else:
            result = activeness_conclusion_dict["5"]
    else:
        result = conclusion_dict['0']

    return result

if __name__ == "__main__":
    """
    c = {'beijing':{'219.224.135.1': 5}}
    b = {0:2, 14400:1,28800:3, 43200:5, 57600:2, 72000:3}
    a = {'花千骨':4}
    k = active_time_description(b)
    m = active_geo_description(c)
    n = hashtag_description(a)
    print m
    print k
    print n
    """
    print conclusion_on_influence('2050856634')



