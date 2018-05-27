# -*- coding: utf-8 -*-

#from extensions import db
from cp_global_config import db

__all__ = ['Topics', 'SentimentKeywords', 'SentimentWeibos', 'SentimentPoint','SentimentGeo', 'SentimentCount', 'SentimentCountRatio',\
        'OpinionTopic', 'OpinionWeibos', 'Opinion', 'OpinionHot', 'CityTopicCount', 'CityTopicCountNews', \
        'CityRepost', 'CityRepostNews','CityWeibos', 'CityNews','PropagateCount', \
        'PropagateCountNews', 'PropagateKeywords', 'PropagateKeywordsNews',\
        'PropagateWeibos', 'PropagateNews', 'AttentionCount', 'QuicknessCount', 'FirstUser','FirstDomainUser',\
           'TopicStatus', 'TopicIdentification', 'OpinionTestRatio',\
          'OpinionTestTime', 'OpinionTestKeywords', 'OpinionTestWeibos', 'IndexTopic', 'OpinionWeibosNew',\
          'FirstUserNews', 'TrendMakerNews', 'TrendPusherNews']


class Topics(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(20))
    start_ts = db.Column(db.BigInteger(10, unsigned=True))
    end_ts = db.Column(db.BigInteger(10, unsigned=True))

    def __init__(self, topic, start_ts, end_ts):
        self.topic = topic
        self.start_ts = start_ts
        self.end_ts = end_ts 

    @classmethod
    def _name(cls):
        return u'Topics'

#实际上这一部分是需要重新修改的，但是在此次测试中用不到，就先不动。
#sentiment部分
class SentimentKeywords(db.Model):#情绪关键词---已改
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    query = db.Column(db.String(20))
    end = db.Column(db.BigInteger(10, unsigned=True))
    range = db.Column(db.BigInteger(10, unsigned=True))
    limit = db.Column(db.BigInteger(10, unsigned=True))
    sentiment = db.Column(db.Integer(1, unsigned=True))
    kcount = db.Column(db.Text)

    def __init__(self, query, range, limit, end, sentiment, kcount):
        self.query = query 
        self.range = range
        self.limit = limit
        self.end = end
        self.sentiment = sentiment
        self.kcount = kcount

    @classmethod
    def _name(cls):
        return u'SentimentKeywords'

class SentimentWeibos(db.Model):#情绪微博--已改
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    query = db.Column(db.String(20))
    end = db.Column(db.BigInteger(10, unsigned=True))
    range = db.Column(db.BigInteger(10, unsigned=True))
    limit = db.Column(db.BigInteger(10, unsigned=True))
    sentiment = db.Column(db.Integer(1, unsigned=True))
    weibos = db.Column(db.Text)

    def __init__(self, query, range, limit, end, sentiment, weibos):
        self.query = query 
        self.range = range
        self.limit = limit
        self.end = end
        self.sentiment = sentiment
        self.weibos = weibos

    @classmethod
    def _name(cls):
        return u'SentimentWeibos'

class SentimentPoint(db.Model):#情绪拐点
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(20))#话题名
    stype = db.Column(db.String(20))#拐点情绪类型标签（'happy','angry','sad'）
    ts = db.Column(db.BigInteger(20, unsigned=True))#拐点时间

    def __init__(self, topic, stype, ts):
        self.topic = topic
        self.stype = stype
        self.ts = ts

    @classmethod
    def _name(cls):
        return u'SentimentPoint'

class SentimentCount(db.Model):#情绪绝对数量曲线--已改
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    query = db.Column(db.String(20))
    end = db.Column(db.BigInteger(10, unsigned=True))
    range = db.Column(db.BigInteger(10, unsigned=True))
    sentiment = db.Column(db.Integer(1, unsigned=True))
    count = db.Column(db.BigInteger(20, unsigned=True))

    def __init__(self, query, range, end, sentiment, count):
        self.query = query 
        self.range = range
        self.end = end
        self.sentiment = sentiment
        self.count = count

    @classmethod
    def _name(cls):
        return u'SentimentCount'

class SentimentCountRatio(db.Model):#情绪相对比例曲线--已改
    id = db.Column(db.Integer, primary_key=True)
    query = db.Column(db.String(20))#话题名
    end = db.Column(db.BigInteger(20, unsigned=True))#时间
    range = db.Column(db.BigInteger(10, unsigned=True))
    count = db.Column(db.BigInteger(20, unsigned=True))
    allcount = db.Column(db.BigInteger(20, unsigned=True))
    sentiment = db.Column(db.Integer(1, unsigned=True))#情绪类型（'happy','angry','sad'）

    def __init__(self, query, end, range, sentiment, count, allcount):
        self.query = query
        self.end = end
        self.ts = ts
        self.count = count
        self.allcount = allcount
        self.sentiment = sentiment

    @classmethod
    def _name(cls):
        return u'SentimentCountRatio'

