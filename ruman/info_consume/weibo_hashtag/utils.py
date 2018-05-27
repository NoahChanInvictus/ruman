# -*- coding: utf-8 -*-
import math
import json,jieba
from gensim import corpora, models, similarities
from user_portrait.parameter import UID_TXT_PATH
from user_portrait.global_config import VIDEO_PATH,video_file
import datetime
import time
import numpy as np

def weibo_get_uid_list(filename):
    uid_list = []
    f = open(UID_TXT_PATH+'/'+filename,'r')
    for line in f.readlines():
        uid_list.append(line.strip('\n\r'))
    return uid_list

def today_time():
	today = datetime.date.today() 
	a = int(time.mktime(today.timetuple()))
	return a

def get_video(hot):
    key = []
    for i in hot:
        key.extend(list(jieba.cut(i)))

    with open(VIDEO_PATH+video_file,'r') as f:
        data = json.loads(f.read())
    newsid_key = []
    for news in data['news']:
        w_list = news['newsKeyword'].split('☆')
        for i in w_list:
            if len(i)>6:
                w_list.extend(list(jieba.cut(i)))
        newsid_key.append([news['newsID'],w_list])
'''
    model = models.Word2Vec([i[1] for i in newsid_key])
    instance = model.wmdistance(key,newsid_key[0][1])
    print instance
'''
'''
    sim = {}
    for news_key in newsid_key:
        for k in key:
            if k in news_key[1]:
                try:
                    sim[news_key[0]] += 1
                except:
                    sim[news_key[0]] = 1
    for i in sim:
        print newsid_key[i]
'''
'''
    dictionary = corpora.Dictionary([i[1] for i in newsid_key])
    corpus = [dictionary.doc2bow(tag[1]) for tag in newsid_key]
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    print corpus_tfidf
    vec_bow = dictionary.doc2bow(key)
    vec_tfidf = tfidf[vec_bow]
    print vec_tfidf
    index = similarities.MatrixSimilarity(corpus_tfidf)
    for i in index:
        print i
    sims = index[vec_tfidf]
    all_sim = list(np.argsort(-sims))
    zero = np.where(sims==0)
    for i in zero[0]:
        all_sim.remove(i)
    final = [newsid_key[i] for i in all_sim]
    print final
    return final
'''




if __name__ == '__main__':
	#all_weibo_count('aoyunhui',1468166400,1468170900)
    test()



