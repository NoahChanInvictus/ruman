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
from calculate import *
from elasticsearch import Elasticsearch

'''因为数据不存于es而舍弃
def es_search(tablename):   #在es中获取此数据框的json及其id
    es = Elasticsearch([{'host':ES_HOST,'port':ES_PORT}])
    query_body = {"query": {"bool": {"must": [{"match": {"caozong_index": tablename}}]}}}
    res = es.search(index="dataframe", doc_type="basic_info", body=query_body,request_timeout=100)
    hits = res['hits']['hits']
    for item in hits:
        id = item['_id']
        datajson = item['_source']["json"]
    return id,datajson

def get_sql_frame(tablename,columnname,year1,month1,day1,year2,month2,day2):   #获得历史的各个数据框
    es = Elasticsearch([{'host':ES_HOST,'port':ES_PORT}])
    conn = default_db()
    cur = conn.cursor()
    codelist = pd.read_sql("SELECT * FROM %s" % (TABLE_STOCK_LIST),conn)['stock_id']   #从数据库获取stocklist，作为当前监测对象
    codelists = []
    datelist = get_tradelist(year1,month1,day1,year2,month2,day2)   #获得交易时间列表
    for code in codelist:
        codelists.append(code.split('.')[0])
    data_frame = pd.DataFrame(columns=codelists)   #建立列数据框
    data_frame = data_frame.sort_index(axis=1)
    datenum = 0
    for date in datelist:
        print date,columnname
        try:
            sql = "SELECT * FROM " + tablename + " WHERE date = '%s'" % (date)   #对于每个日期先获取当天的所有股票对应数据
            df = pd.read_sql(sql,conn)
            df = df.sort_values(by='stock_id')   #将获得的该日期数据框按照股票代码排序
            stock_id_list = list(df['stock_id'])
            column_list = list(df[columnname])
            column_list_new = []
            flag = 0
            for num in range(len(codelists)):   #比对监测对象列表和当天含有信息的列表
                if stock_id_list[flag] == codelists[num]:   #如果有即导入，如果没有则加入空值（股价换手率）或0值（除股价换手率）
                    column_list_new.append(column_list[flag])
                else:
                    if tablename == 'market_daily':
                        column_list_new.append(None)
                    else:
                        column_list_new.append(0)
                    flag -= 1
                flag += 1
            data_frame.loc[date] = column_list_new
            datenum += 1
        except:
            pass
    #print data_frame
    indexbody = {"caozong_index":columnname,"json":data_frame.to_json()}   
    es.index(index="dataframe", doc_type="basic_info", body=indexbody)   #首次插入，以后更新
    #id = es_search(columnname)[0]
    #es.update(index="dataframe", doc_type="basic_info", body={"doc":indexbody},id=id)   #更新json'''

def get_sql_frame_bendi_day(tablename,columnname,year1,month1,day1,year2,month2,day2):   #获得历史的各个数据框(日度)：各种公告，大宗交易，私募，股价换手率
    es = Elasticsearch([{'host':ES_HOST,'port':ES_PORT}])
    conn = default_db()
    cur = conn.cursor()
    codelist = sorted(list(pd.read_sql("SELECT * FROM %s WHERE listed = 1" % (TABLE_STOCK_LIST),conn)['stock_id']))   #从数据库获取stocklist，作为当前监测对象
    datelist = get_tradelist(year1,month1,day1,year2,month2,day2)   #获得交易时间列表
    data_frame = pd.DataFrame(columns=codelist)   #建立列数据框
    data_frame = data_frame.sort_index(axis=1)
    datenum = 0
    for date in datelist:
        print date,columnname
        sql = "SELECT * FROM " + tablename + " WHERE date = '%s'" % (date)   #对于每个日期先获取当天的所有股票对应数据
        df = pd.read_sql(sql,conn)
        #df.to_csv('/home/lfz/python/yaoyan/modelcode/test1.csv',encoding='utf_8_sig')
        df = df.sort_values(by='stock_id')   #将获得的该日期数据框按照股票代码排序
        stock_id_list = list(df['stock_id'])
        column_list = list(df[columnname])
        column_list_new = []
        testlist = []
        for num in range(len(codelist)):   #比对监测对象列表和当天含有信息的列表
            try:
                indexnum = stock_id_list.index(codelist[num])   #查找当前股票代码的位置，如果查不到则添加对应0或空
                if tablename == TABLE_MARKET_DAILY:
                    if column_list[indexnum] == 0:
                        column_list_new.append(None)
                    else:
                        column_list_new.append(column_list[indexnum])
                else:
                    column_list_new.append(column_list[indexnum])
            except:
                if tablename == TABLE_MARKET_DAILY:
                    column_list_new.append(None)
                else:
                    column_list_new.append(0)
        data_frame.loc[date] = column_list_new
        datenum += 1
    #print data_frame
    #indexbody = {"caozong_index":columnname,"json":data_frame.to_json()}   
    data_frame.to_json('testdf/' + columnname + '.json')
    #data_frame.to_csv('/home/lfz/python/yaoyan/modelcode/price1.csv',encoding='utf_8_sig')
    #es.index(index="dataframe", doc_type="basic_info", body=indexbody)   #首次插入，以后更新
    #id = es_search(columnname)[0]
    #es.update(index="dataframe", doc_type="basic_info", body={"doc":indexbody},id=id)   #更新json

