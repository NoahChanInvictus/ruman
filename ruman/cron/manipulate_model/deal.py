#-*-coding: utf-8-*-
import pandas as pd
from config import *
from time_utils import *
from sql_utils import *
from elasticsearch import Elasticsearch
from calculate import *
import numpy as np

def delete(df):
    df = df.dropna(subset=['price_fu1day']).reset_index(drop=True)   #删除‘price_fu1day’为空的数据
    #df.to_csv(r'/home/lfz/python/deleteb.csv',encoding='utf_8_sig')
    l = ['price_fu1day','price_fu5day','price_fu20day','price_fu60day','price_fu125day','price_fu250day']
    for num in range(1,len(l)):   #将后面的数据与前面相同
        indexs = list(df[l[num]][df[l[num]].isnull()].index)
        goodlist = list(df[l[num]])
        for index in indexs:
            goodlist[index] = df[l[num - 1]][index]
        df[l[num]] = goodlist
    #df.to_csv(r'/home/lfz/python/deletea.csv',encoding='utf_8_sig')
    return df

def add(df):
    num = 0
    maxpricelist = []
    for n in [1,5,20,60,125,250]:   #添加三类公告数量和的6列
        num += 1
        invest = 'Investment_announcement' + str(n) + 'day'
        pledge = 'Pledge_announcement' + str(n) + 'day'
        reducing = 'Reducing_announcement' + str(n) + 'day'
        col_name = df.columns.tolist()
        col_name.insert(col_name.index('Reducing_announcement250day')+num,'All_announcement' + str(n) + 'day')
        df = df.reindex(columns=col_name)
        df['All_announcement' + str(n) + 'day'] = sum([df[invest],df[pledge],df[reducing]])
    for i in range(len(df)):   #添加最大股价的1列
        maxprice = max(df.loc[i,['price_fu1day','price_fu5day','price_fu20day','price_fu60day','price_fu125day','price_fu250day']])
        maxpricelist.append(maxprice)
    col_name = df.columns.tolist()
    col_name.insert(col_name.index('price_fu250day')+1,'maxprice_fu')
    df = df.reindex(columns=col_name)
    df['maxprice_fu'] = maxpricelist
    #df.to_csv(r'/home/lfz/python/add.csv',encoding='utf_8_sig')
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

def get_black_list():   #获取黑名单
    conn = default_db()
    cur = conn.cursor()
    sql = "SELECT * FROM black_list WHERE reason = '%d'" % (1)
    cur.execute(sql)
    results = cur.fetchall()
    return results

def get_all_list():   #获取监控名单
    conn = default_db()
    cur = conn.cursor()
    sql = "SELECT * FROM stock_list"
    cur.execute(sql)
    results = cur.fetchall()
    return results

def filter(df):   #过滤出所需要的黑名单公司
    conn = default_db()
    cur = conn.cursor()
    black_list = get_black_list()
    industry_dict = {}
    frame = pd.DataFrame()
    framenots = pd.DataFrame()
    for blackcode in black_list:   #将不同的公司按照证监会行业类别分组，便于过滤
        if blackcode['industry_code'] not in industry_dict:   #将起止时间放入对应行业之中
            industry_dict[blackcode['industry_code']] = [blackcode['start_ts'],blackcode['end_ts']]
        else:
            if industry_dict[blackcode['industry_code']][0] > blackcode['start_ts']:
                industry_dict[blackcode['industry_code']][0] = blackcode['start_ts']
            if industry_dict[blackcode['industry_code']][1] < blackcode['end_ts']:
                industry_dict[blackcode['industry_code']][1] = blackcode['end_ts']
    for industry in industry_dict.keys():   #对于不同行业进行操作
        print industry
        codelist = []
        sql = "SELECT * FROM stock_list WHERE middle_industry_code = '%s'" % (industry)   #从stocklist中选取对应行业所有公司
        cur.execute(sql)
        results = cur.fetchall()
        for result in results:
            codelist.append(result['stock_id'])   #后续数据库会修改，此项会变
        starttime = ts2datetimestr(industry_dict[industry][0]).split('-')
        endtime = ts2datetimestr(industry_dict[industry][1]).split('-')
        datelist = get_tradelist(starttime[0],starttime[1],starttime[2],endtime[0],endtime[1],endtime[2])
        print 'Ready to get black DataFrame...'
        df1 = df[df['code'].isin(codelist)]   #选取含有这些股票的数据
        df2 = df1[df1['date'].isin(datelist)].reset_index(drop=True)   #选取这些股票里带有这些时间的数据
        print 'Ready to delete nan data...'
        df2 = delete(df2)
        print 'Ready to add new DataFrame...'
        df2 = add(df2)
        framenots = pd.concat([framenots,df2]).reset_index(drop=True)
        print 'Ready to standardize DataFrame...'
        df2 = standard(df2)
        frame = pd.concat([frame,df2]).reset_index(drop=True)
    print 'Finish dealing with DataFrame!'
    framenots.to_csv('/home/lfz/python/yaoyan/modelcode/csv/beforestandard20155.csv',encoding='utf_8_sig')
    return frame

def filter_theday(df):   #过滤出所需要的黑名单公司
    conn = default_db()
    cur = conn.cursor()
    code_list = get_all_list()
    industry_dict = {}
    frame = pd.DataFrame()
    for code in code_list:   #将不同的公司按照证监会行业类别分组，便于过滤
        if code['middle_industry_code'] not in industry_dict:   #将同一行业的股票放在一组便于标准化
            industry_dict[code['middle_industry_code']] = [code['stock_id']]
        else:
            industry_dict[code['middle_industry_code']].append(code['stock_id'])
    for industry in industry_dict.keys():   #对于不同行业进行操作
        #print industry
        codelist = industry_dict[industry]
        #starttime = ts2datetimestr(industry_dict[industry][0]).split('-')
        #endtime = ts2datetimestr(industry_dict[industry][1]).split('-')
        #datelist = get_tradelist(starttime[0],starttime[1],starttime[2],endtime[0],endtime[1],endtime[2])
        #print 'Ready to get black DataFrame...'
        df1 = df[df['code'].isin(codelist)]   #选取含有这些股票的数据
        #print 'Ready to delete nan data...'
        df1 = delete(df1)
        #print 'Ready to add new DataFrame...'
        df1 = add(df1)
        #print 'Ready to standardize DataFrame...'
        df1 = standard(df1)
        frame = pd.concat([frame,df1]).reset_index(drop=True)
    print 'Finish dealing with DataFrame!'
    return frame

def deal_data():
    df = filter(get_all())   #和生成大数据框的时间一样，因为模型训练模型的数据都是包含在这些条目中筛选出来的
    return df

def deal_data_theday(theday=today()):
    df = filter_theday(get_all_theday_pro(theday))   #可以选择今天
    return df

if __name__=="__main__":
    #filter(get_all(2015,2,2,2015,2,28))
    deal_data_theday()