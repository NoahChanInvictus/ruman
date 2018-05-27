# -*- coding: utf-8 -*-
from ruman.global_config import db,es_user_profile,profile_index_name,profile_index_type
from ruman.info_consume.model import SentimentCount,SentimentGeo,SentimentWeibos
import math
import json
from sqlalchemy import func
#from socialconsume.global_config import db
#from socialconsume.model import CityTopicCount, CityWeibos



Minute = 60
Fifteenminutes = 15 * Minute
Hour = 3600
SixHour = Hour * 6
Day = Hour * 24
MinInterval = Fifteenminutes

down = [2,3,4,5,6,7]

def _json_loads(weibos):
    try:
        return json.loads(weibos)
    except ValueError:
        if isinstance(weibos, unicode):
            return json.loads(json.dumps(weibos))
        else:
            return None


def get_sen_time_count(topic,start_ts,end_ts,unit=MinInterval):#按时间趋势的不同情绪的数量
    count = {}
    if (end_ts - start_ts < unit):
        upbound = long(math.ceil(end_ts / (unit * 1.0)) * unit)
        items = db.session.query(SentimentCount.sentiment,func.sum(SentimentCount.count)).filter(SentimentCount.end==upbound, \
                                                       SentimentCount.query==topic).group_by(SentimentCount.sentiment).all()

        for item in items:
            try:
                count[end_ts][item[0]] += item[1]
            except:
                count[end_ts]={}
                count[end_ts][item[0]] = item[1]        
    else:
        upbound = long(math.ceil(end_ts / (unit * 1.0)) * unit)
        lowbound = long((start_ts / unit) * unit)
        interval = (upbound-lowbound)/unit
        for i in range(interval, 0, -1):    
            begin_ts = upbound - unit * i
            end_ts = begin_ts + unit
            #print begin_ts,end_ts
            items = db.session.query(SentimentCount.sentiment,func.sum(SentimentCount.count)).filter(SentimentCount.end>begin_ts, \
                                                         SentimentCount.end<=end_ts, \
                                                         SentimentCount.query==topic).group_by(SentimentCount.sentiment).all()
            if items:
                count[end_ts] = {}
                for item in items:
                    # if item[0] in down:
                    #     sen = '2'
                    # else:
                    sen = str(item[0])
                    try:
                        count[end_ts][sen] += str(item[1])
                    except:
                        count[end_ts][sen] = str(item[1])
    return count #{1468947600L: {0L: Decimal('82'), 1L: Decimal('8')}, 1468949400L: {0L: Decimal('57'), 1L: Decimal('7'), 2L: Decimal('1'), 6L: Decimal('1')}}


def get_sen_province_count(topic,start_ts,end_ts,unit=MinInterval): #省市的热力图
    city = {}

    if (end_ts - start_ts < unit):
        upbound = long(math.ceil(end_ts / (unit * 1.0)) * unit)
        items = db.session.query(SentimentGeo).filter(SentimentGeo.end==upbound, \
                                                       SentimentGeo.topic==topic).all()
    else:
        upbound = long(math.ceil(end_ts / (unit * 1.0)) * unit)
        lowbound = long((start_ts / unit) * unit)
        items = db.session.query(SentimentGeo).filter(SentimentGeo.end>lowbound, \
                                                         SentimentGeo.end<=upbound, \
                                                         SentimentGeo.topic==topic).all()
    count_dict = {}
    #city_dict = {}
    if items:
        for item in items:       
            geo = _json_loads(item.geo_count)
            #print geo
            for province,city_dict in geo.iteritems():
                sen = item.sentiment  #每种情绪下，各省的各市的微博数，按省的总数排序
                # if sen in down:
                #     sen0 = '2'
                # else:
                sen0 = str(sen)
                for k,v in city_dict.iteritems():
                    if k == 'total':
                        continue
                    #print k.encode('utf8'),v
                    try:
                        count_dict[sen0][province]['total'] += v
                    except:
                        try:
                            count_dict[sen0][province] = {'total':v}
                        except:
                            count_dict[sen0] = {province:{'total':v}}
                    try:
                        count_dict[sen0][province][k] += v
                    except:
                        count_dict[sen0][province][k] = v
                    #print sen0,count_dict[sen0]
                #print count_dict

            #jln all citys without province
            #for province,city_dict in geo.iteritems():
            #     sen = item.sentiment
            #     if sen in down:
            #         sen0 = '2'
            #     else:
            #         sen0 = str(sen)
            #     for k,v in city_dict.iteritems():
            #         if k == 'total':
            #             continue                
            #         try:
            #             count_dict[sen0][k] += v
            #         except:
            #             try:
            #                 count_dict[sen0][k] = v
            #             except:
            #                 count_dict[sen0] = {}
            #jln 000   城市加起来
            # try:
            #     citys = geo[province]
            #     for k,v in geo[province].iteritems():
            #         try:
            #             city_dict[k] += v
            #         except:
            #             city_dict[k] = v
            # except:
            #     continue  
            # print citys
    #print count_dict
    results = []
    for sen,counts in count_dict.iteritems():
        results.append({sen:sorted(counts.iteritems(),key=lambda x:x[1]['total'],reverse=True)})
    #results = sorted(count_dict.iteritems(),key=lambda x:x[1].values()[0]['total'],reverse=True)
    #print results
    return results

def get_weibo_content(topic,start_ts,end_ts,sort_item='timestamp',sen=0):
    #按时间、转发量、情绪类型  对微博排序
    items = db.session.query(SentimentWeibos).filter(SentimentWeibos.end>start_ts, \
                                                    SentimentWeibos.end<=end_ts, \
                                                    SentimentWeibos.query==topic,\
                                                    SentimentWeibos.sentiment==sen).all()
    weibo_dict = {}
    for item in items:          
        weibos = _json_loads(item.weibos)
        ori_text = set()
        for weibo in weibos:
            try:
                a = weibo['text']
            except:
                continue
            if weibo['text'] not in ori_text:
                ori_text.add(weibo['text'])
                
                weibo_content = {}
                weibo_content['text'] = weibo['text'] 
                weibo_content['uid'] = weibo['uid']
                weibo_content['timestamp'] = weibo['timestamp']
                weibo_content['sentiment'] = weibo['sentiment'] 
                weibo_content['comment'] = weibo['comment']
                weibo_content['retweeted'] = weibo['retweeted']
                weibo_content['keywords'] = weibo['keywords_dict']
                weibo_content['mid'] = weibo['mid']
                try:
                    user = es_user_profile.get(index=profile_index_name,doc_type=profile_index_type,id=weibo_content['uid'])['_source']
                    weibo_content['uname'] = user['nick_name']
                    weibo_content['photo_url'] = user['photo_url']
                except:
                    weibo_content['uname'] = 'unknown'
                    weibo_content['photo_url'] = 'unknown'
                weibo_dict[weibo_content['mid']] = weibo_content

    results = sorted(weibo_dict.items(),key=lambda x:x[1][sort_item],reverse=True)
    #print results
    return results




if __name__ == '__main__':
    #get_sen_province_count('aoyunhui',1468944900,1468946700)
    get_weibo_content('aoyunhui',1468946700,1468948500)
    #get_sen_time_count('aoyunhui',1468946700,1468950300,1800)