#-*-coding: utf-8-*-
#获得每天操纵预警的数目统计
import pandas as pd
from config import *
from time_utils import *
from sql_utils import *

def warning():
    conn = default_db()
    cur = conn.cursor()
    sql = "SELECT * FROM manipulate_result WHERE result = '%s'" % (1)
    df = pd.read_sql(sql,conn)
    for date in get_tradelist(2016,1,1,2016,12,31):
    	print date
        times = len(df[df['date'] == date].index)
        order = 'insert into manipulate_warning ( date,times )values("%s", "%d")' % (date,times)
        try:
            cur.execute(order)
            conn.commit()
        except Exception, e:
            print e

if __name__=="__main__":
    warning()