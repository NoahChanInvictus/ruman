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


@maniPulate.route('/test/')
def test():
	result = 'Hello World!'
	return json.dumps(result,ensure_ascii=False)

