# -*- coding: utf-8 -*-
import pymysql
# from time_utils import datetime2datestr
from config import SQL_HOST, SQL_USER, SQL_PASSWD, DEFAULT_DB, SQL_CHARSET

import sys
reload(sys)
sys.setdefaultencoding('utf8')

def default_db(host=SQL_HOST, user=SQL_USER, passwd=SQL_PASSWD, db=DEFAULT_DB, charset=SQL_CHARSET):
    conn = pymysql.connect(host=host, user=user, passwd=passwd, db=db, charset=charset, cursorclass=pymysql.cursors.DictCursor)
    return conn

