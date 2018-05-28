#-*-coding=utf-8-*-
#vision2
import os
import re
import sys
import json
import csv
import random
from find_users import get_friends, get_user
from domain_by_text import domain_classfiy_by_text
from global_utils_do import labels,zh_labels,txt_labels,r_labels,proto_users,train_users
from user_domain import user_domain_classifier_v2
#from test_data import input_data #测试输入

def user_domain_classifier_v1(friends, fields_value=txt_labels, protou_dict=proto_users):#根据用户的粉丝列表对用户进行分类
    mbr = {'university':0, 'homeadmin':0, 'abroadadmin':0, 'homemedia':0, 'abroadmedia':0, 'folkorg':0, 
          'lawyer':0, 'politician':0, 'mediaworker':0, 'activer':0, 'grassroot':0, 'other':0, 'business':0}
   
    # to record user with friends in proto users

    if len(friends) == 0:
         mbr['other'] += 1
    else:
        for area in fields_value:
            c_set = set(friends) & set(protou_dict[area])
            mbr[area] = len(c_set)
     
    count = 0
    count = sum([v for v in mbr.values()])

    if count == 0:
        return 'other',mbr
    
    sorted_mbr = sorted(mbr.iteritems(), key=lambda (k, v): v, reverse=True)
    field1 = sorted_mbr[0][0]

    return field1,mbr

def getFieldFromProtou(uid, protou_dict=train_users):#判断一个用户是否在种子列表里面

    result = 'Null'
    for k,v in protou_dict.iteritems():
        if uid in v:
            return k

    return result

def get_recommend_result(v_type,label):#根据三种分类结果选出一个标签

    if v_type == 'other':#认证类型字段走不通
        if label[0] != 'other':
            return label[0]
        else:
            return label[2]

    if label[1] in r_labels:#在给定的类型里面分出来的身份
        return label[1]

    if label[1] == 'politician' and v_type == 1:
        return label[1]

    if label[1] == 'activer' and (v_type == 220 or v_type == 200):
        return label[1]

    if label[1] == 'other' and v_type == 400:
        return label[1]

    if label[0] != 'other':#根据粉丝结构分出来身份
        return label[0]
    else:
        return label[2]

def domain_classfiy(uid_list,uid_weibo):#领域分类主函数
    '''
    用户领域分类主函数
    输入数据示例：
    uid_list:uid列表 [uid1,uid2,uid3,...]
    uid_weibo:分词之后的词频字典  {uid1:{'key1':f1,'key2':f2...}...}

    输出数据示例：
    domain：标签字典
    {uid1:[label1,label2,label3],uid2:[label1,label2,label3]...}
    注：label1是根据粉丝结构分类的结果，label2是根据认证类型分类的结果，label3是根据用户文本分类的结果

    re_label：推荐标签字典
    {uid1:label,uid2:label2...}
    '''
    if not len(uid_weibo) and len(uid_list):
        domain = dict()
        r_domain = dict()
        for uid in uid_list:
            domain[uid] = ['other']
            r_domain[uid] = ['other']
        return domain,r_domain
    elif len(uid_weibo) and not len(uid_list):
        uid_list = uid_weibo.keys()
    elif not len(uid_weibo) and not len(uid_list):
        domain = dict()
        r_domain = dict()
        return domain,r_domain
    else:
        pass
    
    users = get_user(uid_list)
    frineds = get_friends(uid_list)

    domain = dict()
    r_domain = dict()
    text_result = dict()
    user_result = dict()
    for k,v in users.iteritems():

        uid = k
        result_label = []
        sorted_mbr = dict()
        field1 = getFieldFromProtou(k, protou_dict=train_users)#判断uid是否在种子用户里面
        if field1 != 'Null':#该用户在种子用户里面
            result_label.append(field1)
        else:
            f= frineds[k]#返回用户的粉丝列表
            if len(f):
                field1,sorted_mbr = user_domain_classifier_v1(f, fields_value=txt_labels, protou_dict=proto_users)
            else:
                field1 = 'other'
                sorted_mbr = {'university':0, 'homeadmin':0, 'abroadadmin':0, 'homemedia':0, 'abroadmedia':0, 'folkorg':0, \
          'lawyer':0, 'politician':0, 'mediaworker':0, 'activer':0, 'grassroot':0, 'other':0, 'business':0}
            result_label.append(field1)
        
        r = v
        if r == 'other':
            field2 = 'other'
        else:
            field2 = user_domain_classifier_v2(r)
        result_label.append(field2)

        if uid_weibo.has_key(k) and len(uid_weibo[k]):
            field_dict,result = domain_classfiy_by_text({k: uid_weibo[k]})#根据用户文本进行分类
            field3 = field_dict[k]
        else:
            field3 = 'other'
        result_label.append(field3)
                
        domain[str(uid)] = result_label

        if r == 'other':
            re_label = get_recommend_result('other',result_label)#没有认证类型字段
        else:
            re_label = get_recommend_result(r['verified_type'],result_label)

        r_domain[str(uid)] = re_label
    
    return domain,r_domain

if __name__ == '__main__':
    uid_list,uid_weibo = input_data()
    uid_weibo = dict()
    domain,r_domain = domain_classfiy(uid_list,uid_weibo)
    print domain
    #print r_domain


    
