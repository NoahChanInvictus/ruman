#-*-coding: utf-8-*-
import pandas as pd
import math
from config import *
from time_utils import *
from sql_utils import *
from elasticsearch import Elasticsearch
from createframe import es_search

class one2six_frame:   #生成历史各个数据框的类
    def __init__(self,tablename):
        self.tablename = tablename
        #self.data_frame = pd.read_json(es_search(tablename)[1])
        readframe = pd.read_json('/home/lfz/python/yaoyan/df/2015-5/' + tablename + '.json')
        readframe = readframe.sort_index(axis=1)   #因为json读取问题而必须重新按列排序一下
        self.data_frame = readframe
        #if tablename == 'Investment_announcement':
            #self.data_frame.to_csv(r'/home/lfz/python/invest.csv',encoding='utf_8_sig')
        #print self.data_frame

    def other_towhatday(self,num):   #除收益率换手率其他的都是计算频率
        framewhatday = pd.DataFrame(columns=self.data_frame.columns)
        if num == 1:    #如果要一天的数据直接返回原数据框
            return self.data_frame
        else:
            for datenum in range(len(self.data_frame.index)):   
                sumlist = []
                for count in range(num):
                    sumlist.append(self.data_frame.loc[self.data_frame.index[datenum - count]])
                    if count == datenum:
                        break
                framewhatday.loc[self.data_frame.index[datenum]] = list(sum(sumlist))   #获取上述n列的和,切记转化为列表，否则因为读取的json的数据框股票代码是整数，会导致匹配错误
            return framewhatday

    def market_towhatday(self,num):   #计算对数收益率
        framewhatday = pd.DataFrame(columns=self.data_frame.columns)
        for datenum in range(len(self.data_frame.index)):
            #datestr = date.strftime('%Y-%m-%d')
            if datenum < num:
                framewhatday.loc[self.data_frame.index[datenum]] = None
            else:
                a = self.data_frame.loc[self.data_frame.index[datenum]]
                b = self.data_frame.loc[self.data_frame.index[datenum - num]]
                #print a,b
                framewhatday.loc[self.data_frame.index[datenum]] = list(pd.Series([math.log(i) for i in a]) - pd.Series([math.log(i) for i in b]))
        #print framewhatday
        return framewhatday

    def simu(self):   #私募不需要进行天数分别，只计算相比于上一季度的新增数（约为60个交易日）
        framewhatday = pd.DataFrame(columns=self.data_frame.columns)
        for datenum in range(len(self.data_frame.index)):
            if datenum < 60:
                framewhatday.loc[self.data_frame.index[datenum]] = 0
            else:
                framewhatday.loc[self.data_frame.index[datenum]] = list(self.data_frame.loc[self.data_frame.index[datenum]] - self.data_frame.loc[self.data_frame.index[datenum - 60]])
        return framewhatday
'''
    def towhatday(self,num):   #针对不同的数据框调用不同函数
        if self.tablename == 'market_daily':
            market_towhatday(self,num)
        elif self.tablename == 'simu':
            simu(self)
        else:
            other_towhatday(self,num)'''

class one2six_frame_theday:   #生成历史各个数据框的类
    def __init__(self,tablename,theday):
        self.tablename = tablename
        #readframe = pd.read_json(es_search(tablename)[1])
        readframe = pd.read_json('/home/lfz/python/yaoyan/df/' + tablename + '.json')
        readframe = readframe.sort_index(axis=1)
        indexlist = []
        for index in readframe.index:
            indexlist.append(str(index).split()[0])
        try:
            self.data_frame = readframe.loc[readframe.index[indexlist.index(theday) - 250:indexlist.index(theday)+1]]   #通过查找对应日期选取出该日期前251交易日的记录
        except:
            raise IndexError
        #if tablename == 'Investment_announcement':
            #self.data_frame.to_csv(r'/home/lfz/python/invest.csv',encoding='utf_8_sig')
        #print self.data_frame

    def other_towhatday(self,num):   #除收益率换手率其他的都是计算频率
        framewhatday = pd.DataFrame(columns=self.data_frame.columns)
        if num == 1:    #如果要一天的数据直接返回原数据框
            return self.data_frame
        else:
            datenum = 250
            sumlist = []
            for count in range(num):
                sumlist.append(self.data_frame.loc[self.data_frame.index[datenum - count]])
            framewhatday.loc[self.data_frame.index[datenum]] = list(sum(sumlist))   #获取上述n列的和,切记转化为列表，否则因为读取的json的数据框股票代码是整数，会导致匹配错误
            return framewhatday

    def market_towhatday(self,num):   #计算对数收益率
        framewhatday = pd.DataFrame(columns=self.data_frame.columns)
        datenum = 250
        #datestr = date.strftime('%Y-%m-%d')
        a = self.data_frame.loc[self.data_frame.index[datenum]]
        b = self.data_frame.loc[self.data_frame.index[datenum - num]]
        framewhatday.loc[self.data_frame.index[datenum]] = list(pd.Series([math.log(i) for i in a]) - pd.Series([math.log(i) for i in b]))
        #print framewhatday
        return framewhatday

    def simu(self):   #私募不需要进行天数分别，只计算相比于上一季度的新增数（约为60个交易日）
        framewhatday = pd.DataFrame(columns=self.data_frame.columns)
        datenum = 250
        framewhatday.loc[self.data_frame.index[datenum]] = list(self.data_frame.loc[self.data_frame.index[datenum]] - self.data_frame.loc[self.data_frame.index[datenum - 60]])
        return framewhatday