def get_quarter_list(year1,quarter1,year2,quarter2):   #通通转化为'2015-01-01,2015-04-01'形式，便于统一
    l = []
    if year1 == year2:
        l = ['%d-%d' % (year1,q) for q in range(quarter1,quarter2 + 1)]
    elif year1 == year2 - 1:
        l = ['%d-%d' % (year1,q) for q in range(quarter1,5)]
        l.extend(['%d-%d' % (year2,q) for q in range(1,quarter2 + 1)])
    else:
        l = ['%d-%d' % (year1,q) for q in range(quarter1,5)]
        l1 = []
        for year in range(year1 + 1,year2 + 1):
            l1.extend(['%d-%d' % (year,q) for q in range(1,5)])
        l2 = ['%d-%d' % (year2,q) for q in range(1,quarter2 + 1)]
        l.extend(l1)
        l.extend(l2)

    for i in range(len(l)):
        if int(l[i].split('-')[1]) == 1:
            l[i] = '%s-01-01' % (l[i].split('-')[0])
        elif int(l[i].split('-')[1]) == 2:
            l[i] = '%s-04-01' % (l[i].split('-')[0])
        elif int(l[i].split('-')[1]) == 3:
            l[i] = '%s-07-01' % (l[i].split('-')[0])
        else:
            l[i] = '%s-10-01' % (l[i].split('-')[0])
    return l

def get_sql_frame_bendi_quarter(tablename,columnname,year1,quarter1,year2,quarter2):   #获取季度数据
    conn = default_db()
    cur = conn.cursor()
    codelist = sorted(list(pd.read_sql("SELECT * FROM %s WHERE listed = 1" % (TABLE_STOCK_LIST),conn)['stock_id']))   #从数据库获取stocklist，作为当前监测对象
    quarterlist = get_quarter_list(year1,quarter1,year2,quarter2)
    data_frame = pd.DataFrame(columns=codelist)   #建立列数据框
    data_frame = data_frame.sort_index(axis=1)
    datenum = 0
    for date in quarterlist:
        print date,columnname
        try:
            sql = "SELECT * FROM " + tablename + " WHERE date = '%s'" % (date)   #对于每个日期先获取当天的所有股票对应数据
            df = pd.read_sql(sql,conn)
            #df.to_csv('/home/lfz/python/yaoyan/modelcode/test1.csv',encoding='utf_8_sig')
            df = df.sort_values(by='stock_id')   #将获得的该日期数据框按照股票代码排序
            stock_id_list = list(df['stock_id'])
            column_list = list(df[columnname])
            column_list_new = []
            testlist = []
            for num in range(len(codelist)):   #比对监测对象列表和当天含有信息的列表
                try:
                    indexnum = stock_id_list.index(codelist[num])   #查找当前股票代码的位置，如果查不到则添加对应0或空
                    if tablename == TABLE_NETPROFIT:
                        if column_list[indexnum] == 0:
                            column_list_new.append(None)
                        else:
                            column_list_new.append(column_list[indexnum])
                    else:
                        column_list_new.append(column_list[indexnum])
                except:
                    if tablename == TABLE_NETPROFIT:
                        column_list_new.append(None)
                    else:
                        column_list_new.append(0)
            data_frame.loc[date] = column_list_new
            datenum += 1
        except:
            pass
    #print data_frame
    #indexbody = {"caozong_index":columnname,"json":data_frame.to_json()}   
    data_frame.to_json('testdf/' + columnname + '.json')

