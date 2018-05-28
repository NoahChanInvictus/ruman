#!/usr/bin/env python
#encoding: utf-8

from flask import Flask, render_template, request, jsonify, Blueprint, send_from_directory, url_for, session
from ruman.db import *
from . import rumor
import json
from ruman.config import *
from utils import search_rumor,search_rumor_infor,rumorWarning,rumorbubbleChart,rumorMonger,rumorpropagate,get_rumor_pusher_maker,get_rumor_source
from ruman.es import *

@rumor.route('/')
def index():

    return render_template('rumor/rumor.html')


@rumor.route('/test/')
def test():
    result = 'Hello World!'
    return json.dumps(result,ensure_ascii=False)


@rumor.route('/get_rumor_list/')
def search_rumor_weibo():
    results = search_rumor()
    return results

@rumor.route('/rumorWarning/',methods=['POST','GET'])
def rumor_warning():
	result = rumorWarning()
	return json.dumps(result,ensure_ascii=False)

@rumor.route('/rumorMonger/',methods=['POST','GET'])
def rumor_monger():
	date = int(request.args.get('date',''))
	result = rumorMonger(date)
	return json.dumps(result,ensure_ascii=False)

@rumor.route('/rumorbubbleChart/')
def rumorbubble_chart():
    results = rumorbubbleChart()
    return json.dumps(results,ensure_ascii=False)

@rumor.route('/get_rumor_infor/')
def search_rumor_weibo_infor():
    en_name = request.args.get('en_name','')
    results = search_rumor_infor(en_name)
    return json.dumps(results,ensure_ascii=False)

@rumor.route('/rumorPropagate/')
def rumor_propagate():
    en_name = request.args.get('en_name','')
    results = rumorpropagate(en_name)
    return json.dumps(results,ensure_ascii=False)

@rumor.route('/get_trend/')
def get_ten_pusher():
    en_name = request.args.get('en_name','')
    results = get_rumor_pusher_maker(en_name)
    return json.dumps(results,ensure_ascii=False)

@rumor.route('/get_source/')
def get_source():
    en_name = request.args.get('en_name','')
    results = get_rumor_source(en_name)
    return json.dumps(results,ensure_ascii=False)