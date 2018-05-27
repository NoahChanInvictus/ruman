# -*- coding: UTF-8 -*-

import os
import time
import re
import scws
import csv
import sys
import json
from textrank4zh import TextRank4Keyword, TextRank4Sentence
from config_ys import load_scws,load_black_words,re_cut

black = load_black_words()
tr4w = TextRank4Keyword()

def get_keyword(w_text, n_gram, n_count):

    tr4w.analyze(text=w_text, lower=True, window=n_gram)
    word_list = dict()
    k_dict = tr4w.get_keywords(n_count, word_min_len=2)
    for item in k_dict:
        if item.word.encode('utf-8').isdigit() or item.word.encode('utf-8') in black:
            continue
        word_list[item.word.encode('utf-8')] = item.weight

    return word_list

def get_weibo_single(text,n_gram=2,n_count=3):
    '''
        针对单条微博提取关键词，但是效率比较低
        输入数据：
        text：单条微博文本，utf-8编码
        n_gram：词语滑动窗口，建议取2
        n_count：返回的关键词数量
        输出数据：
        字典：键是词语，值是词语对应的权重
    '''

    w_text = re_cut(text)
    if w_text:
        w_key = get_keyword(w_text, n_gram, n_count)
        uid_word = w_key
    else:
        uid_word = dict()
    
    return uid_word

def get_weibo(text,n_gram=2,n_count=20):
    '''
        针对一批微博提取关键词
        输入数据：
        text：微博文本列表，utf-8编码
        n_gram：词语滑动窗口，建议取2
        n_count：返回的关键词数量
        输出数据：
        字典：键是词语，值是词语对应的权重
    '''

    text_str = ''
    for item in text:
        w_text = re_cut(item)
        if w_text:
            text_str = text_str + '。' + w_text

    if text_str:
        w_key = get_keyword(text_str, n_gram, n_count)
        uid_word = w_key
    else:
        uid_word = dict()

    return uid_word

if __name__ == '__main__':

    reader = csv.reader(file('./text_2016-05-19_0.csv', 'rb'))
    count = 0
    text_list = []
    for uid,text,ts,geo in reader:
        if count == 0:
            key_single = get_weibo_single(text)
        else:
            text_list.append(text)
        count = count + 1
        if count > 10:
            break

    key_list = get_weibo(text_list)

    print key_single
    print key_list









        