def get_sql_frame_bendi_jiejin(tablename,columnname,year1,month1,day1,year2,month2,day2):   #获取解禁日度数据,保证开始日期早于数据日期1年
    conn = default_db()
    cur = conn.cursor()
    codelist = sorted(list(pd.read_sql("SELECT * FROM %s WHERE listed = 1" % (TABLE_STOCK_LIST),conn)['stock_id']))
    data_frame = pd.DataFrame(columns=codelist)   #建立列数据框
    data_frame = data_frame.sort_index(axis=1)
    datelist = get_tradelist(year1,month1,day1,year2,month2,day2)   #获得交易时间列表
    jiejindata = pd.read_sql("SELECT * FROM %s" % (TABLE_JIEJIN),conn)
    for date in datelist:
        print date,columnname
        jiejinstock = jiejindata[jiejindata[JIEJIN_DATE] <= date]
        l = []
        for i in codelist:
            jiejinlist = sorted(list(jiejinstock[jiejinstock[JIEJIN_STOCK_ID] == i][JIEJIN_DATE]))
            if jiejinlist:
                if jiejinlist[-1] == date:
                    l.append(1)
                elif datelist.index(date) - datelist.index(jiejinlist[-1]) <= 5:
                    l.append(2)
                elif datelist.index(date) - datelist.index(jiejinlist[-1]) <= 20:
                    l.append(3)
                elif datelist.index(date) - datelist.index(jiejinlist[-1]) <= 60:
                    l.append(4)
                elif datelist.index(date) - datelist.index(jiejinlist[-1]) <= 125:
                    l.append(5)
                elif datelist.index(date) - datelist.index(jiejinlist[-1]) <= 250:
                    l.append(6)
                else:
                    l.append(7)
            else:
                l.append(8)
        data_frame.loc[date] = l

    data_frame.to_json('testdf/' + columnname + '.json')


def get_sql_frame_bendi_holders(tablename,columnname,year1,month1,day1,year2,month2,day2):
    es = Elasticsearch([{'host':ES_HOST,'port':ES_PORT}])
    conn = default_db()
    cur = conn.cursor()
    codelist = sorted(list(pd.read_sql("SELECT * FROM %s WHERE listed = 1" % (TABLE_STOCK_LIST),conn)['stock_id']))
    datelist = get_tradelist(year1,month1,day1,year2,month2,day2)   #获得交易时间列表
    data_frame = pd.DataFrame(columns=codelist)   #建立列数据框
    data_frame = data_frame.sort_index(axis=1)
    for date in datelist:
        print date,columnname


def get_sql_frame_day_theday(tablename,columnname,theday=today()):   #每天更新数据框，增添或删除列，增添行
    es = Elasticsearch([{'host':ES_HOST,'port':ES_PORT}])
    conn = default_db()
    cur = conn.cursor()
    codelist = sorted(list(pd.read_sql("SELECT * FROM %s" % (TABLE_STOCK_LIST),conn)['stock_id']))
    if theday in get_tradelist_all():
        datelist = [theday]
        data_frame = pd.read_json('dataframe/' + columnname + '.json')   #读取已经存入本地的json
        data_frame = data_frame.sort_index(axis=1)   #json读取会产生顺序变化故重排序
        codenum = data_frame.columns.size
        if len(codelist) > codenum:   #如果有股票新上市则插入列
            newcodelist = set(data_frame.columns) ^ set(codelist)   #看两个列表是否相同
            if tablename == TABLE_MARKET_DAILY:
                for newcode in newcodelist:
                    data_frame[newcode] = None
            else:
                for newcode in newcodelist:
                    data_frame[newcode] = 0
            data_frame = data_frame.sort_index(axis=1)
        if len(codelist) < codenum:   #如果有股票退市则删除列
            newcodelist = set(data_frame.columns) ^ set(codelist)
            for newcode in newcodelist:
                del data_frame[newcode]
        for date in datelist:
            #print date
            #print data_frame
            print date,columnname
            try:
                sql = "SELECT * FROM " + tablename + " WHERE date = '%s'" % (date)   
                df = pd.read_sql(sql,conn)
                df = df.sort_values(by='stock_id')
                stock_id_list = list(df['stock_id'])
                column_list = list(df[columnname])
                column_list_new = []
                for num in range(len(codelist)):   #比对监测对象列表和当天含有信息的列表
                    try:
                        indexnum = stock_id_list.index(codelist[num])   #查找当前股票代码的位置，如果查不到则添加对应0或空
                        if tablename == TABLE_MARKET_DAILY:
                            if column_list[indexnum] == 0:
                                column_list_new.append(None)
                            else:
                                column_list_new.append(column_list[indexnum])
                        else:
                            column_list_new.append(column_list[indexnum])
                    except:
                        if tablename == TABLE_MARKET_DAILY:
                            column_list_new.append(None)
                        else:
                            column_list_new.append(0)
                data_frame.loc[pd.Timestamp(int(date.split('-')[0]),int(date.split('-')[1]),int(date.split('-')[2]))] = column_list_new   #pandas会将datestr转化为时间戳，故需手动转化写入
                #print data_frame
                #print column_list_new
                #print data_frame
            except:
                pass
        #indexbody = {"caozong_index":columnname,"json":data_frame.to_json()}
        #print data_frame.to_json()[:50000]
        data_frame.to_json('dataframe/' + columnname + '.json')
        #es.index(index="dataframe", doc_type="basic_info", body=indexbody)
        #id = es_search(tablename)[0]
        #es.update(index="dataframe", doc_type="basic_info", body={"doc":indexbody},id=id)
        #print data_frame

