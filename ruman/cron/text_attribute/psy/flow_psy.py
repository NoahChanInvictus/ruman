#-*-coding=utf-8-*-

import os
import time
import csv
import scws
import re
import heapq
from config import re_cut,DS_DICT,DS_COUNT,s_label
#from test_data import input_data2 #测试输入

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

def start_p(data_time):

    domain_p = dict()
    for name in data_time:
        domain_p[name] = 0

    return domain_p

def find_label(text,ds_dict,ds_count):
    #change text type from unicode to utf-8
    text = text.encode('utf-8')
    s_data = ['anger','anx','sad']#第二层分类标签
    domain_s = start_p(s_data)

    for d_k,d_v in ds_dict.iteritems():
        domain_s[d_k] = sum([text.count(v) for v in d_v])

    max_s = 0
    label_s = 'other'
    for k1,v1 in domain_s.iteritems():
        domain_s[k1] = float(v1)/float(ds_count[k1])
        if domain_s[k1] > max_s:
            max_s = domain_s[k1]
            label_s = k1

    return label_s

def flow_psychology_classfiy(text):#心理状态分类主函数

    w_text = re_cut(text)
    if len(w_text):#非空
        label = find_label(w_text,DS_DICT,DS_COUNT)
    else:
        label = 'other'
    
    return label

if __name__ == '__main__':
    uid_weibo = input_data2()
    start = time.time()
    for text in uid_weibo:
        domain = psychology_classfiy(text)
    end = time.time()
    print '%s seconds...' % (end-start)
    
