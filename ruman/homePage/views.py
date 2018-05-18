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

@homePage.route('/test1/')
def hot_spot():
	result = 'Hello World!!!'
	return json.dumps(result,ensure_ascii=False)
