#-*-coding: utf-8-*-
#每日更新stock_list
from config import *
from time_utils import *
from sql_utils import *
from WindPy import *
import pandas as pd
import json

def updatestock(industry_dict_big,industry_dict_small,theday=today()):
    conn = default_db()
    cur = conn.cursor()
    w.start()
    allmarket = w.wset("SectorConstituent",u"date=" + ts2datetimestrnew(datetimestr2ts(theday)) + ";sector=全部A股").Data  #[1]为代码，[2]为名字" + ts2datetimestrnew(datetimestr2ts(today())) + "
    for num in range(len(allmarket[1])):   #对于所有股票获取其股价数据
        name = allmarket[2][num]
        code = allmarket[1][num]
        print code,name,num
        try:
            data = w.wsd(code, "industry_CSRC12", theday, theday, "industryType=5")
            data1 = w.wsd(code, "mkt", theday, theday, "")
            data2 = w.wsd(code, "ev", theday, theday, "unit=1")
            stock_id = code.split('.')[0]
            stock_name = name
            stock_id_new = code
            ev = data2.Data[0][0] / 100000000
            plate = data1.Data[0][0]
            industry_name = data.Data[0][0].split('-')[0]
            industry_code = industry_dict_big[industry_name]
            large_industry_name = data.Data[0][0].split('-')[1]
            large_industry_code = industry_dict_small[large_industry_name]
            middle_industry_name = data.Data[0][0].split('-')[2]
            middle_industry_code = industry_dict_small[middle_industry_name]
            small_industry_name = data.Data[0][0].split('-')[3]
            small_industry_code = industry_dict_small[small_industry_name]
            order = 'insert into stock_list ( stock_id,stock_name,stock_id_new,ev,plate,industry_name,industry_code,large_industry_name,large_industry_code,middle_industry_name,middle_industry_code,small_industry_name,small_industry_code )values("%s", "%s","%s","%f", "%s", "%s","%s", "%s","%s","%s", "%s","%s","%s")' % (stock_id,stock_name,stock_id_new,ev,plate,industry_name,industry_code,large_industry_name,large_industry_code,middle_industry_name,middle_industry_code,small_industry_name,small_industry_code)
            try:
                cur.execute(order)
                conn.commit()
            except Exception, e:
                print e
        except Exception, e:
            print e
            pass

def updatestock_everyday(industry_dict_big,industry_dict_small,theday=today()):
    trade_before = ts2datetimestr(datetimestr2ts(theday) - 2592000).split('-')   #获取前30天日期
    trade_after = ts2datetimestr(datetimestr2ts(theday) + 2592000).split('-')   #获取后30天日期
    trade_list = get_tradelist(int(trade_before[0]),int(trade_before[1]),int(trade_before[2]),int(trade_after[0]),int(trade_after[1]),int(trade_after[2]))   #获取可能包含当天的交易日列表
    year = int(theday.split('-')[0])
    month = int(theday.split('-')[1])
    day = int(theday.split('-')[2])
    if theday in trade_list:
        conn = default_db()
        cur = conn.cursor()
        w.start()
        codelist = list(pd.read_sql("SELECT * FROM stock_list",conn)['stock_id'])
        allmarket = w.wset("SectorConstituent",u"date=" + ts2datetimestrnew(datetimestr2ts(theday)) + ";sector=全部A股").Data
        l = []
        m = []
        n = []
        print 'Start deleting...'
        for num in range(len(allmarket[1])):
            l.append(allmarket[1][num].split('.')[0])   
            m.append(allmarket[1][num])
            n.append(allmarket[2][num])
        todaylist = [l,m,n]   #todaylist包含[0]是没有.SZ/SH，[1]是有的，[2]是名字
        for code in codelist:
            if code not in todaylist[0]:
                print code
                sql = "DELETE FROM stock_list WHERE stock_id = '%s'" % (code)
                try:
                    cur.execute(sql)
                    conn.commit()
                except Exception, e:
                    print e
        print 'Start adding...'
        for num in range(len(todaylist[0])):
            if todaylist[0][num] not in codelist:
                print todaylist[0][num]
                name = todaylist[2][num]
                code = todaylist[1][num]
                print code,name,num
                try:
                    data = w.wsd(code, "industry_CSRC12", theday, theday, "industryType=5")
                    data1 = w.wsd(code, "mkt", theday, theday, "")
                    data2 = w.wsd(code, "ev", theday, theday, "unit=1")
                    stock_id = code.split('.')[0]
                    stock_name = name
                    stock_id_new = code
                    ev = data2.Data[0][0] / 100000000
                    plate = data1.Data[0][0]
                    industry_name = data.Data[0][0].split('-')[0]
                    industry_code = industry_dict_big[industry_name]
                    large_industry_name = data.Data[0][0].split('-')[1]
                    large_industry_code = industry_dict_small[large_industry_name]
                    middle_industry_name = data.Data[0][0].split('-')[2]
                    middle_industry_code = industry_dict_small[middle_industry_name]
                    small_industry_name = data.Data[0][0].split('-')[3]
                    small_industry_code = industry_dict_small[small_industry_name]
                    order = 'insert into stock_list ( stock_id,stock_name,stock_id_new,ev,plate,industry_name,industry_code,large_industry_name,large_industry_code,middle_industry_name,middle_industry_code,small_industry_name,small_industry_code )values("%s", "%s","%s","%f", "%s", "%s","%s", "%s","%s","%s", "%s","%s","%s")' % (stock_id,stock_name,stock_id_new,ev,plate,industry_name,industry_code,large_industry_name,large_industry_code,middle_industry_name,middle_industry_code,small_industry_name,small_industry_code)
                    try:
                        cur.execute(order)
                        conn.commit()
                    except Exception, e:
                        print e
                except Exception, e:
                    print e
                    pass
    else:
        print '今天不是交易日'

