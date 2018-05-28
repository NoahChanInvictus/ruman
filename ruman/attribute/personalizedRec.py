# -*- coding:utf-8 -*-
'''
用户个性化推荐的后台相关计算模块
'''
__author__ = 'zxy'
import Queue
import codecs
import json
import os
import time
import jieba
import random
from collections import namedtuple

from elasticsearch.exceptions import NotFoundError
from ruman.attribute.influence_appendix import weiboinfo2url
from ruman.global_config import R_BEGIN_TIME
from ruman.parameter import DAY, HOUR
from ruman.parameter import RUN_TYPE, RUN_TEST_TIME
from ruman.parameter import topic_en2ch_dict
from ruman.time_utils import ts2datetime, datetime2ts
from ruman.zxy_params import \
    ADS_TOPIC_TFIDF_DIR, RIO_VIDEO_INFO_FILE, TIGER_VIDEO_INFO_FILE, CCTV_ITEM_FILE, CCTV_LIVE_VIDEO_FILE

from ads_classify import adsClassify
from ruman.global_utils import \
    es_flow_text, flow_text_index_name_pre, flow_text_index_type, \
    es_user_profile, profile_index_name, profile_index_type, \
    es_user_portrait, portrait_index_name, portrait_index_type, \
    es_ads_weibo, ads_weibo_index_name, ads_weibo_index_type
from ruman.global_utils import retweet_index_name_pre, retweet_index_type, es_retweet
from new_search import new_get_user_evaluate

def adsRec(uid, queryInterval=HOUR * 24):
    '''
    从广告表中读取当前时间点前一段时间queryInterval内的广微博，得到其中的广告部分
    然后根据用户的key_word信息得到推荐的广告。
    :param uid: 用户ID
    :param queryInterval: 查询之前多久的广告
    :return: 广告微博列表，按照相关度（感兴趣程度）排序
    '''

    # 运行状态，
    # 0 ->  当前为2013-9-8 00:00:00
    # 1 ->  当前时间
    now_date = ts2datetime(time.time()) if RUN_TYPE == 1 else ts2datetime(datetime2ts(RUN_TEST_TIME) - DAY)

    # 获取用户的偏好
    try:
        print uid
        user_portrait_result = es_user_portrait. \
            get_source(index=portrait_index_name, doc_type=profile_index_type, id=uid)
    except:
        return None

    user_key_words = set(user_portrait_result["keywords_string"].split("&"))

    # 直接从广告表中读取并计算
    ads_weibo_all = es_ads_weibo.search(index=ads_weibo_index_name,
                                        doc_type=ads_weibo_index_type,
                                        body={'query': {"filtered": {"filter": {
                                            "range": {"timestamp": {"gte": datetime2ts(now_date) - queryInterval}}}}},
                                            'size': 2000,
                                        }
                                        )['hits']['hits']


    random.shuffle(ads_weibo_all)
    ads_weibo_all = ads_weibo_all[:800]

    # 根据权重得到不同类别上词语的权重TFIDF
    topic_word_weight_dic = construct_topic_word_weight_dic(ADS_TOPIC_TFIDF_DIR)

    # 根据用户发微博的keywords得到用户在广告的topic上的分布
    # 因为已有的topic不太适合广告的分类
    user_topic_dic = construct_topic_feature_dic(user_key_words, topic_word_weight_dic)

    test_user_topic = {
        "3069348215": {u'\u5a31\u4e50': 10.0, u'\u751f\u6d3b': 14.0, u'\u4f53\u80b2': 1.0,
                        u'\u8d22\u7ecf': 0, u'\u6821\u56ed': 0, u'IT': 9.0, u'\u6c7d\u8f66': 1.0,
                        u'\u6e38\u620f\u52a8\u6f2b': 6.0, u'\u6559\u80b2': 2.0},
        "2218894100": {u'\u5a31\u4e50': 0, u'\u751f\u6d3b': 5.0, u'\u4f53\u80b2': 16.0,
                        u'\u8d22\u7ecf': 1.0, u'\u6821\u56ed': 0, u'IT': 0, u'\u6c7d\u8f66': 0,
                        u'\u6e38\u620f\u52a8\u6f2b': 0, u'\u6559\u80b2': 0},
        "1035933493": {u'\u5a31\u4e50': 0, u'\u751f\u6d3b': 10.0, u'\u4f53\u80b2': 17.0,
                        u'\u8d22\u7ecf': 0, u'\u6821\u56ed': 0, u'IT': 9.0, u'\u6c7d\u8f66': 8.0,
                        u'\u6e38\u620f\u52a8\u6f2b': 0, u'\u6559\u80b2': 2.0},
        }

    if uid in test_user_topic:
        user_topic_dic = test_user_topic[uid]



    # topics = [u"IT", u"体育", u"娱乐", u"教育", u"游戏动漫", u"生活", u"校园", u"生活", u"财经"]
    # for topic in topics:
    #     user_topic_dic[topic] = 1.0
    print user_topic_dic
    print "fuck"
    ads_weibo_prefer = adsPreferred(user_topic_dic, ads_weibo_all, topic_word_weight_dic, uid, 30)

    return ads_weibo_prefer


