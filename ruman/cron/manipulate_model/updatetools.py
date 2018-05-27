#-*-coding: utf-8-*-
#一些手动更新表格数据的工具
import sys
reload(sys)
sys.path.append("../../")
import pandas as pd
from config import *
from time_utils import *
from sql_utils import *


def update_day_result():
    conn = default_db()
    cur = conn.cursor()
    sql = "SELECT * FROM %s where %s = '%d'" % (TABLE_RESULT,RESULT_RESULT,1)
    cur.execute(sql)
    results = cur.fetchall()
    for result in results:
        if result[RESULT_PROBABILITY] < 0.75:
            update = "UPDATE %s SET %s = '%d' WHERE %s = %d" % (TABLE_RESULT,RESULT_RESULT,0,RESULT_ID,result[RESULT_ID])
            try:
                cur.execute(update)
                conn.commit()
            except Exception, e:
                print e

def delete_holders():
    conn = default_db()
    cur = conn.cursor()
    sql = "SELECT * FROM %s where %s >= '%s'" % (ES_TABLE_HOLDERS,ES_HOLDERS_SHOW_DATE,'2018-02-01')
    cur.execute(sql)
    results = cur.fetchall()
    print len(results)
    for result in results:
        delete = "DELETE FROM %s WHERE %s = %d" % (ES_TABLE_HOLDERS,ES_HOLDERS_SHOW_ID,result[ES_HOLDERS_SHOW_ID])
        try:
            cur.execute(delete)
            conn.commit()
        except Exception, e:
            print e

def delete_holders_pct():
    conn = default_db()
    cur = conn.cursor()
    sql = "SELECT * FROM %s where %s >= '%s'" % (TABLE_HOLDERS_PCT,ES_HOLDERS_PCT_DATE,'2018-04-01')
    cur.execute(sql)
    results = cur.fetchall()
    print len(results)
    for result in results:
        delete = "DELETE FROM %s WHERE %s = %d" % (TABLE_HOLDERS_PCT,ES_HOLDERS_PCT_ID,result[ES_HOLDERS_PCT_ID])
        try:
            cur.execute(delete)
            conn.commit()
        except Exception, e:
            print e

def update_day_label():
    conn = default_db()
    cur = conn.cursor()
    sql = "SELECT * FROM %s WHERE %s = '0'" % (TABLE_DAY,DAY_MANIPULATE_LABEL)
    cur.execute(sql)
    results = cur.fetchall()
    num = len(results)
    for result in results:
        print num
        update = "UPDATE %s SET %s = '%d' WHERE %s = %d" % (TABLE_DAY,DAY_MANIPULATE_LABEL,1,DAY_ID,result[DAY_ID])
        try:
            cur.execute(update)
            conn.commit()
        except Exception, e:
            print e
        num -= 1

def delete_day_type():
    conn = default_db()
    cur = conn.cursor()
    sql = "SELECT * FROM %s WHERE %s = '%d'" % (TABLE_DAY,DAY_MANIPULATE_TYPE,2)
    cur.execute(sql)
    results = cur.fetchall()
    num = len(results)
    for result in results:
        print num
        delete = "DELETE FROM %s WHERE %s = %d" % (TABLE_DAY,DAY_ID,result[DAY_ID])
        try:
            cur.execute(delete)
            conn.commit()
        except Exception, e:
            print e
        num -= 1

def increaseratio(lastday,nowday,stock_id):
    conn = default_db()
    cur = conn.cursor()
    pricesql = "SELECT * FROM %s WHERE %s >= '%s' and %s <= '%s' and %s = '%s'" % (TABLE_MARKET_DAILY,MARKET_DATE,lastday,MARKET_DATE,nowday,MARKET_STOCK_ID,stock_id)   #获取最新收益率
    cur.execute(pricesql)
    results = cur.fetchall()
    if results[0][MARKET_PRICE]:
        increase_ratio = (results[-1][MARKET_PRICE] - results[0][MARKET_PRICE]) / results[0][MARKET_PRICE]
    else:
        increase_ratio = 0
    return increase_ratio

