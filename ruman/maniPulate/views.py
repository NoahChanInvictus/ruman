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
