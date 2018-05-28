#!/usr/bin/env python
#-*-coding:utf-8-*-
from operator import itemgetter, attrgetter  
import datetime
import json
import sys
from global_utils_do import txt_labels as classes,xs,read_by_xapian

def readUidByArea(area):
    uidlist = []
    with open("./domain_combine/" + area + ".txt") as f:
        for line in f:
            uid = line.split()[0]
            uidlist.append(uid)
    return uidlist

def readFriendsByArea(area):
    user_friends_dict = dict()
    f = open('./dogapi_combine/'+area+'_friends.jl')
    for line in f:
        user = json.loads(line.strip())
        user_friends_dict[str(user['id'].encode('utf-8'))] = user['friends']
    f.close()
    return user_friends_dict

def get_seed_main():
    
    flag_dict = dict()

    for name in classes:
        flag_dict[name] = []
    error = 0
    for area in classes:
        uidlist = readUidByArea(area)
        ufriends = readFriendsByArea(area)
        for uid in uidlist:
            try:
                for f in ufriends[uid]:
                    v_t = read_by_xapian(xs,f)
                    if v_t != 'other':
                        flag = user_domain_classifier_v2(v_t)
                        if flag != 'other':
                            flag_dict[name].append(f)
            except:
                error +=1
                pass
            flag_dict[area].append(uid)

    protou=open('./protou_combine/protou.txt','w')
    count = 0
    for k,v in flag_dict.items():
        if count == 0:
            protou.write(k+':')
            count = count + 1
        else:
            protou.write('\n'+k+':')
        for uid in v:
            protou.write(' '+str(uid))

if __name__ == '__main__':

    get_seed_main()
    