def get_sql_frame_quarter_theday(tablename,columnname,theday=today()):   #每季度初更新数据框，增添或删除列，增添行
    es = Elasticsearch([{'host':ES_HOST,'port':ES_PORT}])
    conn = default_db()
    cur = conn.cursor()
    codelist = sorted(list(pd.read_sql("SELECT * FROM %s" % (TABLE_STOCK_LIST),conn)['stock_id']))
    if int(theday.split('-')[1]) in [1,4,7,10] and int(theday.split('-')[2]) == 1:
        if tablename == TABLE_NETPROFIT:
            quarterlist = [what_quarter(theday)[0]]
        else:
            quarterlist = [theday]
        data_frame = pd.read_json('dataframe/' + columnname + '.json')   #读取已经存入本地的json
        data_frame = data_frame.sort_index(axis=1)   #json读取会产生顺序变化故重排序
        codenum = data_frame.columns.size
        if len(codelist) > codenum:   #如果有股票新上市则插入列
            newcodelist = set(data_frame.columns) ^ set(codelist)   #看两个列表是否相同
            if tablename == TABLE_NETPROFIT:
                for newcode in newcodelist:
                    data_frame[newcode] = None
            else:
                for newcode in newcodelist:
                    data_frame[newcode] = 0
            data_frame = data_frame.sort_index(axis=1)
        if len(codelist) < codenum:   #如果有股票退市则删除列
            newcodelist = set(data_frame.columns) ^ set(codelist)
            for newcode in newcodelist:
                del data_frame[newcode]
        for date in quarterlist:
            print date,columnname
            try:
                sql = "SELECT * FROM " + tablename + " WHERE date = '%s'" % (date)   #对于每个日期先获取当天的所有股票对应数据
                df = pd.read_sql(sql,conn)
                #df.to_csv('/home/lfz/python/yaoyan/modelcode/test1.csv',encoding='utf_8_sig')
                df = df.sort_values(by='stock_id')   #将获得的该日期数据框按照股票代码排序
                stock_id_list = list(df['stock_id'])
                column_list = list(df[columnname])
                column_list_new = []
                testlist = []
                for num in range(len(codelist)):   #比对监测对象列表和当天含有信息的列表
                    try:
                        indexnum = stock_id_list.index(codelist[num])   #查找当前股票代码的位置，如果查不到则添加对应0或空
                        if tablename == TABLE_NETPROFIT:
                            if column_list[indexnum] == 0:
                                column_list_new.append(None)
                            else:
                                column_list_new.append(column_list[indexnum])
                        else:
                            column_list_new.append(column_list[indexnum])
                    except:
                        if tablename == TABLE_NETPROFIT:
                            column_list_new.append(None)
                        else:
                            column_list_new.append(0)
                data_frame.loc[pd.Timestamp(int(date.split('-')[0]),int(date.split('-')[1]),int(date.split('-')[2]))] = column_list_new   #pandas会将datestr转化为时间戳，故需手动转化写入
            except:
                pass
        #print data_frame
        #indexbody = {"caozong_index":columnname,"json":data_frame.to_json()}   
        data_frame.to_json('dataframe/' + columnname + '.json')

