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

