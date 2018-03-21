#!/usr/bin/env python
#encoding: utf-8

from flask import Flask, render_template, request, jsonify, Blueprint, send_from_directory, url_for, session
from ruman.db import *
from . import perceivedLie
import json
from ruman.config import *

from ruman.es import *

@perceivedLie.route('/')
def index():

	return render_template('perceivedLie/perceived_lie.html')


@perceivedLie.route('/test/')
def test():
	result = 'Hello World!'
	return json.dumps(result,ensure_ascii=False)

