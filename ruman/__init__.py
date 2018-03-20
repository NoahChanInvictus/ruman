#!/usr/bin/env python
# encoding: utf-8


from ruman.manipulate.views import homePage
from ruman.manipulate.views import manipulate

from flask import Flask, render_template, request, jsonify, Blueprint

def create_app():
	app = Flask(__name__)
	app.register_blueprint(manipulate,url_prefix='/homepage')
	app.register_blueprint(manipulate,url_prefix='/manipulate')
	
	return app
