#!/usr/bin/env python
#encoding: utf-8

from flask import Flask, render_template, request, jsonify, Blueprint, send_from_directory, url_for, session
from ruman.db import *
from . import index
import json
from ruman.config import *

from ruman.es import *

@index.route('/lieDetail/')
def lieDetail():
	uid = request.args.get('uid','')
	en_name = request.args.get('en_name','')
	return render_template('index/lieDetail.html',uid=uid,en_name=en_name)

@index.route('/setDetail/')
def setDetail():
	stock = request.args.get('stock','')
	id = request.args.get('id','')
	manipulate_type_num = request.args.get('manipulate_type_num','')
	return render_template('index/setDetail.html',stock=stock,id=id,manipulate_type_num=manipulate_type_num)

@index.route('/hotDetail/')
def hotDetail():
	id = request.args.get('id','')
	return render_template('index/hotDetail.html',id=id)

@index.route('/hotweiboDetail/')
def hotweiboDetail():
	uid = request.args.get('uid','')
	en_name = request.args.get('en_name','')
	return render_template('index/hotweiboDetail.html',uid=uid,en_name=en_name)

# 合并 微博热点 和 溯源分析 为 热点监测
@index.route('/newHotspotDetail_weibo/')
def newHotspotDetail_weibo():
	id = request.args.get('id','')
	return render_template('index/newHotspotDetail_weibo.html',id=id)

@index.route('/newHotspotDetail_news/')
def newHotspotDetail_news():
	id = request.args.get('id','')
	return render_template('index/newHotspotDetail_news.html',id=id)

# ========

@index.route('/test/')
def test():
    result = 'Hello World!'
    return json.dumps(result,ensure_ascii=False)

