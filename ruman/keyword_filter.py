# -*- coding: UTF-8 -*-
import codecs
from textrank4zh import TextRank4Keyword, TextRank4Sentence



try:
    from . import zxy_params
    EXTRA_BLACK_LIST_PATH = zxy_params.BASE_DIR+"/ruman/cron/text_attribute/black.txt"
except:
    EXTRA_BLACK_LIST_PATH = '/home/ubuntu2/jiangln/jln/user_portrait/user_portrait/dict/black.txt'

def load_black_words():
    one_words = [line.strip('\r\n') for line in file(EXTRA_BLACK_LIST_PATH)]
    return one_words


black_word = set(load_black_words())

tr4w = TextRank4Keyword()
word_count = 50

#keyword_list = [[word, count], [word, count]]
def keyword_filter(keyword_dict):
    keyword_list = [item.encode('utf-8') for item in keyword_dict]
    keyword_string = ''.join(keyword_list)
    tfidf = tr4w.tfidf_feature(keyword_string)
    print tfidf
    tr4w.analyze(text=keyword_string,tfidf='', lower=True, window=2)
    k_dict = tr4w.get_keywords(word_count, word_min_len=2)
    word_dict = dict()
    for item in k_dict:
        if item.word.encode('utf-8').isdigit() or item.word.encode('utf-8') in black_word:
            continue
        word_dict[item.word] = item.weight * 100
    return word_dict
    
    