# Index 模块
class IndexTopic(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    topic = db.Column(db.Text)
    count = db.Column(db.Integer) # 微博数
    user_count = db.Column(db.Integer) # 用户数
    begin = db.Column(db.BigInteger(10,unsigned = True)) # 起始时间
    end = db.Column(db.BigInteger(10,unsigned = True)) # 终止时间
    area = db.Column(db.Text) # 地理区域
    key_words = db.Column(db.Text) # 关键词
    opinion = db.Column(db.Text) # 代表文本
    media_opinion = db.Column(db.Text) # 媒体观点

    def __init__(self, topic, count, user_count, begin, end, area, key_words, opinion, media_opinion):
        self.topic = topic
        self.count = count
        self.user_count = user_count
        self.begin = begin
        self.end = end
        self.area = area
        self.key_words = key_words
        self.opinion = opinion
        self.media_opinion = media_opinion

    @classmethod
    def _name(cls):
        return u'IndexTopic'

#city模块
class CityTopicCount(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(20))
    end = db.Column(db.BigInteger(10, unsigned=True))
    range = db.Column(db.BigInteger(10, unsigned=True))
    mtype = db.Column(db.Integer(1, unsigned=True))  #message_type:原创-1、转发-2、评论-3
    ccount = db.Column(db.Text)                      #city_count:{city:count}
    first_item = db.Column(db.Text)          # 原创 初始微博 其他类型为空

    def __init__(self, topic, range, end, mtype, ccount, first_item):
        self.topic = query 
        self.range = range
        self.end = end
        self.mtype = mtype
        self.ccount = ccount
        self.first_item = first_item

    @classmethod
    def _name(cls):
        return u'CityTopicCount'

class CityTopicCountNews(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(20))
    end = db.Column(db.BigInteger(10, unsigned=True))
    range = db.Column(db.BigInteger(10, unsigned=True))
    mtype = db.Column(db.Integer(1, unsigned=True))  #message_type:原创-1、转发-2
    ccount = db.Column(db.Text)                      #city_count:{city:count}
    first_item = db.Column(db.Text)          # 原创 初始微博 其他类型为空

    def __init__(self, topic, range, end, mtype, ccount, first_item):
        self.topic = query 
        self.range = range
        self.end = end
        self.mtype = mtype
        self.ccount = ccount
        self.first_item = first_item

    @classmethod
    def _name(cls):
        return u'CityTopicCountNews'

class CityRepost(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    original = db.Column(db.Integer(1,unsigned = True))
    topic = db.Column(db.String(20))
    mid = db.Column(db.String(20)) # 微博ID
    ts = db.Column(db.BigInteger(20, unsigned=True))
    origin_location = db.Column(db.Text) # 原始微博发布地点
    repost_location = db.Column(db.Text) # 转发微博发布地点

    def __init__(self, original, topic, mid, ts, origin_location, repost_location ):
        self.topic = topic
        self.original = original
        self.mid = mid
        self.ts = ts
        self.origin_location = origin_location
        self.repost_location = repost_location

    @classmethod
    def _name(cls):
        return u'CityRepost'

class CityRepostNews(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    original = db.Column(db.Integer(1,unsigned = True))
    topic = db.Column(db.String(20))
    mid = db.Column(db.String(20)) # 新闻ID
    ts = db.Column(db.BigInteger(20, unsigned=True))
    origin_location = db.Column(db.Text) # 原始新闻发布地点
    repost_location = db.Column(db.Text) # 转发新闻发布地点

    def __init__(self, original, topic, mid, ts, origin_location, repost_location ):
        self.topic = topic
        self.original = original
        self.mid = mid
        self.ts = ts
        self.origin_location = origin_location
        self.repost_location = repost_location

    @classmethod
    def _name(cls):
        return u'CityRepostNews'

class CityWeibos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(20))
    end = db.Column(db.BigInteger(10, unsigned=True))
    range = db.Column(db.BigInteger(10, unsigned=True))
    limit = db.Column(db.BigInteger(10, unsigned=True), primary_key=True)
    weibos = db.Column(db.Text) # weibos=[weibos]

    def __init__(self, topic, end, range, limit, weibos):
        self.topic = topic
        self.end = end
        self.range = range
        self.limit = limit
        self.weibos = weibos

    @classmethod
    def _name(cls):
        return u'CityWeibos'

class CityNews(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(20))
    end = db.Column(db.BigInteger(10, unsigned=True))
    range = db.Column(db.BigInteger(10, unsigned=True))
    limit = db.Column(db.BigInteger(10, unsigned=True), primary_key=True)
    news = db.Column(db.Text) # news=[news]

    def __init__(self, topic, end, range, limit, news):
        self.topic = topic
        self.end = end
        self.range = range
        self.limit = limit
        self.news = news

    @classmethod
    def _name(cls):
        return u'CityNews'

#时间分析模块
class PropagateCount(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(20))
    end = db.Column(db.BigInteger(10, unsigned=True))
    range = db.Column(db.BigInteger(10, unsigned=True))
    mtype = db.Column(db.Integer(1, unsigned=True))   
    dcount = db.Column(db.Text) # dcount={domain:count}领域对应的count                      

    def __init__(self, topic, range, end, mtype, dcount):
        self.topic = topic 
        self.range = range
        self.end = end
        self.mtype = mtype
        self.dcount = dcount

    @classmethod
    def _name(cls):
        return u'PropagateCount'

class PropagateCountNews(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(20))
    end = db.Column(db.BigInteger(10, unsigned=True))
    range = db.Column(db.BigInteger(10, unsigned=True))
    mtype = db.Column(db.Integer(1, unsigned=True))   
    dcount = db.Column(db.Text) # dcount={'other':count}领域对应的count                      

    def __init__(self, topic, range, end, mtype, dcount):
        self.topic = topic 
        self.range = range
        self.end = end
        self.mtype = mtype
        self.dcount = dcount

    @classmethod
    def _name(cls):
        return u'PropagateCountNews'

class AttentionCount(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(20))
    end = db.Column(db.BigInteger(10, unsigned=True))
    range = db.Column(db.BigInteger(10, unsigned=True))
    mtype = db.Column(db.Integer(1, unsigned=True))   
    domain = db.Column(db.String(20))
    covernum = db.Column(db.BigInteger(20, unsigned=True))
    allnum = db.Column(db.BigInteger(20, unsigned=True))

    def __init__(self, topic, range, end, mtype, domain, covernum, allnum):
        self.topic = topic
        self.range = range
        self.end = end
        self.mtype = mtype
        self.domain = domain
        self.covernum = covernum
        self.allnum = allnum

    @classmethod
    def _name(cls):
        return u'AttentionCount'

class QuicknessCount(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(20))
    end = db.Column(db.BigInteger(10, unsigned=True))
    range = db.Column(db.BigInteger(10, unsigned=True))
    mtype = db.Column(db.Integer(1, unsigned=True))   
    domain = db.Column(db.String(20))
    topnum = db.Column(db.BigInteger(20, unsigned=True))
    allnum = db.Column(db.BigInteger(20, unsigned=True))

    def __init__(self, topic, range, end, mtype, domain, topnum, allnum):
        self.topic = topic
        self.range = range
        self.end = end
        self.mtype = mtype
        self.domain = domain
        self.topnum = topnum
        self.allnum = allnum

    @classmethod
    def _name(cls):
        return u'QuicknessCount'

class PropagateKeywords(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(20))
    end = db.Column(db.BigInteger(10, unsigned=True))
    range = db.Column(db.BigInteger(10, unsigned=True))
    mtype = db.Column(db.Integer(1, unsigned=True))
    limit = db.Column(db.BigInteger(10, unsigned=True), primary_key=True)
    kcount = db.Column(db.Text) # kcount=[terms]

    def __init__(self, topic, end, range, mtype, limit, kcount):
        self.topic = topic
        self.end = end
        self.range = range
        self.limit = limit
        self.mtype = mtype
        self.kcount = kcount

    @classmethod
    def _name(cls):
        return u'PropagateKeywords'

class PropagateKeywordsNews(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(20))
    end = db.Column(db.BigInteger(10, unsigned=True))
    range = db.Column(db.BigInteger(10, unsigned=True))
    mtype = db.Column(db.Integer(1, unsigned=True))
    limit = db.Column(db.BigInteger(10, unsigned=True), primary_key=True)
    kcount = db.Column(db.Text) # kcount=[terms]

    def __init__(self, topic, end, range, mtype, limit, kcount):
        self.topic = topic
        self.end = end
        self.range = range
        self.limit = limit
        self.mtype = mtype
        self.kcount = kcount

    @classmethod
    def _name(cls):
        return u'PropagateKeywordsNews'

class PropagateWeibos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(20))
    end = db.Column(db.BigInteger(10, unsigned=True))
    range = db.Column(db.BigInteger(10, unsigned=True))
    mtype = db.Column(db.Integer(1, unsigned=True))
    limit = db.Column(db.BigInteger(10, unsigned=True), primary_key=True)
    weibos = db.Column(db.Text) # weibos=[weibos]

    def __init__(self, topic, end, range, mtype, limit, weibos):
        self.topic = topic
        self.end = end
        self.range = range
        self.mtype = mtype
        self.limit = limit
        self.weibos = weibos

    @classmethod
    def _name(cls):
        return u'PropagateWeibos'

class PropagateNews(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(20))
    end = db.Column(db.BigInteger(10, unsigned=True))
    range = db.Column(db.BigInteger(10, unsigned=True))
    mtype = db.Column(db.Integer(1, unsigned=True))
    limit = db.Column(db.BigInteger(10, unsigned=True), primary_key=True)
    news = db.Column(db.Text) # news=[news]

    def __init__(self, topic, end, range, mtype, limit, news):
        self.topic = topic
        self.end = end
        self.range = range
        self.mtype = mtype
        self.limit = limit
        self.news = news

    @classmethod
    def _name(cls):
        return u'PropagateNews'

class TopicStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    module = db.Column(db.String(10))# 显示是哪个模块---moodlens/evolution/propagate/identify
    status = db.Column(db.Integer)# 1: completed 0: computing, -1:not compute, -2:delete
    topic = db.Column(db.Text)
    start = db.Column(db.BigInteger(10, unsigned=True))#起始时间
    end = db.Column(db.BigInteger(10, unsigned=True))#终止时间
    db_date = db.Column(db.BigInteger(10, unsigned=True))#入库时间❯

    def __init__(self, module, status, topic, start, end, db_date):
        self.module = module
        self.status = status
        self.topic = topic
        self.start = start
        self.end = end
        self.db_date = db_date

    @classmethod
    def _name(cls):
        return u'TopicStatus'

class NewTopicStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    module = db.Column(db.String(20))
    start_ts = db.Column(db.BigInteger(10, unsigned=True))
    end_ts = db.Column(db.BigInteger(10, unsigned=True))
    category = db.Column(db.String(20))
    db_date = db.Column(db.Date)
    status = db.Column(db.Integer)

    def __init__(self, module, start_ts, end_ts, category, db_date, status):
        self.module = module
        self.start_ts = start_ts
        self.end_ts = end_ts
        self.category = category
        self.db_date = db_date
        self.status = status

    @classmethod
    def _name(cls):
        return u'NewTopicStatus'

#网络模块--存放pagerank的计算结果
class TopicIdentification(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(20))
    rank = db.Column(db.Integer)
    userId = db.Column(db.BigInteger(11, unsigned=True))
    identifyDate = db.Column(db.Date)
    identifyWindow = db.Column(db.Integer, default=1)
    identifyMethod = db.Column(db.String(20), default='pagerank')
    pr = db.Column(db.Float)

    def __init__(self, topic, rank, userId, identifyDate, identifyWindow, identifyMethod, pr):
        self.topic = topic
        self.rank = rank
        self.userId = userId
        self.identifyDate = identifyDate
        self.identifyWindow = identifyWindow
        self.identifyMethod = identifyMethod
        self.pr = pr

    @classmethod
    def _name(cls):
        return u'TopicIdentification'

class DsTopicIdentification(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(20))
    rank = db.Column(db.Integer)
    userId = db.Column(db.BigInteger(11, unsigned=True))
    identifyDate = db.Column(db.Date)
    identifyWindow = db.Column(db.Integer, default=1)
    identifyMethod = db.Column(db.String(20), default='pagerank')
    pr = db.Column(db.String(20), default='pagerank')

    def __init__(self, topic, rank, userId, identifyDate, identifyWindow, identifyMethod, pr):
        self.topic = topic
        self.rank = rank
        self.userId = userId
        self.identifyDate = identifyDate
        self.identifyWindow = identifyWindow
        self.identifyMethod = identifyMethod
        self.pr = pr

    @classmethod
    def _name(cls):
        return u'DsTopicIdentification'

class TsRank(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(20))
    rank = db.Column(db.Integer)
    uid = db.Column(db.BigInteger(11, unsigned=True))
    date = db.Column(db.Date)
    windowsize = db.Column(db.Integer, default=1)
    tr = db.Column(db.Float)

    def __init__(self, topic, rank, uid, date, windowsize, tr):
        self.topic = topic
        self.rank = rank
        self.uid = uid
        self.date = date
        self.windowsize = windowsize
        self.tr = tr

    @classmethod
    def _name(cls):
        return u'TsRank'

class DegreeCentralityUser(db.Model): 
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(20))
    date = db.Column(db.Date)
    windowsize = db.Column(db.Integer, default=1)
    rank  = db.Column(db.Integer)
    userid = db.Column(db.BigInteger(11, unsigned=True))
    dc = db.Column(db.Float)

    def __init__(self, topic, date, windowsize, rank, userid, dc):
        self.topic = topic
        self.date = date
        self.windowsize = windowsize
        self.rank = rank
        self.userid = userid
        self.dc = dc

    @classmethod
    def _name(cls):
        return u'DegreeCentralityUser'

