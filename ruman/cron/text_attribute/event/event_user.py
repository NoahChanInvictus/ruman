# -*-coding=utf-8-*-

import os
import re
import csv
import time
from config import WORD_WEIGHT,TOTAL_WEIGHT,RANK_AVARAGE,RANK_WEIGHT

def event_classfiy(uid_weibo):
    '''
    民运倾向性分类主函数
    输入数据示例：字典
    {uid1:str(weibo1-weibo2-...)...}

    输出数据示例：倾向性字典（取值范围0-3）
    {uid1:2.8, uid2:2.9...}
    '''

    user_weight = dict()
    for k,v in uid_weibo.items():
        weight1 = 0
        weight2 = 0
        count = 0
        v = v.encode('utf-8')
        for k1,v1 in WORD_WEIGHT.items():           
            if v.count(k1):
                weight1 = weight1 + v1
                weight2 = weight2 + v.count(k1)*v1
                count = count + v.count(k1)

        if float(weight1)/float(TOTAL_WEIGHT) >= RANK_AVARAGE:
            u_weight1 = float(weight1)/float(TOTAL_WEIGHT)
        else:
            u_weight1 = 0
            
        if count < 6:
            u_weight2 = 0
        else:
            if float(weight2)/float(count) >= RANK_WEIGHT:
                u_weight2 = float(weight2)/float(count)
            else:
                u_weight2 = 0

        if (u_weight1 != 0) and (u_weight2 != 0):
            user_weight[k] = u_weight1*u_weight2
        else:
            user_weight[k] = 0

    return user_weight


if __name__ == '__main__':

    uid_weibo = input_data()
    user_weight = event_classfiy(uid_weibo)






  
