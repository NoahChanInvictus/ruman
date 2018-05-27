# -*- coding: utf-8 -*-
from ruman.global_config import db, es_user_profile
from flask import Blueprint,render_template,request
from utils import get_gexf ,get_trend_pusher, get_trend_maker,find2jump,\
get_maker_weibos_byts, get_pusher_weibos_byts, get_pusher_weibos_byhot,\
get_maker_weibos_byhot, gexf_process,get_top_pagerank
import json
from ruman.time_utils import ts2datetime, datetime2ts
from ruman.parameter import MYSQL_TOPIC_LEN
import networkx as nx
from networkx.generators.atlas import *

mod = Blueprint('topic_network_analyze',__name__,url_prefix='/topic_network_analyze')

Minute = 60
Fifteenminutes = 15 * Minute
Hour = 3600
SixHour = Hour * 6
Day = Hour * 24
MinInterval = Fifteenminutes
dictG=nx.Graph()

@mod.route('/networkdata')
def networkdata():
    f = open('/home/ubuntu2/yuanhuiru/info_consume/user_portrait/user_portrait/info_consume/topic_network_analyze/networkdata.min10.json','r')
    a = f.readlines()
    results = a[0]
    print json.loads(results),type(results)
    return results

@mod.route('/get_gexf/')
def GetGexf():
    topic =request.args.get('topic', '')
    end_ts = request.args.get('end_ts', '')     #''代表默认值为空
    end_ts = long(end_ts)
    start_ts = request.args.get('start_ts', '')
    start_ts = long(start_ts)
    date = ts2datetime(end_ts)
    windowsize = (end_ts - start_ts) / Day # 确定时间跨度的大小
    raw_data = get_gexf(topic, date, windowsize)
    print type(raw_data),len(raw_data)
    G=nx.Graph()
    results,G = gexf_process(raw_data)
    global dictG
    dictG=G
    return json.dumps(results)

@mod.route('/get_subgexf/')
def GetSubGraph():
    uid=request.args.get('uid','')
    if dictG:
        results=find2jump(uid,3,dictG)
    else:
        results={}
        print "no graph"
    
    return json.dumps(results)


@mod.route('/get_trend_pusher/')
def GetPusher():
    topic =request.args.get('topic', '')
    # if MYSQL_TOPIC_LEN == 0:
    #     topic = topic[:20]
    # end_ts = request.args.get('end_ts', '')     #''代表默认值为空
    # end_ts = long(end_ts)
    # start_ts = request.args.get('start_ts', '')
    # start_ts = long(start_ts)
    # date = ts2datetime(end_ts)
    # windowsize = (end_ts - start_ts) / Day # 确定时间跨度的大小
    results = get_trend_pusher(topic)
    return json.dumps(results)

@mod.route('/get_trend_maker/')
def GetMaker():
    topic =request.args.get('topic', '')
    topic=topic[:20]
    # if MYSQL_TOPIC_LEN == 0:
        # topic = topic[:20]
    # end_ts = request.args.get('end_ts', '')     #''代表默认值为空
    # end_ts = long(end_ts)
    # start_ts = request.args.get('start_ts', '')
    # start_ts = long(start_ts)
    # date = ts2datetime(end_ts)
    # windowsize = (end_ts - start_ts) / Day # 确定时间跨度的大小
    results = get_trend_maker(topic)
    return json.dumps(results)

@mod.route('/pusher_weibos_byts/')
def GetPusherWeibosByts():
    topic =request.args.get('topic', '')
    if MYSQL_TOPIC_LEN == 0:
        topic = topic[:20]
    print topic
    end_ts = request.args.get('end_ts', '')     #''代表默认值为空
    end_ts = long(end_ts)
    start_ts = request.args.get('start_ts', '')
    start_ts = long(start_ts)
    date = ts2datetime(end_ts)
    windowsize = (end_ts - start_ts) / Day # 确定时间跨度的大小
    results = get_pusher_weibos_byts(topic, date, windowsize)
    return json.dumps(results)

@mod.route('/maker_weibos_byts/')
def maker_weibos_byts():
    topic =request.args.get('topic', '')
    if MYSQL_TOPIC_LEN == 0:
        topic = topic[:20]
    end_ts = request.args.get('end_ts', '')     #''代表默认值为空
    end_ts = long(end_ts)
    start_ts = request.args.get('start_ts', '')
    start_ts = long(start_ts)
    date = ts2datetime(end_ts)
    windowsize = (end_ts - start_ts) / Day # 确定时间跨度的大小
    results = get_maker_weibos_byts(topic, date, windowsize)
    return json.dumps(results)

@mod.route('/maker_weibos_byhot/')
def maker_weibos_byhot():
    topic =request.args.get('topic', '')
    if MYSQL_TOPIC_LEN == 0:
        topic = topic[:20]
    end_ts = request.args.get('end_ts', '')     #''代表默认值为空
    end_ts = long(end_ts)
    start_ts = request.args.get('start_ts', '')
    start_ts = long(start_ts)
    date = ts2datetime(end_ts)
    windowsize = (end_ts - start_ts) / Day # 确定时间跨度的大小
    results = get_maker_weibos_byhot(topic, date, windowsize)
    return json.dumps(results)

@mod.route('/pusher_weibos_byhot/')
def pusher_weibos_byhot():
    topic =request.args.get('topic', '')
    if MYSQL_TOPIC_LEN == 0:
        topic = topic[:20]
    print topic
    end_ts = request.args.get('end_ts', '')     #''代表默认值为空
    end_ts = long(end_ts)
    start_ts = request.args.get('start_ts', '')
    start_ts = long(start_ts)
    date = ts2datetime(end_ts)
    windowsize = (end_ts - start_ts) / Day # 确定时间跨度的大小
    results = get_pusher_weibos_byhot(topic, date, windowsize)
    return json.dumps(results)

@mod.route('/get_pagerank/')
def get_pagerank():
    topic =request.args.get('topic', '')
    if MYSQL_TOPIC_LEN == 0:
        topic = topic[:20]
    end_ts = request.args.get('end_ts', '')     #''代表默认值为空
    end_ts = long(end_ts)
    start_ts = request.args.get('start_ts', '')
    start_ts = long(start_ts)
    date = ts2datetime(end_ts)
    windowsize = (end_ts - start_ts) / Day # 确定时间跨度的大小
    result = get_top_pagerank(topic, date, windowsize)
    return json.dumps(result)
