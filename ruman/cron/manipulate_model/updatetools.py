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
                break

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
            break

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
            break


if __name__=="__main__":
    update_day_result()
    #delete_holders_pct()