# 广告分类词的TF-IDF
def construct_topic_word_weight_dic(topic_word_weight_dir):
    topic_word_weight_dic = dict()
    # topic_word_weight_dir = topic_word_weight_dir.decode("ascii")
    for file_name in os.listdir(topic_word_weight_dir):
        # file_name = file_name.decode("utf-8")
        # print file_name
        weight_file = os.path.join(topic_word_weight_dir, file_name)
        # print weight_file
        if not os.path.isfile(weight_file):
            continue
        with codecs.open(weight_file, encoding="utf-8") as f:
            word_weight_dic = dict()
            for line in f.readlines():
                items = line.split(" ")
                word_weight_dic[items[0]] = float(items[1])
            # fix 2016.11.24 在上面将topic_word_weight_dir直接decode成Unicode
            # 使用Unicode路径listdir得到就直接为Unicode
            topic_word_weight_dic[file_name[:-4].decode("utf-8")] = word_weight_dic
    return topic_word_weight_dic


# user在广告topic上的preference
def construct_topic_feature_dic(words, topic_word_weight_dic):
    user_prefer_dic = dict()
    for (topic_name, word_weight_dic) in topic_word_weight_dic.items():
        user_prefer_dic[topic_name] = 0
        for word in words:
            if word in word_weight_dic:
                user_prefer_dic[topic_name] = user_prefer_dic[topic_name] + word_weight_dic[word]
    return user_prefer_dic


# 判断广告类别
def judge_ads_topic(words, topic_word_weight_dic):
    ads_feature_dic = construct_topic_feature_dic(words, topic_word_weight_dic)
    max_topic = u"IT"
    max_value = 0
    for (topic, value) in ads_feature_dic.items():
        if value > max_value:
            max_value = value
            max_topic = topic
    return max_topic


def adsPreferred(user_topic_dic, weibo_all, topic_word_weight_dic, sourceuid, k=30):
    '''
    :param user_topic: 用户的topic偏好
    :param weibo: weibo/ad_weibo列表
    :param topic_word_weight_dic: 不同类别下word的TFIDF权重值
    :return: 返回用户喜欢的k个广告微博
    '''
    adsPreferList = []
    weiboMap = dict()
    ads_midsPrefered = dict()
    # 微博用户的个人信息
    uids = set()

    # 这里的微博已经是ads
    for weibo in weibo_all:
        weiboSource = weibo["_source"]
        uids.add(weiboSource["uid"])
        mid = weiboSource["mid"]
        words = weiboSource["ads_keywords"]
        ads_topic = judge_ads_topic(list(jieba.cut(weiboSource["text"])), topic_word_weight_dic)
        weiboSource["ads_topic"] = ads_topic
        #print weiboSource["text"], ads_topic
        ads_midsPrefered[mid] = user_topic_dic[ads_topic]

        #  加上retweet和recomment的字段，适配非线上环境
        for keytobeadded in ['retweeted', 'comment']:
            if keytobeadded not in weiboSource.keys():
                weiboSource[keytobeadded] = 0
        weiboMap[mid] = weiboSource

    # 获取待选微博的用户信息
    weibo_user_profiles = search_user_profile_by_user_ids(uids)
    ads_midsPrefered = sorted(ads_midsPrefered.items(), key=lambda ads: ads[1], reverse=True)

    test_user_topic = {
        "2218894100": {u'\u5a31\u4e50': 0, u'\u751f\u6d3b': 5.0, u'\u4f53\u80b2': 16.0,
                       u'\u8d22\u7ecf': 1.0, u'\u6821\u56ed': 0, u'IT': 0, u'\u6c7d\u8f66': 0,
                       u'\u6e38\u620f\u52a8\u6f2b': 0, u'\u6559\u80b2': 0},
        "1035933493": {u'\u5a31\u4e50': 0, u'\u751f\u6d3b': 10.0, u'\u4f53\u80b2': 17.0,
                       u'\u8d22\u7ecf': 0, u'\u6821\u56ed': 0, u'IT': 9.0, u'\u6c7d\u8f66': 8.0,
                       u'\u6e38\u620f\u52a8\u6f2b': 0, u'\u6559\u80b2': 2.0},
    }

    if sourceuid in test_user_topic:
        print "ok"
    else:
        random.shuffle(ads_midsPrefered)

    k = min(k, len(ads_midsPrefered))

    for midInfo in ads_midsPrefered[:k]:
        mid = midInfo[0]
        uid = weiboMap[mid]["uid"]
        weiboMap[mid]["weibo_url"] = weiboinfo2url(uid, mid)
        # 可能出现许多userprofile查不到的情况
        if uid in weibo_user_profiles:
            weiboMap[mid]["photo_url"] = weibo_user_profiles[uid]["photo_url"]
            weiboMap[mid]["nick_name"] = weibo_user_profiles[uid]["nick_name"]
        else:
            weiboMap[mid]["photo_url"] = "None"
            weiboMap[mid]["nick_name"] = "None"
        adsPreferList.append(weiboMap[midInfo[0]])

    return adsPreferList


