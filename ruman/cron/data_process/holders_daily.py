# -*- coding:utf-8 -*-
#step1：从windgd.py里获得股东信息存入MySQL
from raw_data_import.windgd import get_gudong,get_gudong_everyday

def holders_daily(theday):
    get_gudong_everyday(theday)   #将指定日期股东信息导入MySQL
    print theday,'announcement import&stastics finished!'

if __name__ == '__main__':
    holders_daily('2018-03-06')