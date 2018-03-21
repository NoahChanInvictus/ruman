#!/usr/bin/env python
#encoding: utf-8

from flask import Flask, render_template, request, jsonify, Blueprint, send_from_directory, url_for, session
from ruman.db import *
from . import manipulate
import json
from ruman.config import *

from ruman.es import *

@manipulate.route('/',methods=['POST','GET'])
def index():
	
	return render_template('homePage/homePage.html')

@manipulate.route('/manipulateWarningText/',methods=['POST','GET'])
def manipulate_warning_text():
	result = manipulateWarningText()
	return json.dumps(result,ensure_ascii=False)

@manipulate.route('/manipulateWarningNum/',methods=['POST','GET'])
def manipulate_warning_num():
	date = int(request.args.get('date',''))
	result = manipulateWarningNum(date)
	return json.dumps(result,ensure_ascii=False)

@manipulate.route('/manipulateInfluence/',methods=['POST','GET'])
def manipulate_influence():
	date = int(request.args.get('date',''))
	result = manipulateInfluence(date)
	return json.dumps(result,ensure_ascii=False)

@manipulate.route('/manipulateIndustry/',methods=['POST','GET'])
def manipulate_industry():
	date = int(request.args.get('date',''))
	result = manipulateIndustry(date)
	return json.dumps(result,ensure_ascii=False)

@manipulate.route('/manipulateType/',methods=['POST','GET'])
def manipulate_type():
	date = int(request.args.get('date',''))
	result = manipulateType(date)
	return json.dumps(result,ensure_ascii=False)

@manipulate.route('/manipulateEv/',methods=['POST','GET'])
def manipulate_ev():
	date = int(request.args.get('date',''))
	result = manipulateEv(date)
	return json.dumps(result,ensure_ascii=False)

@manipulate.route('/manipulatereport/history/',methods=['POST','GET'])
def manipulate_history():
	result = manipulateHistory(stock_id)
	return json.dumps(result,ensure_ascii=False)

@manipulate.route('/manipulatereport/price/',methods=['POST','GET'])
def manipulate_price():
	result = manipulatePrice(stock_id)
	return json.dumps(result,ensure_ascii=False)