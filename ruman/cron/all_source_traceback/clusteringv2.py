# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.path.append('../../')
sys.setdefaultencoding('utf-8')
import re
import json
import jieba
jieba.load_userdict('../all_source_traceback/30wdict_utf8.txt')

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import TransportError
from elasticsearch.helpers import bulk
from elasticsearch import helpers
from config import *
from elasticsearch import Elasticsearch
from sklearn.feature_extraction.text import  TfidfVectorizer
from sklearn.cluster import KMeans
 
def jieba_tokenize(text):
    return jieba.lcut(text) 


# 创建停用词list  
def stopwordslist(filepath):  
    stopwords = [line.strip() for line in open(filepath, 'r').readlines()]  
    return stopwords  
stopwords = stopwordslist('../all_source_traceback/中文停用词库_utf-8.txt')
def stop_words_filter(seg_list):
    
    new_seg_list = []
    for word in seg_list:
        if word not in stopwords:  
            if word != '\t':  
                new_seg_list.append(word)
    while ' ' in new_seg_list:
        new_seg_list.remove(' ')
    return new_seg_list

def defaultDatabase():
    conn = mysql.connect(host=SQL_HOST,user=SQL_USER,password=SQL_PASSWD,db=DEFAULT_DB,charset=SQL_CHARSET,cursorclass=pymysql.cursors.DictCursor)
    conn.autocommit(True)
    cur = conn.cursor()
    return cur

def get_allsource_content(news_id,size=10000):
    allsource_result = {}
    es = Elasticsearch([{'host':ES_HOST,'port':ES_PORT}])
    query_body = {
        "query": {

        "bool": {
        "must": [
        # {
        # "range": {
        #     "publish_time": {
        #     "from": begin_ts,
        #     "to": end_ts
        #     }
        # }
        # },
        
        {"term":{"news_id":news_id,}}
        
        ],
        "must_not": [ ],
        "should": [ ]
        }
        },
        "from": 0,
        "size": size,
        "sort": [ ],
        "facets": { }
    }
    for source in TOPIC_ABOUT_DOCTYPE:
        iter_results = {}
        # print TOPIC_ABOUT_INDEX,query_body
        es_result = es.search(index=TOPIC_ABOUT_INDEX, doc_type=source,body=query_body,timeout=400)['hits']['hits']
        # print len(es_result)
        iter_dict = {source:es_result}
        allsource_result.update(iter_dict)
    return allsource_result

def pre_process(content):
    # content = content.decode('utf-8')
    # 文本预处理
    # content = str(content)
    multi_version = re.compile(u'-\{.*?(zh-hans|zh-cn):([^;]*?)(;.*?)?\}-')
    punctuation = re.compile(u"[-~!@#$%^&*()_+`=\[\]\\\{\}\"|;':,./<>?·！@#￥%……&*（）——+【】、；‘：“”，。、《》？「『」』]")
    content = multi_version.sub(u'\2', content)
    content = punctuation.sub('', content)
    pattern = re.compile(u'http://[a-zA-Z0-9.?/&=:]*',re.S)
    content = pattern.sub("",content)
    # 所有符号处理
    r1 = u'[a-zA-Z0-9’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~]+'#用户也可以在此进行自定义过滤字符
    # r2 = u'\s+;'
    content=re.sub(r1, '', content) #过滤内容中的各种标点符号
    # content = content.encode('utf-8')    
    return content

def text_proprocess(source,es_result):
    content_list = []
    for item in es_result:
        content = item['_source']['content']
        # print content.encode('utf-8')
        
        content = pre_process(content)
        content_list.append(content)
        # seg_list = jieba.cut(content,cut_all=False)

        # # 去掉停用词
        # seg_list = stop_words_filter(seg_list)
        # seg_string = ' '.join(seg_list)
        # print seg_string
    return content_list

def transform(dataset,n_features=1000):
    vectorizer = TfidfVectorizer(max_df=0.5, max_features=n_features, min_df=2,use_idf=True)
    X = vectorizer.fit_transform(dataset)
    return X,vectorizer
def kmeans(content_list):
    tfidf_vectorizer = TfidfVectorizer(tokenizer=jieba_tokenize, \
    lowercase=False)
    '''
    tokenizer: 指定分词函数
    lowercase: 在分词之前将所有的文本转换成小写，因为涉及到中文文本处理，
    所以最好是False
    '''
    tfidf_matrix = tfidf_vectorizer.fit_transform(content_list)
    num_clusters = CLUSTER_NUM
    km_cluster = KMeans(n_clusters=num_clusters, max_iter=300, n_init=8, \
                        init='k-means++',n_jobs=8)
    '''
    n_clusters: 指定K的值
    max_iter: 对于单次初始值计算的最大迭代次数
    n_init: 重新选择初始值的次数
    init: 制定初始值选择的算法
    n_jobs: 进程个数，为-1的时候是指默认跑满CPU
    注意，这个对于单个初始值的计算始终只会使用单进程计算，
    并行计算只是针对与不同初始值的计算。比如n_init=10，n_jobs=40, 
    服务器上面有20个CPU可以开40个进程，最终只会开10个进程
    '''
    #返回各自文本的所被分配到的类索引
    result = km_cluster.fit_predict(tfidf_matrix)
    print "Predicting result: ", result
    return result
def save_cluster(news_id,cluster_data):
    es = Elasticsearch([{'host':ES_HOST,'port':ES_PORT}])
    doc_type = 'type1'
    ACTIONS = []
    count = 0
    for item in cluster_data:
        action = { 
                    "_op_type":"index" ,
                    "_index":CLUSTER_INDEX,  
                    "_type":doc_type,
                    # "_id":doc_id,  
                    "_source":item
                    }
        ACTIONS.append(action)
        count += 1
        if count % 1000 == 0:
            success, _ = bulk(es, ACTIONS, raise_on_error=True, request_timeout=400)
            ACTIONS = []
            print 'in',doc_type,count,'has been inserted!'
    # 最后把余下的也bulk进去
    if ACTIONS != []:
        success, _ = bulk(es, ACTIONS, raise_on_error=True, request_timeout=400)
        ACTIONS = []
def clustering_main(news_id):
    all_result = get_allsource_content(news_id)
    
    for source,es_result in all_result.iteritems():
        print len(all_result[source]),'text need to be clusterd'
        content_list = text_proprocess(source,es_result)
        # content_list = text_proprocess('zhihu',es_result)
        kmeans_result = kmeans(content_list)
        print 'kmeans finished'
        final_result = []
        for i in range(len(es_result)):
            iter_result = es_result[i]['_source']
            iter_result['source'] = source
            # print type(int(kmeans_result[i]))
            iter_result['text_id'] = es_result[i]['_id']
            iter_result['cluster_id'] = int(kmeans_result[i])
            final_result.append(iter_result)
            # print kmeans_result[i],content_list[i]
        # print final_result[0]
    # return final_result
        save_cluster(news_id,final_result)

if __name__ == '__main__':
    clustering_main(2)