'''
下面是用户推荐的部分
'''


def personRec(uid, k=200):
    direct_attention_id_set = search_attention_id(uid, 1)
    user_used_set = direct_attention_id_set.copy()
    # 候选推荐
    candidate_attention_id_set = set()
    search_queue = Queue.Queue()
    for user_id in direct_attention_id_set:
        search_queue.put(user_id)

    while search_queue.not_empty and len(candidate_attention_id_set) < k:
        temp_uid = search_queue.get(block=False)
        user_attention = search_attention_id(temp_uid)
        for user_id in user_attention:
            if user_id not in candidate_attention_id_set and \
                            user_id not in direct_attention_id_set:
                candidate_attention_id_set.add(user_id)
                search_queue.put(user_id)

    candidate_attention_id_set = candidate_attention_id_set - direct_attention_id_set
    candidate_attention_user_profile = search_user_profile_by_user_ids(candidate_attention_id_set)
    # dict: {topic: user_id_set}
    user_recommend_dic = sim_user(uid, candidate_attention_id_set)
    user_recommend_return_list = []
    for topic_prefered, user_ids in user_recommend_dic.items():
        user_ids = user_ids & set(candidate_attention_user_profile.keys())
        for user_id in user_ids:
            temp_user_profile = candidate_attention_user_profile[user_id]
            temp_user_profile["topic"] = topic_en2ch_dict[topic_prefered]
            temp_user_profile["influence"] = new_get_user_evaluate(user_id)["influence"][0]
            if user_id == "1223178222":
                temp_user_profile["influence"] = 100.00
            if user_id == "1191258123":
                temp_user_profile["influence"] = 100.00
            user_recommend_return_list.append(temp_user_profile)

    return user_recommend_return_list


def sim_user(uid, candidate_attention_id_set):
    user_portrait = es_user_portrait. \
        get_source(index=portrait_index_name, doc_type=profile_index_type, id=uid)

    candidate_attention_user_portraits = search_user_portrait_by_user_ids(candidate_attention_id_set)

    # user_topic = sorted(json.loads(user_portrait["topic"]).items(), key=lambda x: x[1])
    user_prefer_topic_list = map(lambda x: x[0],
                                 sorted(json.loads(user_portrait["topic"]).items(),
                                        key=lambda x: x[1],
                                        reverse=True)[:4])
    user_prefer_dict = dict()
    for temp_topic in user_prefer_topic_list:
        user_prefer_dict[temp_topic] = set()
    # map(lambda x: user_prefer_dict.setdefault(set()), user_prefer_topic_list)

    for temp_uid, temp_portrait in candidate_attention_user_portraits.items():
        temp_topics = sorted(json.loads(temp_portrait["topic"]).items(), key=lambda x: x[1], reverse=True)
        for temp_topic in temp_topics:
            if temp_topic[0] in user_prefer_dict:
                user_prefer_dict[temp_topic[0]].add(temp_uid)
                break

    return user_prefer_dict


