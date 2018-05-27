# -*- coding: utf-8 -*-

from flask import Blueprint,render_template,request
from utils import weibo_get_uid_list,today_time,get_video
import json,re,jieba
from ruman.global_utils import R_CLUSTER_FLOW2 as r_cluster

mod = Blueprint('weibo_hashtag',__name__,url_prefix='/weibo_hashtag')


@mod.route('/get_weibo_hashtag/')
def weibo_count():
    uid_list = weibo_get_uid_list('uid.txt')
    today = today_time()
    hashtag_list = {}
    for uid in uid_list:
    	hashtag = r_cluster.hget('hashtag_'+'1480176000',uid)
    	if hashtag != None:
    		hashtag = hashtag.encode('utf8')
	    	hashtag = json.loads(hashtag)

    		for k,v in hashtag.iteritems():
    			try:
	    			hashtag_list[k] += v
	    		except:
	    			hashtag_list[k] = v
    	#r_cluster.hget('hashtag_'+str(a))


    hashtag_list = sorted(hashtag_list.items(),key=lambda x:x[1],reverse=True)[:20]
    
    return json.dumps(hashtag_list)


@mod.route('/video_recom/')
def video_recom():
    a = json.loads(weibo_count())
    hot = [i[0] for i in a]
    result = get_video(hot)

    return json.dumps(result)