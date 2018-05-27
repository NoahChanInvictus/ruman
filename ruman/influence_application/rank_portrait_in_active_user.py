# -*- coding = utf-8 -*-

# "user" field

import sys
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
from elasticsearch import RequestError
"""
reload(sys)
sys.path.append('./../')
from global_utils import ES_CLUSTER_FLOW1 as es
from global_utils import es_user_profile as es_profile
from global_utils import es_user_portrait as es_portrait
"""
from ruman.global_utils import ES_CLUSTER_FLOW1 as es
from ruman.global_utils import es_user_portrait as es_portrait
from ruman.global_utils import es_user_profile as es_profile


index_name = "20130901"

def search_k(es, index_name, index_type, start, field="user_index", size=100):
    query_body = {
        "query":{
            "match_all": {}
            },
        "size": size,
        "from": start,
        "sort": [{field: {"order": "desc"}}]
    }

    result = es.search(index=index_name, doc_type=index_type, body=query_body)['hits']['hits']

    search_list = []
    for item in result:
        search_list.append(item['_source'])

    return search_list

def search_portrait_user_in_activity(es, number, active_index, active_type, portrait_index, portrait_type, field="user_index"):

    return_list = []
    index_exist = es.indices.exists(index=active_index)
    if not index_exist:
        return "no active_index exist"
        sys.exit(0)

    count_s = 0
    count_c = 0
    start = 0
    rank = 1
    while 1:
        search_list = []
        user_list = search_k(es, active_index, active_type, start, field, 100)
        start += 100
        for item in user_list:
            if field == "vary":
                uid = item.get('uid', '0') # obtain uid, notice "uid" or "user"
            else:
                uid = item.get('user', '0')
            search_list.append(uid) # uid list

        search_result = es_portrait.mget(index=portrait_index, doc_type=portrait_type, body={"ids": search_list}, _source=True)["docs"]
        profile_result = es_profile.mget(index="weibo_user", doc_type="user", body={"ids": search_list}, _source=True)["docs"]

        key_list = ["origin_weibo_retweeted_total_number", "origin_weibo_retweeted_average_number", "origin_weibo_retweeted_top_number", "origin_weibo_retweeted_brust_average", \
                   "origin_weibo_comment_total_number", "origin_weibo_comment_average_number", "origin_weibo_comment_top_number", "origin_weibo_retweeted_brust_average", \
                   "retweeted_weibo_retweeted_total_number", "retweeted_weibo_retweeted_average_number", "retweeted_weibo_retweeted_top_number", "retweeted_weibo_retweeted_brust_average", \
                   "retweeted_weibo_comment_total_number", "retweeted_weibo_comment_average_number", "retweeted_weibo_comment_top_number", "retweeted_weibo_retweeted_brust_average"]
        for item in search_result:
            if item["found"]:
                info = ['','','','','','']
                info[0] = rank
                index = search_result.index(item)

                if profile_result[index]['found']:
                    info[1] = profile_result[index]['_source'].get('photo_url','')
                    info[3] = profile_result[index]['_source'].get('nick_name','')
                info[2] = search_result[index].get('_id','')
                info[4] = user_list[index]['user_index']
                info[5] = "1"
                if field == 'origin_weibo_retweeted_brust_average':
                    info.append(user_list[index]['origin_weibo_retweeted_brust_average'])
                    for key in key_list:
                        info.append(user_list[index][key])
                elif field == 'origin_weibo_comment_brust_average':
                    info.append(user_list[index]['origin_weibo_comment_brust_average'])
                    for key in key_list:
                        info.append(user_list[index][key])
                else:
                    pass
                return_list.append(info)
                rank += 1
                count_c += 1

                if count_c >= int(number):
                    return return_list

def search_portrait_user(es, number, active_index, active_type, portrait_index, portrait_type, field="user_index"):

    return_list = []
    index_exist = es.indices.exists(index=active_index)
    if not index_exist:
        return "no active_index exist"
        sys.exit(0)

    count_s = 0
    count_c = 0
    start = 0
    rank = 1
    while 1:
        search_list = []
        user_list = search_k(es, active_index, active_type, start, field, 100)
        start += 100
        for item in user_list:
            if field == "vary":
                uid = item.get('uid', '0') # obtain uid, notice "uid" or "user"
            else:
                uid = item.get('user', '0')
            search_list.append(uid) # uid list

        search_result = es_portrait.mget(index=portrait_index, doc_type=portrait_type, body={"ids": search_list}, _source=True)["docs"]
        profile_result = es_profile.mget(index="weibo_user", doc_type="user", body={"ids": search_list}, _source=True)["docs"]

        for item in search_result:
            if item["found"]:
                info = ['','','','','','']
                info[0] = rank
                index = search_result.index(item)

                if profile_result[index]['found']:
                    info[1] = profile_result[index]['_source'].get('photo_url','')
                    info[3] = profile_result[index]['_source'].get('nick_name','')
                info[2] = search_result[index].get('_id','')
                info[4] = user_list[index][field]
                info[5] = "1"
                return_list.append(info)
                rank += 1
                count_c += 1

                if count_c >= int(number):
                    return return_list


def portrait_user_vary(es, number, active_index, active_type, portrait_index, portrait_type, field="vary"):

    return_list = []
    index_exist = es.indices.exists(index=active_index)
    if not index_exist:
        return "no active_index exist"
        sys.exit(0)

    count_s = 0
    count_c = 0
    start = 0
    rank = 1
    try:
        while 1:
            search_list = []
            user_list = search_k(es, active_index, active_type, start, field, 100)
            start += 100
            for item in user_list:
                uid = item.get('uid', '0') # obtain uid, notice "uid" or "user"
                search_list.append(uid) # uid list
            search_result = es_portrait.mget(index="user_portrait", doc_type="user", body={"ids": search_list}, _source=True)["docs"]
            profile_result = es_profile.mget(index="weibo_user", doc_type="user", body={"ids": search_list}, _source=True)["docs"]

            for item in search_result:
                count_c += 1
                if item["found"]:
                    info = ['','','','','','1']
                    info[0] = rank
                    index = search_result.index(item)

                    if profile_result[index]['found']:
                        info[1] = profile_result[index]['_source'].get('photo_url','')
                        info[3] = profile_result[index]['_source'].get('nick_name','')
                    info[2] = search_result[index].get('_id','')
                    info[4] = user_list[index]['vary']
                    return_list.append(info)
                    rank += 1
                    if rank == int(number)+1:
                        return return_list

            if count_c > 10000:
                break
    except RequestError:
        print "timeout"

    return return_list
if __name__ == "__main__":
    print search_portrait_user_in_activity(es, 2, "20130901", "bci", "user_index_profile", "manage")
