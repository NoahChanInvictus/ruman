# -*- coding: utf-8 -*-
__author__ = 'zxy'
import sys
import os
import jieba
import re
import csv

thisFilePath = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(thisFilePath,"../cron/util/")))
sys.path.append('/home/lcr/libsvm-3.17/python/')
import svmutil


DATA_PATH = os.path.abspath(os.path.join(thisFilePath,"../cron/trainData/adsClassify"))
TRAIN_FEATURE_FILE = os.path.abspath(os.path.join(DATA_PATH,"./new_train.txt"))
WORD_FEATURE_MAP_FILE = os.path.abspath(os.path.join(DATA_PATH,"./new_feature.csv"))
SAVED_MODEL = os.path.abspath(os.path.join(DATA_PATH,"./ads_classify_svm.model"))

# 在用户字典中添加了new_feature中的词语，确保分词准确
USER_DICT_FILE = os.path.abspath(os.path.join(DATA_PATH,"./userdic.txt"))

'''
广告识别，使用词袋模型+SVM
'''
class adsClassify:
    def __init__(self,train_feature_file = TRAIN_FEATURE_FILE):
        if os.path.exists(SAVED_MODEL):
            self.model = svmutil.svm_load_model(SAVED_MODEL)
        else:
            y, x = svmutil.svm_read_problem(train_feature_file)
            self.model = svmutil.svm_train(y, x, '-c 4')
            svmutil.svm_save_model(SAVED_MODEL,self.model)

        # y, x = svmutil.svm_read_problem(train_feature_file)
        # print svmutil.svm_predict(y, x, self.model)

    def adsPredict(self, weiboList):
        '''
        :param weiboList: 微博列表
        :return: 返回被判定为广告的微博id以及其对应的分词结果
        '''
        jieba.load_userdict(USER_DICT_FILE)
        feature_word_dict = self.loadfeature_word_dict()
        ads_midWordsMap = dict()
        for weiboInfo in weiboList:
            try:
                text = weiboInfo["_source"]["text"].decode("utf-8")
            except:
                text = weiboInfo["_source"]["text"]

            wordCount = self.makePredict(text, feature_word_dict)

            if wordCount is not None:
                ads_midWordsMap[weiboInfo["_source"]["mid"]] = set(wordCount.keys())
        return ads_midWordsMap

    def loadfeature_word_dict(self):
        with open(WORD_FEATURE_MAP_FILE) as f:
            reader = csv.reader(f)
            word_dict = dict()
            for line in reader:
                # 中文以utf-8编码,line[1]为特征编号，不用编码
                word_dict[line[0].decode("utf-8")] = line[1]
            return word_dict

    def makePredict(self,text,feature_word_dict):
        '''
        :param text: 微博文本
        :param feature_word_dict: feature的字典
        :return: None表示非广告，如果是广告返回分词后的结果
        '''
        if text.count('@') >= 5 or (u"新浪微博" in text and u"客户端" in text):
            return None
        text = self.cut_filter(text)
        if len(text) == 0 or text == u'转发微博':
            return None

        wordsList = jieba.cut(text)
        # featureCount记录单词特征号的count，用于svm的输入
        featureCount = dict()
        # wordCount 记录单词的count，用于结果返回
        wordCount = dict()
        for word in wordsList:
            if word in feature_word_dict.keys():
                if word in featureCount.keys():
                    featureCount[int(feature_word_dict[word])] += 1
                    wordCount[word] += 1
                else:
                    featureCount[int(feature_word_dict[word])] = 1
                    wordCount[word] = 1
        # print(wordCount)
        label = svmutil.svm_predict_single(featureCount, self.model)
        # print label
        return wordCount if label > 0.5 else None

    def cut_filter(self, text):
        pattern_list = [r'\（分享自 .*\）', r'http://\w*']
        for i in pattern_list:
            p = re.compile(i)
            text = p.sub('', text)
        return text

if __name__ == '__main__':
    a = adsClassify()
    weiboList = []
    #with open(DATA_PATH+"/aaaa.txt") as f:
    #      for line in f:
    #          weiboList.append(line.split("   "))
    weiboList = [[123,u"没有失败只有暂时没有成功 @尼姑可爱多 @木子坊红酒 @傻乎乎飞白  地址：http://t.cn/z8xXuQh"]]
    print a.adsPredict(weiboList)