class DsDegreeCentralityUser(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(20))
    date = db.Column(db.Date)
    windowsize = db.Column(db.Integer, default=1)
    rank = db.Column(db.Integer)
    userid = db.Column(db.BigInteger(11, unsigned=True))
    dc = db.Column(db.Float)

    def __init__(self, topic, date, windowsize, rank, userid, dc):
        self.topic = topic
        self.date = date
        self.windowsize = windowsize
        self.rank = rank
        self.userid = userid
        self.dc = dc

    @classmethod
    def _name(cls):
        return u'DsDegreeCentralityUser'

class BetweenessCentralityUser(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(20))
    date = db.Column(db.Date)
    windowsize = db.Column(db.Integer, default=1)
    rank  = db.Column(db.Integer)
    userid = db.Column(db.BigInteger(11, unsigned=True))
    bc = db.Column(db.Float)

    def __init__(self, topic, date, windowsize, rank, userid, bc):
        self.topic =topic
        self.date = date
        self.windowsize = windowsize
        self.rank = rank
        self.userid = userid
        self.bc = bc

    @classmethod
    def _name(cls):
        return u'BetweenessCentralityUser'

class DsBetweenessCentralityUser(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(20))
    date = db.Column(db.Date)
    windowsize = db.Column(db.Integer, default=1)
    rank = db.Column(db.Integer)
    userid = db.Column(db.BigInteger(11, unsigned=True))
    bc = db.Column(db.Float)

    def __init__(self, topic, date, windowsize, rank, userid, bc):
        self.topic = topic
        self.date = date
        self.windowsize = windowsize
        self.rank = rank
        self.userid = userid
        self.bc = bc

    @classmethod
    def _name(cls):
        return u'DsBetweenessCentralityUser'