def search_attention_id(uid, k=30):
    now_ts = time.time()
    db_number = get_db_num(now_ts)
    index_name = retweet_index_name_pre + str(db_number)
    try:
        retweet_result = es_retweet.get(index=index_name, doc_type=retweet_index_type, id=uid)['_source']
    except:
        return set()
    if retweet_result:
        retweet_dict = json.loads(retweet_result['uid_retweet'])
        return set(retweet_dict.keys())


def get_db_num(timestamp):
    date = ts2datetime(timestamp)
    date_ts = datetime2ts(date)
    r_beigin_ts = datetime2ts(R_BEGIN_TIME)
    db_number = ((date_ts - r_beigin_ts) / (DAY * 7)) % 2 + 1
    # run_type
    if RUN_TYPE == 0:
        db_number = 1
    return db_number


def search_user_portrait_by_user_ids(users):
    users = list(users)
    user_portrait_return = dict()
    try:
        candidate_attention_user_portraits = es_retweet.mget(index=portrait_index_name,
                                                             doc_type=portrait_index_type,
                                                             body={'ids': list(users)})['docs']
    except:
        candidate_attention_user_portraits = []

    for out_user_item in candidate_attention_user_portraits:
        if out_user_item['found']:
            uid = out_user_item['_id']
            user_portrait_return[uid] = out_user_item['_source']
    return user_portrait_return


def search_user_profile_by_user_ids(users):
    users = list(users)
    user_profile_return = dict()
    try:
        user_result = es_user_profile.mget(index=profile_index_name,
                                           doc_type=profile_index_type,
                                           body={'ids': users})['docs']
    except:
        user_result = []

    for out_user_item in user_result:
        if out_user_item['found']:
            uid = out_user_item['_id']
            user_profile_return[uid] = out_user_item['_source']
    return user_profile_return


# 本地的新闻微推荐，先获取本地微博
def localRec(uid, queryInterval=HOUR*25*7, k=200):
    # 运行状态，
    # 0 ->  当前为2016-11-28 00:00:00
    # 1 ->  当前时间
    now_timestamp = datetime2ts(ts2datetime(time.time()))
    if RUN_TYPE == 0:
        now_timestamp = datetime2ts(RUN_TEST_TIME)

    flow_text_index_list = []
    for i in range(7, 0, -1):
        iter_date = ts2datetime(now_timestamp - DAY * i)
        flow_text_index_list.append(flow_text_index_name_pre + iter_date)

    # 获取用户地理位置
    # user_geos = get_user_geo(uid)
    # # 根据位置查询weibo
    # weibo_all = es_flow_text.search(index=flow_text_index_list, doc_type=ads_weibo_index_type,
    #                                 body={"query":{"bool":{"must":
    #                                                                 [{"match":{"keywords_string":"新闻"}},
    #                                                                  {"match":{"geo":"合肥"}}
    #                                                                  ]}},
    #                                            "size": 200
    #                                       })["hits"]["hits"]

    '''可以直接查询长度大于100的但是很慢
    {"query":{"filtered":{"query":{"bool":{"must":[{"match":{"keywords_string":"新闻"}},{"match":{"geo":"合肥"}}]}},"filter":{"regexp":{"text":{"value":".{100,}"}}}}}}
    '''
    ip = get_user_ip(uid)
    ip = ".".join(ip.split(".")[:-2])
    print '326'
    weibo_all = es_flow_text.search(index=flow_text_index_list, doc_type=ads_weibo_index_type,
                                    body={"query": {"bool": {"must": [{"prefix": {"text.ip": ip}}]}},
                                          "size": 2000})["hits"]["hits"]

    local_weibo_rec = []
    weibo_user_uids = [weibo["_source"]["uid"] for weibo in weibo_all]
    print '332',len(weibo_all)
    # user_profiles = search_user_profile_by_user_ids(weibo_user_uids)
    exists_ip = set()
    topic_word_weight_dic = construct_topic_word_weight_dic(ADS_TOPIC_TFIDF_DIR)
    for weibo in weibo_all:
        weibo = weibo["_source"]
        weibo_text = weibo["text"]
        if weibo["ip"] in exists_ip:
            continue
        # 一个ip只选一个
        exists_ip.add(weibo["ip"])
        if not is_suit(weibo_text):
            continue
        weibo["len"] = len(weibo_text)
        try:
            mid = weibo["mid"]
            uid = weibo["uid"]
        except:
            continue
        weibo["weibo_url"] = weiboinfo2url(uid, mid)
        weibo["weibo_topic"] = judge_ads_topic(list(jieba.cut(weibo_text)), topic_word_weight_dic)
        # 可能出现许多userprofile查不到的情况
        # if uid in user_profiles:
        #     weibo["photo_url"] = user_profiles[uid]["photo_url"]
        #     weibo["nick_name"] = user_profiles[uid]["nick_name"]
        # else:
        #     weibo["photo_url"] = "None"
        #     weibo["nick_name"] = "None"
        #     local_weibo_rec.append(weibo)
        local_weibo_rec.append(weibo)
    return local_weibo_rec


