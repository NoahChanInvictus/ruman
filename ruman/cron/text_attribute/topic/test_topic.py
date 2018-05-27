#-*- coding: UTF-8 -*-

import os
import sys
import time
import csv
import heapq
import copy
import random
from decimal import *
from config import abs_path,DOMAIN_DICT,DOMAIN_COUNT,LEN_DICT,TOTAL,name_list,TOPIC_DICT
#from test_data import input_data #测试输入

class TopkHeap(object):
    def __init__(self, k):
        self.k = k
        self.data = []
 
    def Push(self, elem):
        if len(self.data) < self.k:
            heapq.heappush(self.data, elem)
        else:
            topk_small = self.data[0][0]
            if elem[0] > topk_small:
                heapq.heapreplace(self.data, elem)
 
    def TopK(self):
        return [x for x in reversed([heapq.heappop(self.data) for x in xrange(len(self.data))])]

def com_p(word_list,domain_dict,domain_count,len_dict,total):

    p = 0
    test_word = set(word_list.keys())
    train_word = set(domain_dict.keys())
    c_set = test_word & train_word
    p = sum([float(domain_dict[k]*word_list[k])/float(domain_count) for k in c_set])

    return p

def load_weibo(uid_weibo):

    result_data = dict()
    p_data = dict()
    for k,v in uid_weibo.iteritems():
        domain_p = TOPIC_DICT
        for d_k in domain_p.keys():
            domain_p[d_k] = com_p(v,DOMAIN_DICT[d_k],DOMAIN_COUNT[d_k],LEN_DICT[d_k],TOTAL)#计算文档属于每一个类的概率
            #end_time = time.time()
        #print 'domain_p',k,domain_p
        result_data[k] = copy.deepcopy(domain_p)
        p_data[k] = rank_result(domain_p)
        
    return result_data,p_data

def rank_dict(has_word):

    n = len(has_word)
    keyword = TopkHeap(n)
    count = 0
    for k,v in has_word.iteritems():
        keyword.Push((v,k))
        count = count + v

    keyword_data = keyword.TopK()
    return keyword_data,count    

def rank_result(domain_p):
    
    data_v,count = rank_dict(domain_p)
    if count == 0:
        uid_topic = ['life']
    else:
        uid_topic = [data_v[0][1],data_v[1][1],data_v[2][1]]

    return uid_topic

def topic_classfiy(uid_list,uid_weibo):#话题分类主函数
    '''
    用户话题分类主函数
    输入数据示例：
    uidlist:uid列表（[uid1,uid2,uid3,...]）
    uid_weibo:分词之后的词频字典（{uid1:{'key1':f1,'key2':f2...}...}）

    输出数据示例：字典
    用户18个话题的分布：
    {uid1:{'art':0.1,'social':0.2...}...}
    用户关注较多的话题（最多有3个）：
    {uid1:['art','social','media']...}
    '''
    if not len(uid_weibo) and len(uid_list):
        result_data = dict()
        uid_topic = dict()
        for uid in uid_list:
            result_data[uid] = TOPIC_DICT
            uid_topic[uid] = ['life']
        return result_data,uid_topic
    elif len(uid_weibo) and not len(uid_list):
        uid_list = uid_weibo.keys()
    elif not len(uid_weibo) and not len(uid_list):
        result_data = dict()
        uid_topic = dict()
        return result_data,uid_topic
    else:
        pass        
        
    result_data,uid_topic = load_weibo(uid_weibo)#话题分类主函数

    for uid in uid_list:
        if not result_data.has_key(uid):
            result_data[uid] = TOPIC_DICT
            uid_topic[uid] = ['life']
    
    return result_data,uid_topic


if __name__ == '__main__':

    #uid_list,uid_weibo = input_data()
    uid_list=[3069348215]
    #uid_weibo = {3069348215:{u'\u7b97\u4e86': 3, u'\u665a\u5b89': 4, u'\u5f55\u5236': 4, u'\u7b11': 7, u'\u8303\u51b0\u51b0': 3, u'\u7d2f': 3, u'\u644a\u624b': 25, u'\u72ee\u5b50': 4, u'\u5904\u5973\u5ea7': 10, u'\u5df2\u7ecf': 3, u'\u91d1\u725b\u5ea7': 3, u'\u53d1\u5fae': 4, u'\u5389\u5bb3': 3, u'\u62bd\u5956': 6, u'\u751f\u6d3b': 4, u'\u54d2\u54d2': 3, u'\u4e00\u4e2a': 7, u'doge': 18, u'\u5154\u5b50': 3, u'\u72ee\u5b50\u5ea7': 4, u'\u53cc\u5b50': 6, u'\u5fc3\u75bc': 3, u'\u661f\u5ea7': 9, u'\u767d\u7f8a': 6, u'\u89c6\u9891': 10, u'\u5fc3': 16, u'\u6b63\u7ecf': 3, u'\u5c04\u624b': 5, u'\u62dc\u62dc': 12, u'\u6240\u6709': 4, u'\u6d41\u91cf': 4, u'\u5410\u69fd': 7, u'\u6ca1\u9519': 3, u'\u4e00\u672c': 3, u'\u4e0d\u7231': 4, u'\u53eb\u505a': 3, u'\u6469\u7faf': 9, u'\u5fae\u7b11': 15, u'\u54c8\u54c8\u54c8\u54c8': 4, u'\u5c0f\u91ce\u59b9\u5b50': 4, u'\u8fd9\u662f': 5, u'\u6c34\u74f6': 8, u'\u91d1\u725b': 10, u'\u54ed': 5, u'\u70ed\u95e8': 4, u'\u55b5\u55b5': 3, u'\u559c\u6b22': 3, u'\u9177': 3, u'\u54c8\u54c8\u54c8': 24, u'\u5904\u5973': 5}}
    uid_weibo = {3069348215:{"摊手":25,"哈哈哈":24,"doge":18,"心":16,"微笑":15,"拜拜":12,"视频":10,"金牛":10,"处女座":10,"摩羯":9,"星座":9,"水瓶":8,"吐槽":7,"笑":7,"一个":7,"双子":6,"白羊":6,"抽奖":6,"哭":5,"这是":5,"处女":5,"射手":5,"生活":4,"哈哈哈哈":4,"狮子":4,"流量":4,"录制":4,"狮子座":4,"所有":4,"热门":4,"晚安":4,"小野妹子":4,"不爱":4,"发微":4,"哒哒":3,"叫做":3,"金牛座":3,"心疼":3,"兔子":3,"没错":3,"累":3,"范冰冰":3,"喜欢":3,"正经":3,"一本":3,"厉害":3,"喵喵":3,"算了":3,"酷":3,"已经":3}}
    result_data,uid_topic = topic_classfiy(uid_list,uid_weibo)
    print result_data
    print uid_topic







        
