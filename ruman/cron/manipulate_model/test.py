#-*-coding: utf-8-*-
import pandas as pd

tablelist = ['price_fu','holder_top10byinst','Investment_announcement','Pledge_announcement','Reducing_announcement','frequency']
for tablename in tablelist:
	print tablename
	readframe = pd.read_json('/home/lfz/python/yaoyan/df/df/' + tablename + '.json')
	df = readframe.iloc[:581]
	df.to_json('/home/lfz/python/yaoyan/df/2016-5/' + tablename + '.json')