# 根据微博的text判断微博是否展示效果比较好
def is_suit(weibo_text):
    if len(weibo_text) < 50:
        return False
    if weibo_text.count('@') > 2:
        return False
    if weibo_text.find("@") < 10:
        return False
    return True


# 如果user portrait中有就直接读取，否则读取用户微博得到位置信息
def get_user_geo(uid, dropped_geos=u"中国&美国"):
    """
    :param uid: 用户的id
    :param dropped_geos: &分割的地点，因为geo中都包含中国
    :return: geo 位置的set
    """
    dropped_geos = set(dropped_geos.split("&"))
    # 获取用户的偏好
    try:
        user_portrait_result = es_user_portrait. \
            get_source(index=portrait_index_name, doc_type=profile_index_type, id=uid)
    except NotFoundError:
        user_portrait_result = None

    # portrait表中存在geo信息
    if user_portrait_result and len(user_portrait_result["activity_geo"]) > 0:
        geos = user_portrait_result["activity_geo"] - dropped_geos

    # 不存在geo信息，获取之前发去的微博提取
    else:
        flow_text_index_list = []
        now_timestamp = datetime2ts(ts2datetime(time.time()))
        if RUN_TYPE == 0:
            now_timestamp = datetime2ts(RUN_TEST_TIME)
        for i in range(7, 0, -1):
            iter_date = ts2datetime(now_timestamp - DAY * i)
            flow_text_index_list.append(flow_text_index_name_pre + iter_date)

        weibo_all = es_flow_text.search(index=flow_text_index_list,
                                        doc_type=flow_text_index_type,
                                        body={'query': {'filtered': {'filter': {'term': {'uid': uid}}}},
                                              'size': 2000,
                                              })['hits']['hits']
        geos = set()
        for temp in weibo_all:
            geos |= set(temp["_source"]["geo"].split("&"))

    return geos


def get_user_ip(uid):
    flow_text_index_list = []
    now_timestamp = datetime2ts(ts2datetime(time.time()))
    if RUN_TYPE == 0:
        now_timestamp = datetime2ts(RUN_TEST_TIME)
    for i in range(7, 0, -1):
        iter_date = ts2datetime(now_timestamp - DAY * i)
        flow_text_index_list.append(flow_text_index_name_pre + iter_date)

    weibo_all = es_flow_text.search(index=flow_text_index_list,
                                    doc_type=flow_text_index_type,
                                    body={'query': {'filtered': {'filter': {'term': {'uid': uid}}}},
                                          'size': 10,
                                          })['hits']['hits']
    ip = weibo_all[0]["_source"]["ip"]
    return ip