def get_all():
    conn = default_db()
    cur = conn.cursor()
    readframe = pd.read_json('/home/lfz/python/yaoyan/df/2015-5/price_fu.json')   #对于需要使用的json进行读取，需更改
    codelist = readframe.columns
    codelists = []
    for code in codelist:
        codelists.append('%06d' % code)
    codelists.sort()
    datelist = []
    for date in readframe.index:
        datelist.append(str(date).split()[0])
    datelist_frame = datelist*len(codelists)   #生成股票数量的时间序列
    codelists_frame = []
    for code in codelists:
        codelists_frame += [code]*len(datelist)   #每个股票对应时间序列的个数
    df = pd.DataFrame()
    df['date'] = datelist_frame
    df['code'] = codelists_frame
    tablelist = ['price_fu','holder_top10byinst','Investment_announcement','Pledge_announcement','Reducing_announcement','frequency']
    print 'Ready to create DataFrame...'
    for tablename in tablelist:   #对于31个数据框循环计算
        if tablename == tablelist[0]:   #对于不同的表采用不同的算法
            calculate = one2six_frame(tablename)
            for n in [1,5,20,60,125,250]:
                print 'Creating DataFrame ' + tablename + str(n) + 'day' + ' ...'
                frame = calculate.market_towhatday(n)
                df[tablename + str(n) + 'day'] = pd.concat([frame[code] for code in frame.columns]).reset_index(drop=True)   #将每一列取出后重排，作为新数据框的一列
        elif tablename == tablelist[1]:
            print 'Creating DataFrame ' + tablename + ' ...'
            calculate = one2six_frame(tablename)
            frame = calculate.simu()
            df[tablename] = pd.concat([frame[code] for code in frame.columns]).reset_index(drop=True)
        else:
            calculate = one2six_frame(tablename)
            for n in [1,5,20,60,125,250]:
                print 'Creating DataFrame ' + tablename + str(n) + 'day' + ' ...'
                frame = calculate.other_towhatday(n)
                df[tablename + str(n) + 'day'] = pd.concat([frame[code] for code in frame.columns]).reset_index(drop=True)
    #print df
    #df.to_csv('/home/lfz/python/yaoyan/modelcode/ques1.csv',encoding='utf_8_sig')
    print 'Finish creating DataFrame!'
    return df

def get_all_theday(theday):
    conn = default_db()
    cur = conn.cursor()
    readframe = pd.read_json('/home/lfz/python/yaoyan/df/price_fu.json')   #对于需要使用的json进行读取，需更改
    codelist = readframe.columns
    codelists = []
    for code in codelist:
        codelists.append('%06d' % code)
    codelists.sort()
    datelist = [theday]
    datelist_frame = datelist*len(codelists)   #生成股票数量的时间序列
    codelists_frame = []
    for code in codelists:
        codelists_frame += [code]*len(datelist)   #每个股票对应时间序列的个数
    df = pd.DataFrame()
    df['date'] = datelist_frame
    df['code'] = codelists_frame
    tablelist = ['price_fu','holder_top10byinst','Investment_announcement','Pledge_announcement','Reducing_announcement','frequency']
    print 'Ready to create DataFrame...'
    for tablename in tablelist:   #对于31个数据框循环计算
        if tablename == tablelist[0]:   #对于不同的表采用不同的算法
            calculate = one2six_frame_theday(tablename,theday)
            for n in [1,5,20,60,125,250]:
                #print 'Creating DataFrame ' + tablename + str(n) + 'day' + ' ...'
                frame = calculate.market_towhatday(n)
                df[tablename + str(n) + 'day'] = pd.concat([frame[code] for code in frame.columns]).reset_index(drop=True)   #将每一列取出后重排，作为新数据框的一列
        elif tablename == tablelist[1]:
            #print 'Creating DataFrame ' + tablename + ' ...'
            calculate = one2six_frame_theday(tablename,theday)
            frame = calculate.simu()
            df[tablename] = pd.concat([frame[code] for code in frame.columns]).reset_index(drop=True)
        else:
            calculate = one2six_frame_theday(tablename,theday)
            for n in [1,5,20,60,125,250]:
                #print 'Creating DataFrame ' + tablename + str(n) + 'day' + ' ...'
                frame = calculate.other_towhatday(n)
                df[tablename + str(n) + 'day'] = pd.concat([frame[code] for code in frame.columns]).reset_index(drop=True)
    #print df
    #df.to_csv(r'/home/lfz/python/ques1.csv',encoding='utf_8_sig')
    print 'Finish creating DataFrame!'
    return df

def get_all_theday_pro(theday):
    trade_before = ts2datetimestr(datetimestr2ts(theday) - 2592000).split('-')   #获取前30天日期
    trade_after = ts2datetimestr(datetimestr2ts(theday) + 2592000).split('-')   #获取后30天日期
    trade_list = get_tradelist(int(trade_before[0]),int(trade_before[1]),int(trade_before[2]),int(trade_after[0]),int(trade_after[1]),int(trade_after[2]))   #获取可能包含当天的交易日列表
    if theday in trade_list:
        df = get_all_theday(theday)
        #df.to_csv('/home/lfz/python/yaoyan/modelcode/gettoday1.csv',encoding='utf_8_sig')
        return df

if __name__=="__main__":
    #get_all(2015,2,2,2016,2,29)
    get_all_theday_pro('2013-01-04')