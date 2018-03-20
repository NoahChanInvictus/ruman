#!/usr/bin/env python
#encoding: utf-8

from flask import Flask, render_template, request, jsonify, Blueprint, send_from_directory, url_for, session
from ruman.db import *
from . import manipulate
import json
from ruman.config import *

from ruman.es import *

@manipulate.route('/')
def index():
	
	return render_template('homePage/homePage.html')

@manipulate.route('/test/')
def test():
	result = 'Hello World!'
	return json.dumps(result,ensure_ascii=False)

