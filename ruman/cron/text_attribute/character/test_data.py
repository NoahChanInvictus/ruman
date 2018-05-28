#-*-coding=utf-8-*-
#vision2
import os
import re
import sys
import json
import csv
import time
import datetime
from global_utils_ch import abs_path
from config import load_scws

def input_data(name):#测试输入

    uid_list = []
    reader = csv.reader(file(abs_path + '/weibo_data/0122_uid.txt', 'rb'))
    for line in reader:
        uid = line[0].strip('\t\r\n')
        uid = uid.strip('\xef\xbb\xbf')
        uid_list.append(uid)

    uid_weibo = dict()
    sw = load_scws()
    reader = csv.reader(file(abs_path + '/test_weibo/com_weibo0126.csv', 'rb'))
    for mid,w_text,ts in reader:
        mid = mid.strip('\xef\xbb\xbf')
        if mid in uid_list:
            if uid_weibo.has_key(mid):
                item = uid_weibo[mid]
                item = item + '_' + w_text
                uid_weibo[mid] = item
            else:
                item = w_text
                uid_weibo[mid] = item

    uid_word = dict()
    for k,v in uid_weibo.iteritems():
        item = dict()
        words = sw.participle(v)
        for word in words:
            if item.has_key(word[0]):
                item[word[0]] = item[word[0]] + 1
            else:
                item[word[0]] = 1
        uid_word[k] = item
    
    return uid_list,uid_word

def input_data2(name):#测试输入
    
    uid_list = []
    #reader = csv.reader(file(abs_path + '/weibo_data/%s_uid.txt' % name, 'rb'))
    reader = csv.reader(file(abs_path + '/weibo_data/0122_uid.txt', 'rb'))
    for line in reader:
        uid = line[0].strip('\t\r\n')
        uid = uid.strip('\xef\xbb\xbf')
        uid_list.append(uid)

    uid_weibo = []
    reader = csv.reader(file(abs_path + '/test_weibo/com_weibo0126.csv', 'rb'))
    for mid,w_text,ts in reader:
        mid = mid.strip('\xef\xbb\xbf')
        if mid in uid_list:
            uid_weibo.append([mid,w_text,ts])
    
    return uid_list,uid_weibo

def input_data3():#测试输入

    uid_list = []
    reader = csv.reader(file(abs_path + '/weibo_data/0122_uid.txt', 'rb'))
    for line in reader:
        uid = line[0].strip('\t\r\n')
        uid = uid.strip('\xef\xbb\xbf')
        uid_list.append(uid)
    
    return uid_list

def combine_weibo():

    name_list = ['2013-09-01','2013-09-02','2013-09-03','2013-09-04',\
                 '2013-09-05','2013-09-06','2013-09-07']

    weibo_list = []
    for name in name_list:
        reader = csv.reader(file(abs_path + '/test_weibo/word_%s.csv' % name, 'rb'))
        ts = int(time.mktime(time.strptime(name,'%Y-%m-%d')))
        for mid,s,w_text in reader:
            mid = mid.strip('\xef\xbb\xbf')
            weibo_list.append([mid,w_text,ts])

    with open(abs_path + '/test_weibo/com_weibo0126.csv', 'wb') as f:
        writer = csv.writer(f)
        for item in weibo_list:
           writer.writerow((item[0],item[1],item[2]))

if __name__ == '__main__':
    uid_list = input_data3()
            
    