def update1(theday):
    conn = default_db()
    cur = conn.cursor()
    w.start()
    codedict = {}
    allmarket = w.wset("SectorConstituent",u"date=20180306;sector=全部A股").Data
    l = {}
    for i in allmarket[1]:
        l[i.split('.')[0]] = i
    sql = "SELECT * FROM stock_list"
    cur.execute(sql)
    results = cur.fetchall()
    for result in results:
        codedict[result['stock_id']] = [l[result['stock_id']],result['id']]
    codelist = codedict.keys()
    codelist.sort()
    for code in codelist:
        print code
        stock_id_new = codedict[code][0]
        data1 = w.wsd(stock_id_new, "mkt", theday, theday, "")
        data2 = w.wsd(stock_id_new, "ev", theday, theday, "unit=1")
        ev = data2.Data[0][0] / 100000000
        plate = data1.Data[0][0]
        update = "UPDATE stock_list SET stock_id_new = '%s',ev = '%f',plate = '%s' WHERE id = '%d'" % (stock_id_new, ev, plate, codedict[code][1])
        cur.execute(update)
        conn.commit() 

def get_json(industry_name):
    conn = default_db()
    cur = conn.cursor()
    w.start()
    f = open(r'C:\Users\lifengzhi\Desktop\code\stock.json','w')
    allmarket = w.wset("SectorConstituent",u"date=20180205;sector=全部A股").Data
    dic = {}
    for code in allmarket[1]:
        data = w.wsd(code, "industry_CSRC12", "2018-02-05", "2018-02-05", "industryType=5")
        industry_name = data.Data[0][0].split('-')[0]
        industry_code = industry_dict_big[industry_name]
        dic[code.split('.')[0]] = industry_code
    j = json.dumps(dic)
    f.write(j)
    f.close()



