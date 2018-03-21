#!/usr/bin/env python
# coding:utf-8
from db import *
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#table
TABLE_HOLDERS = 'holders'
TABLE_DAY = 'manipulate_day'
TABLE_WARNING = 'manipulate_warning'

#es
ES_HOST = '219.224.134.214'
ES_PORT = 9202

#db
HOST = "219.224.134.214"
USER = "root"
PASSWORD = ""
DEFAULT_DB = "ruman"
CHARSET = "utf8"
TEST_DB = ""



#index_name
DAY_STOCK_ID = 'stock_id'
DAY_STOCK_NAME = 'stock_name'
DAY_START_DATE = 'start_date'
DAY_IFEND = 'ifend'
DAY_END_DATE = 'end_date'
DAY_MANIPULATE_TYPE = 'manipulate_type'
DAY_INDUSTRY_NAME = 'industry_name'
DAY_INCREASE_RATIO = 'increase_ratio'
WARNING_DATE = 'date'
WARNING_TIMES = 'times'