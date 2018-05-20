#-*-coding: utf-8-*-
#一些手动更新表格数据的工具
import sys
reload(sys)
sys.path.append("../../")
import pandas as pd
from config import *
from time_utils import *
from sql_utils import *

def update_day_result():
    conn = default_db()
    cur = conn.cursor()
    sql = "SELECT * FROM %s where %s = '%d'" % (TABLE_RESULT,RESULT_RESULT,1)
    cur.execute(sql)
    results = cur.fetchall()
    for result in results:
        if result[RESULT_PROBABILITY] < 0.75:
            update = "UPDATE %s SET %s = '%d' WHERE %s = %d" % (TABLE_RESULT,RESULT_RESULT,0,RESULT_ID,result[RESULT_ID])
            try:
                cur.execute(update)
                conn.commit()
            except Exception, e:
                print e

def delete_holders():
    conn = default_db()
    cur = conn.cursor()
    sql = "SELECT * FROM %s where %s >= '%s'" % (ES_TABLE_HOLDERS,ES_HOLDERS_SHOW_DATE,'2018-02-01')
    cur.execute(sql)
    results = cur.fetchall()
    print len(results)
    for result in results:
        delete = "DELETE FROM %s WHERE %s = %d" % (ES_TABLE_HOLDERS,ES_HOLDERS_SHOW_ID,result[ES_HOLDERS_SHOW_ID])
        try:
            cur.execute(delete)
            conn.commit()
        except Exception, e:
            print e

def delete_holders_pct():
    conn = default_db()
    cur = conn.cursor()
    sql = "SELECT * FROM %s where %s >= '%s'" % (TABLE_HOLDERS_PCT,ES_HOLDERS_PCT_DATE,'2018-04-01')
    cur.execute(sql)
    results = cur.fetchall()
    print len(results)
    for result in results:
        delete = "DELETE FROM %s WHERE %s = %d" % (TABLE_HOLDERS_PCT,ES_HOLDERS_PCT_ID,result[ES_HOLDERS_PCT_ID])
        try:
            cur.execute(delete)
            conn.commit()
        except Exception, e:
            print e

def update_day_label():
    conn = default_db()
    cur = conn.cursor()
    sql = "SELECT * FROM %s WHERE %s = '0'" % (TABLE_DAY,DAY_MANIPULATE_LABEL)
    cur.execute(sql)
    results = cur.fetchall()
    num = len(results)
    for result in results:
        print num
        update = "UPDATE %s SET %s = '%d' WHERE %s = %d" % (TABLE_DAY,DAY_MANIPULATE_LABEL,1,DAY_ID,result[DAY_ID])
        try:
            cur.execute(update)
            conn.commit()
        except Exception, e:
            print e
        num -= 1

def delete_day_type():
    conn = default_db()
    cur = conn.cursor()
    sql = "SELECT * FROM %s WHERE %s = '%d'" % (TABLE_DAY,DAY_MANIPULATE_TYPE,5)
    cur.execute(sql)
    results = cur.fetchall()
    num = len(results)
    for result in results:
        print num
        delete = "DELETE FROM %s WHERE %s = %d" % (TABLE_DAY,DAY_ID,result[DAY_ID])
        try:
            cur.execute(delete)
            conn.commit()
        except Exception, e:
            print e
        num -= 1

if __name__=="__main__":
    update_day_label()
    #delete_holders_pct()
    #delete_day_type()