class ClosenessCentralityUser(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(20))
    date = db.Column(db.Date)
    windowsize = db.Column(db.Integer, default=1)
    rank  = db.Column(db.Integer)
    userid = db.Column(db.BigInteger(11, unsigned=True))
    cc = db.Column(db.Float)

    def __init__(self, topic, date, windowsize, rank, userid, cc):
        self.topic = topic
        self.date = date
        self.windowsize = windowsize
        self.rank = rank
        self.userid = userid
        self.cc = cc

    @classmethod
    def _name(cls):
        return u'ClosenessCentralityUser'

class DsClosenessCentralityUser(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(20))
    date = db.Column(db.Date)
    windowsize = db.Column(db.Integer, default=1)
    rank = db.Column(db.Integer)
    userid = db.Column(db.BigInteger(11, unsigned=True))
    cc= db.Column(db.Float)

    def __init__(self, topic, date, windowsize, rank , userid, cc):
        self.topic = topic
        self.date = date
        self.windowsize = windowsize
        self.rank = rank
        self.userid = userid
        self.cc = cc

    @classmethod
    def _name(cls):
        return u'DsClosenessCentralityUser'
        
'''
class NodeDegreeUser(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(20))
    date = db.Column(db.Date)
    windowsize = db.Column(db.Integer, default=1)
    sorted_dict = db.Column(db.Text)

    def __init__(self, topic, date, windowsize, sorted_dict):
        self.topic = topic
        self.date = date
        self.windowsize = windowsize
        self.sorted_dict = sorted_dict
'''

class LocalBridge(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(20))
    date = db.Column(db.Date)
    windowsize = db.Column(db.Integer, default=1)
    a_node = db.Column(db.BigInteger(11, unsigned=True))
    b_node = db.Column(db.BigInteger(11, unsigned=True))
    span_ab = db.Column(db.Integer)

    def __init__(self, topic, date, windowsize, a_node, b_node, span_ab):
        self.topic = topic
        self.date = date
        self.windowsize = windowsize
        self.a_node = a_node
        self.b_node = b_node
        self.span_ab = span_ab

    @classmethod
    def _name(cls):
        return u'LocalBridge'

class Source(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(20))
    date = db.Column(db.Date)
    windowsize = db.Column(db.Integer, default=1)
    userid = db.Column(db.BigInteger(20, unsigned=True))

    def __init__(self, topic, date, windowsize, userid):
        self.topic = topic
        self.date = date
        self.windowsize = windowsize
        self.userid = userid

    @classmethod
    def _name(cls):
        return u'Source'

class FirstUser(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(20))
    date = db.Column(db.Date)
    windowsize = db.Column(db.Integer, default=1)
    uid = db.Column(db.BigInteger(11, unsigned=True))
    timestamp = db.Column(db.BigInteger(20, unsigned=True))
    user_info = db.Column(db.Text)
    weibo_info = db.Column(db.Text)
    user_domain = db.Column(db.String(20))

    def __init__(self, topic, date, windowsize, uid, timestamp, user_info, weibo_info, user_domain):
        self.topic =topic
        self.date = date
        self.windowsize = windowsize
        self.uid = uid
        self.timestamp = timestamp
        self.user_info = user_info
        self.weibo_info = weibo_info
        self.user_domain = user_domain

    @classmethod
    def _name(cls):
        return u'FirstUser'

