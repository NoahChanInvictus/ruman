#!/usr/bin/env python
# encoding: utf-8


from ruman.homePage.views import homePage
from ruman.maniPulate.views import maniPulate
from ruman.rumor.views import rumor
from ruman.perceivedLie.views import perceivedLie
from ruman.perceivedSet.views import perceivedSet
from ruman.userManage.views import userManage
from ruman.index.views import index

from flask import Flask, render_template, request, jsonify, Blueprint

def create_app():
	app = Flask(__name__)
	app.register_blueprint(homePage,url_prefix='/homePage')
	app.register_blueprint(maniPulate,url_prefix='/maniPulate')
	app.register_blueprint(rumor,url_prefix='/rumor')
	app.register_blueprint(perceivedLie,url_prefix='/perceivedLie')
	app.register_blueprint(perceivedSet,url_prefix='/perceivedSet')
	app.register_blueprint(userManage,url_prefix='/userManage')
	app.register_blueprint(index,url_prefix='/index')

	return app
