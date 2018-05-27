#!/usr/bin/env python
# encoding: utf-8


from ruman.homePage.views import homePage
from ruman.maniPulate.views import maniPulate
from ruman.hotSpot.views import hotSpot
from ruman.newHotSpot.views import newHotSpot
from ruman.hotSpotweibo.views import hotSpotweibo
from ruman.rumor.views import rumor
from ruman.perceivedLie.views import perceivedLie
from ruman.perceivedSet.views import perceivedSet
from ruman.userManage.views import userManage
from ruman.index.views import index
from ruman.attribute.views import mod as attributeModule
from ruman.influence_application.views import mod as influenceModule
from info_consume.topic_sen_analyze.views import mod as topicSenModule
from info_consume.topic_language_analyze.views import mod as topicLanModule
from info_consume.topic_time_analyze.views import mod as topicTimeModule
from info_consume.topic_network_analyze.views import mod as topicNetworkModule
from info_consume.person_social.views import mod as personSocialModule
from ruman.social_sensing.views import mod as sensingModule

from flask import Flask, render_template, request, jsonify, Blueprint

def create_app():
	app = Flask(__name__)
	app.register_blueprint(homePage,url_prefix='/homePage')
	app.register_blueprint(maniPulate,url_prefix='/maniPulate')
	app.register_blueprint(hotSpot,url_prefix='/hotSpot')
	app.register_blueprint(newHotSpot,url_prefix='/newHotSpot')
	app.register_blueprint(hotSpotweibo,url_prefix='/hotSpotweibo')
	app.register_blueprint(rumor,url_prefix='/rumor')
	app.register_blueprint(perceivedLie,url_prefix='/perceivedLie')
	app.register_blueprint(perceivedSet,url_prefix='/perceivedSet')
	app.register_blueprint(userManage,url_prefix='/userManage')
	app.register_blueprint(index,url_prefix='/index')
	app.register_blueprint(attributeModule)
	app.register_blueprint(influenceModule)
	app.register_blueprint(topicLanModule)
	app.register_blueprint(topicTimeModule)
	app.register_blueprint(topicNetworkModule)
	app.register_blueprint(personSocialModule)
	app.register_blueprint(sensingModule)
	app.register_blueprint(topicSenModule)

	return app
