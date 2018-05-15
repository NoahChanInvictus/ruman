#-*-coding: utf-8-*-
#对于所有的统计表进行归一，同时进行，注意现有数据是否能够支持统计
from manipulate_warning import manipulatewarning, warning_all
from manipulate_influence import manipulateratio, influence_all
from manipulate_industry import manipulateindustry, industry_all
from manipulate_panel import manipulatepanel, panel_all
from manipulate_type import manipulatetype, type_all

def show_theday(theday):   #单独一天
	print 'Counting manipulatewarning...'
	manipulatewarning(theday)
	print 'Counting manipulateratio...'
	manipulateratio(theday)
	print 'Counting manipulateindustry...'
	manipulateindustry(theday)
	print 'Counting manipulatepanel...'
	manipulatepanel(theday)
	print 'Counting manipulatetype...'
	manipulatetype(theday)

def show_all(year1,month1,day1,year2,month2,day2):   #一段时间
	print 'Counting warning_all...'
	warning_all(year1,month1,day1,year2,month2,day2)
	print 'Counting influence_all...'
	influence_all(year1,month1,day1,year2,month2,day2)
	print 'Counting industry_all...'
	industry_all(year1,month1,day1,year2,month2,day2)
	print 'Counting panel_all...'
	panel_all(year1,month1,day1,year2,month2,day2)
	print 'Counting type_all...'
	type_all(year1,month1,day1,year2,month2,day2)