# -*-coding:utf-8-*-

import sys
import json
import time
from ruman.global_utils import R_CLUSTER_FLOW1 as r
from ruman.global_utils import es_user_profile, es_user_portrait
from ruman.global_utils import profile_index_name, profile_index_type, portrait_index_name, portrait_index_type
from ruman.parameter import RUN_TYPE

def get_temporal_rank(task_type, sort="retweeted", number=100):
    number = int(number) - 1
    if int(task_type) == 0: # 到目前位置
        sort_list = r.zrange("influence_%s" %sort, 0, number, withscores=True, desc=True)
    elif int(task_type) == 1:
        sort_list = r.zrange("influence_%s_1" %sort, 0, number, withscores=True, desc=True)
    elif int(task_type) == 2:
        sort_list = r.zrange("influence_%s_2" %sort, 0, number, withscores=True, desc=True)
    elif int(task_type) == 3:
        sort_list = r.zrange("influence_%s_3" %sort, 0, number, withscores=True, desc=True)
    else:
        sort_list = r.zrange("influence_%s_4" %sort, 0, number, withscores=True, desc=True)

    uid_list = []
    for item in sort_list:
        uid_list.append(item[0])

    if sort == "retweeted":
        other = "comment"
    else:
        other = "retweeted"

    results = []
    # 查看背景信息
    if uid_list:
        profile_result = es_user_profile.mget(index=profile_index_name, doc_type=profile_index_type, body={"ids":uid_list})["docs"]
        bci_result = es_user_profile.mget(index="bci_history", doc_type="bci", body={"ids":uid_list},_source=False, fields=['user_fansnum',"weibo_month_sum" ])["docs"]
        count = 0
        for item in profile_result:
            _id = item['_id']
            index = profile_result.index(item)
            tmp = []
            tmp.append(item['_id'])
            if item['found']:
                item = item['_source']
                tmp.append(item['nick_name'])
                tmp.append(item['statusnum'])
                tmp.append(item['user_location'])
                tmp.append(item['fansnum'])
            else:
                tmp.extend(['',0,'',0])
            try:
                user_fansnum = bci_result[count]['fields']['user_fansnum'][0]
                tmp[4] = user_fansnum
            except:
                pass
            try:
                weibo_number = bci_result[count]['fields']["weibo_month_sum"][0]
                tmp[2] = weibo_number
            except:
                pass
            count_1 = int(sort_list[index][1])
            if int(task_type) == 0:
                tmp_count = r.zscore("influence_%s" %other, _id)
                if tmp_count:
                    count_2 =  int(tmp_count)
                else:
                    count_2 = 0
            else:
                tmp_count =  r.zscore("influence_%s_%s" %(other,task_type), _id)
                if tmp_count:
                    count_2 = int(tmp_count)
                else:
                    count_2 = 0
            if sort == "retweeted":
                tmp.append(count_1)
                tmp.append(count_2)
            else:
                tmp.append(count_2)
                tmp.append(count_1)
            results.append(tmp)
            count += 1

    if uid_list:
        count = 0
        portrait_result = es_user_portrait.mget(index=portrait_index_name, doc_type=portrait_index_type, body={"ids":uid_list})["docs"]
        for item in portrait_result:
            if item['found']:
                results[count].append("1")
            else:
                results[count].append("0")
            count += 1

    return results

if __name__ == "__main__":
    print get_temporal_rank(1, "comment")
