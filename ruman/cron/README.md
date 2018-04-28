# ruman_model
原始数据的导入统一放在/data_process/raw_data_import/路径下
对于原始数据的统计处理位于/data_process/stastics（用于模型的统计值）和/data_process/present（用于前台展示的统计值）

##########lfz#############
getprice.py 从wind获取股价并存入mysql数据库，从tushare获取净利润，更新至mysql
    what_quarter()    获取对应季度
        输入：日期('2017-01-01')    输出：当前季度，前一季度(2017,1,2016,4)
    create()    导入历史股价
        输入：开始日期，结束日期    输出：无（插入至数据库）
    get_profit()    季度大范围更新历史净利润（按季度，稍快）
        输入：交易日时间列表，年，月    输出：无（插入至数据库）
    get_profit_new()    季度小范围更新历史净利润（按天，稍慢）
        输入：交易日时间列表，年，月    输出：无（插入至数据库）
    get_market_history()    选定极度利用上两个函数更新（默认为get_profit,ftype=1为get_profit_new）
        输入：函数类型(int)    输出：无（插入至数据库）
    get_market_daily()    更新当天的股价及净利润
        输入：日期('2017-01-01')（默认为今天，不为今天只执行净利润）    输出：无（插入至数据库）

insertresult.py  不用

updatestock.py  更新监测股票的基本信息
    updatestock()   更新初始表
        输入：日期('2017-01-01'，仅用于获取数据，默认为今天)，大行业字典，中行业字典   输出：无（插入至数据库）
    updatestock_everyday()    更新每天表
        输入：日期('2017-01-01'，仅用于获取数据，默认为今天)，大行业字典，中行业字典   输出：无（插入至数据库）

warning.py   更新每天预警数

windgd.py   更新每天序列股东信息
    get_gudong()   更新初始表
        输入：开始日期，结束日期   输出：无（插入至数据库）
    get_gudong_everyday()   更新每天表
        输入：日期(默认今天)   输出：无（插入至数据库）

windgdnew.py   更新季度股东信息供展示
    get_gd()   获得展示列表（因为目前数据库问题有部分注释掉）
        输入：开始年月日，结束年月日   输出：无（插入至数据库）
    get_pct()   从每天的序列拿数据至展示数据库

ggdr.py   将公告导入es
    ggdr()   更新初始表
        输入：开始年月日，结束年月日   输出：无（插入至数据库）
    ggdr_today()   更新每天表
        输入：日期(默认今天)   输出：无（插入至数据库）

模型：
    先createframe→create，运行create.py创建时间json存于本地，再利用calculate→deal→train，运行train.py训练并存储模型，再每天利用获取的数据训练新数据存于数据库
    


############lys###########
eastMoneyDaily.py 从东方财富上爬取每天的大宗交易的数据，存到ES数据库（这个必须每天晚上8-9点更新）
trans_stat.py 统计大宗交易频率



announcement_stat.py 从ES数据库中统计每只股票每天每种类型公告的数目
      getkind(line)  输入：每一条公告     输出：该公告属于那种类型

manipulate_influence.py  在统计疑似操纵股票中，统计股票的涨幅

manipulate_industry.py  在统计疑似操纵股票中，统计股票的行业

manipulate_panel.py 在疑似操纵的股票中，统计股票所属的板块

manipulate_type.py  在疑似操纵的股票中，统计操纵的类型