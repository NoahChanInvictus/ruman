#-*-coding: utf-8-*-
import pandas as pd
from config import *
from time_utils import *
from sql_utils import *
from elasticsearch import Elasticsearch

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
    codelist = pd.read_sql("SELECT * FROM stock_list",conn)['stock_id']   #从数据库获取stocklist，作为当前监测对象
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
    #es.update(index="dataframe", doc_type="basic_info", body={"doc":indexbody},id=id)   #更新json

def get_sql_frame_bendi(tablename,columnname,year1,month1,day1,year2,month2,day2):   #获得历史的各个数据框
    es = Elasticsearch([{'host':ES_HOST,'port':ES_PORT}])
    conn = default_db()
    cur = conn.cursor()
    codelist = pd.read_sql("SELECT * FROM stock_list",conn)['stock_id']   #从数据库获取stocklist，作为当前监测对象
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
            #df.to_csv('/home/lfz/python/yaoyan/modelcode/test1.csv',encoding='utf_8_sig')
            df = df.sort_values(by='stock_id')   #将获得的该日期数据框按照股票代码排序
            stock_id_list = list(df['stock_id'])
            column_list = list(df[columnname])
            column_list_new = []
            testlist = []
            for num in range(len(codelists)):   #比对监测对象列表和当天含有信息的列表
                try:
                    indexnum = stock_id_list.index(codelists[num])   #查找当前股票代码的位置，如果查不到则添加对应0或空
                    if tablename == 'market_daily_new':
                        if column_list[indexnum] == 0:
                            column_list_new.append(None)
                        else:
                            column_list_new.append(column_list[indexnum])
                    else:
                        column_list_new.append(column_list[indexnum])
                except:
                    if tablename == 'market_daily_new':
                        column_list_new.append(None)
                    else:
                        column_list_new.append(0)
            data_frame.loc[date] = column_list_new
            datenum += 1
        except:
            pass
    #print data_frame
    indexbody = {"caozong_index":columnname,"json":data_frame.to_json()}   
    data_frame.to_json('/home/lfz/python/yaoyan/df/' + columnname + '.json')
    #data_frame.to_csv('/home/lfz/python/yaoyan/modelcode/price1.csv',encoding='utf_8_sig')
    #es.index(index="dataframe", doc_type="basic_info", body=indexbody)   #首次插入，以后更新
    #id = es_search(columnname)[0]
    #es.update(index="dataframe", doc_type="basic_info", body={"doc":indexbody},id=id)   #更新json

def get_sql_frame_theday(tablename,columnname,theday=today()):   #每天更新数据框，增添或删除列，增添行
    es = Elasticsearch([{'host':ES_HOST,'port':ES_PORT}])
    conn = default_db()
    cur = conn.cursor()
    codelist = pd.read_sql("SELECT * FROM stock_list",conn)['stock_id']
    codelists = []
    datelist = []
    datelist.append(theday)
    for code in codelist:
        codelists.append(code.split('.')[0])
    data_frame = pd.read_json('/home/lfz/python/yaoyan/df/' + columnname + '.json')   #读取已经存入本地的json
    data_frame = data_frame.sort_index(axis=1)   #json读取会产生顺序变化故重排序
    codenum = data_frame.columns.size
    if len(codelists) > codenum:   #如果有股票新上市则插入列
        newcodelist = set(data_frame.columns) ^ set(codelists)   #看两个列表是否相同
        if tablename == 'market_daily_new':
            for newcode in newcodelist:
                data_frame[newcode] = None
        else:
            for newcode in newcodelist:
                data_frame[newcode] = 0
        data_frame = data_frame.sort_index(axis=1)
    if len(codelists) < codenum:   #如果有股票退市则删除列
        newcodelist = set(data_frame.columns) ^ set(codelists)
        for newcode in newcodelist:
            del data_frame[newcode]
    for date in datelist:
        #print date
        #print data_frame
        try:
            sql = "SELECT * FROM " + tablename + " WHERE date = '%s'" % (date)   
            df = pd.read_sql(sql,conn)
            df = df.sort_values(by='stock_id')
            stock_id_list = list(df['stock_id'])
            column_list = list(df[columnname])
            column_list_new = []
            for num in range(len(codelists)):   #比对监测对象列表和当天含有信息的列表
                try:
                    indexnum = stock_id_list.index(codelists[num])   #查找当前股票代码的位置，如果查不到则添加对应0或空
                    if tablename == 'market_daily_new':
                        if column_list[indexnum] == 0:
                            column_list_new.append(None)
                        else:
                            column_list_new.append(column_list[indexnum])
                    else:
                        column_list_new.append(column_list[indexnum])
                except:
                    if tablename == 'market_daily_new':
                        column_list_new.append(None)
                    else:
                        column_list_new.append(0)
            data_frame.loc[pd.Timestamp(int(date.split('-')[0]),int(date.split('-')[1]),int(date.split('-')[2]))] = column_list_new   #pandas会将datestr转化为时间戳，故需手动转化写入
            #print column_list_new
            #print data_frame
        except:
            pass
    indexbody = {"caozong_index":columnname,"json":data_frame.to_json()}
    #print data_frame.to_json()[:50000]
    data_frame.to_json('/home/lfz/python/yaoyan/df/' + columnname + '.json')
    #es.index(index="dataframe", doc_type="basic_info", body=indexbody)
    #id = es_search(tablename)[0]
    #es.update(index="dataframe", doc_type="basic_info", body={"doc":indexbody},id=id)
    #print data_frame

def get_sql_frame_today_pro(theday=today()):
    trade_before = ts2datetimestr(datetimestr2ts(theday) - 2592000).split('-')   #获取前30天日期
    trade_after = ts2datetimestr(datetimestr2ts(theday) + 2592000).split('-')   #获取后30天日期
    trade_list = get_tradelist(int(trade_before[0]),int(trade_before[1]),int(trade_before[2]),int(trade_after[0]),int(trade_after[1]),int(trade_after[2]))   #获取可能包含当天的交易日列表
    year = int(theday.split('-')[0])
    month = int(theday.split('-')[1])
    day = int(theday.split('-')[2])
    if theday in trade_list:
        get_sql_frame_today(theday)

if __name__=="__main__":
    #get_sql_frame()
    for day in get_tradelist(2016,1,1,2016,1,31):
        get_sql_frame_today_pro(day)