#!/usr/bin/env python
#encoding: utf-8

from flask import Flask, render_template, request, jsonify, Blueprint, send_from_directory, url_for, session
from ruman.db import *
from . import hotSpotweibo
import json
from ruman.config import *
from utils import search_hotspot,search_hotspot_infor

from ruman.es import *

@hotSpotweibo.route('/')
def index():
    return render_template('hotSpotweibo/hotSpotweibo.html')

@hotSpotweibo.route('/get_hotSpotweibo_list/')
def search_hotspot_weibo():
    results = search_hotspot()
    return results

@hotSpotweibo.route('/get_hotSpotweibo_infor/')
def search_hotspot_weibo_infor():
    en_name = request.args.get('en_name','')
    results = search_hotspot_infor(en_name)
    return json.dumps(results,ensure_ascii=False)