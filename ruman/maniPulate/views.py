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

@maniPulate.route('/manipulateWarningText/',methods=['POST','GET'])
def manipulate_warning_text():
	result = manipulateWarningText()
	return json.dumps(result,ensure_ascii=False)

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

@maniPulate.route('/manipulateEv/',methods=['POST','GET'])
def manipulate_ev():
	date = int(request.args.get('date',''))
	result = manipulateEv(date)
	return json.dumps(result,ensure_ascii=False)

@maniPulate.route('/manipulatereport/history/',methods=['POST','GET'])
def manipulate_history():
	stock_id = request.args.get('date','')
	result = manipulateHistory(stock_id)
	return json.dumps(result,ensure_ascii=False)

@maniPulate.route('/manipulatereport/price/',methods=['POST','GET'])
def manipulate_price():
	stock_id = request.args.get('date','')
	start_date = request.args.get('date','')
	end_date = request.args.get('date','')
	result = manipulatePrice(stock_id,start_date,end_date)
	return json.dumps(result,ensure_ascii=False)
