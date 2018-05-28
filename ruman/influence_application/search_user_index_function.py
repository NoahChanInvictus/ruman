# -*- coding: UTF-8 -*-
import math
import time
import datetime
import sys
from numpy import *
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError
from rank_portrait_in_active_user import search_k

from mid2weibolink import weiboinfo2url
from ruman.global_utils import ES_CLUSTER_FLOW1 as es
from ruman.global_utils import es_user_profile as es_profile # user profile es
from ruman.global_utils import es_user_portrait as es_portrait # user portrait es
from ruman.global_utils import profile_index_name, profile_index_type, portrait_index_name, portrait_index_type, copy_portrait_index_name, copy_portrait_index_type

"""
based on user_index, search users in different range

"""
def count_es(es, index_name,doctype, sort_order="user_index",range_1=0, range_2=3000):
    query_body = {
        "query":{
            "filtered": {
                "query": {
                    "match_all":{}
                },
                "filter": {
                    "range": {
                        sort_order: {
                            "gte": range_1,
                            "lt": range_2
                        }
                    }
                }
            }
        }
    }


    result = es.count(index=index_name, doc_type=doctype, body=query_body)['count']

    return result

def user_index_range_distribution(index_name,doctype, sort_order):

    return_list = []
    distribute_range = []
    top_index = search_top_index(index_name=index_name,index_type=doctype, top_k=1, top=True,sort_order=sort_order)
    max_score = int(math.ceil(top_index/100.0)) * 100

    # devide active user based on active degree

    score_range = [0,100,200,500,600, 700,800, 900, 1100, 1300, 1500, max_score]
    for i in range(len(score_range)-1):
        temp_number = count_es(es, index_name, doctype, sort_order, score_range[i], score_range[i+1])
        distribute_range.append(temp_number)
    return_list.append(score_range)
    return_list.append(distribute_range)

    return return_list

def query_brust(index_name,field_name, range_1=0, range_2=50000, count=0):
    query_body = {
        "query":{
            "filtered": {
                "query": {
                    "match_all":{}
                },
                "filter": {
                    "range": {
                        field_name: {
                            "gte": range_1,
                            "lt": range_2
                        }
                    }
                }
            }
        }
    }

    if count == 1:
        result = es.count(index=index_name, doc_type="bci", body=query_body)['count']
        return result

    else:
        query_body['size'] = 1000
        result = es.search(index=index_name, doc_type="bci", body=query_body)['hits']['hits']

        profile_list = []
        for item in result:
            profile_list.append(item['_id'])

        return profile_list


# search user_index top_k

def search_top_index(index_name, top_k=1, index_type="bci", top=False, sort_order="user_index"):
    query_body = {
        "query": {
            "match_all": {}
        },
        "size": top_k,
        "sort": [{sort_order: {"order": "desc"}}]
    }

    if top:
        result = es.search(index=index_name, doc_type=index_type, body=query_body)['hits']['hits'][0]['_source'][sort_order]
    else:
        search_result = es.search(index=index_name, doc_type=index_type, body=query_body)['hits']['hits']

        uid_list = []
        for item in search_result:
            uid_list.append(item['_id'])
        profile_result = es_profile.mget(index=profile_index_name,doc_type=profile_index_type, body={"ids":uid_list}, _source=True)['docs']
        portrait_result = es_portrait.mget(index=portrait_index_name, doc_type=portrait_index_type, body={"ids":uid_list}, _source=True)['docs']

        result = []
        rank = 1
        for i in range(len(search_result)):
            info = ['','','','']
            info[0] = rank
            if profile_result[i]['found']:
                info[1] = profile_result[i]['_source'].get('photo_url','')
                info[3] = profile_result[i]['_source'].get('nick_name','')

            info[2] = search_result[i].get('_id','')
            if sort_order in ["user_index","origin_weibo_retweeted_brust_average","origin_weibo_comment_brust_average"]:
                info.append(search_result[i]['_source'][sort_order])
                if portrait_result[i]['found']:
                    info.append("1")
                else:
                    info.append("0")
            elif sort_order == "origin_weibo_retweeted_top_number":
               info.append(search_result[i]['_source']['origin_weibo_retweeted_top_number']) 
               mid = search_result[i]['_source']['origin_weibo_top_retweeted_id']
               info.append(weiboinfo2url(info[2],mid))
               if portrait_result[i]['found']:
                   info.append("1")
               else:
                   info.append("0")
            elif sort_order == "origin_weibo_comment_top_number":
                info.append(search_result[i]['_source']['origin_weibo_comment_top_number'])
                mid = search_result[i]['_source']['origin_weibo_top_comment_id']
                info.append(weiboinfo2url(info[2],mid))
                if portrait_result[i]['found']:
                    info.append("1")
                else:
                    info.append("0")

            rank += 1
            result.append(info)

    return result

"""
based on uid_list, obtain detail active info

"""

def search_influence_detail(uid_list, index_name, doctype):
    print es,index_name,doctype,uid_list
    result = es.mget(index=index_name, doc_type=doctype, body={"ids": uid_list}, _source=True)["docs"]
    if result:
        return result[0]['_source']
    else:
        return None


"""
search single field max value

"""

