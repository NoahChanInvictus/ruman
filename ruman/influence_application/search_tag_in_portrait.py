# -*- coding = utf-8 -*-

import sys
from elasticsearch import Elasticsearch
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

from rank_portrait_in_active_user import search_k


def search_tag(es, number, active_index, active_type, portrait_index, portrait_type, tag):

    #field_dict = {"domain":"art"}
    return_list = []
    count_s = 0
    count_c = 0
    start = 0
    rank = 1

    while 1:
        search_list = []
        user_list = search_k(es, active_index, active_type, start, "user_index", 10000)
        start += 10000
        for item in user_list:
            uid = item.get('user', '0')
            search_list.append(uid) # uid list

        search_result = es_portrait.mget(index=portrait_index, doc_type=portrait_type, body={"ids": search_list}, _source=True)["docs"]
        profile_result = es_profile.mget(index="weibo_user", doc_type="user", body={"ids": search_list}, _source=True)["docs"]
        for item in search_result:
            count_s += 1
            if item['found'] and tag in item['_source']['domain']:
                info = ['','','','','','','']
                info[0] = rank
                index = search_result.index(item)

                if profile_result[index]['found']:
                    info[1] = profile_result[index]['_source'].get('photo_url','')
                    info[3] = profile_result[index]['_source'].get('nick_name','')
                info[2] = search_result[index].get('_id','')
                info[4] = user_list[index]['user_index']
                info[5] = search_result[index]['_source'].get('activeness','')
                info[6] = search_result[index]['_source'].get('importance','')

                rank += 1
                return_list.append(info)

                if rank >= int(number)+1:
                   return return_list

        if count_s > 100000:
            return return_list