class FirstUserNews(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(20))
    start_ts = db.Column(db.BigInteger(20, unsigned=True))
    end_ts = db.Column(db.BigInteger(20, unsigned=True))
    timestamp = db.Column(db.BigInteger(20, unsigned=True))
    news_info = db.Column(db.Text)

    def __init__(self, topic, start_ts, end_ts, timestamp, news_info):
        self.topic = topic
        self.start_ts = start_ts
        self.end_ts = end_ts
        self.timestamp = timestamp
        self.news_info = news_info

    @classmethod
    def _name(cls):
        return u'FirstUserNews'

class TrendMakerNews(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(20))
    start_ts = db.Column(db.BigInteger(20, unsigned=True))
    end_ts = db.Column(db.BigInteger(20, unsigned=True))
    news_id = db.Column(db.Text)
    timestamp = db.Column(db.BigInteger(20, unsigned=True))
    weight = db.Column(db.Float)
    news_info = db.Column(db.Text)

    def __init__(self, topic, start_ts, end_ts, news_id, timestamp, weight, news_info):
        self.topic = topic
        self.start_ts = start_ts
        self.end_ts = end_ts
        self.news_id = news_id
        self.timestamp = timestamp
        self.weight = weight
        self.news_info = news_info
    
    @classmethod
    def _name(cls):
        return u'TrendMakerNews'

class TrendPusherNews(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(20))
    start_ts = db.Column(db.BigInteger(20, unsigned=True))
    end_ts = db.Column(db.BigInteger(20, unsigned=True))
    news_id = db.Column(db.Text)
    timestamp = db.Column(db.BigInteger(20, unsigned=True))
    comments_count = db.Column(db.Integer)
    news_info = db.Column(db.Text)

    def __init__(self, topic, start_ts, end_ts, news_id, timestamp, comments_count, news_info):
        self.topic = topic
        self.start_ts = start_ts
        self.end_ts = end_ts
        self.news_id = news_id
        self.timestamp = timestamp
        self.comments_count = comments_count
        self.news_info = news_info

    @classmethod
    def _name(cls):
        return u'TrendPusherNews'

class FirstDomainUser(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(20))
    date = db.Column(db.Date)
    windowsize = db.Column(db.Integer, default=1)
    uid = db.Column(db.BigInteger(11, unsigned=True))
    timestamp = db.Column(db.BigInteger(20, unsigned=True))
    user_info = db.Column(db.Text)
    weibo_info = db.Column(db.Text)
    user_domain = db.Column(db.String(20))
    rank = db.Column(db.Integer)

    def __init__(self, topic, date, windowsize, uid, timestamp, user_info, weibo_info, user_domain, rank):
        self.topic = topic
        self.date = date
        self.windowsize = windowsize
        self.uid = uid
        self.timestamp = timestamp
        self.user_info = user_info
        self.weibo_info = weibo_info
        self.user_domain = domain
        self.rank = rank

    @classmethod
    def _name(cls):
        return u'FirstDomainUser'

class TrendMaker(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(20))
    date = db.Column(db.Date)
    windowsize = db.Column(db.Integer, default=1)
    uid = db.Column(db.BigInteger(11, unsigned=True))
    timestamp = db.Column(db.BigInteger(20, unsigned=True))
    user_info = db.Column(db.Text)
    weibo_info = db.Column(db.Text)
    domain = db.Column(db.String(20))
    rank = db.Column(db.Integer)
    value = db.Column(db.Integer)
    key_item = db.Column(db.Text)

    def __init__(self, topic, date, windowsize, uid, timestamp, user_info, weibo_info, domain, rank, value, key_item):
        self.topic = topic
        self.date = date
        self.windowsize = windowsize
        self.uid = uid
        self.timestamp = timestamp
        self.user_info = user_info
        self.weibo_info = weibo_info
        self.domain = domain
        self.rank = rank
        self.value = value
        self.key_item = key_item
    
    @classmethod
    def _name(cls):
        return u'TrendMaker'

class TrendPusher(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(20))
    date = db.Column(db.Date)
    windowsize = db.Column(db.Integer, default=1)
    uid = db.Column(db.BigInteger(11, unsigned=True))
    timestamp = db.Column(db.BigInteger(20, unsigned=True))
    user_info = db.Column(db.Text)
    weibo_info = db.Column(db.Text)
    domain = db.Column(db.String(20))
    rank = db.Column(db.Integer)

    def __init__(self, topic, date, windowsize, uid, timestamp, user_info, weibo_info, domain, rank):
        self.topic = topic
        self.date = date
        self.windowsize = windowsize
        self.uid = uid
        self.timestamp = timestamp
        self.user_info = user_info
        self.weibo_info = weibo_info
        self.domain = domain
        self.rank = rank

    @classmethod
    def _name(cls):
        return u'TrendPusher'

class TrendKeyUser(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(20))
    date = db.Column(db.Date)
    windowsize = db.Column(db.Integer, default=1)
    maker = db.Column(db.Text)
    pusher = db.Column(db.Text)

    def __init__(self, topic, date, windowsize, maker, pusher):
        self.topic = topic
        self.date = date
        self.windowsize = windowsize
        self.maker = maker
        self.pusher = pusher

    @classmethod
    def _name(cls):
        return u'TrendKeyUser'



