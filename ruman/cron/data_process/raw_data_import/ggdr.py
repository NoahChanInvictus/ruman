#-*-coding: utf-8-*-
import sys
reload(sys)
sys.path.append("../../../")
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk, streaming_bulk
import tushare as ts
import pandas as pd
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('../')
from time_utils import *
import datetime


def tostr(year,month,day):
    date = str(year)+'-'+str(month)+'-'+str(day)
    return date

def datelist(year1,month1,day1,year2,month2,day2):
	date_list = []
	begin_date = datetime.datetime.strptime(tostr(year1,month1,day1), "%Y-%m-%d")
	end_date = datetime.datetime.strptime(tostr(year2,month2,day2), "%Y-%m-%d")
	while begin_date <= end_date:
		date_str = begin_date.strftime("%Y-%m-%d")
		date_list.append(date_str)
		begin_date += datetime.timedelta(days=1)   #输出时间列表的函数
	return date_list

def basic_info_insert(info_data):
    #info_data = basic_info_reader()
    es = Elasticsearch([{'host':'219.224.134.214','port':9202}])
    count = 0
    bulk_action = []
    if len(info_data):
        for pre_item in info_data:
            #basic_es_insert("gongshang","basic_info",item)
            item = {}
            item['stock_id'] = pre_item['stock_id']
            item['title'] = pre_item['title']
            item['publish_time'] = pre_item['publish_time']
            item['url'] = pre_item['url']
            item['type'] = pre_item['type']
            #item['content'] = pre_item['content']
            #print item['id']
            action = {"index":{}} #action  "_id": item['url']
            request_body = item # request body
            bulk_action.extend ([action,request_body]) # 在列表中组织形式   

            count += 1
            if count % 1000 == 0:
                try:
                    es.bulk(bulk_action, index="announcement", doc_type="basic_info",timeout=1000)
                    bulk_action = []
                    print count
                except Exception,e:
                    print e

            
        #把最后剩余不足1000条的也插入
        es.bulk(bulk_action, index="announcement", doc_type="basic_info",timeout=1000)

def dingzeng_date(words1,words2,words3,line):
    num = 0
    for i in words1:
        if i in line:
            num += 1
    if num:
        if words2 in line:
            number = 0
            for i in words3:
                if i in line:
                    number += 1
            if number:
                return False
            else:
                return True
        else:
            return False
    else:
        return False

def dingzeng_start(line):
    words1 = ['非公开发行','向特定对象发行','定向发行','非公开增发','向特定对象增发','定向增发']
    words2 = '预案'
    words3 = ['修正','修订','调整','补充','更新','更正','修改','变更','增加','差异','摘要','草案','到期失效','补充','恢复','延长','筹划','谋划','进展','停牌','填补','变动','下滑','策划','更换','完善','中止','终止','到期失效','撤回','放弃','取消','暂缓','损益','利润','业绩','亏损','回报','法律','核查','董事','意见','回复','说明','股东','律师','会计','核准','批复','批准','获准','同意','答复','审核','通过','审核通过','结果','审核结果','受理','转让保荐书','复核报告','权益价值评估说明书','论证分析报告','提醒性公告','议案','提示性公告','评估报告','披露','提示','复牌','承诺','函']
    return dingzeng_date(words1,words2,words3,line)

def dingzeng_end(line):
    words1 = ['非公开发行','向特定对象发行','定向发行','非公开增发','向特定对象增发','定向增发']
    words2 = '审核通过'
    words3 = ['不','未','债券','更正','更新','补充','英文','回复','修正']
    return dingzeng_date(words1,words2,words3,line)

def getkind(line):   #简单分类器
    if '资产置换' in line or '资产重组' in line or '购买资产' in line or '收购' in line:
        a = 1
        #print '类别：并购重组'
    elif '投资' in line:
        a = 2
        #print '类别：对外投资'
    elif '质押' in line:
        a = 3
        #print '类别：股权质押'
    elif '减持' in line:
        a = 4
        #print '类别：大股东减持'
    elif '利润分配' in line or '分配利润' in line or '分红派息' in line:
        a = 5
        #print '类别：利润分配'
    elif '关联交易' in line:
        a = 6
        #print '类别：关联交易'
    elif '发行股份' in line:
        a = 7
        #print '类别：定向增发'
    elif '配股' in line:
        a = 8
        #print '类别：配股'
    elif '停牌' in line:
        a = 9
        #print '类别：停牌'
    elif '辞职' in line:
        a = 10
        #print '类别：高管辞职'
    elif dingzeng_start(line):
        a = 12
        #print '类别：定增开始'
    elif dingzeng_end(line):
        a = 13
        #print '类别：定增结束'
    else:
        a = 11
        #print '类别：其他'
    return a

def gonggao_dict(gongsi,year1,month1,day1,year2,month2,day2):
    gg = pd.DataFrame()
    ggl =[]
    dated = datelist(year1,month1,day1,year2,month2,day2)
    for date in dated:
    	print gongsi,date
        try:
            hhd = ts.get_notices(gongsi,date)
            gg = gg.append(hhd,ignore_index=True)
        except:
            pass
    try:
        for num in range(gg.iloc[:,0].size):
    	    ggd = {}
            ggd['stock_id'] = gongsi
            ggd['title'] = gg.loc[num]['title']
            ggd['publish_time'] = datetimestr2ts(gg.loc[num]['date'])
            ggd['url'] = gg.loc[num]['url']
            ggd['type'] = getkind(gg.loc[num]['title'])
            #ggd['content'] = '待取'
            ggl.append(ggd)
    except:
    	pass
    return ggl

def ggdr(year1,month1,day1,year2,month2,day2):
    gongsilist = ts.get_stock_basics().index
    a = len(gongsilist)
    for gongsi in gongsilist:
        basic_info_insert(gonggao_dict(gongsi,year1,month1,day1,year2,month2,day2))
        a -= 1
        print '还剩',a,'家'

def ggdr_today(theday=today()):
    gongsilist = ts.get_stock_basics().index
    a = len(gongsilist)
    for gongsi in gongsilist:
        year = int(theday.split('-')[0])
        month = int(theday.split('-')[1])
        day = int(theday.split('-')[2])
        basic_info_insert(gonggao_dict(gongsi,year,month,day,year,month,day))
        a -= 1
        if a % 100 == 0:
            print '还剩',a,'家'

def delete():
    es = Elasticsearch([{'host':'219.224.134.214','port':9202}])
    query_body = {"size":100000,"query":{ "filtered": {
        "filter":{"range":{"publish_time":{"gte": 1520380800,"lte": 1528329600}}}
    }}}
    res = es.search(index="announcement", doc_type="basic_info", body=query_body,request_timeout=100)
    hits = res['hits']['hits']
    print len(hits)
    num = 0
    for hit in hits:
        es.delete(index="announcement", doc_type="basic_info", id=hit['_id'])
        if num %1000 == 0:
            print num
        num += 1




if __name__ == '__main__':
    ggdr(2018,3,7,2018,5,15)
    #ggdr_today()
    #delete()