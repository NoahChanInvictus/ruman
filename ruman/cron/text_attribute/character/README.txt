人物性格分类：
调用方法
1、根据情绪曲线分类：from test_ch_sentiment import classify_sentiment

【输入】用户id列表，微博列表，查询es的开始时间（字符串），查询es的结束时间（字符串），是否需要再计算情绪（int，1表示需要计算，0表示不需要计算）

输入样例：

示例1（需要计算情感）：[uid1,uid2,uid3,...],[[uid1,text1,ts1],[uid2,text2,ts2],...],'2013-09-01','2013-09-07',1

示例0（不需要计算情感）：[uid1,uid2,uid3,...],[[uid1,text1,s1,ts1],[uid2,text2,s2,ts2],...],'2013-09-01','2013-09-07',0

【输出】字典  uid对应其性格指数：冲动指数+抑郁指数

输出样例:{uid1:{'impulse':w1,'depressed':w2},uid2:{'impulse':w1,'depressed':w2}，...}

'impulse'：冲动指数，'depressed'：抑郁指数

2、根据用户语言分类：from test_ch_topic import classify_topic

【输入】用户id列表，用户微博分词列表

输入样例：[uid1,uid2,uid3,...],{uid1:{'w1':f1,'w2':f2...}...}


【输出】字典  uid对应其性格指数：事业指数+家庭指数
输出样例:{uid1:{'work':w1,'home':w2}，uid2:{'work':w1,'home':w2}，...}

'work'：事业指数，'home'：家庭指数