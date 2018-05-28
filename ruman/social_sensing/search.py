# -*- coding:utf-8 -*-

import sys
import time
import json
import pynlpir
pynlpir.open()
from aggregation_weibo import aggregation_sensor_keywords
reload(sys)
sys.path.append("./../")
from global_utils import es_flow_text as es_text
from global_utils import es_user_profile as es_profile
from global_utils import es_user_portrait
from time_utils import ts2datetime, datetime2ts
from global_utils import flow_text_index_name_pre, flow_text_index_type, profile_index_name, profile_index_type, \
                         portrait_index_name, portrait_index_type

# based on nick_name search group
# postname--nickname后缀
def search_specified_group(postname="报"):
    query_body = {
        "query":{
            "bool": {
                "must": [
                    {"wildcard": {
                        "uname": {
                            "wildcard": "*" + postname
                        }
                    }},
                    {"range": {
                        "fansnum": {
                            "gte": 100000
                        }
                    }}
                ]
            }
        },
        "size": 10000
    }

    search_results = es_profile.search(index="user_portrait_1222", doc_type="user", body=query_body)["hits"]["hits"]
    uid_list = []
    for item in search_results:
        uid_list.append(item['_id'])
        print item['_id'], item['_source']['uname'], '\n'
    print "该群体有：", len(uid_list)
    return uid_list


# select top influence users as social sensor based on domain and topic
# search in user_portrait
def filter_top_influence_user(index_name, domain=[], topic=[], size=1000, influence=0):
    query_body = {
        "query": {
            "filtered":{
                "filter": {
                    "bool": {
                        "must": [
                            #{"terms": {"topic_string": topic}},
                            #{"terms": {"domain": domain}},
                            {"range": {
                                "influence": {
                                    "gte": influence
                                }
                            }}
                        ]
                    }
                }
            }
        },
        "sort": {"influence": {"order": "desc"}},
        "size": size
    }

    if domain:
        query_body["query"]["filtered"]["filter"]["bool"]["must"].append({"terms": {"domain": domain}})
    if topic:
        query_body["query"]["filtered"]["filter"]["bool"]["must"].append({"terms": {"topic_string": topic}})

    search_results = es_user_portrait.search(index=portrait_index_name, doc_type=portrait_index_type, body=query_body)["hits"]["hits"]
    uid_list = []
    for item in search_results:
        uid_list.append(item['_id'])

    print len(uid_list)
    return uid_list


if __name__ == "__main__":
    """
    s = "2014年6月30我们冒雨上访，警方迅速出动200警力“维稳”并将村民代表马维真和喇学良带走，称:马维真因吸毒需强制戒毒两年。PS:小样，看你们还敢上访！@甘肃发布 [威武]@临夏发布 [威武]@临夏公安[威武] 让我们一起为临夏警方迅速处置”恐怖分子”点赞，我们很多村民微博被封号，又是马仲山带队抓人。"
    pynlpir.segment(s, pos_tagging=False)
    print pynlpir.get_key_words(s)
    """
    media_list = search_specified_group()
    print media_list
    #media_list = filter_top_influence_user("user_portrait_1222", ["活跃人士","草根","媒体"], ["经济类","民生_就业类"], 100)
    """
    query_body = aggregation_sensor_keywords(1378557829, 1378557829+100000, media_list, "keywords_string", 50)
    search_results = es_text.search(index="flow_text_2013-09-07", doc_type="text", body=query_body)['aggregations']['all_keywords']['buckets']
    print search_results
    for item in search_results:
        print item["key"].encode("utf-8", "ignore"), item["doc_count"], "\n"
    """