def insert_sql(df):
    conn = default_db()
    cur = conn.cursor()
    for num in range(len(df)):
        sql = "SELECT * FROM %s where %s = '%s'"%(TABLE_STOCK_LIST,STOCK_LIST_STOCK_ID,df.iloc[num]['stock_id'])
        cur.execute(sql)
        result = cur.fetchone()
        start_date = to_tradeday(df.iloc[num]['start_date'],-1)
        lastdate = lasttradedate(start_date)
        end_date = to_tradeday(df.iloc[num]['end_date'],1)
        stock_name = result[STOCK_LIST_STOCK_NAME]
        stock_id = result[STOCK_LIST_STOCK_ID]

        increase_ratio = increaseratio(lastdate,end_date,stock_id)
        industry_name = result[STOCK_LIST_INDUSTRY_NAME]
        manipulate_type = 2
        ifend = 1
        marketplate = result[STOCK_LIST_PLATE]
        industry_code = result[STOCK_LIST_INDUSTRY_CODE]
        print stock_name,stock_id,start_date,end_date,industry_name,increase_ratio,manipulate_type,ifend,marketplate,industry_code
        order = 'insert into ' + TABLE_DAY + '(stock_name,stock_id,manipulate_label,ifpunish,start_date,end_date,increase_ratio,industry_name,manipulate_type,industry_code,ifend,market_plate,ifshow)values\
        ("%s","%s","%d","%d","%s","%s","%f","%s","%d","%s","%d","%s","%d")' % (stock_name,stock_id,1,1,start_date,end_date,increase_ratio,industry_name,manipulate_type,industry_code,ifend,marketplate,1)
        try:
            cur.execute(order)
            conn.commit()
        except Exception, e:
            print e
            break

def update_hotnews():
    conn = default_db()
    cur = conn.cursor()
    idlist = []
    '''
    file = open('news_wenben.csv')
    file2 = open('news_0523.csv')
    csv_file = csv.reader(file)
    csv_file2 = csv.reader(file2)
    text_id_first_list = []
    text_id_end_list = []'''
    file3 = open('news_add.csv')
    csv_file3 = csv.reader(file3)
    '''
    for row in csv_file:
        text_id = row[1]
        idlist.append(text_id)
    for row in csv_file2:
        text_id = row[1]
        idlist.append(text_id)'''
    for row in csv_file3:
        text_id = row[1]
        idlist.append(text_id)
    num = 0
    for text_id in idlist:
        sql = "SELECT * FROM %s WHERE %s = '%s'" %(TABLE_HOTNEWS,HOT_NEWS_TEXT_ID,text_id)
        cur.execute(sql)
        idresults = cur.fetchall()
        if len(idresults):
            print num
            update = "UPDATE %s SET %s = '%d' WHERE %s = %d" % (TABLE_HOTNEWS,'ifshow',1,HOT_NEWS_ID,idresults[0][HOT_NEWS_ID])
            try:
                cur.execute(update)
                conn.commit()
            except Exception, e:
                print e
            num += 1

def update_day_show():
    conn = default_db()
    cur = conn.cursor()
    idlist = [826,837,1615,1386,980,759,1725,1362,2276,2277,2279,2278,872,1737,2280,2281,986,940,920,896,881,851,826,1024,989,926,1807,1789,1795,1018,1018,1186,1272,1545,1563,1674,1716,1759,1484,1523,1616,1660,1703,1750,1283,1309,1361,1560,1634,1675,1745,1787,1817,473,575,1304,1316,1354,1435]
    num = 0
    for id in idlist:
        print num
        update = "UPDATE %s SET %s = '%d' WHERE %s = %d" % (TABLE_DAY,'ifshow',1,DAY_ID,id)
        try:
            cur.execute(update)
            conn.commit()
        except Exception, e:
            print e
        num += 1

def delete_day():
    conn = default_db()
    cur = conn.cursor()
    sql = "SELECT * FROM %s" % (TABLE_DAY+'_gao')
    cur.execute(sql)
    results = cur.fetchall()
    print len(results)
    for result in results:
        delete = "DELETE FROM %s WHERE %s = %d" % (TABLE_DAY+'_gao',ES_HOLDERS_SHOW_ID,result[ES_HOLDERS_SHOW_ID])
        try:
            cur.execute(delete)
            conn.commit()
        except Exception, e:
            print e

