#-*-coding=utf-8-*-

import os
import re
import sys
import json
import csv
import heapq
import scws
import time
from decimal import *
from global_utils_do import txt_labels,DOMAIN_DICT,DOMAIN_COUNT,LEN_DICT,TOTAL,DOMAIN_P

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

def rank_dict(has_word):

    n = len(has_word)
    keyword = TopkHeap(n)
    count = Decimal(0)
    for k,v in has_word.iteritems():
        keyword.Push((v,k))
        count = count + Decimal(v)

    if count > 0:
        keyword_data = keyword.TopK()
        label = txt_labels[txt_labels.index(keyword_data[0][1])]
    else:
        label = 'other'
        keyword_data = keyword.TopK()
    return label,keyword_data

def domain_classfiy_by_text(user_weibo):#根据用户微博文本进行领域分类
    '''
    输入数据：字典
    {uid:{'key1':f1,'key2':f2...},...}
    输出数据：字典
    {uid:label1,uid2:label2,...}
    '''

    result_data = dict()
    p_data = dict()
    for k,v in user_weibo.items():
        start = time.time()
        domain_p = DOMAIN_P
        for d_k in domain_p.keys():
            domain_p[d_k] = com_p(v,DOMAIN_DICT[d_k],DOMAIN_COUNT[d_k],LEN_DICT[d_k],TOTAL)#计算文档属于每一个类的概率
            end_time = time.time()
        label,rank_data = rank_dict(domain_p)
        result_data[k] = label
        p_data[k] = rank_data

    return result_data,p_data
    