class AllFrequentUser(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    db_time = db.Column(db.Date)
    ffu_kind = db.Column(db.String(20))
    user_frequent = db.Column(db.Text)

    def __init__(self, db_time, ffu_kind, user_frequent):
        self.db_time = db_time
        self.ffu_kind = ffu_kind
        self.user_frequent = user_frequent

    @classmethod
    def _name(cls):
        return u'AllFrequentUser'

# opinion module used in test
class OpinionTestTime(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(20))
    child_topic = db.Column(db.Text)
    start_ts = db.Column(db.BigInteger(20, unsigned=True))
    end_ts = db.Column(db.BigInteger(20, unsigned=True))

    def __init__(self, topic, child_topic, start_ts, end_ts):
        self.topic = topic
        self.child_topic = child_topic
        self.start_ts = start_ts
        self.end_ts = end_ts

    @classmethod
    def _name(cls):
        return u'OpinionTestTime'

class OpinionTestRatio(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(20))
    #ts = db.clumns(db.BigInteger(10),unsigned=True)
    child_topic = db.Column(db.Text)
    ratio = db.Column(db.Float)

    def __init__(self, topic, child_topic, ratio):
        self.topc = topic
        self.child_topic = child_topic
        self.ratio = ratio

    @classmethod
    def _name(cls):
        return u'OpinionTestRatio'

class OpinionTestKeywords(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(20))
    child_topic = db.Column(db.Text)
    keywords = db.Column(db.Text)

    def __init__(self, topic, child_topic, keywords):
        self.topic = topic
        self.child_topic = child_topic
        self.keywords = keywords

    @classmethod
    def _name(cls):
        return u'OpinionTestKeywords'

class OpinionTestWeibos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(20))
    child_topic = db.Column(db.String(20))
    weibos = db.Column(db.Text)

    def __init__(self, topic, child_topic, weibos):
        self.topic = topic
        self.child_topic = child_topic
        self.weibos = weibos

    @classmethod
    def _name(cls):
        return u'OpinionTestWeibos'

class OpinionWeibosNew(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(20))
    child_topic = db.Column(db.Text)
    weight = db.Column(db.Float)
    mid = db.Column(db.String(20))
    uid = db.Column(db.String(20))
    weibos = db.Column(db.Text)
    time = db.Column(db.String(20))    
    r_count = db.Column(db.Integer)
    c_count = db.Column(db.Integer)
    repeat = db.Column(db.Integer)

    def __init__(self, topic, child_topic, weight, mid, uid, weibos, time, r_count, c_count, repeat):
        self.topic = topic
        self.child_topic = child_topic
        self.weight = weight
        self.mid = mid
        self.uid = uid
        self.weibos = weibos
        self.time = time        
        self.r_count = r_count
        self.c_count = c_count
        self.repeat = repeat

    @classmethod
    def _name(cls):
        return u'OpinionWeibosNew'

# Quota_system Module
class QuotaAttention(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(20))
    start_ts = db.Column(db.BigInteger(10, unsigned=True))
    end_ts = db.Column(db.BigInteger(10, unsigned=True))
    domain = db.Column(db.String(20))
    attention = db.Column(db.Float)

    def __init__(self, topic, start_ts, end_ts, domain, attention):
        self.topic = topic
        self.start_ts = start_ts
        self.end_ts = end_ts
        self.domain = domain
        self.attention = attention

    @classmethod
    def _name(cls):
        return u'QuotaAttention'

# 关注度经验值QuotaAttentionExp
class QuotaAttentionExp(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(20))
    start_ts = db.Column(db.BigInteger(10, unsigned=True))
    end_ts = db.Column(db.BigInteger(10, unsigned=True))
    exp = db.Column(db.Text) # exp={'media':x1, 'other':x2, 'opinion_leader':x3, 'oversea':x4, 'folk':x5}

    def __init__(self, topic, start_ts, end_ts, exp):
        self.topic = topic
        self.start_ts = start_ts
        self.end_ts = end_ts
        self.exp = exp

    @classmethod
    def _name(cls):
        return u'QuotaAttentionExp'

# QuotaPenetration 弃用
# 分为两个：QuotaMediaImportance, QuotaGeoPenetration
class QuotaMediaImportance(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(20))
    start_ts = db.Column(db.BigInteger(10, unsigned=True))
    end_ts = db.Column(db.BigInteger(10, unsigned=True))
    media_importance = db.Column(db.Float)

    def __init__(self, topic, start_ts, end_ts, media_importance):
        self.topic =topic
        self.start_ts = start_ts
        self.end_ts = end_ts
        self.media_importance = media_importance

    @classmethod
    def _name(cls):
        return u'QuotaMediaImportance'

class QuotaGeoPenetration(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(20))
    start_ts = db.Column(db.BigInteger(10, unsigned=True))
    end_ts = db.Column(db.BigInteger(10, unsigned=True))
    pcount = db.Column(db.Text)

    def __init__(self, topic, start_ts, end_ts, pcount):
        self.topic = topic
        self.start_ts = start_ts
        self.end_ts = end_ts
        self.pcount = pcount

    @classmethod
    def _name(cls):
        return u'QuotaGeoPenetration'

class GeoWeight(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    weight_dict = db.Column(db.Text)

    def __init__(self, weight_dict):
        self.weight_dict = weight_dict

    @classmethod
    def _name(cls):
        return u'GeoWeight'

class QuotaQuickness(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(20))
    start_ts = db.Column(db.BigInteger(10, unsigned=True))
    end_ts = db.Column(db.BigInteger(10, unsigned=True))
    domain = db.Column(db.String(20))
    quickness = db.Column(db.Float)

    def __init__(self, topic, start_ts, end_ts, domain, quickness):
        self.topic = topic
        self.start_ts = start_ts
        self.end_ts = end_ts
        self.domain = domain
        self.quickness = quickness

    @classmethod
    def _name(cls):
        return u'QuotaQuickness'

class QuotaSentiment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(20))
    start_ts = db.Column(db.BigInteger(10, unsigned=True))
    end_ts = db.Column(db.BigInteger(10, unsigned=True))
    sratio = db.Column(db.Text)
    
    def __init__(self, topic, start_ts, end_ts, sratio):
        self.topic = topic
        self.start_ts = start_ts
        self.end_ts = end_ts
        self.sratio = sratio

    @classmethod
    def _name(cls):
        return u'QuotaSentiment'

