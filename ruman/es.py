#!/usr/bin/env python
#coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from elasticsearch import Elasticsearch


from ruman.config import *

es = Elasticsearch([{'host':ES_HOST,'port':ES_PORT}])


