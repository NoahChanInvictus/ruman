# -*- coding:utf-8 -*-

import sys
import re
import json
import os
import uuid
import math
import time
from elasticsearch import Elasticsearch
from collections import Counter
from config import load_scws, load_dict, cut_filter, re_cut
#from aggregation_weibo import query_mid_list, query_related_weibo
#reload(sys)
#sys.path.append('./../')
#from global_utils import es_flow_text as es_text
#from global_utils import flow_text_index_name_pre, flow_text_index_type
#from time_utils import ts2datetime, datetime2ts
#from parameter import SOCIAL_SENSOR_TIME_INTERVAL as time_interval
#from parameter import SOCIAL_SENSOR_FORWARD_RANGE as forward_time_range

PROCESS_GRAM = 3
Min_CLUSTER_NUM = 2
MAX_CLUSTER_NUM = 15
CLUTO_FOLDER = 'cluto'
COMMENT_WORDS_CLUSTER_NUM = 10
CLUSTERING_KMEANS_CLUSTERING_NUM = 10
CLUTO_EXECUTE_PATH = './cluto-2.1.2/Linux-i686/vcluster'
AB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), './')

sw = load_scws()
#cx_dict = set(['Ag','a','an','Ng','n','nr','ns','nt','nz','Vg','v','vd','vn','@','j'])
cx_dict = set(['Ng','n','nr','ns','nt','nz']) # 关键词词性词典, 保留名词



def freq_word(items):
    """
    统计一条文本的词频，对文本进行过滤后再分词
    input:
        items:微博字典，{"mid": 12345, "text": text}
    output:
        top_word:词和词频构成的字典，如:{词:词频, 词:词频}
    """

    word_list = []
    text = items["text"]
    #print type(text)
    text = re_cut(text)
    cut_text = sw.participle(text.encode('utf-8'))
    #print cut_text
    cut_word_list = [term for term, cx in cut_text if cx in cx_dict]
    for w in cut_word_list:
        word_list.append(w)


    counter = Counter(word_list)
    total = sum(counter.values())
    topk_words = counter.most_common()
    top_word = {k:(float(v)/float(total)) for k,v in topk_words}

    return top_word


def tfidf(inputs):
    """
    计算每条文本中每个词的tfidf，对每个词在各个文本中tfidf加和除以出现的文本次数作为该词的权值
    输入数据：
        inputs: [{"mid": mid, "text": text}]
    输出结果：
        result_tfidf[:topk]:前20%tfidf词及tfidf值的列表,示例：[(词,tfidf)]
        input_word_dict:每一条记录的词及tfidf,示例：{"_id":{词：tfidf,词：tfidf,...}}
    """

    total_document_count = len(inputs)
    tfidf_dict = {} #词在各个文本中的tfidf之和
    count_dict = {} #词出现的文本数
    count = 0 #记录每类下词频总数
    input_word_dict = {} #每条记录每个词的tfidf,{"_id":{词：tfidf，词：tfidf}}
    for iter_input in inputs:
        word_count = freq_word(iter_input)
        count += sum(word_count.values())
        word_tfidf_row = {}#每一行中词的tfidf
        for k,v in word_count.iteritems():
            tf = v
            document_count = sum([1 for input_item in inputs if k in input_item['text'].encode("utf-8")])
            idf = math.log(float(total_document_count)/(float(document_count+1)))
            tfidf = tf*idf
            word_tfidf_row[k] = tfidf
            try:
                tfidf_dict[k] += tfidf
            except:
                tfidf_dict[k] = 1
        input_word_dict[iter_input["mid"]] = word_tfidf_row

    for k,v in tfidf_dict.iteritems():
        tfidf_dict[k] =  float(tfidf_dict[k])/float(len(inputs))

    sorted_tfidf = sorted(tfidf_dict.iteritems(), key = lambda asd:asd[1],reverse = True)
    result_tfidf = [(k,v)for k,v in sorted_tfidf]
    #result_tfidf = sorted_tfidf

    topk = int(math.ceil(float(len(result_tfidf))*0.2))#取前20%的tfidf词
    return result_tfidf[:topk],input_word_dict


