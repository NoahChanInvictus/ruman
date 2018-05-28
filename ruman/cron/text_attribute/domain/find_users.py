# -*- coding: UTF-8 -*-

import os
import time
import scws
import csv
import sys
import json
from global_utils_do import abs_path,es_user_profile,es_retweet,profile_index_name,\
                         profile_index_type,retweet_index_name_pre,retweet_index_type,get_db_num

zh_text = ['nick_name','rel_name','description','sp_type','user_location']

def write_user(friends,area):

    fw = open(abs_path+'./dogapi_combine/'+area+'_info.jl','w')
    for k,v in friends.items():
        data = {'user':v,'id':k}
        d = json.dumps(data)
        fw.write(d + '\n')

def write_friends(friends,area):

    fw = open(abs_path+'./dogapi_combine/'+area+'_friends.jl','w')
    for k,v in friends.items():
        data = {'friends':v,'id':k}
        d = json.dumps(data)
        fw.write(d + '\n')

def readUidByArea(area):
    uidlist = []
    with open(abs_path+"./domain_combine/" + area +".txt") as f:
        for line in f:
            uid = line.split()[0]
            uid = uid.strip('\ufeff')
            uidlist.append(uid)
    return uidlist

def readcsv(name):

    f = open(abs_path+'./test_user/uid_%s.txt' % name)
    uidlist = []
    i = 1
    for line in f:
        line = line.strip('\r\n')
        if i == 1:
            i = 2
            continue
        uidlist.append(line)

    return uidlist

def train_data():#训练数据
    classes = ['mediaworker', 'activer', 'grassroot', 'business',\
               'university', 'homeadmin', 'abroadadmin', 'homemedia', 'abroadmedia', 'folkorg', 'lawyer', 'politician']
    for area in classes:
        #print '%s start....' % area
        uidlist = readUidByArea(area)
        friend_list = find_friends(uidlist)
        user_info = get_info(uidlist)
        write_friends(friend_list,area)
        write_user(user_info,area)
        #print '%s end....' % area

def get_user(uidlist):#返回用户的背景信息
    '''
        返回用户的景信息
        输入数据：uid列表
        输出数据：users列表
    '''
    user_list = dict()
    search_result = es_user_profile.mget(index=profile_index_name, doc_type=profile_index_type, body={"ids": uidlist})["docs"]
    for item in search_result:
        print item
        uid = item['_id']
        if not item['found']:
            user_list[str(uid)] = 'other'
        else:
            data = item['_source']
            row = dict()
            for k,v in data.items():
                if k in set(zh_text):
                    row[k] = v.encode('utf-8')
                else:
                    row[k] = v
            user_list[str(uid)] = row

    return user_list

def get_friends(uidlist):#返回用户的粉丝结构
    '''
        返回用户的粉丝结构
        输入数据：uid列表
        输出数据：friend列表
    '''

    ts = get_db_num(time.time())    
    friend_list = dict()
    search_result = es_retweet.mget(index=retweet_index_name_pre+str(ts), doc_type=retweet_index_type, body={"ids": uidlist})["docs"]
    for item in search_result:
        uid = item['_id']
        if not item['found']:
            friend_list[str(uid)] = []
        else:
            data = item['_source']['uid_retweet']
            data = eval(data)
            row = []
            for i in data.keys():
                row.append(i)
            friend_list[str(uid)] = row
    
    return friend_list

if __name__ == '__main__':

    uidlist = readcsv('111')
    user_list = get_user(uidlist)
    #friend_list = get_friends(uidlist)
    print user_list
    #train_data()

    
    