def search_max_single_field(field, index_name, doctype, top_k=3):

    # field = "origin_weibo_retweeted_top_number", "origin_weibo_comment_top_number"
    query_body = {
        "query": {
            "match_all": {}
        },
        "sort": [{field: {"order": "desc"}}],
        "size": top_k
    }

    
    return_list = []
    rank = 1
    count_c = 0
    start = 0

    while 1:
        search_list = []
        user_list = search_k(es, index_name, doctype, start, field, 100)
        start += 100
        for item in user_list:
            uid = item.get('user','0')
            search_list.append(uid) # uid list

        search_result = es_portrait.mget(index=portrait_index_name, doc_type=portrait_index_type, body={"ids": search_list}, _source=True)["docs"]
        profile_result = es_profile.mget(index=profile_index_name, doc_type=profile_index_type, body={"ids": search_list}, _source=True)["docs"]

        for i in range(len(search_result)):
            if search_result[i]['found']:
                info = ['','','','','','','1']
                info[0] = rank
                info[2] = search_result[i].get('_id','')

                if profile_result[i]['found']:
                    info[1] = profile_result[i]['_source'].get('photo_url','')
                    info[3] = profile_result[i]['_source'].get('nick_name','')

                if 'retweeted' in field:
                    temp_mid = user_list[i]['origin_weibo_top_retweeted_id']
                    info[5] = weiboinfo2url(info[2], temp_mid)
                    info[4] = user_list[i]['origin_weibo_retweeted_top_number']
                else:
                    temp_mid = user_list[i]['origin_weibo_top_comment_id']
                    info[5] = weiboinfo2url(info[2], temp_mid)
                    info[4] = user_list[i]['origin_weibo_comment_top_number']

                rank += 1
                return_list.append(info)

                if rank >= int(top_k)+1:
                    return return_list

def time_series(date):
    date_list = []
    date_list.append(date)
    time_struct = datetime.date(int(date[0:4]), int(date[4:6]), int(date[6:]))
    timestamp = time.mktime(time_struct.timetuple())

    i =1
    next_timestamp = timestamp
    while 1:
        next_timestamp -= 86400
        if i == 7:
            break
        else:
            date_list.append(time.strftime('%Y%m%d',time.localtime(next_timestamp)))
            i += 1
    print date_list
    return date_list

def search_portrait_history_active_info(uid, date, index_name=copy_portrait_index_name, doctype=copy_portrait_index_name):
    # date.formate: 20130901
    date_list = time_series(date)

    try:
        result = es.get(index=index_name, doc_type=doctype, id=uid, _source=True)['_source']
    except NotFoundError:
        return "NotFound"
    except:
        return None
    
    date_max = {}
    for date_str in date_list:
        query_body = {
            'query':{
                'match_all':{}
                },
            'size': 1,
            'sort': [{date_str: {'order': 'desc'}}]
        }
        try:
            max_item = es.search(index=index_name, doc_type=doctype, body=query_body)['hits']['hits']
        except Exception, e:
            raise e
        date_max[date_str] = max_item[0]['_source'][date_str]
    print 'date_max:', date_max

    return_dict = {}
    for item in date_list:
        return_dict[item] = result.get(item, 0)

    in_list = []
    normal_list = []
    for item in sorted(date_list):
        in_list.append(return_dict[item])
        normal_value = math.log((return_dict[item] / date_max[item]) * 9 + 1 , 10) * 100
        normal_list.append(normal_value)
    
    #print 'in_list:', in_list
    max_influence = max(in_list)
    ave_influence = sum(in_list) / float(7)
    min_influence = min(in_list)
    if max_influence - min_influence <= 400 and ave_influence >= 900:
        mark = u'平稳高影响力'
    elif max_influence - min_influence > 400 and ave_influence >= 900:
        mark = u'波动高影响力'
    elif max_influence - min_influence <= 400 and ave_influence < 900 and ave_influence >= 500:
        mark = u'平稳一般影响力'
    elif max_influence - min_influence > 400 and ave_influence < 900 and ave_influence >= 500:
        mark = u'波动一般影响力'
    elif max_influence - min_influence <= 400 and ave_influence < 500:
        mark = u'平稳低影响力'
    else:
        mark = u'波动低影响力'
    description = [u'该用户为', mark]
    return [normal_list, description]


if __name__ == "__main__":

    es = ES_CLUSTER_FLOW1

    """
    all_range = []
    distribute_range = []
    top_index = search_top_index(index_name="20130901",top_k=1, top=True)
    print top_index
    max_score = int(math.ceil(top_index/100.0)) * 100

    # devide active user based on active degree


    score_range = [0, 100, 200, 500, 700, 900, 1100, 1300, 1500, max_score]
    for i in range(len(score_range)-1):
        temp_number = query_es(index_name, score_range[i], score_range[i+1])
        all_range.append(temp_number)
    print all_range



    # draw all active user seperately


    index_range = range(0, max_score+100, 100)
    for i in range(len(index_range)-1):
        temp_number = query_es(index_name, index_range[i], index_range[i+1])
        distribute_range.append(temp_number)
    print distribute_range



    # search brust
    ss = range(0,1000,10)
    ss_set = []
    for i in range(len(ss)-1):
        result = query_brust(index_name, ss[i], ss[i+1], count=1)
        ss_set.append(result)
    print ss_set


    uid_list = ['1713926427','2758565493']
    result_dict = search_influence_detail(uid_list, '20130901', 'bci')
    print result_dict


    field_name = "origin_weibo_comment_top_number"
    result = search_max_single_field(field_name, '20130901', 'bci')
    print result


    result = search_portrait_history_active_info('2256040435', "20130901", "20130910")
    print result

    """