class QuotaDuration(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(20))
    start_ts = db.Column(db.BigInteger(10, unsigned=True))
    end_ts = db.Column(db.BigInteger(10, unsigned=True))
    duration = db.Column(db.Float)

    def __init__(self, topic, start_ts, end_ts, duration):
        self.topic = topic
        self. start_ts = start_ts
        self.end_ts = end_ts
        self.duration = duration

    @classmethod
    def _name(cls):
        return u'QuotaDuration'

# 持续度经验值QuotaDurationExp
class QuotaPersonSensitivity(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(20))
    start_ts = db.Column(db.BigInteger(10, unsigned=True))
    end_ts = db.Column(db.BigInteger(10, unsigned=True))
    pr = db.Column(db.Float)

    def __init__(self, topic, start_ts, end_ts, pr):
        self.topic = topic
        self.start_ts = start_ts
        self.end_ts = end_ts
        self.pr = pr

    @classmethod
    def _name(cls):
        return u'QuotaPersonSensitivity'

class PersonSensitivity(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(20))
    start_ts = db.Column(db.BigInteger(10, unsigned=True))
    end_ts = db.Column(db.BigInteger(10, unsigned=True))
    person = db.Column(db.Text)
    
    def __init__(self, topic, start_ts, end_ts, person):
        self.topic = topic
        self.start_ts = start_ts
        self_end_ts = end_ts
        self.person = person
    
    @classmethod
    def _name(cls):
        return u'PersonSensitivity'

class QuotaDurationExp(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(20))
    start_ts = db.Column(db.BigInteger(10, unsigned=True))
    end_ts = db.Column(db.BigInteger(10, unsigned=True))
    exp = db.Column(db.Float)

    def __init__(self, topic, start_ts, end_ts, exp):
        self.topic = topic
        self.start_ts = start_ts
        self.end_ts = end_ts
        self.exp = exp
    
    @classmethod
    def _name(cls):
        return u'QuotaDurationExp'

class QuotaSensitivity(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(20))
    start_ts = db.Column(db.BigInteger(10, unsigned=True))
    end_ts = db.Column(db.BigInteger(10, unsigned=True))
    classfication = db.Column(db.Integer(1, unsigned=True)) # ['category':1, 'word':2, 'place':3]
    score = db.Column(db.Float) # 1<=score<=5

    def __init__(self, topic, start_ts, end_ts, classfication, score):
        self.topic = topic
        self.start_ts = start_ts
        self.end_ts = end_ts
        self.classfication = classfication
        self.score = score

    @classmethod
    def _name(cls):
        return u'QuotaSensitivity'

# 类型敏感词表、词汇敏感词表、地点敏感词表
class ClassSensitivity(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(20))
    start_ts = db.Column(db.BigInteger(10, unsigned=True))
    end_ts = db.Column(db.BigInteger(10, unsigned=True))
    words = db.Column(db.Text)

    def __init__(self, topic, start_ts, end_ts, words):
        self.topic = topic
        self.start_ts = start_ts
        self.end_ts = end_ts
        self.words = words

    @classmethod
    def _name(cls):
        return u'ClassSensitivity'

class WordSensitivity(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(20))
    start_ts = db.Column(db.BigInteger(10, unsigned=True))
    end_ts = db.Column(db.BigInteger(10, unsigned=True))
    words = db.Column(db.Text)

    def __init__(self, topic, start_ts, end_ts, words):
        self.topic = topic
        self.start_ts = start_ts
        self.end_ts = end_ts
        self.words = words

    @classmethod
    def _name(cls):
        return u'WordSensitivity'

class PlaceSensitivity(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(20))
    start_ts = db.Column(db.BigInteger(10, unsigned=True))
    end_ts = db.Column(db.BigInteger(10, unsigned=True))
    words = db.Column(db.Text)

    def __init__(self, topic, start_ts, end_ts, words):
        self.topic = topic
        self.start_ts = start_ts
        self.end_ts = end_ts
        self.words = words

    @classmethod
    def _name(cls):
        return u'PlaceSensitivity'

class QuotaImportance(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(20))
    start_ts = db.Column(db.BigInteger(10, unsigned=True))
    end_ts = db.Column(db.BigInteger(10, unsigned=True))
    score = db.Column(db.Float)
    weight = db.Column(db.Float) # 0<=weight<=1

    def __init__(self, topic, start_ts, end_ts, score, weight):
        self.topic = topic
        self.start_ts = start_ts
        self.end_ts = end_ts
        self.score = score # 0<=score<1
        self.weight = weight

    @classmethod
    def _name(cls):
        return u'QuotaImportance'

