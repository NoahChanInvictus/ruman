#!/usr/bin/env python
#encoding: utf-8

from flask import Flask, render_template, request, jsonify, Blueprint, send_from_directory, url_for, session
from ruman.db import *
from . import maniPulate
import json
from ruman.config import *

from ruman.es import *

@maniPulate.route('/')
def index():
	return render_template('maniPulate/manipulate.html')

@maniPulate.route('/manipulateWarning/',methods=['POST','GET'])
def manipulate_warning():
	result = manipulateWarning()
	return json.dumps(result,ensure_ascii=False)

@maniPulate.route('/manipulateWarningText/',methods=['POST','GET'])
def manipulate_warning_text():
	result = manipulateWarningText()
	return json.dumps(result,ensure_ascii=False)

@maniPulate.route('/manipulateWarningUser/',methods=['POST','GET'])
def manipulate_warning_user():
	id = int(request.args.get('id',''))
	ifmanipulate = int(request.args.get('ifmanipulate',''))
	result = manipulateWarningUser(id,ifmanipulate)
	if result:
		return json.dumps({'status':'ok'},ensure_ascii=False)
	else:
		return json.dumps({'status':'fail'},ensure_ascii=False)

@maniPulate.route('/manipulateWarningNum/',methods=['POST','GET'])
def manipulate_warning_num():
	date = int(request.args.get('date',''))
	result = manipulateWarningNum(date)
	return json.dumps(result,ensure_ascii=False)

@maniPulate.route('/manipulateInfluence/',methods=['POST','GET'])
def manipulate_influence():
	date = int(request.args.get('date',''))
	result = manipulateInfluence(date)
	return json.dumps(result,ensure_ascii=False)

@maniPulate.route('/manipulateIndustry/',methods=['POST','GET'])
def manipulate_industry():
	date = int(request.args.get('date',''))
	result = manipulateIndustry(date)
	return json.dumps(result,ensure_ascii=False)

@maniPulate.route('/manipulateType/',methods=['POST','GET'])
def manipulate_type():
	date = int(request.args.get('date',''))
	result = manipulateType(date)
	return json.dumps(result,ensure_ascii=False)

@maniPulate.route('/manipulatePanel/',methods=['POST','GET'])
def manipulate_panel():
	date = int(request.args.get('date',''))
	result = manipulatePanel(date)
	return json.dumps(result,ensure_ascii=False)

@maniPulate.route('/manipulateReport/gongshang/',methods=['POST','GET'])
def manipulate_gongshang():
	id = int(request.args.get('id',''))
	result = manipulateGongshang(id)
	return json.dumps(result,ensure_ascii=False)

@maniPulate.route('/manipulateReport/history/',methods=['POST','GET'])
def manipulate_history():
	id = int(request.args.get('id',''))
	result = manipulateHistory(id)
	return json.dumps(result,ensure_ascii=False)

@maniPulate.route('/manipulateReport/price/',methods=['POST','GET'])
def manipulate_price():
	id = int(request.args.get('id',''))
	result = manipulatePrice(id)
	return json.dumps(result,ensure_ascii=False)

@maniPulate.route('/manipulateReport/trading/',methods=['POST','GET'])
def manipulate_trading():
	id = int(request.args.get('id',''))
	result = manipulateTrading(id)
	return json.dumps(result,ensure_ascii=False)

@maniPulate.route('/manipulateReport/profit/',methods=['POST','GET'])
def manipulate_profit():
	id = int(request.args.get('id',''))
	result = manipulateProfit(id)
	return json.dumps(result,ensure_ascii=False)

@maniPulate.route('/manipulateReport/announcement/',methods=['POST','GET'])
def manipulate_announcement():
	id = int(request.args.get('id',''))
	result = manipulateAnnouncement(id)
	return json.dumps(result,ensure_ascii=False)

@maniPulate.route('/manipulateReport/seasonBox/',methods=['POST','GET'])
def manipulate_seasonbox():
	id = int(request.args.get('id',''))
	result = manipulateSeasonbox(id)
	return json.dumps(result,ensure_ascii=False)

@maniPulate.route('/manipulateReport/top10holders/',methods=['POST','GET'])
def manipulate_top10holders():
	id = int(request.args.get('id',''))
	seasonid = request.args.get('seasonid','')
	result = manipulateTop10holders(id,seasonid)
	return json.dumps(result,ensure_ascii=False)

@maniPulate.route('/manipulateReport/Largetrans/',methods=['POST','GET'])
def manipulate_Largetrans():
	id = int(request.args.get('id',''))
	result = manipulateLargetrans(id)
	return json.dumps(result,ensure_ascii=False)

@maniPulate.route('/manipulateReport/seasonBoxpct/',methods=['POST','GET'])
def manipulate_seasonbox_pct():
	id = int(request.args.get('id',''))
	result = manipulateSeasonboxpct(id)
	return json.dumps(result,ensure_ascii=False)

@maniPulate.route('/manipulateReport/holderspct/',methods=['POST','GET'])
def manipulate_holderspct():
	id = int(request.args.get('id',''))
	seasonid = request.args.get('seasonid','')
	result = manipulateHolderspct(id,seasonid)
	return json.dumps(result,ensure_ascii=False)

@maniPulate.route('/manipulateReport/holderspctline/',methods=['POST','GET'])
def manipulate_holderspctline():
	id = int(request.args.get('id',''))
	result = manipulateHolderspctline(id)
	return json.dumps(result,ensure_ascii=False)

@maniPulate.route('/manipulateReport/rumantext/',methods=['POST','GET'])
def manipulate_rumantext():
	id = int(request.args.get('id',''))
	result = manipulateRumantext(id)
	return json.dumps(result,ensure_ascii=False)

@maniPulate.route('/manipulateReport/rumancomment/',methods=['POST','GET'])
def manipulate_rumancomment():
	id = int(request.args.get('id',''))
	result = manipulateRumancomment(id)
	return json.dumps(result,ensure_ascii=False)

@maniPulate.route('/manipulateReport/credit/',methods=['POST','GET'])
def manipulate_credit():
	id = int(request.args.get('id',''))
	result = manipulateCredit(id)
	return json.dumps(result,ensure_ascii=False)