#-*-coding: utf-8-*-
#创立操纵模型所需数据的数据框
#前三个函数分别对应日度、季度和日度解禁的导入，中间三个是相对应的每日更新版，最后一个是根据更新日期写出的pro版
import sys
reload(sys)
sys.path.append("../../")
import pandas as pd
from config import *
from time_utils import *
from sql_utils import *
import pandas as pd
from elasticsearch import Elasticsearch

def reades(typenum):    #12为开始，13为结束
    es = Elasticsearch([{'host':ES_HOST,'port':ES_PORT}])
    df = pd.DataFrame(columns=['date','stock_id','title'])
    query_body = {"size":20000,"query":{"match":{"type":typenum}}}
    res = es.search(index=DIC_ANNOUNCEMENT['index'], doc_type=DIC_ANNOUNCEMENT['type'], body=query_body,request_timeout=100)
    hits = res['hits']['hits']
    num = 0
    while 1:
        try:
            a = ts.trade_cal()
            break
        except:
            pass
    if len(hits):
        for hit in hits:
            res = hit['_source']
            hitdf = a[a['calendarDate'] == ts2datetime(res['publish_time'])]
            if hitdf.iloc[0]['isOpen'] == 0:
                dayindex = hitdf.index[0]
                print ts2datetime(res['publish_time']),res['stock_id']
                for i in range(dayindex + 1,dayindex + 30):
                    if a.loc[i]['isOpen'] == 1:
                        date = a.loc[i]['calendarDate']
                        break
            else:
                date = ts2datetime(res['publish_time'])
            df.loc[num] = [date,res['stock_id'],res['title']]
            num += 1
    return df

