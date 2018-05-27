# -*- coding: utf-8 -*-

from flask import Blueprint,render_template,request
from ruman.global_config import db
from utils import  get_weibo_by_time,get_time_count,get_predict_count
from ruman.parameter import MYSQL_TOPIC_LEN
import json

mod = Blueprint('topic_time_analyze',__name__,url_prefix='/topic_time_analyze')

Minute = 60
Fifteenminutes = 15 * Minute
Hour = 3600
SixHour = Hour * 6
Day = Hour * 24
MinInterval = Fifteenminutes

# @mod.route('/date_detail/')
# def date_detail():
#     topic_name_on_detail = request.args.get('topic_name','')
#     return render_template('/info_consume/date_detail.html',topic_name=topic_name_on_detail)


@mod.route('/truth_predict/')
def Predict():
    topic = request.args.get('topic','')
    # if MYSQL_TOPIC_LEN == 0:
    #     topic = topic[:20]
    print topic
    during = request.args.get('pointInterval', Fifteenminutes)
    during = int(during)
    end_ts = request.args.get('end_ts', '')
    end_ts = long(end_ts)
    start_ts = request.args.get('start_ts', '')
    start_ts = long(start_ts)
    ts_arr = []
    results = get_predict_count(topic,start_ts,end_ts,during)
    
    #print json.dump(results)
   #print 'predict函数'
    #print 'type_results',type(results)
    return json.loads(json.dumps(results))
    #return json.dumps(results)



@mod.route('/date_time')
def date_time():
    return render_template('/info_consume/date_time.html')

@mod.route('/time/')
def time():
    topic_name_on_detail = request.args.get('topic_name','')
    topic_name_on_detail_ch = request.args.get('en_name','')
    date_from = request.args.get('date_from','')
    date_to = request.args.get('date_to','')
    return render_template('/info_consume/date_detail.html',topic_name=topic_name_on_detail,en_name=topic_name_on_detail_ch,date_from=date_from,date_to=date_to)
    # return render_template('/info_consume/date_detail.html')

# @mod.route('/truth_predict/')

# def Predict():
#     topic = request.args.get('topic','')
#     if MYSQL_TOPIC_LEN == 0:
#         topic = topic[:20]
#     print topic
#     during = request.args.get('pointInterval', Fifteenminutes)   #默认查询时间粒度为900秒
#     during = int(during)
#     end_ts = request.args.get('end_ts', '')     #''代表默认值为空
#     end_ts = long(end_ts)
#     start_ts = request.args.get('start_ts', '')
#     start_ts = long(start_ts)
#     ts_arr = []
#     results = get_predict_count(topic,start_ts,end_ts,during)
#     return json.dumps(results)


@mod.route('/mtype_count/')
def MtypeCount():      #每类微博的数量
    topic = request.args.get('topic','')
    if MYSQL_TOPIC_LEN == 0:
        topic = topic[:20]
    print topic
    during = request.args.get('pointInterval', Fifteenminutes)   #默认查询时间粒度为900秒
    during = int(during)
    end_ts = request.args.get('end_ts', '')     #''代表默认值为空
    end_ts = long(end_ts)
    start_ts = request.args.get('start_ts', '')
    start_ts = long(start_ts)
    ts_arr = []
    results = get_time_count(topic,start_ts,end_ts,during)
    #results = mtype_count('aoyunhui',1468944000,1471622400,1) 
    return json.dumps(results)

@mod.route('/time_order_weibos/')
def TimeOrderWeibos():
    topic =request.args.get('topic', '')
    end_ts = request.args.get('end_ts', '')     #''代表默认值为空
    end_ts = long(end_ts)
    start_ts = request.args.get('start_ts', '')
    start_ts = long(start_ts)
    sort_item = request.args.get('sort_item', 'timestamp')
    ts_arr = []
    weibos = get_weibo_by_time(topic,start_ts,end_ts,sort_item)
    return json.dumps(weibos)


@mod.route('/hot_order_weibos/')
def HotOrderWeibos():
    topic =request.args.get('topic', '')
    during = request.args.get('pointInterval', Fifteenminutes)   #默认查询时间粒度为900秒
    end_ts = request.args.get('end_ts', '')     #''代表默认值为空
    end_ts = long(end_ts)
    start_ts = request.args.get('start_ts', '')
    start_ts = long(start_ts)
    ts_arr = []
    weibos = get_weibo_by_hot(topic,start_ts,end_ts)
    return json.dumps(weibos)
# @mod.route('/hot_order_weibos/')
# def HotOrderWeibos():
#     topic =results.args.get('topic', '')
#     during = request.args.get('pointInterval', Fifteenminutes)   #默认查询时间粒度为900秒
#     end_ts = request.args.get('end_ts', '')     #''代表默认值为空
#     end_ts = long(end_ts)
#     start_ts = request.args.get('start_ts', '')
#     start_ts = long(start_ts)
#     ts_arr = []
#     weibos = get_weibo_by_hot(topic,start_ts,end_ts)

