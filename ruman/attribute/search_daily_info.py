# -*- coding: utf-8 -*-

"""
return basic attribute: origin/retweeted weibo number, origin/retweeted weibo\
        retweeted/comment total/average/top number/mid, fans number

"""

import sys
from elasticsearch import Elasticsearch
from search_daily_basic_info import search_weibo_behavior

def search_origin_attribute(user_index, uid, doc_type="bci"):

    origin_weibo_iter_keys = ['origin_weibo_retweeted_average_number', 'origin_weibo_top_comment_id', 'origin_weibo_comment_top_number', \
        'origin_weibo_retweeted_total_number', 'origin_weibo_top_retweeted_id', 'origin_weibo_comment_average_number', \
        'origin_weibo_retweeted_top_number','origin_weibo_number', 'origin_weibo_comment_total_number']

    user_info = search_weibo_behavior(user_index, uid)
    basic_attribute = {}

    if not user_info:
        return basic_attribute

    for key in origin_weibo_iter_keys:
        basic_attribute[key] = user_info[key]

    return basic_attribute


def search_retweeted_attribute(user_index, uid, doc_type="bci"):

    retweeted_weibo_iter_keys = ['retweeted_weibo_number', 'retweeted_weibo_top_retweeted_id', 'retweeted_weibo_comment_top_number', \
            'retweeted_weibo_retweeted_total_number', 'retweeted_weibo_retweeted_average_number', 'retweeted_weibo_top_comment_id',\
            'retweeted_weibo_comment_average_number', 'retweeted_weibo_retweeted_top_number', 'retweeted_weibo_comment_total_number']

    user_info = search_weibo_behavior(user_index, uid)
    basic_attribute = {}

    if not user_info:
        return basic_attribute

    for key in retweeted_weibo_iter_keys:
        basic_attribute[key] = user_info[key]

    return basic_attribute

def search_user_index(user_index, uid, doc_type="bci"):


    user_info = search_weibo_behavior(user_index, uid)
    activity_attribute = {}

    if not user_info:
        return activity_attribute
    else:
        activity_attribute["user_index"] = user_info["user_index"]

    return activity_attribute



if __name__ == "__main__":

    print search_origin_attribute("20130901", "1713926427")