def insert_type2():
    conn = default_db()
    cur = conn.cursor()
    sql = "SELECT * FROM %s" % (TABLE_DAY+'_gaonew')
    cur.execute(sql)
    results = cur.fetchall()
    num = len(results) 
    for result in results:
        print num
        order = 'insert into ' + TABLE_DAY + '(stock_name,stock_id,manipulate_label,start_date,end_date,increase_ratio,industry_name,manipulate_type,industry_code,ifend,market_plate)values\
                ("%s","%s","%d","%s","%s","%f","%s","%d","%s","%d","%s")' % (result['stock_name'],result['stock_id'],result['manipulate_label'],result['start_date'],result['end_date'],result['increase_ratio'],result['industry_name'],result['manipulate_type'],result['industry_code'],result['ifend'],result['market_plate'])
        try:
            cur.execute(order)
            conn.commit()
        except Exception, e:
            print e
        num -= 1

def delete_nouse():
    conn = default_db()
    cur = conn.cursor()
    sql = "SELECT * FROM %s WHERE stock_id = '%s' and date >= '%s' and date <= '%s'" % (TABLE_MARKET_DAILY,'002609','2010-12-30','2011-12-29')
    cur.execute(sql)
    results = cur.fetchall()
    num = len(results) 
    for result in results:
        delete = "DELETE FROM %s WHERE %s = %d" % (TABLE_MARKET_DAILY,ES_HOLDERS_SHOW_ID,result[ES_HOLDERS_SHOW_ID])
        try:
            cur.execute(delete)
            conn.commit()
        except Exception, e:
            print e

def count():
    conn = default_db()
    cur = conn.cursor()
    sql = "SELECT * FROM %s" % (TABLE_DAY)
    cur.execute(sql)
    results = cur.fetchall()
    num = 0
    for result in results:
        if result['start_date'] > result['end_date']:
            delete = "DELETE FROM %s WHERE %s = %d" % (TABLE_DAY,ES_HOLDERS_SHOW_ID,result[ES_HOLDERS_SHOW_ID])
            try:
                cur.execute(delete)
                conn.commit()
            except Exception, e:
                print e
            num += 1
    print num

def transfer2es(start_date,end_date):
    conn = default_db()
    cur = conn.cursor()
    sql = "SELECT * FROM %s WHERE date >= '%s' and date <= '%s'" % (ES_TABLE_HOLDERS,start_date,end_date)
    cur.execute(sql)
    results = cur.fetchall()
    insertlist = []
    for result in results:
        insertlist.append(result)
        #order = 'insert into holders( stock_id,stock_name,date,ts,holder_name,holder_top1,holder_top2,holder_top3,holder_top4,holder_top5,holder_top6,holder_top7,holder_top8,holder_top9,holder_top10,holder_top10byinst,holder_top10pct,holder_pctbyinst)values("%s", "%s","%s","%f","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%d","%f","%f")' % (stock_id,stock_name,date,ts, holder_name,holder_top_list[0],holder_top_list[1],holder_top_list[2],holder_top_list[3],holder_top_list[4],holder_top_list[5],holder_top_list[6],holder_top_list[7],holder_top_list[8],holder_top_list[9],holder_top10byinst,holder_top10pct,holder_pctbyinst)
        '''
        try:
            cur.execute(order)
            conn.commit()
        except Exception, e:
            print e'''
    print len(insertlist)
    basic_info_insert(insertlist)
    endtime = datetime.datetime.now()
    #a -= 1
    #print 'Fight!已经到',codelists[1][code],'公司啦(￣▽￣)~*！马上搞定！程序用时',(endtime - starttime).seconds,'s','!还剩',len(codelists[1]) - code - 1,'家啦！'
    #except:
        #pass

    #print '程序共用时',(datetime.datetime.now() - starttime).seconds,'s'

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
            item['stock_name'] = pre_item['stock_name']
            item['date'] = pre_item['date']
            item['ts'] = pre_item['ts']
            item['holder_name'] = pre_item['holder_name']
            item['holder_top1'] = pre_item['holder_top1']
            item['holder_top2'] = pre_item['holder_top2']
            item['holder_top3'] = pre_item['holder_top3']
            item['holder_top4'] = pre_item['holder_top4']
            item['holder_top5'] = pre_item['holder_top5']
            item['holder_top6'] = pre_item['holder_top6']
            item['holder_top7'] = pre_item['holder_top7']
            item['holder_top8'] = pre_item['holder_top8']
            item['holder_top9'] = pre_item['holder_top9']
            item['holder_top10'] = pre_item['holder_top10']
            item['holder_top10byinst'] = pre_item['holder_top10byinst']
            item['holder_top10pct'] = pre_item['holder_top10pct']
            item['holder_pctbyinst'] = pre_item['holder_pctbyinst']
            #item['content'] = pre_item['content']
            #print item['id']
            action = {"index":{}} #action  "_id": item['url']
            request_body = item # request body
            bulk_action.extend ([action,request_body]) # 在列表中组织形式   

            count += 1
            if count % 1000 == 0:
                try:
                    es.bulk(bulk_action, index="holders", doc_type="type1",timeout=400)
                    bulk_action = []
                    print count
                except Exception,e:
                    print e

            
        #把最后剩余不足1000条的也插入
        es.bulk(bulk_action, index="holders", doc_type="type1",timeout=400)

