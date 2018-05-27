# -*- coding: UTF-8 -*-
import time
import csv
import scws




def get_liwc_dict():
    results = dict()
    f = open('/home/ubuntu8/huxiaoqian/user_portrait/user_portrait/cron/flow2/extract_word.csv', 'rb')
    reader = csv.reader(f)
    for line in reader:
        num = line[0]
        word = line[1]
        try:
            results[num].append(word)
        except:
            results[num] = [word]
    return results

liwc_dict = get_liwc_dict()

def deal_text_word(user, text):
    liwc_result = dict()
    for num in liwc_dict:
        liwc_result[num] = {}
        for liwc_word in liwc_dict[num]:
            if liwc_word in text.encode('utf-8'):
                try:
                    liwc_result[num][liwc_word] += 1
                except:
                    liwc_result[num][liwc_word] = 1
    if liwc_result != {'126':{}, '127':{}, '128':{}, '129':{}}:
        for num in liwc_result:
            for word in liwc_result[num]:
                print 'user, num, word, count:', user, num, word, liwc_result[num][word]
        print 'text:', text.encode('utf-8')

