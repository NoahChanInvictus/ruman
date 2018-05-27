# -*- coding: UTF-8 -*-
'''
deal topic and domain input data
'''
import sys

reload(sys)
sys.path.append('../../')
from model_config import re_cut, sw, black, single_word_whitelist, cx_dict


#get user weibo string dict
#write in version: 15-12-08
#input: user_weibo_dict {uid:[weibo1, weibo2,...]}
#output: user_weibo_string_dict {uid1:'weibo1,weibo2,...', uid2:'weibo1,weibo2...',...}
def get_user_weibo_string(user_weibo_dict):
    user_weibo_string_dict = {}
    for uid ,weibo_list in user_weibo_dict.iteritems():
        weibo_string = ','.join([re_cut(item['text']) for item in weibo_list])
        user_weibo_string_dict[uid] = weibo_string
    return user_weibo_string_dict

#get user keywords dict
#write in version: 15-12-08
#input: user_weibo_dict: {uid1:[weibo1,weibo2,...], uid2:[weibo1,weibo2..],...}
#output: user_keywords_dict: {uid1:{word1:count1, word2:count...}, uid2:{},...}
def get_user_keywords_dict(user_weibo_string_dict):
    user_keywords_dict = {}
    #use ',' connect weibo string
    for uid, user_weibo_string in user_weibo_string_dict.iteritems():
        #user_weibo_string = ','.join([re_cut(item['text']) for item in weibo_list])
        words = sw.participle(user_weibo_string.encode('utf-8'))
        word_list = {}
        for word in words:
            if (word[1] in cx_dict) and 3 < len(word[0]) < 30 and (word[0] not in black) and (word[0] not in single_word_whitelist):#选择分词结果的名词、动词、形容词，并去掉单个词
                try:
                    word_list[word[0]] += 1
                except:
                    word_list[word[0]] = 1

        user_keywords_dict[uid] = word_list

    return user_keywords_dict
