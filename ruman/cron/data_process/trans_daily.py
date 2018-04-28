# -*- coding:utf-8 -*-
# step1:从东方财富网获取大宗交易数据存入es
# step2:从es中读数据进行统计，将结果存入es
from raw_data_import.eastMoneyDaily import eastMoney
from stastics.trans_stat import transfrequency
def trans_daily(theday):
    eastMoney(theday)           #从东方财富网获取大宗交易数据存入es
    transfrequency(theday)

if __name__ == '__main__':
    trans_daily('2018-04-18')   #04-18,04-19和04-20是用来测试的