def update_announce():
    conn = default_db()
    cur = conn.cursor()
    sql = "SELECT * FROM %s WHERE date <= '%s'" % ('large_trans','2017-03-16')
    cur.execute(sql)
    results = cur.fetchall()
    es = Elasticsearch([{'host':'219.224.134.214','port':9202}])
    count = 0
    bulk_action = []
    for result in results:
        del result['id']
        del result['currency_code']
        del result['industry_category']
        del result['security_type']
        result['Discount_ratio'] = result.pop('discount_ratio')
        result['Buyer'] = result.pop('buyer')
        result['Seller'] = result.pop('seller')
        action = {"index":{}}
        bulk_action.extend ([action,result])
        count += 1
        if count % 1000 == 0:
            try:
                es.bulk(bulk_action, index="east_money", doc_type="type1",timeout=400)
                bulk_action = []
                print count
            except Exception,e:
                print e

    es.bulk(bulk_action, index="east_money", doc_type="type1",timeout=400)

def delele_trading():
    conn = default_db()
    cur = conn.cursor()
    sql = "SELECT * FROM %s WHERE stock_id = '%s'" % ('trading','600189')
    cur.execute(sql)
    results = cur.fetchall()
    num = len(results) 
    for result in results:
        delete = "DELETE FROM %s WHERE %s = %d" % ('trading',ES_HOLDERS_SHOW_ID,result[ES_HOLDERS_SHOW_ID])
        try:
            cur.execute(delete)
            conn.commit()
        except Exception, e:
            print e

if __name__=="__main__":
    #update_day_label()
    #delete_holders_pct()
    #delete_day_type()
    '''
    df1 = pd.DataFrame(data=[['000902','2014-05-01','2014-09-30'],
        ['002211','2014-05-29','2014-12-09'],
        ['002219','2013-05-09','2013-07-05'],
        ['300380','2014-11-01','2015-05-27'],
        ['300028','2015-02-16','2015-06-09'],
        ['002306','2014-03-03','2014-12-18']],
        columns=['stock_id','start_date','end_date'])'''
    #df2 = pd.DataFrame(data=[['600401','2014-12-24','2015-01-30']],
    #    columns=['stock_id','start_date','end_date'])
    '''
    df3 = pd.DataFrame(data=[['000703','2011-06-27','2012-03-26']],
        columns=['stock_id','start_date','end_date'])'''
    #df2 = pd.DataFrame(data=[['600401','2014-12-24','2015-01-30']],
    #    columns=['stock_id','start_date','end_date'])
    #insert_sql(df2)
    #update_hotnews()
    #insert_type2()
    #update_hotnews()
    #delete_nouse()
    #count()
    #transfer2es('2018-01-01','2018-05-15')
    #update_announce()
    delele_trading()