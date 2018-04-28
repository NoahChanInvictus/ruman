#-*-coding: utf-8-*-
#import pandas as pd
#十大股东导入，注意在windows运行
from WindPy import *
import datetime
import time_utils
from sql_utils import *
import time
import datetime
from time_utils import *

def timelist(list1,list2):   #生成字符串序列的年月日列表
    for i in range(len(list2)):
        list1.append(list2[i].strftime("%Y-%m-%d"))
    return list1

def get_top10byinst(line):   #判断是否为机构投资者
    if line is None:
        return 0,['None','None','None','None','None','None','None','None','None','None']
    else:
        holder_name_list = line.split(';')
        holder_name_listn = []
        count = 0
        for holder_name in holder_name_list:
            if len(holder_name) > 4:
                count += 1
        for i in range(10):
            try:
                teststr = holder_name_list[i]
                holder_name_listn.append(str(holder_name_list[i]))
            except:
                holder_name_listn.append('None')
        return count,holder_name_listn

def get_gudong(start_date,end_date):
    conn = default_db()
    cur = conn.cursor()
    starttime = datetime.datetime.now()
    w.start()
    l = []
    #ldata = w.wsd('000001.SZ', "holder_name", "2015-01-01", "2018-02-01", "order=0;Days=Alldays;Fill=Previous")
    #l = timelist(l,ldata.Times)
    codelists = w.wset("SectorConstituent",u"date=20180301;sector=全部A股").Data   #获取股票代码全套
    #print len(codelists[1])
    for code in range(len(codelists[1])):  #获取所有股票数据，可更改
        #try:
        data = w.wsd(codelists[1][code], "holder_name,holder_top10pct,holder_pctbyinst", start_date, end_date, "order=0;Days=Alldays;Fill=Previous")
        stock_id = codelists[1][code].split('.')[0]
        stock_name = codelists[2][code]
        print stock_id
        #print len(data.Times)
        for time in range(len(data.Times)-1):
            date = datetime2datestr(data.Times[time+1])
            ts = datetimestr2ts(date)
            holder_name = data.Data[0][time+1]
            holder_top10pct = data.Data[1][time+1]
            holder_pctbyinst = data.Data[2][time+1]
            holder_top10byinst = get_top10byinst(holder_name)[0]
            if holder_name is None:
                holder_name = 'None'
            if holder_top10pct is None:
                holder_top10pct = float('nan')
            if holder_pctbyinst is None:
                holder_pctbyinst = float('nan')
            holder_top_list = get_top10byinst(holder_name)[1]
            #print stock_id,stock_name,date,ts, holder_name,holder_top_list[0],holder_top_list[1],holder_top_list[2],holder_top_list[3],holder_top_list[4],holder_top_list[5],holder_top_list[6],holder_top_list[7],holder_top_list[8],holder_top_list[9],holder_top10byinst,holder_top10pct,holder_pctbyinst
            #print holder_name,holder_top10byinst,holder_top10pct,holder_pctbyinst
            order = 'insert into holders( stock_id,stock_name,date,ts,holder_name,holder_top1,holder_top2,holder_top3,holder_top4,holder_top5,holder_top6,holder_top7,holder_top8,holder_top9,holder_top10,holder_top10byinst,holder_top10pct,holder_pctbyinst)values("%s", "%s","%s","%f","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%d","%f","%f")' % (stock_id,stock_name,date,ts, holder_name,holder_top_list[0],holder_top_list[1],holder_top_list[2],holder_top_list[3],holder_top_list[4],holder_top_list[5],holder_top_list[6],holder_top_list[7],holder_top_list[8],holder_top_list[9],holder_top10byinst,holder_top10pct,holder_pctbyinst)
            try:
                cur.execute(order)
                conn.commit()
            except Exception, e:
                print e
        endtime = datetime.datetime.now()
        #a -= 1
        #print 'Fight!已经到',codelists[1][code],'公司啦(￣▽￣)~*！马上搞定！程序用时',(endtime - starttime).seconds,'s','!还剩',len(codelists[1]) - code - 1,'家啦！'
        #except:
            #pass

    print '程序共用时',(datetime.datetime.now() - starttime).seconds,'s'

def get_gudong_everyday(theday=today()):
    get_gudong(theday,theday)

if __name__=="__main__":
    get_gudong('2014-12-31','2018-01-31')