#-*-coding: utf-8-*-
#from WindPy import *
import datetime
import time_utils
from sql_utils import *
import time
import datetime
from time_utils import *
import pandas as pd

def get_season(year1,month1,day1,year2,month2,day2):
	l = []
	for year in range(year1,year2 + 1):
		l.append("%d-01-01" % (year))
		l.append("%d-04-01" % (year))
		l.append("%d-07-01" % (year))
		l.append("%d-10-01" % (year))
	datelist = get_datelist(year1,month1,day1,year2,month2,day2)
	listnew = sorted(list(set(datelist).intersection(set(l))))
	y = int(listnew[0].split('-')[0])
	m = int(listnew[0].split('-')[1])
	d = int(listnew[0].split('-')[2])
	if m == 1:
		listnew.append("%d-10-01" % (y - 1))
		listnew.sort()
	else:
		listnew.append("%d-0%d-01" % (y,m - 3))
		listnew.sort()
	return listnew

def get_gd(year1,month1,day1,year2,month2,day2):
	conn = default_db()
	cur = conn.cursor()
	w.start()
	datelist = get_season(year1,month1,day1,year2,month2,day2)
	codelists = w.wset("SectorConstituent",u"date=20180305;sector=全部A股").Data
	print len(codelists[1])
	stock_str = ""
	for code in codelists[1]:
		stock_str = stock_str + code + ","
	stock_str = stock_str.strip(",")
	for datenum in range(1,len(datelist)):
		print datelist[datenum]
		sql = "SELECT * FROM holders_show WHERE date = '%s'" % (datelist[datenum - 1])
		df = pd.read_sql(sql,conn)
		for num in range(1,11):
			data1 = w.wsd(stock_str, "holder_pct", datelist[datenum], datelist[datenum], "order=%d;Days=Alldays;Fill=Previous" % (num))
			data2 = w.wsd(stock_str, "holder_quantity", datelist[datenum], datelist[datenum], "unit=1;order=%d;Days=Alldays;Fill=Previous" % (num))
			data3 = w.wsd(stock_str, "holder_name", datelist[datenum], datelist[datenum], "order=%d;Days=Alldays;Fill=Previous" % (num))
			ranking = num
			for codenum in range(len(data1.Codes)):   #1
				stock_id = data1.Codes[codenum].split('.')[0]
				print stock_id,num,datelist[datenum]
				holder_name = data3.Data[0][codenum]
				holder_quantity = data2.Data[0][codenum]
				holder_pct = data1.Data[0][codenum]
				if len(df):
					stockdf = df[(df['stock_id'] == stock_id) & (df['holder_name'] == holder_name)]
					if len(stockdf):
						
						holder_quantity_change = holder_quantity - stockdf.iloc[0]['holder_quantity']
						if holder_quantity_change > 0:
							holder_pct_change = holder_pct - stockdf.iloc[0]['holder_pct']
							holder_hold_direction = u'增持'
						elif holder_quantity_change == 0:
							holder_pct_change = 0
							holder_hold_direction = u'不变'
						else:
							holder_quantity_change = abs(holder_quantity_change)
							holder_pct_change = abs(holder_pct - stockdf.iloc[0]['holder_pct'])
							holder_hold_direction = u'减持'
					else:
						holder_quantity_change = holder_quantity
						holder_pct_change = holder_pct
						if holder_name is None:
							holder_hold_direction = u'无'
						else:
							holder_hold_direction = u'新进'
				else:
					holder_quantity_change = 0
					holder_pct_change = 0
					holder_hold_direction = u'初始'
				#print stock_id,datelist[datenum],ranking,holder_name,holder_quantity,holder_pct,holder_quantity_change,holder_pct_change,holder_hold_direction
				order = 'insert into holders_show ( stock_id,date,ranking,holder_name,holder_quantity,holder_pct,holder_quantity_change,holder_pct_change,holder_hold_direction)values("%s","%s","%d","%s","%f","%f","%f","%f","%s")' % (stock_id,datelist[datenum],ranking,holder_name,holder_quantity,holder_pct,holder_quantity_change,holder_pct_change,holder_hold_direction)
				try:
					cur.execute(order)
					conn.commit()
				except Exception, e:
					conn.rollback()
					print e
		print '-------------------------'
		'''
		data4 = w.wsd(stock_str, "holder_top10pct", datelist[datenum], datelist[datenum], "Days=Alldays;Fill=Previous")
		data5 = w.wsd(stock_str, "holder_pctbyinst", datelist[datenum], datelist[datenum], "Days=Alldays;Fill=Previous")
		for codenum in range(len(data4.Codes)):
			stock_id = data4.Codes[codenum].split('.')[0]
			print stock_id
			print data4.Data[0][codenum]
			holder_top10pct = data4.Data[0][codenum]
			holder_pctbyinst = data5.Data[0][codenum]
			order = 'insert into holders_pct ( stock_id,date,holder_top10pct,holder_pctbyinst)values("%s","%s","%f","%f")' % (stock_id,datelist[datenum],holder_top10pct,holder_pctbyinst)
			try:
				cur.execute(order)
				conn.commit()
			except Exception, e:
				conn.rollback()
				print e'''

def get_pct(year1,month1,day1,year2,month2,day2):
	conn = default_db()
	cur = conn.cursor()
	datelist = get_season(year1,month1,day1,year2,month2,day2)
	for date in datelist[1:]:
		sql = "SELECT * FROM holders WHERE date = '%s'" % (date)
		cur.execute(sql)
		results = cur.fetchall()
		for result in results:
			stock_id = result['stock_id']
			print date,stock_id
			holder_top10pct = result['holder_top10pct']
			holder_pctbyinst = result['holder_pctbyinst']
			order = 'insert into holders_pct ( stock_id,date,holder_top10pct,holder_pctbyinst)values("%s","%s","%f","%f")' % (stock_id,date,holder_top10pct,holder_pctbyinst)
			try:
				cur.execute(order)
				conn.commit()
			except Exception, e:
				conn.rollback()
				print e

def test():
	conn = default_db()
	cur = conn.cursor()
	sql = "SELECT * FROM holders_show WHERE holder_name = 'None'"
	cur.execute(sql)
	results = cur.fetchall()
	n = 0
	for result in results:
		if result['holder_hold_direction'] == u'新进':
			print n
			update = "UPDATE holders_show SET holder_hold_direction = '%s' WHERE id = '%d'" % ('无',result['id'])
			try:
				cur.execute(update)
				conn.commit()
			except Exception, e:
				conn.rollback()
				print e
			n += 1

if __name__=="__main__":
	#print get_season(2015,5,6,2018,6,3)
	#get_gd(2013,7,1,2018,3,30)
	#get_pct(2015,1,1,2018,1,30)
	test()