class QuotaWeight(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    weight_dict = db.Column(db.Text)

    def __init__(self, weight_dict):
        self.weight_dict = weight_dict

    @classmethod
    def _name(cls):
        return u'QuotaWeight'

class CoverageExp(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(20))
    start_ts= db.Column(db.BigInteger(10, unsigned=True))
    end_ts = db.Column(db.BigInteger(10, unsigned=True))
    coverage_exp = db.Column(db.Integer)

    def __init__(self, topic, start_ts, end_ts, coverage_exp):
        self.topic = topic
        self.start_ts = start_ts
        self.end_ts = end_ts
        self.coverage_exp = coverage_exp

    @classmethod
    def _name(cls):
        return u'CoverageExp'

class QuotaCoverage(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(20))
    start_ts = db.Column(db.BigInteger(10, unsigned=True))
    end_ts = db.Column(db.BigInteger(10, unsigned=True))
    coverage = db.Column(db.Float)
    def __init__(self, topic, start_ts, end_ts, coverage):
        self.topic = topic
        self.start_ts = start_ts
        self.end_ts = end_ts
        self.coverage = coverage

    @classmethod
    def _name(cls):
        return u'QuotaCoverage'

class QuotaFSensitivity(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(20))
    start_ts = db.Column(db.BigInteger(10, unsigned=True))
    end_ts = db.Column(db.BigInteger(10, unsigned=True))
    f_sensitivity = db.Column(db.Float)
     
    def __init__(self, topic, start_ts, end_ts, f_sensitivity):
        self.topic = topic
        self.start_ts = start_ts
        self.end_ts = end_ts
        self.f_sensitivity = f_sensitivity

    @classmethod
    def _name(cls):
        return u'QuotaFSensitivity'

class QuotaFSentiment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(20))
    start_ts = db.Column(db.BigInteger(10, unsigned=True))
    end_ts = db.Column(db.BigInteger(10, unsigned=True))
    f_sentiment = db.Column(db.Float)

    def __init__(self, topic, start_ts, end_ts, f_sentiment):
        self.topic = topic
        self.start_ts = start_ts
        self.end_ts = end_ts
        self.f_sentiment = f_sentiment

    @classmethod
    def _name(cls):
        return u'QuotaFSentiment'

class QuotaFTransmission(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(20))
    start_ts =db.Column(db.BigInteger(10, unsigned=True))
    end_ts = db.Column(db.BigInteger(10, unsigned=True))
    f_transmission = db.Column(db.Float)

    def __init__(self, topic, start_ts, end_ts, f_transmission):
        self.topic = topic
        self.start_ts =start_ts
        self.end_td = end_ts
        self.f_transmission = f_transmission

    @classmethod
    def _name(cls):
        return u'QuotaFTransmission'

class QuotaFInvolved(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(20))
    start_ts = db.Column(db.BigInteger(10, unsigned=True))
    end_ts = db.Column(db.BigInteger(10, unsigned=True))
    f_involved = db.Column(db.Float)

    def __init__(self, topic, start_ts, end_ts, f_involved):
        self.topic = topic
        self,start_ts = start_ts
        self.end_ts = end_ts
        self.f_involved = f_involved

    @classmethod
    def _name(cls):
        return u'QuotaFInvolved'

class QuotaIndex(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(20))
    start_ts = db.Column(db.BigInteger(10, unsigned=True))
    end_ts = db.Column(db.BigInteger(10, unsigned=True))
    index = db.Column(db.Float)

    def __init__(self, topic, start_ts, end_ts, index):
        self.topic = topic
        self.start_ts =start_ts
        self.end_ts = end_ts
        self.index = index

    @classmethod
    def _name(cls):
        return u'QuotaIndex'

#以下是语义模块（李文文看）#话题、观点对应表
class OpinionTopic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(20))#话题
    opinion = db.Column(db.String(20))#观点

    def __init__(self, topic, opinion):
        self.topic = topic
        self.opinion = opinion

    @classmethod
    def _name(cls):
        return u'OpinionTopic'

#观点微博
class OpinionWeibos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    opinionTopic = db.Column(db.Integer)#话题、观点对应表中id字段
    mid = db.Column(db.String(20))#微博id
    weibos = db.Column(db.Text)#微博文本
    user = db.Column(db.String(20))#用户昵称
    userid = db.Column(db.String(20))#用户id
    posttime = db.Column(db.String(20))#发布时间
    weibourl = db.Column(db.String(20))#微博url（目前没啥用，都是‘#’）
    userurl = db.Column(db.String(20))#用户url（目前没啥用，都是‘#’）
    repost = db.Column(db.Integer)#转发数
    stype = db.Column(db.String(20))#情绪类型（'happy','angry','sad'）

    def __init__(self, opinionTopic, mid, weibos, user, userid, posttime, weibourl, userurl, repost, stype):
        self.opinionTopic = opinionTopic
        self.mid = mid
        self.weibos = weibos
        self.user = user
        self.userid = userid
        self.posttime = posttime
        self.weibourl = weibourl
        self.userurl = userurl
        self.repost = repost
        self.stype = stype

    @classmethod
    def _name(cls):
        return u'OpinionWeibos'

#观点
class Opinion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    opinionTopic = db.Column(db.Integer)#话题、观点对应表中id字段
    start = db.Column(db.BigInteger(20, unsigned=True))#开始时间
    end = db.Column(db.BigInteger(20, unsigned=True))#结束时间
    count = db.Column(db.Integer)#所占微博数量
    opinionWord = db.Column(db.String(20))#关键词
    positive = db.Column(db.Float)#正极性情绪比例
    nagetive = db.Column(db.Float)#负极性情绪比例

    def __init__(self, opinionTopic, start, end, count, opinionWord, positive, nagetive):
        self.opinionTopic = opinionTopic
        self.start = start
        self.end = end
        self.count = count
        self.opinionWord = opinionWord
        self.positive = positive
        self.nagetive = nagetive

    @classmethod
    def _name(cls):
        return u'Opinion'

#观点热度值
class OpinionHot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    opinionTopic = db.Column(db.Integer)#话题、观点对应表中id字段
    ts = db.Column(db.BigInteger(20, unsigned=True))#时间
    count = db.Column(db.Integer)#热度

    def __init__(self, opinionTopic, ts, count):
        self.opinionTopic = opinionTopic
        self.ts = ts
        self.count = count

    @classmethod
    def _name(cls):
        return u'OpinionHot'


class SentimentGeo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(20))
    end = db.Column(db.BigInteger(10, unsigned=True))
    range = db.Column(db.BigInteger(10, unsigned=True))
    sentiment = db.Column(db.Integer(1, unsigned=True))  
    geo_count = db.Column(db.Text)                

    def __init__(self, topic, range, end, sentiment, geo_count):
        self.topic = topic 
        self.range = range
        self.end = end
        self.sentiment = sentiment
        self.geo_count = geo_count
    @classmethod
    def _name(cls):
        return u'SentimentGeo'