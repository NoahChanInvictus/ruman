#-*-coding=utf-8-*-

import os
import sys
import json
from global_utils_do import STATUS_THRE,FOLLOWER_THRE,labels,outlist,lawyerw,cut,load_scws,adminw,mediaw,businessw

s = load_scws()

def user_domain_classifier_v2(user):
    r = user
    label = labels[11]

    verified_type = r['verified_type']
    location = r['user_location']
    province = location.split(' ')[0]

    followers_count = r['fansnum']
    statuses_count = r['statusnum']

    name = r['nick_name']
    description = r['description']

    if verified_type == 4:
        label = labels[0] # 高校微博

    elif verified_type == 1:
        label = labels[7]#政府机构及人士
        
    elif verified_type == 8 or verified_type == 7 or verified_type == 2:
        if province not in outlist:
            label = labels[1] # 境内机构
        else:
            label = labels[2] # 境外机构

    elif verified_type == 3:
        if location not in outlist:
            label = labels[3] # 境内媒体
        else:
            label = labels[4] # 境外媒体 

    elif verified_type == 5 or verified_type == 6:
        label = labels[5] # 民间组织

    elif verified_type == 0:
        text = name + description
        kwdlist = cut(s, text)
        lawyer_weight = sum([1 for keyword in kwdlist if keyword in lawyerw]) # 律师
        adminw_weight = sum([1 for keyword in kwdlist if keyword in adminw]) # 政府官员
        mediaw_weight = sum([1 for keyword in kwdlist if keyword in mediaw]) # 媒体人士
        businessw_weight = sum([1 for keyword in kwdlist if keyword in businessw]) # 商业人士

        max_weight = 0
        '''
        if max_weight < lawyer_weight:
            max_weight = lawyer_weight
            label = labels[6]
        '''
        
        if max_weight < businessw_weight:
            max_weight = businessw_weight
            label = labels[12]

        if max_weight < adminw_weight:
            max_weight = adminw_weight
            label = labels[7]

        if max_weight < mediaw_weight:
            max_weight = mediaw_weight
            label = labels[8]

        if max_weight == 0:
            label = labels[9]

        if lawyer_weight!=0:
            label = labels[6]

    elif verified_type == 220 or verified_type == 200:
        label = labels[9]

    elif verified_type == 400:
        label = labels[11]    

    else:
        if followers_count >= FOLLOWER_THRE and statuses_count >= STATUS_THRE:
            label = labels[10] # 草根

        lawyer_weight = 0
        text = name + description
        kwdlist = cut(s, text)
        lawyer_weight = sum([1 for keyword in kwdlist if keyword in lawyerw])

        if lawyer_weight != 0:
            label = labels[6]

    return label

