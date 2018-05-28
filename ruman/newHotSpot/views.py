#!/usr/bin/env python
#encoding: utf-8

from flask import Flask, render_template, request, jsonify, Blueprint, send_from_directory, url_for, session
from ruman.db import *
from . import newHotSpot
import json
from ruman.config import *

from ruman.es import *

@newHotSpot.route('/')
def index():
    return render_template('newHotSpot/newHotSpot.html')

@newHotSpot.route('/newhotspotandrumanText/',methods=['POST','GET'])
def newhotspotandruman_text():
    result = newhotspotcombineText()
    return json.dumps(result,ensure_ascii=False)