def process_for_cluto(word, inputs, gram=PROCESS_GRAM):
    """
    处理成cluto的输入格式，词-文本聚类
    输入数据：
        word：特征词，[(词，tfidf)]
        input_dict: 每条文本包含的词及tfidf，{词：tfidf，词：tfidf}
        inputs: 过滤后的评论数据
    输出数据：
        cluto输出文件位置
    """

    row = len(word) #词数
    column = len(inputs) #特征列数
    #row = 0
    nonzero_count = 0 #非0特征数
    count = 0

    cluto_input_folder = os.path.join(AB_PATH, CLUTO_FOLDER)
    if not os.path.exists(cluto_input_folder):
        os.makedirs(cluto_input_folder)
    file_name = os.path.join(cluto_input_folder, '%s.txt' % os.getpid()) #尝试用时间

    with open(file_name, 'w') as fw:
        lines = []
        #词频聚类
        for w in word:
            row_record = []
            for i in range(len(inputs)):
                n = (inputs[i]['text'].encode('utf-8')).count(str(w[0]))
                if n != 0:
                    nonzero_count += 1
                    row_record.append('%s %s' %(str(i+1), n))
            line = ' '.join(row_record) + '\r\n'
            lines.append(line)

        fw.write('%s %s %s\r\n' %(row, column, nonzero_count))
        fw.writelines(lines)

    return file_name


def cluto_kmeans_vcluster(k=CLUSTERING_KMEANS_CLUSTERING_NUM, input_file=None, vcluster=None):
    """
    cluto kmeans 聚类
    输入数据：
        k: 聚簇数
        input_files: cluto输入文件路径，如果不指定，以cluto_input_folder + pid.txt方式命名
        vcluster: cluto vcluster可执行文件路径

    输出数据：
        cluto聚类结果，list
        聚类结果评价文件位置及名称
    """
    # 聚类结果文件, result_file

    cluto_input_folder = os.path.join(AB_PATH, CLUTO_FOLDER)

    if not input_file:
        input_file = os.path.join(cluto_input_folder, '%s.txt' % os.getpid())
        result_file = os.path.join(cluto_input_folder, '%s.txt.clustering.%s' % (os.getpid(), k))
        evaluation_file = os.path.join(cluto_input_folder, '%s_%s.txt' %(os.getpid(), k))
    else:
        result_file = os.path.join(cluto_input_folder, '%s.clustering.%s' % (input_file, k))
        evaluation_file = os.path.join(cluto_input_folder, '%s_%s.txt' % (os.getpid(), k))

    if not vcluster:
        vcluster = os.path.join(AB_PATH, CLUTO_EXECUTE_PATH)

    command = '%s -niter=20 %s %s > %s' % (vcluster, input_file, k, evaluation_file)
    os.popen(command)

    # 提取聚类结果
    results = [line.strip() for line in open(result_file)]


    # 提取每类聚类结果
    with open(evaluation_file) as f:
        s = f.read()
        pattern = re.compile(r'\[I2=(\S+?)\]')
        res = pattern.search(s).groups()
        evaluation_results = res[0]

    if os.path.isfile(result_file):
        os.remove(result_file)

    if os.path.isfile(input_file):
        os.remove(input_file)

    if os.path.isfile(evaluation_file):
        os.remove(evaluation_file)

    return results, evaluation_results


def label2uniqueid(labels):
    """
    为聚类结果不为其他类的生成唯一的类标号
    input：
        labels: 一批类标号，可重复
    output:
        label2id: 各类标号到全局唯一ID的映射
    """

    label2id = dict()
    for label in set(labels):
        label2id[label] = str(uuid.uuid4())

    return label2id



