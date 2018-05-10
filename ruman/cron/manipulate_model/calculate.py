#-*-coding: utf-8-*-
import sys
reload(sys)
sys.path.append("../../")
import pandas as pd
import math
import numpy as np
from config import *
from time_utils import *
from sql_utils import *
from elasticsearch import Elasticsearch
#from createframe import es_search
from create import table1,table2

def what_quarter(theday):   
    year = int(str(theday).split('-')[0])
    month = int(str(theday).split('-')[1])
    if month in [1,2,3]:
        return '%d-07-01' % (year - 1),'%d-04-01' % (year - 1),'%d-01-01' % (year)
    elif month in [4,5,6]:
        return '%d-10-01' % (year - 1),'%d-07-01' % (year - 1),'%d-04-01' % (year)
    elif month in [7,8,9]:
        return '%d-01-01' % (year),'%d-10-01' % (year - 1),'%d-07-01' % (year)
    else:
        return '%d-04-01' % (year),'%d-01-01' % (year),'%d-10-01' % (year)

class one2six_frame:   #生成历史各个数据框的类
    def __init__(self,tablename,datelist,datelistlong):
        self.tablename = tablename
        #self.data_frame = pd.read_json(es_search(tablename)[1])
        readframe = pd.read_json('dataframe/' + tablename + '.json')
        readframe = readframe.sort_index(axis=1)   #因为json读取问题而必须重新按列排序一下
        self.data_frame = readframe
        self.datelist = [pd.Timestamp(int(date.split('-')[0]),int(date.split('-')[1]),int(date.split('-')[2])) for date in datelist]
        self.datelistlong = [pd.Timestamp(int(date.split('-')[0]),int(date.split('-')[1]),int(date.split('-')[2])) for date in datelistlong]
        #if tablename == 'Investment_announcement':
            #self.data_frame.to_csv(r'/home/lfz/python/invest.csv',encoding='utf_8_sig')
        #print self.data_frame

    def other_towhatday(self,num):   #除收益率换手率其他的都是计算频率
        framewhatday = pd.DataFrame(columns=self.data_frame.columns)
        if num == 1:    #如果要一天的数据直接返回原数据框
            return self.data_frame.loc[self.datelist]
        else:
            for datenum in range(len(self.datelist)):   
                sumlist = []
                for count in range(num):
                    if self.datelistlong[self.datelistlong.index(self.datelist[datenum]) - count] in self.data_frame.index:
                        sumlist.append(self.data_frame.loc[self.datelistlong[self.datelistlong.index(self.datelist[datenum]) - count]])
                    else:
                        break
                framewhatday.loc[self.datelist[datenum]] = list(sum(sumlist))   #获取上述n列的和,切记转化为列表，否则因为读取的json的数据框股票代码是整数，会导致匹配错误
            return framewhatday

    def market_towhatday(self,num):   #计算对数收益率或换手率增长率
        framewhatday = pd.DataFrame(columns=self.data_frame.columns)
        for datenum in range(len(self.datelist)):
            #datestr = date.strftime('%Y-%m-%d')
            if self.datelistlong[self.datelistlong.index(self.datelist[datenum]) - num] not in self.data_frame.index:
                framewhatday.loc[self.datelist[datenum]] = None
            else:
                a = self.data_frame.loc[self.datelist[datenum]]
                b = self.data_frame.loc[self.datelistlong[self.datelistlong.index(self.datelist[datenum]) - num]]
                #print a,b
                if self.tablename == MARKET_PRICE_FU:
                    framewhatday.loc[self.datelist[datenum]] = list(pd.Series([math.log(i) for i in a]) - pd.Series([math.log(i) for i in b]))   #输出对数收益率
                else:
                    framewhatday.loc[self.datelist[datenum]] = list(a / b - 1)   #输出换手率增长率
        #print framewhatday
        return framewhatday

    def simu(self):   #私募不需要进行天数分别，只计算相比于上一季度的新增数（约为60个交易日）
        framewhatday = pd.DataFrame(columns=self.data_frame.columns)
        for datenum in range(len(self.datelist)):
            if self.datelistlong[self.datelistlong.index(self.datelist[datenum]) - 60] not in self.data_frame.index:
                framewhatday.loc[self.datelist[datenum]] = 0
            else:
                framewhatday.loc[self.datelist[datenum]] = list(self.data_frame.loc[self.datelist[datenum]] - self.data_frame.loc[self.datelistlong[self.datelistlong.index(self.datelist[datenum]) - 60]])
        return framewhatday

    def jiejin_quarter(self):   #利用解禁数据的时间序列合成解禁数据
        framewhatday1 = pd.DataFrame(columns=self.data_frame.columns)
        framewhatday2 = pd.DataFrame(columns=self.data_frame.columns)
        framewhatday3 = pd.DataFrame(columns=self.data_frame.columns)
        netprofit = pd.read_json('dataframe/' + NETPROFIT_NETPROFIT + '.json')
        netprofit = netprofit.sort_index(axis=1)
        holder_top10pct = pd.read_json('dataframe/' + ES_HOLDERS_PCT_HOLDER_TOP10PCT + '.json')
        holder_top10pct = holder_top10pct.sort_index(axis=1)
        holder_pctbyinst = pd.read_json('dataframe/' + ES_HOLDERS_PCT_HOLDER_PCTBYINST + '.json')
        holder_pctbyinst = holder_pctbyinst.sort_index(axis=1)
        for date in self.datelist:
            quarterday = what_quarter(str(date).split()[0])
            if quarterday[1] in netprofit.index:
                framewhatday1.loc[date] = (netprofit.loc[quarterday[0]] / netprofit.loc[quarterday[1]] - 1)
            else:
                framewhatday1.loc[date] = None
            if quarterday[2] in holder_top10pct.index:
                framewhatday2.loc[date] = holder_top10pct.loc[quarterday[2]] / 100
            else:
                framewhatday2.loc[date] = 0
            if quarterday[2] in holder_pctbyinst.index:
                framewhatday3.loc[date] = holder_pctbyinst.loc[quarterday[2]] / 100
            else:
                framewhatday3.loc[date] = 0
        framewhatday1 = framewhatday1.fillna(0)   #净利润为空的直接设为0
        return {JIEJIN_DATE:self.data_frame,NETPROFIT_NETPROFIT:framewhatday1,ES_HOLDERS_PCT_HOLDER_TOP10PCT:framewhatday2,ES_HOLDERS_PCT_HOLDER_PCTBYINST:framewhatday3}

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
        readframe = pd.read_json('dataframe/' + tablename + '.json')
        readframe = readframe.sort_index(axis=1)
        indexlist = []
        self.theday = theday
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
        if self.tablename == MARKET_PRICE_FU:
            framewhatday.loc[self.data_frame.index[datenum]] = list(pd.Series([math.log(i) for i in a]) - pd.Series([math.log(i) for i in b]))   #输出对数收益率
        else:
            l = list(a / b - 1)
            '''
            for i in range(len(l)):
                if l[i] == float('nan'):
                    l[i] =0'''
            framewhatday.loc[self.data_frame.index[datenum]] = l   #输出换手率增长率(如果这一天没有就会导致之前都没有，需询问)
        #print framewhatday
        return framewhatday

    def simu(self):   #私募不需要进行天数分别，只计算相比于上一季度的新增数（约为60个交易日）
        framewhatday = pd.DataFrame(columns=self.data_frame.columns)
        datenum = 250
        framewhatday.loc[self.data_frame.index[datenum]] = list(self.data_frame.loc[self.data_frame.index[datenum]] - self.data_frame.loc[self.data_frame.index[datenum - 60]])
        return framewhatday

    def jiejin_quarter(self):   #利用解禁数据的时间序列合成解禁数据
        framewhatday1 = pd.DataFrame(columns=self.data_frame.columns)
        framewhatday2 = pd.DataFrame(columns=self.data_frame.columns)
        framewhatday3 = pd.DataFrame(columns=self.data_frame.columns)
        netprofit = pd.read_json('dataframe/' + NETPROFIT_NETPROFIT + '.json')
        netprofit = netprofit.sort_index(axis=1)
        holder_top10pct = pd.read_json('dataframe/' + ES_HOLDERS_PCT_HOLDER_TOP10PCT + '.json')
        holder_top10pct = holder_top10pct.sort_index(axis=1)
        holder_pctbyinst = pd.read_json('dataframe/' + ES_HOLDERS_PCT_HOLDER_PCTBYINST + '.json')
        holder_pctbyinst = holder_pctbyinst.sort_index(axis=1)
        quarterday = what_quarter(self.theday)
        framewhatday1.loc[self.theday] = list((netprofit.loc[quarterday[0]] / netprofit.loc[quarterday[1]] - 1))
        framewhatday2.loc[self.theday] = holder_top10pct.loc[quarterday[2]] / 100
        framewhatday3.loc[self.theday] = holder_pctbyinst.loc[quarterday[2]] / 100
        framewhatday1 = framewhatday1.fillna(0)
        return {JIEJIN_DATE:self.data_frame[self.data_frame.index == self.theday],NETPROFIT_NETPROFIT:framewhatday1,ES_HOLDERS_PCT_HOLDER_TOP10PCT:framewhatday2,ES_HOLDERS_PCT_HOLDER_PCTBYINST:framewhatday3}

