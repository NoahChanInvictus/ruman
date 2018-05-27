#-*-coding: utf-8-*-
#获得每天操纵预警的数目统计
import sys
reload(sys)
sys.path.append("../../../")
import pandas as pd
from config import *
from time_utils import *
from sql_utils import *

def manipulatewarning(theday):
    print theday
    conn = default_db()
    cur = conn.cursor()
    sql = "SELECT * FROM %s WHERE %s <= '%s' and %s >= '%s'" % (TABLE_DAY,DAY_START_DATE,theday,DAY_END_DATE,theday)
    df = pd.read_sql(sql,conn)
    times = len(df)
    #print df
    order = 'insert into %s ( %s,%s )values("%s", "%d")' % (TABLE_WARNING,WARNING_DATE,WARNING_TIMES,theday,times)
    try:
        cur.execute(order)
        conn.commit()
    except Exception, e:
        print e

def warning_all(year1,month1,day1,year2,month2,day2):
    for date in get_tradelist(year1,month1,day1,year2,month2,day2):
        manipulatewarning(date)

if __name__=="__main__":
    #warning('2016-01-05')
    warning_all(2015,7,1,2018,5,15)