if __name__=="__main__":
    industry_dict_big = {u'农、林、牧、渔业':u'A',u'采矿业':u'B',u'制造业':u'C',u'电力、热力、燃气及水生产和供应业':u'D',
                        u'建筑业':u'E',u'批发和零售业':u'F',u'交通运输、仓储和邮政业':u'G',u'住宿和餐饮业':u'H',
                        u'信息传输、软件和信息技术服务业':u'I',u'金融业':u'J',u'房地产业':u'K',u'租赁和商务服务业':u'L',
                        u'科学研究和技术服务业':u'M',u'水利、环境和公共设施管理业':u'N',u'居民服务、修理和其他服务业':u'O',
                        u'教育':u'P',u'卫生和社会工作':u'Q',u'文化、体育和娱乐业':u'R',u'综合':u'S'}
    industry_dict_small = {u'农业':u'A01',u'林业':u'A02',u'畜牧业':u'A03',u'渔业':u'A04',u'农、林、牧、渔服务业':u'A05',
                        u'煤炭开采和洗选业':u'B06',u'石油和天然气开采业':u'B07',u'黑色金属矿采选业':u'B08',
                        u'有色金属矿采选业':u'B09',u'非金属矿采选业':u'B10',u'开采辅助活动':u'B11',u'其他采矿业':u'B12',
                        u'农副食品加工业':u'C13',u'食品制造业':u'C14',u'酒、饮料和精制茶制造业':u'C15',u'烟草制品业':u'C16',
                        u'纺织业':u'C17',u'纺织服装、服饰业':u'C18',u'皮革、毛皮、羽毛及其制品和制鞋业':u'C19',
                        u'木材加工及木、竹、藤、棕、草制品业':u'C20',u'家具制造业':u'C21',u'造纸及纸制品业':u'C22',
                        u'印刷和记录媒介复制业':u'C23',u'文教、工美、体育和娱乐用品制造业':u'C24',
                        u'石油加工、炼焦及核燃料加工业':u'C25',u'化学原料及化学制品制造业':u'C26',u'医药制造业':u'C27',
                        u'化学纤维制造业':u'C28',u'橡胶和塑料制品业':u'C29',u'非金属矿物制品业':u'C30',
                        u'黑色金属冶炼及压延加工':u'C31',u'有色金属冶炼及压延加工':u'C32',u'金属制品业':u'C33',
                        u'通用设备制造业':u'C34',u'专用设备制造业':u'C35',u'汽车制造业':u'C36',
                        u'铁路、船舶、航空航天和其他运输设备制造业':u'C37',u'电气机械及器材制造业':u'C38',
                        u'计算机、通信和其他电子设备制造业':u'C39',u'仪器仪表制造业':u'C40',u'其他制造业':u'C41',
                        u'废弃资源综合利用业':u'C42',u'金属制品、机械和设备修理业':u'C43',u'电力、热力生产和供应业':u'D44',
                        u'燃气生产和供应业':u'D45',u'水的生产和供应业':u'D46',u'房屋建筑业':u'E47',u'土木工程建筑业':u'E48',
                        u'建筑安装业':u'E49',u'建筑装饰和其他建筑业':u'E50',u'批发业':u'F51',u'零售业':u'F52',
                        u'铁路运输业':u'G53',u'道路运输业':u'G54',u'水上运输业':u'G55',u'航空运输业':u'G56',
                        u'管道运输业':u'G57',u'装卸搬运和其他运输代理':u'G58',u'仓储业':u'G59',u'邮政业':u'G60',
                        u'住宿业':u'H61',u'餐饮业':u'H62',u'电信、广播电视和卫星传输服务':u'I63',u'互联网和相关服务':u'I64',
                        u'软件和信息技术服务业':u'I65',u'货币金融服务':u'J66',u'资本市场服务':u'J67',u'保险业':u'J68',
                        u'其他金融业':u'J69',u'房地产业':u'K70',u'租赁业':u'L71',u'商务服务业':u'L72',u'研究和试验发展':u'M73',
                        u'专业技术服务业':u'M74',u'科技推广和应用服务业':u'M75',u'水利管理业':u'N76',
                        u'生态保护和环境治理业':u'N77',u'公共设施管理业':u'N78',u'居民服务业':u'O79',
                        u'机动车、电子产品和日用产品修理业':u'O80',u'其他服务业':u'O81',u'教育':u'P82',u'卫生':u'Q83',
                        u'社会工作':u'Q84',u'新闻和出版业':u'R85',u'广播、电视、电影和影视录音制作业':u'R86',
                        u'文化艺术业':u'R87',u'体育':u'R88',u'娱乐业':u'R89',u'综合':u'S90'}
    #updatestock('2018-03-06',industry_dict_big,industry_dict_small)
    #updatestock_everyday(industry_dict_big,industry_dict_small)
    update1('2018-03-06')