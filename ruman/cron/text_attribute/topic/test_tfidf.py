#-*-coding=utf-8-*-

import os
import time
import csv
import heapq
import re
import math
from decimal import *
from config import DOMAIN_DICT_ORI,DOMAIN_COUNT_ORI,abs_path

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

def cal_idf(word,domain_dict,domain_count,topic):

    idf_word = 0
    idf_count = 0
    for k,v in domain_dict.items():
        if k != topic:
            if v.has_key(word):
                idf_word = idf_word + v[word]
                idf_count = domain_count[k]

    if idf_word  == 0 or idf_count == 0:
        idf = 1
    else:
        idf = - math.log(Decimal(idf_word)/Decimal(idf_count),2)

    return idf
    
def main():

    weight = dict()
    for k,v in DOMAIN_DICT_ORI.items():
        weight_dict = dict()
        for k1,v1 in v.items():
            tf = Decimal(v1)/Decimal(DOMAIN_COUNT_ORI[k])
            idf = cal_idf(k1,DOMAIN_DICT_ORI,DOMAIN_COUNT_ORI,k)
            weight_dict[k1] = Decimal(tf)*Decimal(idf)
        weight[k] = weight_dict

    return weight,domain_dict    

def rank_tfidf(word_dict):

    n = int(len(word_dict)*0.8)
    keyword = TopkHeap(n)

    for k,v in word_dict.items():
        keyword.Push((v,k))

    keyword_data = keyword.TopK()

    return keyword_data

def write_file(result_data,name,domain_dict):

    data = rank_tfidf(result_data)
    
    with open('%s/topic_dict/%s_tfidf.csv' % (abs_path,name), 'wb') as f:
        writer = csv.writer(f)
        for i in range(0,len(data)):
            writer.writerow((domain_dict[data[i][1]],data[i][1]))

    return len(data)

if __name__ == '__main__':
    
    result_data,domain_dict = main()
##    count = 0
##    for k,v in result_data.items():
##        n = write_file(v,k,domain_dict[k])
##        count = count + n
##
##    print count

    print result_data







        
