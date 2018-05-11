# -*-coding:utf-8-*-

# import uniout  # 编码格式，解决中文输出乱码问题
import jieba
import jieba.analyse
import jieba.posseg as pseg
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import pynlpir
import sys  
reload(sys)  
  
sys.setdefaultencoding('utf-8')

"""
       TF-IDF权重：
           1、CountVectorizer 构建词频矩阵
           2、TfidfTransformer 构建tfidf权值计算
           3、文本的关键字
           4、对应的tfidf矩阵
"""



# jieba分词器通过词频获取关键词
def jieba_keywords(text,n):
	keywords = list(jieba.analyse.extract_tags(text, topK=n,withWeight=False, allowPOS=('n', 'nr', 'nr1', 'nr2', 'nrj', 'nrf', 'ns', 'nsf', 'nt', 'nz','nl','ng','v','vd','vn','vshi','vyou','vf','vx','vi','vl','vg')))
	
    # print "\nkeywords by extract_tags:"
    # for keyword in keywords:
	   #  print keyword + "/",
	   
	#print keywords
	return keywords 
def textrank_keywords(text,n):
	# 引入TextRank关键词抽取接口
	# print "\nkeywords by textrank:"
	# 基于TextRank算法进行关键词抽取
	keywords = list(jieba.analyse.textrank(text,topK = n))
	# 输出抽取出的关键词
	# for keyword in keywords:
	# 	print keyword + '/',
	print keywords
	return keywords
def nlpir_keywords(text,n):
	pynlpir.open()
	# print '关键词测试:\n'
	key_words = list(pynlpir.get_key_words(text,n,weighted=False))
	# for key_word in key_words:
	#     print key_word[0], '\t', key_word[1]
	 
	pynlpir.close()
	
	print key_words
	return key_words
def jieba_fenci(text):
	NOUNSET = set(['n', 'nr', 'nr1', 'nr2', 'nrj', 'nrf', 'ns', 'nsf', 'nt', 'nz','nl','ng','v','vd','vn','vshi','vyou','vf','vx','vi','vl','vg'])
	stopwords = []
	st = {}.fromkeys([ line.rstrip() for line in open('./stop_words_zh.txt','r+')])
	for line in st:
		line = line.strip()
		stopwords.append(line)
	word_list = pseg.cut(text)
	# print word_list
	keywords = []
	for t in word_list:
		if t.word not in stopwords:
			# if t.flag == 'n':
			if t.flag in NOUNSET and len(t.word)>1:
				keywords.append(t.word)
	return keywords

if __name__ == '__main__':
	f = open('keywords_58.txt','w+')  

	text =['北大教授详析：中国房地产是将要破灭的巨大泡沫吗？',
	'东北投资考察曾靠拼酒：商人心里发怵 一下飞机就喝',
	'离岸市场人民币飙升 中国央行疑似干预',
    '中国政法大学教授：金融领域或存在数量庞大腐败隐案',
    '5月财新制造业PMI为49.6  11个月来首次低于荣枯线',
    '多地公布2016年平均工资 统计局释疑你为啥总拖后腿',
    '多地2016年平均工资出炉 官方释疑你为啥总拖后腿',
    '资金荒来袭：银行理财收益率破5%已不罕见 还能涨多久',
    '央行：5月中期借贷便利操作共4590亿元',
    '离岸人民币暴涨千点 这次给空头挖坑的是它',
    '我国结婚登记人数连续三年减少 各产业积极应变',
    '人民日报：逾1.3亿职工缴存住房公积金 人均1.27万',
    '深圳二手住宅均价70周来最低 跌破5万',
    '王蒙徽任住建部党组书记 孙绍骋任国土部党组书记',
    '人民币只是引入新因子而已 涨势如虹大空头去哪了？',
    '专家：为何民众总感觉自己拖了平均工资的“后腿”',
    '中财办官员党报撰文：杠杆率居高不下成金融风险总源头',
    '外汇局：将采集银行卡在境外单笔1000元以上消费信息',
    '走近北上广的实习漂：生活不易 坚强挺过',
    '燕郊楼市调查：房价一平方跌8000元？没这么夸张！']
	for line in text:
		f.write(line+'\n')
		words = jieba_keywords(line,7)
		f.write(' '.join(words)+'\n')
		words = jieba_fenci(line)
		f.write(' '.join(words)+'\n')
	f.close()