def get_all(reason,year1,month1,day1,year2,month2,day2):
    conn = default_db()
    cur = conn.cursor()
    readframe = pd.read_json('dataframe/%s.json' % (MARKET_PRICE_FU))   #对于需要使用的json进行读取，需更改
    codelist = readframe.columns
    codelists = []
    for code in codelist:
        codelists.append('%06d' % code)
    codelists.sort()
    while 1:
        try:
            datelist = get_tradelist(year1,month1,day1,year2,month2,day2)   #获得交易时间列表
            datelistlong = get_tradelist(year1 - 2,month1,day1,year2,month2,day2)
            break
        except:
            pass
    datelist_frame = datelist*len(codelists)   #生成股票数量的时间序列
    codelists_frame = []
    for code in codelists:
        codelists_frame += [code]*len(datelist)   #每个股票对应时间序列的个数
    df = pd.DataFrame()
    df['date'] = datelist_frame
    df['code'] = codelists_frame
    if reason == 1:
        tablelist = [i[1] for i in table1]
        print 'Ready to create DataFrame...'
        for tablename in tablelist:   #对于31个数据框循环计算
            if tablename == tablelist[0]:   #对于不同的表采用不同的算法
                calculate = one2six_frame(tablename,datelist,datelistlong)
                for n in [1,5,20,60,125,250]:
                    print 'Creating DataFrame ' + tablename + str(n) + 'day' + ' ...'
                    frame = calculate.market_towhatday(n)
                    df[tablename + str(n) + 'day'] = pd.concat([frame[code] for code in frame.columns]).reset_index(drop=True)   #将每一列取出后重排，作为新数据框的一列
            elif tablename == tablelist[1]:
                print 'Creating DataFrame ' + tablename + ' ...'
                calculate = one2six_frame(tablename,datelist,datelistlong)
                frame = calculate.simu()
                df[tablename] = pd.concat([frame[code] for code in frame.columns]).reset_index(drop=True)
            else:
                calculate = one2six_frame(tablename,datelist,datelistlong)
                for n in [1,5,20,60,125,250]:
                    print 'Creating DataFrame ' + tablename + str(n) + 'day' + ' ...'
                    frame = calculate.other_towhatday(n)
                    df[tablename + str(n) + 'day'] = pd.concat([frame[code] for code in frame.columns]).reset_index(drop=True)
        return df
    elif reason == 2:
        tablelist = [i[1] for i in table2]
        print 'Ready to create DataFrame...'
        for tablename in tablelist:   #对于31个数据框循环计算
            if tablename == tablelist[0] or tablename == tablelist[1]:   #对于不同的表采用不同的算法
                calculate = one2six_frame(tablename,datelist,datelistlong)
                for n in [1,5,20,60,125,250]:
                    print 'Creating DataFrame ' + tablename + str(n) + 'day' + ' ...'
                    frame = calculate.market_towhatday(n)
                    df[tablename + str(n) + 'day'] = pd.concat([frame[code] for code in frame.columns]).reset_index(drop=True)   #将每一列取出后重排，作为新数据框的一列
            elif tablename == tablelist[2]:
                calculate = one2six_frame(tablename,datelist,datelistlong)
                frame = calculate.jiejin_quarter()
                for i in frame.keys():
                    print 'Creating DataFrame ' + i + ' ...'
                    df[i] = pd.concat([frame[i][code] for code in frame[i].columns]).reset_index(drop=True)
            else:
                calculate = one2six_frame(tablename,datelist,datelistlong)
                for n in [1,5,20,60,125,250]:
                    print 'Creating DataFrame ' + tablename + str(n) + 'day' + ' ...'
                    frame = calculate.other_towhatday(n)
                    df[tablename + str(n) + 'day'] = pd.concat([frame[code] for code in frame.columns]).reset_index(drop=True)
        return df
    #print df
    #df.to_csv('test3.csv',encoding='utf_8_sig')
    print 'Finish creating DataFrame!'

