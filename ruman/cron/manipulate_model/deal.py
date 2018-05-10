#-*-coding: utf-8-*-
import sys
reload(sys)
sys.path.append("../../")
import pandas as pd
from config import *
from time_utils import *
from sql_utils import *
from elasticsearch import Elasticsearch
from calculate import *
import numpy as np

def delete(df,reason):   #删除空列并补全数据
    if reason == 1:
        df = df.dropna(subset=['%s1day' % (MARKET_PRICE_FU)]).reset_index(drop=True)
        column = [['%s%dday' % (MARKET_PRICE_FU,n) for n in [1,5,20,60,125,250]]]
    elif reason == 2:
        df = df.dropna(subset=['%s1day' % (MARKET_PRICE_FU),'%s1day' % (MARKET_TURNOVER_RATE)]).reset_index(drop=True)   #删除‘price_fu1day’为空的数据
        #df.to_csv(r'/home/lfz/python/deleteb.csv',encoding='utf_8_sig')
        column = [['%s%dday' % (MARKET_PRICE_FU,n) for n in [1,5,20,60,125,250]],['%s%dday' % (MARKET_TURNOVER_RATE,n) for n in [1,5,20,60,125,250]]]
    for l in column:
        for num in range(1,len(l)):   #将后面的数据与前面相同
            indexs = list(df[l[num]][df[l[num]].isnull()].index)
            goodlist = list(df[l[num]])
            for index in indexs:
                goodlist[index] = df[l[num - 1]][index]
            df[l[num]] = goodlist
    #df.to_csv('deletea.csv',encoding='utf_8_sig')
    return df

def add(df,reason):   #添加新变量
    if reason == 1:
        num = 0
        maxpricelist = []
        for n in [1,5,20,60,125,250]:   #添加三类公告数量和的6列
            num += 1
            invest = ANNOUNCEMENT_INVESTMENT + str(n) + 'day'
            pledge = ANNOUNCEMENT_PLEDGE + str(n) + 'day'
            reducing = ANNOUNCEMENT_REDUCING + str(n) + 'day'
            col_name = df.columns.tolist()
            col_name.insert(col_name.index('%s250day' % (ANNOUNCEMENT_REDUCING))+num,'All_announcement' + str(n) + 'day')
            df = df.reindex(columns=col_name)
            df['All_announcement' + str(n) + 'day'] = sum([df[invest],df[pledge],df[reducing]])
        for i in range(len(df)):   #添加最大股价的1列
            maxprice = max(df.loc[i,['%s%dday' % (MARKET_PRICE_FU,n) for n in [1,5,20,60,125,250]]])
            maxpricelist.append(maxprice)
        col_name = df.columns.tolist()
        col_name.insert(col_name.index('%s250day' % (MARKET_PRICE_FU))+1,'maxprice_fu')
        df = df.reindex(columns=col_name)
        df['maxprice_fu'] = maxpricelist
        #df.to_csv(r'/home/lfz/python/add.csv',encoding='utf_8_sig')
        return df
    elif reason == 2:
        num = 0
        maxpricelist = []
        maxratelist = []
        for n in [1,5,20,60,125,250]:   #添加三类公告数量和的6列
            num += 1
            pledge = ANNOUNCEMENT_PLEDGE + str(n) + 'day'
            reducing = ANNOUNCEMENT_PLEDGE + str(n) + 'day'
            profit = ANNOUNCEMENT_PROFIT + str(n) + 'day'
            col_name = df.columns.tolist()
            col_name.insert(col_name.index('%s250day' % (ANNOUNCEMENT_PROFIT))+num,'All_announcement' + str(n) + 'day')
            df = df.reindex(columns=col_name)
            df['All_announcement' + str(n) + 'day'] = sum([df[pledge],df[reducing],df[profit]])
        for i in range(len(df)):   #添加最大股价的1列
            maxprice = max(df.loc[i,['%s%dday' % (MARKET_PRICE_FU,n) for n in [1,5,20,60,125,250]]])
            maxrate = max(df.loc[i,['%s%dday' % (MARKET_TURNOVER_RATE,n) for n in [1,5,20,60,125,250]]])
            maxpricelist.append(maxprice)
            maxratelist.append(maxrate)
        col_name = df.columns.tolist()
        col_name.insert(col_name.index('%s250day' % (MARKET_PRICE_FU))+1,'maxprice_fu')
        col_name.insert(col_name.index('%s250day' % (MARKET_TURNOVER_RATE))+1,'maxturnover_rate')
        df = df.reindex(columns=col_name)
        df['maxprice_fu'] = maxpricelist
        df['maxturnover_rate'] = maxratelist
        #df.to_csv('add.csv',encoding='utf_8_sig')
        return df

