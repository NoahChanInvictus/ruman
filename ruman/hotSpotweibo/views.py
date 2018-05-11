#!/usr/bin/env python
#encoding: utf-8

from flask import Flask, render_template, request, jsonify, Blueprint, send_from_directory, url_for, session
from ruman.db import *
from . import hotSpotweibo
import json
from ruman.config import *

from ruman.es import *

@hotSpotweibo.route('/')
def index():
    return render_template('hotSpotweibo/hotSpotweibo.html')

