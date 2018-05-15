#-*-coding: utf-8-*-
#启动操纵模块的每日计算和历史数据计算
import sys
reload(sys)
sys.path.append("../")
from config import *
from time_utils import *
from sql_utils import *
from manipulate_model.train import predict
from manipulate_model.manipulate_day import insertday
from manipulate_model.dingxiang import predict_dz
from manipulate_model.gaosongzhuan import gaosongzhuan
from data_process.present.firstpage_stastic import show_theday, show_all

def insert_sql(year1,month1,day1,year2,month2,day2):   #完成历史的模型计算及前端数据库生成
	tradelist = get_tradelist_all()
	for day in get_tradelist(year1,month1,day1,year2,month2,day2):
		predict(day)
	for day in get_tradelist(year1,month1,day1,year2,month2,day2):
		insertday(day,tradelist)
	predict_dz(year1,month1,day1,year2,month2,day2)
	gaosongzhuan()
	show_all(year1,month1,day1,year2,month2,day2)

if __name__=="__main__":
	print 'hello,world!'