def standard(df):   #标准化
    df = df.sort_values(axis=0,ascending=True,by='date').reset_index(drop=True)
    for column in df.columns:
        if column != 'code' and column != 'date':
            datelist = list(set(df['date']))
            datelist.sort()
            l = []
            for date in datelist:
                dflist = list(df.loc[df[df['date'] == date].index.tolist()][column])
                l.extend(dflist - np.mean(dflist))
            df[column] = l #求平均
    #df.to_csv(r'/home/lfz/python/standardnew.csv',encoding='utf_8_sig')
    
    return df

def get_black_list(reason):   #获取黑名单
    conn = default_db()
    cur = conn.cursor()
    sql = "SELECT * FROM %s WHERE %s = '%d'" % (TABLE_BLACK_LIST,BLACK_LIST_REASON,reason)
    cur.execute(sql)
    results = cur.fetchall()
    return results

def get_all_list():   #获取监控名单
    conn = default_db()
    cur = conn.cursor()
    sql = "SELECT * FROM %s WHERE %s = '%d'" % (TABLE_STOCK_LIST,STOCK_LIST_LISTED,1)
    cur.execute(sql)
    results = cur.fetchall()
    return results

def filter(df,reason):   #过滤出所需要的黑名单公司
    conn = default_db()
    cur = conn.cursor()
    if reason == 1:
        black_list = get_black_list(1)
    elif reason == 2:
        black_list = get_black_list(2)
    industry_dict = {}
    frame = pd.DataFrame()
    framenots = pd.DataFrame()
    for blackcode in black_list:   #将不同的公司按照证监会行业类别分组，便于过滤
        if blackcode[BLACK_LIST_INDUSTRY_CODE] not in industry_dict:   #将起止时间放入对应行业之中
            industry_dict[blackcode[BLACK_LIST_INDUSTRY_CODE]] = [blackcode[BLACK_LIST_START_TS],blackcode[BLACK_LIST_END_TS]]
        else:
            if industry_dict[blackcode[BLACK_LIST_INDUSTRY_CODE]][0] > blackcode[BLACK_LIST_START_TS]:
                industry_dict[blackcode[BLACK_LIST_INDUSTRY_CODE]][0] = blackcode[BLACK_LIST_START_TS]
            if industry_dict[blackcode[BLACK_LIST_INDUSTRY_CODE]][1] < blackcode[BLACK_LIST_END_TS]:
                industry_dict[blackcode[BLACK_LIST_INDUSTRY_CODE]][1] = blackcode[BLACK_LIST_END_TS]
    for industry in industry_dict.keys():   #对于不同行业进行操作
        print industry
        codelist = []
        sql = "SELECT * FROM %s WHERE %s = '%s'" % (TABLE_STOCK_LIST,STOCK_LIST_MIDDLE_INDUSTRY_CODE,industry)   #从stocklist中选取对应行业所有公司
        cur.execute(sql)
        results = cur.fetchall()
        for result in results:
            codelist.append(result[STOCK_LIST_STOCK_ID])   #后续数据库会修改，此项会变
        starttime = ts2datetimestr(industry_dict[industry][0]).split('-')
        endtime = ts2datetimestr(industry_dict[industry][1]).split('-')
        datelist = get_tradelist(starttime[0],starttime[1],starttime[2],endtime[0],endtime[1],endtime[2])
        print 'Ready to get black DataFrame...'
        df1 = df[df['code'].isin(codelist)]   #选取含有这些股票的数据
        df2 = df1[df1['date'].isin(datelist)].reset_index(drop=True)   #选取这些股票里带有这些时间的数据
        print 'Ready to delete nan data...'
        df2 = delete(df2,reason)
        print 'Ready to add new DataFrame...'
        df2 = add(df2,reason)
        framenots = pd.concat([framenots,df2]).reset_index(drop=True)
        print 'Ready to standardize DataFrame...'
        df2 = standard(df2)
        frame = pd.concat([frame,df2]).reset_index(drop=True)
    print 'Finish dealing with DataFrame!'
    #framenots.to_csv('/home/lfz/python/yaoyan/modelcode/csv/beforestandard20155.csv',encoding='utf_8_sig')
    #frame.to_csv('frame1.csv',encoding='utf_8_sig')
    return frame

