用户话题分类函数test_topic.py中的topic_classfiy函数

add_dict为扩充语料的代码
test_tfidf为根据语料中词频计算词语的tfidf，去掉tfidf较低的20%的词语


用户话题偏好分类调用方法：
from test_topic import topic_classfiy
函数输入、输出说明：
输入数据示例：
uidlist:uid列表（[uid1,uid2,uid3,...]）
uid_weibo:分词之后的词频字典（{uid1:{'key1':f1,'key2':f2...}...}）

输出数据示例：字典
1、用户18个话题的分布：
{uid1:{'art':0.1,'social':0.2...}...}
2、用户关注较多的话题（最多有3个）：
{uid1:['art','social','media']...}