# -*- coding = utf-8 -*-

import math
import datetime
import time
import sys
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError
from ruman.global_utils import ES_CLUSTER_FLOW1
from ruman.global_utils import es_user_profile as es_profile
from ruman.global_utils import es_user_portrait as es_portrait

es = ES_CLUSTER_FLOW1
index_name = "vary"
doctype = "bci"

# generate a time period with format 20130901, 20130902 
def generate_date(former_date, later_date="21000101"):
    date_list = []
    date_list.append(former_date)
    former_struct = datetime.date(int(former_date[0:4]), int(former_date[4:6]), int(former_date[6:]))
    later_struct = datetime.date(int(later_date[0:4]), int(later_date[4:6]), int(later_date[6:]))
    former_timestamp = time.mktime(former_struct.timetuple())
    later_timestamp = time.mktime(later_struct.timetuple())
    i=1

    next_timestamp = former_timestamp
    while 1:
        print next_timestamp, later_timestamp
        next_timestamp += 86400
        if next_timestamp <= later_timestamp:
            date_list.append(time.strftime('%Y%m%d',time.localtime(next_timestamp)))
            i += 1
            if i == 7:
                break
        else:
            break

    return date_list


# return specified uid vary 

def search_history_index(uid, index_name, doctype, start_date, end_date):
    # date.formate: 20130901
    try:
        result = es.get(index=index_name, doc_type=doctype, id=uid, _source=True)['_source']
    except NotFoundError:
        return NotFound
    return result


"""
return vary top_k

"""

def query_vary_top_k(index_name, doctype, top_k, sort_index="vary"):
    query_body = {
        "query": {
            "match_all": {}
        },
        "size": top_k,
        "sort": [{sort_index: {"order": "desc"}}]
    }

    result = es.search(index=index_name, doc_type=doctype, body=query_body)['hits']['hits']
    uid_list = []
    for item in result:
        uid_list.append(item['_id'])

    portrait_result = es_portrait.mget(index="user_portrait", doc_type="user", body={"ids":uid_list}, _source=True)['docs']
    profile_result = es_profile.mget(index="weibo_user",doc_type="user", body={"ids":uid_list}, _source=True)['docs']

    return_list = []
    rank = 1
    for i in range(len(result)):
        info = ['','','','','']
        info[0] = rank
        if profile_result[i]['found']:
            info[1] = profile_result[i]['_source'].get('photo_url','')
            info[3] = profile_result[i]['_source'].get('nick_name','')
        info[2] = result[i].get('_id','')
        info[4] = result[i]['_source']['vary']
        if portrait_result[i]['found']:
            info.append('1')
        else:
            info.append('0')
        return_list.append(info)
        rank += 1

    return return_list


if __name__ == "__main__":
    print search_history_index('1990921871', index_name, doctype, '20130901', '20130904')
    print query_vary_top_k("vary", "bci", 10, "vary")