def kmeans(word, inputs, k=CLUSTERING_KMEANS_CLUSTERING_NUM, gram=PROCESS_GRAM):
    """
    kmeans聚类函数
    输入数据：
        word：前20%tfidf词及tfidf值的列表，示例：[(词，tfidf)]
        input_dict: 每条文本中包含的词及tfidf,{"mid": {词:tfidf,词:tfidf}}
        inputs:[{"mid": mid, "text": text}]
        k: 聚类个数
    输出数据：
        每类词构成的字典，{类标签：[词1,词2, ...]}
        聚类效果评价文件路径
    """

    #if len(inputs) < 2:
        #raise ValueError("length of input items must be larger than 2")

    input_file = process_for_cluto(word, inputs, gram=gram)
    labels, evaluation_results = cluto_kmeans_vcluster(k=k, input_file=input_file)
    label2id = label2uniqueid(labels)

    #将词对归类，{类标签：[词1，词2，...]}
    word_label = {}
    for i in range(len(word)):
        l = labels[i]
        if int(l) != -1:
            l = label2id[l]
        else:
            l = 'other'

        if word_label.has_key(l):
            item = word_label[l]
            item.append(word[i][0])
        else:
            item = []
            item.append(word[i][0])
            word_label[l] = item

    return word_label, evaluation_results



def choose_cluster(tfidf_word, inputs, cluster_min=Min_CLUSTER_NUM, cluster_max=MAX_CLUSTER_NUM, cluster_num=COMMENT_WORDS_CLUSTER_NUM):
    """
    选取聚类个数cluster_min(2)~cluster_max(5)个中聚类效果最好的保留
    输入数据：
        tfidf_word:tfidf topk词及权值，[(词，权值)]
        inputs:过滤后的评论
        cluster_min:尝试的最小聚类个数
        cluster_max:尝试的最大聚类个数
    输出数据：
        聚类效果最好的聚类个数下的词聚类结果
    """

    results, evaluation = kmeans(tfidf_word, inputs, k=cluster_num)

    return results



def text_classify(inputs, word_label, tfidf_word):
    """
    对每条评论分别计算属于每个类的权重，将其归入权重最大的类
    输入数据：
        inputs:评论字典的列表，[{'_id':评论id,'news_id':新闻id,'content':评论内容}]
        word_cluster:词聚类结果,{'类标签'：[词1，词2，...]}
        tfidf_word:tfidf topk词及权值，[(词，权值)]

    输出数据：
        每条文本的归类，字典，{'_id':[类，属于该类的权重]}
    """

    #将词及权值整理为字典格式
    word_weight = {}
    for idx,w in enumerate(tfidf_word):
        word_weight[w[0]] = w[1]

    #计算每条评论属于各个类的权值
    for input in inputs:
        text_weight = {}
        text = input['text']
        text_list = []
        text = re_cut(text)
        cut_text = sw.participle(text.encode('utf-8'))
        #print cut_text
        cut_word_list = [term for term, cx in cut_text if cx in cx_dict]
        for w in cut_word_list:
            text_list.append(w)

        if text_list == []:
            continue

        for l, w_list in word_label.iteritems():
            weight = 0
            for w in w_list:
                weight += text.encode('utf-8').count(w)*word_weight[w]
            text_weight[l] = float(weight)/(float(len(text_list)))
        sorted_weight = sorted(text_weight.iteritems(), key=lambda asd:asd[1], reverse=True)
        if sorted_weight[0][1] != 0:
            clusterid, weight = sorted_weight[0]
        else:
            clusterid = 'other'
            weight = 0
        input.pop('text')
        input['label'] = clusterid
        input['weight'] = weight

    return inputs

def cluster_evaluation(items, min_size=10):
    """
    只保留文本数大于num的类
    输入数据：
        items：["mid":mid, "text":text, "label":label]
        num: 类文本最小值
    输出数据：
        各簇的文本，dict
    """

    # 将文本按照类标签进行归类
    items_dict = {}
    for item in items:
        if item.has_key('label'):
            try:
                items_dict[item['label']].append(item)
            except:
                items_dict[item['label']] = [item]

    other_items = []
    cluster_dict = dict()
    for label in items_dict.keys():
        items = items_dict[label]
        if len(items) > min_size:
            cluster_dict[label] = len(items)

    #print cluster_dict

    """
    try:
        items_dict['other'].extend(other_items)
    except:
        items_dict['other'] = other_items
    """
    return cluster_dict






