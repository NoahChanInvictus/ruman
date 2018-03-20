#!/usr/bin/env python
#encoding: utf-8

from flask import Flask, render_template, request, jsonify, Blueprint, send_from_directory, url_for, session
from economy.db import *
from . import homePage
import json
from economy.config import *
from economy.entityPortrait import views
from economy.es import *

@manipulate.route('/')
def index():
	
	return render_template('homePage/homePage.html',username=username,role_id=role_id,uid=uid)

@manipulate.route('/test/')
def test():
	result = 'Hello World!'
	return json.dumps(result,ensure_ascii=False)