# 视频节目推荐，分为rio和tiger，每个k个
def cctv_video_rec(uid, k=10):
    flow_text_index_list = []
    now_timestamp = datetime2ts(ts2datetime(time.time()))
    if RUN_TYPE == 0:
        now_timestamp = datetime2ts(RUN_TEST_TIME)
    for i in range(7, 0, -1):
        iter_date = ts2datetime(now_timestamp - DAY * i)
        flow_text_index_list.append(flow_text_index_name_pre + iter_date)

    weibo_all = es_flow_text.search(index=flow_text_index_list,
                                    doc_type=flow_text_index_type,
                                    body={'query': {'filtered': {'filter': {'term': {'uid': uid}}}},
                                          'size': 100,
                                          })['hits']['hits']
    user_words = set()
    for weibo in weibo_all:
        weibo_text = weibo["_source"]["text"]
        user_words |= set(jieba.cut(weibo_text))

    rio_dict = load_topic_video_dict(RIO_VIDEO_INFO_FILE)
    tiger_videos = load_videos(TIGER_VIDEO_INFO_FILE)

    ret_dict = dict()
    ret_dict["tiger"] = random.sample(tiger_videos, k)

    user_pref_topic = set(rio_dict.keys()) & user_words
    # 若找不到，随机分配topic
    if len(user_pref_topic) == 0:
        user_pref_topic = set(random.sample(rio_dict.keys(), k))
    ret_dict["rio"] = list()
    for topic in user_pref_topic:
        ret_dict["rio"].extend(rio_dict[topic])
        if len(ret_dict["rio"]) >= k:
            ret_dict["rio"] = ret_dict["rio"][:k]
            break
    return ret_dict


def load_topic_video_dict(filepath):
    ret_dict = dict()
    with open(filepath) as f:
        lines = f.readlines()
    for line in lines:
        words = line.strip().split("||")
        ret_dict[words[0]] = words[1].split(",")
    return ret_dict


def load_videos(filepath):
    ret_set = set()
    with open(filepath) as f:
        lines = f.readlines()
    for line in lines:
        ret_set.add(line.strip().split("||")[1])
    return ret_set


# cctv的直播节目推荐
def cctv_live_video_rec(uid):
    # 获取推荐的视频列表, 还是直接返回
    rec_video_dict = cctv_video_rec(uid, 20)
    rec_video_list = [] + rec_video_dict["rio"] + rec_video_dict["tiger"]
    random.shuffle(rec_video_list)

    # 载入视频信息
    # 10840000000||CCTV新闻频道||东方时空精切||53
    video_info_dict = dict()
    attrs = namedtuple("attrs", ["channel", "title", "duration"])
    with open(CCTV_LIVE_VIDEO_FILE) as f:
        for line in f.readlines():
            videoID, channel, title, duration = line.split("||")
            video_info_dict[videoID] = attrs(channel, title, int(duration))

    # 堆成返回的直播格式
    live_video_ret = []

    # HumanTime类，用于将秒数转换成hour:minute的时间
    class HumanTime:
        def __init__(self, start_time = 0):
            self._now_second = start_time

        # 将秒数补全至整数分钟
        def _add_to_integer_minute(self):
            if self._now_second%60 == 0:
                return
            else:
                self._now_second += (60-self._now_second%60)

        def __iadd__(self, other):
            self._now_second += other
            self._add_to_integer_minute()
            return self

        @property
        def formatted(self):
            time = self._now_second
            hour = str(time / 3600)
            if len(hour) == 1: hour = "0" + hour
            time %= 3600
            minute = str(time / 60)
            if len(minute) == 1: minute = "0" + minute
            return hour + ":" + minute

        @property
        def finished(self):
            if self._now_second>3600*24:
                return True
            else:
                return False

    start_time = HumanTime()
    for videoID in rec_video_list:
        video_attrs = video_info_dict[videoID]
        live_video_ret.append({"videoID": videoID,
                               "start_time": start_time.formatted,
                               "channel": video_attrs.channel,
                               "title": video_attrs.title})
        start_time += video_attrs.duration
        if start_time.finished:
            break

    # 推荐的不够，补齐
    rec_video_set = set(rec_video_list)
    if start_time < 24*3600:
        for videoID in video_info_dict.keys():
            if videoID not in rec_video_set:
                video_attrs = video_info_dict[videoID]
                live_video_ret.append({"videoID": videoID,
                                       "start_time": start_time.formatted,
                                       "channel": video_attrs.channel,
                                       "title": video_attrs.title})
                start_time += video_attrs.duration
                if start_time.finished:
                    break

    return live_video_ret

# cctv的商品推荐
def cctv_item_rec(uid, k=10):
    random.seed(int(uid))
    item_set = load_items(CCTV_ITEM_FILE)
    return random.sample(item_set, k)


def load_items(filepath):
    with open(filepath) as f:
        lines = f.readlines()
    item_set = set(map(lambda line: line.strip(), lines))
    return item_set


if __name__ == '__main__':
    uid = 1640601392
    result = adsRec(uid)
    for rr in result:
        print(rr)
