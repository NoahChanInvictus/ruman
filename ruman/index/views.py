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
	return render_template('index/lieDetail.html')

@index.route('/setDetail/')
def setDetail():
	stock = request.args.get('stock','')
	id = request.args.get('id','')
	return render_template('index/setDetail.html',stock=stock,id=id)

@index.route('/hotDetail/')
def hotDetail():
    stock = request.args.get('stock','')
    id = request.args.get('id','')
    return render_template('index/hotDetail.html',stock=stock,id=id)

@index.route('/test/')
def test():
	result = 'Hello World!'
	return json.dumps(result,ensure_ascii=False)