def get_sql_frame_jiejin_theday(tablename,columnname,theday=today()):   #每天更新数据框，增添或删除列，增添行
    es = Elasticsearch([{'host':ES_HOST,'port':ES_PORT}])
    conn = default_db()
    cur = conn.cursor()
    codelist = sorted(list(pd.read_sql("SELECT * FROM %s" % (TABLE_STOCK_LIST),conn)['stock_id']))
    if theday in get_tradelist_all():
        tradelist = [theday]
        datelist = get_tradelist(2011,1,1,int(theday.split('-')[0]),int(theday.split('-')[1]),int(theday.split('-')[2]))   #获得交易时间列表
        data_frame = pd.read_json('dataframe/' + columnname + '.json')   #读取已经存入本地的json
        data_frame = data_frame.sort_index(axis=1)   #json读取会产生顺序变化故重排序
        codenum = data_frame.columns.size
        if len(codelist) > codenum:   #如果有股票新上市则插入列
            newcodelist = set(data_frame.columns) ^ set(codelist)   #看两个列表是否相同
            for newcode in newcodelist:
                data_frame[newcode] = 8
            data_frame = data_frame.sort_index(axis=1)
        if len(codelist) < codenum:   #如果有股票退市则删除列
            newcodelist = set(data_frame.columns) ^ set(codelist)
            for newcode in newcodelist:
                del data_frame[newcode]
        jiejindata = pd.read_sql("SELECT * FROM %s" % (TABLE_JIEJIN),conn)
        for date in tradelist:
            print date,columnname
            jiejinstock = jiejindata[jiejindata[JIEJIN_DATE] <= date]
            l = []
            for i in codelist:
                jiejinlist = sorted(list(jiejinstock[jiejinstock[JIEJIN_STOCK_ID] == i][JIEJIN_DATE]))
                if jiejinlist:
                    if jiejinlist[-1] == date:
                        l.append(1)
                    elif datelist.index(date) - datelist.index(jiejinlist[-1]) <= 5:
                        l.append(2)
                    elif datelist.index(date) - datelist.index(jiejinlist[-1]) <= 20:
                        l.append(3)
                    elif datelist.index(date) - datelist.index(jiejinlist[-1]) <= 60:
                        l.append(4)
                    elif datelist.index(date) - datelist.index(jiejinlist[-1]) <= 125:
                        l.append(5)
                    elif datelist.index(date) - datelist.index(jiejinlist[-1]) <= 250:
                        l.append(6)
                    else:
                        l.append(7)
                else:
                    l.append(8)
            data_frame.loc[pd.Timestamp(int(date.split('-')[0]),int(date.split('-')[1]),int(date.split('-')[2]))] = l   #pandas会将datestr转化为时间戳，故需手动转化写入

        data_frame.to_json('dataframe/' + columnname + '.json')
'''
def get_sql_frame_today_pro(tablename,columnname,theday=today()):
    trade_before = ts2datetimestr(datetimestr2ts(theday) - 2592000).split('-')   #获取前30天日期
    trade_after = ts2datetimestr(datetimestr2ts(theday) + 2592000).split('-')   #获取后30天日期
    trade_list = get_tradelist(int(trade_before[0]),int(trade_before[1]),int(trade_before[2]),int(trade_after[0]),int(trade_after[1]),int(trade_after[2]))   #获取可能包含当天的交易日列表
    year = int(theday.split('-')[0])
    month = int(theday.split('-')[1])
    day = int(theday.split('-')[2])
    if theday in trade_list:
        get_sql_frame_day_theday(tablename,columnname,theday)
        get_sql_frame_jiejin_theday(tablename,columnname,theday)
    if int(theday.split('-')[1]) in [1,4,7,10] and int(theday.split('-')[2]) == 1:
        get_sql_frame_quarter_theday(tablename,columnname,theday)'''

if __name__=="__main__":
    #get_sql_frame()
    #for day in get_tradelist(2016,1,1,2016,1,31):
    #    get_sql_frame_today_pro(day)
    #get_sql_frame_day_theday('announcement','Profit_announcement','2015-12-31')
    get_sql_frame_bendi_day(TABLE_TRANSACTION_STAT,TRANSACTION_STAT_FREQUENCY,2013,1,1,2013,1,31)
    #get_sql_frame_bendi_day('announcement','Profit_announcement',2013,1,1,2015,12,30)
    #get_sql_frame_bendi_quarter('netprofit','netprofit',2012,1,2015,4)
    #get_sql_frame_quarter_theday('netprofit','netprofit','2016-01-01')
    #get_sql_frame_bendi_quarter('holders_pct','holder_pctbyinst',2013,1,2015,4)
    #get_sql_frame_jiejin_theday('jiejin','jiejin_date','2016-04-01')

'''
测试状况：
get_sql_frame_bendi_day   利润分配公告添加成功，换手率添加成功
get_sql_frame_bendi_quarter   净利润添加成功，股东比例添加成功
get_sql_frame_bendi_jiejin   解禁信息添加成功
get_sql_frame_day_theday  复权每日增添成功，大宗交易增添成功，总体成功
get_sql_frame_quarter_theday   净利润每季度添加成功
get_sql_frame_jiejin_theday   解禁日度信息添加成功
'''