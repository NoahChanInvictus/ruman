#!/usr/bin/env python
#encoding: utf-8

from flask import Flask, render_template, request, jsonify, Blueprint, send_from_directory, url_for, session
from ruman.db import *
from . import rumor
import json
from ruman.config import *

from ruman.es import *

@rumor.route('/')
def index():

    return render_template('rumor/rumor.html')


@rumor.route('/test/')
def test():
    result = 'Hello World!'
    return json.dumps(result,ensure_ascii=False)

