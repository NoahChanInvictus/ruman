#!/usr/bin/env python
#encoding: utf-8

from flask import Flask, render_template, request, jsonify, Blueprint, send_from_directory, url_for, session
from ruman.db import *
from . import newHotSpot
import json
from ruman.config import *
import numpy as np
from ruman.es import *
from ruman.cron.sample_data.sample_main import *

@newHotSpot.route('/')
def index():
    return render_template('newHotSpot/newHotSpot.html')

@newHotSpot.route('/newhotspotandrumanText/',methods=['POST','GET'])
def newhotspotandruman_text():
    result = newhotspotcombineText()
    return json.dumps(result,ensure_ascii=False)
    
@newHotSpot.route('/hotspotReport/xw_propagate/')
def xinwen_hotspot_propagate():
    # id = int(request.args.get('id',''))
    text_id = request.args.get('text_id','')
    # source = request.args.get('source','')
    # result = hotspotPropagate(id,source)
    result = sample_data_main(text_id,'news')
    return json.dumps(result,ensure_ascii=False)

@newHotSpot.route('/hotspotReport/wb_propagate/')
def weibo_hotspot_propagate():
    mid = request.args.get('mid','')
    mid = np.int64(mid)
    result = sample_data_main(mid,'weibo')
    return json.dumps(result,ensure_ascii=False)

@newHotSpot.route('/hotspotReport/yy_propagate/')
def yaoyan_hotspot_propagate():
    mid = request.args.get('mid','')
    mid = np.int64(mid)
    # mid = 4041660423826613
    result = sample_data_main(mid,'yaoyan')
    return json.dumps(result,ensure_ascii=False)