def get_all_theday(reason,theday):
    conn = default_db()
    cur = conn.cursor()
    readframe = pd.read_json('dataframe/%s.json' % (MARKET_PRICE_FU))   #对于需要使用的json进行读取，需更改
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
    if reason == 1:
        tablelist = [i[1] for i in table1]
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
        #df.to_csv('day1.csv',encoding='utf_8_sig')
        print 'Finish creating DataFrame!'
        #print df
        return df
    elif reason == 2:
        tablelist = [i[1] for i in table2]
        print 'Ready to create DataFrame...'
        for tablename in tablelist:   #对于31个数据框循环计算
            if tablename == tablelist[0] or tablename == tablelist[1]:   #对于不同的表采用不同的算法
                calculate = one2six_frame_theday(tablename,theday)
                for n in [1,5,20,60,125,250]:
                    #print 'Creating DataFrame ' + tablename + str(n) + 'day' + ' ...'
                    frame = calculate.market_towhatday(n)
                    df[tablename + str(n) + 'day'] = pd.concat([frame[code] for code in frame.columns]).reset_index(drop=True)   #将每一列取出后重排，作为新数据框的一列
            elif tablename == tablelist[2]:
                #print 'Creating DataFrame ' + tablename + ' ...'
                calculate = one2six_frame_theday(tablename,theday)
                frame = calculate.jiejin_quarter()
                for i in frame.keys():
                    #print 'Creating DataFrame ' + i + ' ...'
                    df[i] = pd.concat([frame[i][code] for code in frame[i].columns]).reset_index(drop=True)
            else:
                calculate = one2six_frame_theday(tablename,theday)
                for n in [1,5,20,60,125,250]:
                    #print 'Creating DataFrame ' + tablename + str(n) + 'day' + ' ...'
                    frame = calculate.other_towhatday(n)
                    df[tablename + str(n) + 'day'] = pd.concat([frame[code] for code in frame.columns]).reset_index(drop=True)
        #df.to_csv('day2.csv',encoding='utf_8_sig')
        print 'Finish creating DataFrame!'
        #print df
        return df


'''
def get_all_theday_pro(reason,theday):
    trade_before = ts2datetimestr(datetimestr2ts(theday) - 2592000).split('-')   #获取前30天日期
    trade_after = ts2datetimestr(datetimestr2ts(theday) + 2592000).split('-')   #获取后30天日期
    trade_list = get_tradelist(int(trade_before[0]),int(trade_before[1]),int(trade_before[2]),int(trade_after[0]),int(trade_after[1]),int(trade_after[2]))   #获取可能包含当天的交易日列表
    if theday in trade_list:
        df = get_all_theday(reason,theday)
        #df.to_csv('/home/lfz/python/yaoyan/modelcode/gettoday1.csv',encoding='utf_8_sig')
        return df
    else:
        print '貌似你输入的日期并不是交易日'
        '''

if __name__=="__main__":
    #get_all('table2',2014,5,1,2014,5,31)
    get_all_theday(1,'2016-01-04')

'''
总统计表输出成功
日度统计表输出成功
#但需要询问两处有疑问的地方
#净利润为空的问题，换手率为空的问题
净利润置0，换手率处理方式同收益率
'''