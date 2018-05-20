#!/usr/bin/env python
#encoding: utf-8

from flask import Flask, render_template, request, jsonify, Blueprint, send_from_directory, url_for, session
from ruman.db import *
from . import homePage
import json
from ruman.config import *
from ruman.es import *

@homePage.route('/')
def index():

	return render_template('homePage/homePage.html')

@homePage.route('/hotspotandrumanText/',methods=['POST','GET'])
def hotspotandruman_text():
	result = hotspotandrumanText()
	return json.dumps(result,ensure_ascii=False)

@homePage.route('/hotspotandrumanUser/',methods=['POST','GET'])
def hotspotandruman_user():
	id = request.args.get('id','')
	ifruman = int(request.args.get('ifruman',''))
	indextype = request.args.get('indextype','')
	result = hotspotandrumanUser(id,indextype,ifruman)
	if result:
		return json.dumps({'status':'ok'},ensure_ascii=False)
	else:
		return json.dumps({'status':'fail'},ensure_ascii=False)

@homePage.route('/hotspotbubbleChart/',methods=['POST','GET'])
def hotspotbubble_chart():
	result = hotspotbubbleChart()
	return json.dumps(result,ensure_ascii=False)

@homePage.route('/rumorWarning/',methods=['POST','GET'])
def rumor_warning():
	result = rumorWarning()
	return json.dumps(result,ensure_ascii=False)

@homePage.route('/rumorWarningNum/',methods=['POST','GET'])
def rumor_warning_num():
	result = rumorWarningNum()
	return json.dumps(result,ensure_ascii=False)

@homePage.route('/manipulateWarning/',methods=['POST','GET'])
def manipulate_warning():
	result = manipulateWarning()
	return json.dumps(result,ensure_ascii=False)

@homePage.route('/manipulateIndustry/',methods=['POST','GET'])
def manipulate_industry():
	result = manipulateIndustry(90)
	return json.dumps(result,ensure_ascii=False)

@homePage.route('/manipulatePanel/',methods=['POST','GET'])
def manipulate_panel():
	result = manipulatePanel(90)
	return json.dumps(result,ensure_ascii=False)

@homePage.route('/hotspotSourceDistribute/',methods=['POST','GET'])
def hotspotSourceDistribute():
	result = hotspot_source_distribute()
	return json.dumps(result,ensure_ascii=False)

@homePage.route('/hotspotWordCloud/',methods=['POST','GET'])
def hotspotWordCloud():	
	result = homepageWordcloud()
	return json.dumps(result,ensure_ascii=False)

@homePage.route('/test1/')
def hot_spot():
	result = 'Hello World!!!'
	return json.dumps(result,ensure_ascii=False)