def filter_theday(df,reason):   #过滤出所需要的黑名单公司
    conn = default_db()
    cur = conn.cursor()
    code_list = get_all_list()
    industry_dict = {}
    frame = pd.DataFrame()
    for code in code_list:   #将不同的公司按照证监会行业类别分组，便于过滤
        if code[STOCK_LIST_MIDDLE_INDUSTRY_CODE] not in industry_dict:   #将同一行业的股票放在一组便于标准化
            industry_dict[code[STOCK_LIST_MIDDLE_INDUSTRY_CODE]] = [code[STOCK_LIST_STOCK_ID]]
        else:
            industry_dict[code[STOCK_LIST_MIDDLE_INDUSTRY_CODE]].append(code[STOCK_LIST_STOCK_ID])
    for industry in industry_dict.keys():   #对于不同行业进行操作
        #print industry
        codelist = industry_dict[industry]
        #starttime = ts2datetimestr(industry_dict[industry][0]).split('-')
        #endtime = ts2datetimestr(industry_dict[industry][1]).split('-')
        #datelist = get_tradelist(starttime[0],starttime[1],starttime[2],endtime[0],endtime[1],endtime[2])
        #print 'Ready to get black DataFrame...'
        df1 = df[df['code'].isin(codelist)]   #选取含有这些股票的数据
        #print 'Ready to delete nan data...'
        df1 = delete(df1,reason)
        #print 'Ready to add new DataFrame...'
        df1 = add(df1,reason)
        #if industry == industry_dict.keys()[0]:
        #    df1.to_csv('add%d.csv' % (reason),encoding='utf_8_sig')
        #print 'Ready to standardize DataFrame...'
        df1 = standard(df1)
        frame = pd.concat([frame,df1]).reset_index(drop=True)
    print 'Finish dealing with DataFrame!'
    #frame.to_csv('frameday%d.csv' % (reason),encoding='utf_8_sig')
    return frame

def deal_data(reason,year1,month1,day1,year2,month2,day2):
    if reason == 1:
        df = filter(get_all(reason,year1,month1,day1,year2,month2,day2),reason)   #时间输入为预处理数据的时间范围，尽量与操纵总时期接近以减少计算时间
    elif reason == 2:
        df = filter(get_all(reason,year1,month1,day1,year2,month2,day2),reason)
    return df

def deal_data_theday(reason,theday):
    if reason == 1:
        df = filter_theday(get_all_theday(reason,theday),reason)   #可以选择今天
    elif reason == 2:
        df = filter_theday(get_all_theday(reason,theday),reason)
    #print df
    return df

if __name__=="__main__":
    #filter(get_all(2015,2,2,2015,2,28))
    deal_data_theday(1,'2016-01-04')
    #deal_data(1,2013,5,1,2015,6,30)