def get_es_frame_bendi_dingzeng(year1,month1,day1,year2,month2,day2):
    conn = default_db()
    cur = conn.cursor()
    codelist = sorted(list(pd.read_sql("SELECT * FROM %s WHERE listed = 1" % (TABLE_STOCK_LIST),conn)['stock_id']))
    datelist = get_tradelist(year1,month1,day1,year2,month2,day2)
    data_frame_s = pd.DataFrame(data=0,columns=codelist,index=datelist)   #建立列数据框
    data_frame_s = data_frame_s.sort_index(axis=1)
    data_frame_e = pd.DataFrame(data=0,columns=codelist,index=datelist)   #建立列数据框
    data_frame_e = data_frame_e.sort_index(axis=1)
    startdf = reades(12)
    enddf = reades(13)
    '''
    for i in datelist:
        print i
        dfdates = startdf[startdf['date'] == i]
        dfdatee = enddf[enddf['date'] == i]
        ls = []
        le = []
        for code in codelist:
            dfcodes = dfdates[dfdates['stock_id'] == code]
            ls.append(len(dfcodes))
        for code in codelist:
            dfcodee = dfdatee[dfdatee['stock_id'] == code]
            le.append(len(dfcodee))
        data_frame_s.loc[i] = ls
        data_frame_e.loc[i] = le'''
    for i in datelist:
        print i
        dfdates = startdf[startdf['date'] == i]
        dfdatee = enddf[enddf['date'] == i]
        for code in set(dfdates['stock_id']):
            dfcodes = dfdates[dfdates['stock_id'] == code]
            data_frame_s.loc[i][code] = len(dfcodes)
        for code in set(dfdatee['stock_id']):
            dfcodee = dfdatee[dfdatee['stock_id'] == code]
            data_frame_e.loc[i][code] = len(dfcodee)

    data_frame_sta = pd.DataFrame(data=0,columns=data_frame_s.columns,index=data_frame_s.index)   #建立列数据框
    data_frame_dz = pd.DataFrame(columns=['stock_id','start_date','end_date'])
    num = 0

    for code in codelist:
        print code
        codedfs = data_frame_s[code]
        codedfe = data_frame_e[code]
        stadf = data_frame_sta[code]
        for date in data_frame_e.index:
            if codedfe.loc[date] > 0:
                stadf_date = stadf[stadf.index <= date]
                stadf_isanli = stadf_date[stadf_date == 1]   #选出之前在案例内的日期
                if len(stadf_isanli):   #如果之前存在案例
                    lastdate = stadf_isanli.index[-1]
                    codedfs_date = codedfs[(codedfs.index <= date) & (codedfs.index > lastdate)]   #选出来在上个案例和本案例之间的预案
                    codedfs_isstart = codedfs_date[codedfs_date > 0]   #选出其中存在的预案
                    if len(codedfs_isstart) == 1:   #如果预案只有1个
                        stadf_change = stadf[(stadf.index <= date) & (stadf.index >= codedfs_isstart.index[0])]   #直接令这期间的sta为1
                        startdate = codedfs_isstart.index[0]
                        stadf.loc[stadf_change.index] = 1
                        data_frame_dz.loc[num] = [code,startdate,date]
                        num += 1
                    elif len(codedfs_isstart) > 1:   #如果预案大于1个
                        for i in range(-1,-len(codedfs_isstart) - 1,-1):   #向前遍历
                            if i == -len(codedfs_isstart):   #如果已经遍历到最后一个（前面的都相等）
                                stadf_change = stadf[(stadf.index <= date) & (stadf.index >= codedfs_isstart.index[i])]   #直接将最后一个对应日期期间的sta标为1
                                startdate = codedfs_isstart.index[0]
                                stadf.loc[stadf_change.index] = 1
                                break
                            if startdf[startdf['date'] == codedfs_isstart.index[i]].iloc[0]['title'] != startdf[startdf['date'] == codedfs_isstart.index[i - 1]].iloc[0]['title']:   #如果两个日期的预案不一样
                                stadf_change = stadf[(stadf.index <= date) & (stadf.index >= codedfs_isstart.index[i])]   #将前面预案对应日期期间的sta标为1
                                startdate = codedfs_isstart.index[0]
                                stadf.loc[stadf_change.index] = 1
                                break
                        data_frame_dz.loc[num] = [code,startdate,date]
                        num += 1
                else:   #如果没有案例
                    codedfs_date = codedfs[codedfs.index <= date]   #选出之前所有日期
                    codedfs_isstart = codedfs_date[codedfs_date > 0]   #选出其中存在的预案
                    if len(codedfs_isstart) == 1:   #如果预案只有1个
                        stadf_change = stadf[(stadf.index <= date) & (stadf.index >= codedfs_isstart.index[0])]   #直接令这期间的sta为1
                        startdate = codedfs_isstart.index[0]
                        stadf.loc[stadf_change.index] = 1
                        data_frame_dz.loc[num] = [code,startdate,date]
                        num += 1
                    elif len(codedfs_isstart) > 1:   #如果预案大于1个
                        for i in range(-1,-len(codedfs_isstart) - 1,-1):   #向前遍历
                            if i == -len(codedfs_isstart):   #如果已经遍历到最后一个（前面的都相等）
                                stadf_change = stadf[(stadf.index <= date) & (stadf.index >= codedfs_isstart.index[i])]   #直接将最后一个对应日期期间的sta标为1
                                startdate = codedfs_isstart.index[0]
                                stadf.loc[stadf_change.index] = 1
                                break
                            if startdf[startdf['date'] == codedfs_isstart.index[i]].iloc[0]['title'] != startdf[startdf['date'] == codedfs_isstart.index[i - 1]].iloc[0]['title']:   #如果两个日期的预案不一样
                                stadf_change = stadf[(stadf.index <= date) & (stadf.index >= codedfs_isstart.index[i])]   #将前面预案对应日期期间的sta标为1
                                startdate = codedfs_isstart.index[0]
                                stadf.loc[stadf_change.index] = 1
                                break
                        data_frame_dz.loc[num] = [code,startdate,date]
                        num += 1
        data_frame_sta[code] = list(stadf)
    data_frame_s.to_csv('data_frame_s.csv',encoding='utf_8_sig')
    data_frame_e.to_csv('data_frame_e.csv',encoding='utf_8_sig')
    data_frame_sta.to_csv('data_frame_sta.csv',encoding='utf_8_sig')
    data_frame_dz.to_csv('data_frame_dz.csv',encoding='utf_8_sig')
    return data_frame_dz

def calculate(year1,month1,day1,year2,month2,day2):
    conn = default_db()
    cur = conn.cursor()
    #df = get_es_frame_bendi_dingzeng(year1,month1,day1,year2,month2,day2)
    df = pd.DataFrame(data=['000001','2013-09-09','2013-12-16'],columns=['stock_id','start_date','end_date'])
    datelist = get_tradelist(year1 - 1,month1,day1,year2,month2,day2)
    for num in range(len(df)):
        start_date = df.loc[i]['start_date']
        end_date = df.loc[i]['end_date']
        stock_id = df.loc[i]['stock_id']
        start_date_20 = datelist[datelist.index(start_date) - 20]
        sql = "SELECT * FROM " + TABLE_MARKET_DAILY + " WHERE stock_id = %s'" % (stock_id)
        pricedf = pd.read_sql(sql,conn)
        pricelist1 = list(pricedf[(pricedf['date'] >= start_date_20) & (pricedf['date'] <= end_date)]['price_fu'])
        pricelist2 = list(pricedf[(pricedf['date'] >= start_date) & (pricedf['date'] <= end_date)]['price_fu'])
        print pricelist1,len(pricelist1)
        print pricelist2,len(pricelist2)


if __name__=="__main__":
    #get_es_frame_bendi_dingzeng(2012,1,1,2015,12,31)
    calculate(2012,1,1,2015,12,31)