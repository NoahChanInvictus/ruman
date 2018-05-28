#-*-coding=utf-8-*-

import os
import time
from scwsutil.utils import load_scws, cut
s = load_scws()

ABSOLUTE_DICT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), './'))
EXTRA_STOPWORD_PATH = os.path.join(ABSOLUTE_DICT_PATH, 'stopwords.txt')


cx_dict = set(['Ag','a','an','Ng','n','nr','ns','nt','nz','Vg','v','vd','vn','@','j']) # 关键词词性词典, 保留名词、动词、形容词
cx_dict_noun = set(['Ng','n','nr','ns','nt','nz']) # 关键词词性词典, 保留名词

def load_stopwords():
  with open(EXTRA_STOPWORD_PATH) as f:
    stopwords = [w.strip() for w in f]
  return set(stopwords)

stopwords = load_stopwords()


def cut_words(text):
    '''分词, 加入黑名单过滤单个词，保留名词、动词、形容词
       input
           texts: 输入text的list，utf-8
       output:
           terms: 关键词list
    '''
    if not isinstance(text, str):
        raise ValueError("cut words input text must be string")

    cx_terms = cut(s, text, cx=True)

    return [term for term, cx in cx_terms if cx in cx_dict and term not in stopwords]


def cut_words_noun(text):
    '''分词, 加入黑名单过滤单个词，保留名词
       input
           texts: 输入text的list，utf-8
       output:
           terms: 关键词list
    '''
    if not isinstance(text, str):
        raise ValueError("cut words input text must be string")

    cx_terms = cut(s, text, cx=True)

    return [term for term, cx in cx_terms if cx in cx_dict_noun and term not in stopwords]