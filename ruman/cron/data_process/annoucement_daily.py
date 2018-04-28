# -*- coding:utf-8 -*-
# step1: 从ggdr.py中获取公告信息存入es
# step2: announcement-daily.py 从ES数据库中统计每只股票每天每种类型公告的数目
from raw_data_import.ggdr import ggdr,ggdr_today
from stastics.announcement_stat import announcment_stastic_main


def annoucement_daily(theday):
    ggdr_today(theday)      #将指定日期的公告导入es   #公告2018-03-03已导入
    announcment_stastic_main(theday)               #统计2018-03-05已计算
    print theday,'announcement import&stastics finished!'

if __name__ == '__main__':
    annoucement_daily('2018-03-06')