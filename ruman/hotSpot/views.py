#!/usr/bin/env python
#encoding: utf-8

from flask import Flask, render_template, request, jsonify, Blueprint, send_from_directory, url_for, session
from ruman.db import *
from . import hotSpot
import json
from ruman.config import *

from ruman.es import *

@hotSpot.route('/')
def index():
    return render_template('hotSpot/hotSpot.html')

@hotSpot.route('/hotspotNewsText/')
def hotspot_text():
	result = hotspotText()
	return json.dumps(result,ensure_ascii=False)

@hotSpot.route('/hotspotReport/basicMessage/')
def hotspot_basicmessage():
	id = int(request.args.get('id',''))
	result = hotspotbasicMessage(id)
	return json.dumps(result,ensure_ascii=False)

@hotSpot.route('/hotspotReport/evolution/')
def hotspot_evolution():
	id = int(request.args.get('id',''))
	frequency = int(request.args.get('frequency',''))
	source = request.args.get('source','')
	result = hotspotEvolution(id,frequency,source)
	return json.dumps(result,ensure_ascii=False)

@hotSpot.route('/hotspotReport/propagate/')
def hotspot_propagate():
	id = int(request.args.get('id',''))
	source = request.args.get('source','')
	result = hotspotPropagate(id,source)
	return json.dumps(result,ensure_ascii=False)

@hotSpot.route('/hotspotReport/wordcloud/')
def hotspot_wordcloud():
	id = int(request.args.get('id',''))
	source = request.args.get('source','')
	result = hotspotWordcloud(id,source)
	return json.dumps(result,ensure_ascii=False)

@hotSpot.route('/hotspotReport/topicaxis/')
def hotspot_topicaxis():
	id = int(request.args.get('id',''))
	source = request.args.get('source','')
	result = hotspotTopicaxis(id,source)
	return json.dumps(result,ensure_ascii=False)