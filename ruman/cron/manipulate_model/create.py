#-*-coding: utf-8-*-
from createframe import *

table = [['market_daily_new','price_fu'],['holders','holder_top10byinst'],['announce','Investment_announcement'],['announce','Pledge_announcement'],['announce','Reducing_announcement'],['transaction_stat','frequency']]#

def get_frame():
    for l in table:
        #get_sql_frame_bendi(l[0],l[1],2013,1,1,2013,1,4)
        for day in get_tradelist(2016,2,1,2016,12,31):
            print day,l[1]
            get_sql_frame_theday(l[0],l[1],day)
        #get_sql_frame_today(l[0],l[1])['market_daily','price'],['holders','holder_top10byinst'],['announce','Investment_announcement'],['announce','Pledge_announcement'],

if __name__=="__main__":
    get_frame()