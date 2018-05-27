#!/usr/bin/env python
# coding:utf-8
from db import *
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#table
ES_TABLE_HOLDERS = 'holders'
TABLE_RESULT = 'manipulate_result'
TABLE_DAY = 'manipulate_day'
TABLE_WARNING = 'manipulate_warning'
TABLE_MARKET_DAILY = 'market_daily'
TABLE_TRADING = 'trading'
TABLE_HOLDERS_SHOW = 'holders_show'
TABLE_HOLDERS_PCT = 'holders_pct'
TABLE_INFLUENCE="manipulate_influence"
TABLE_INDUSTRY="manipulate_industry"
TABLE_TYPE="manipulate_type"
TABLE_PANEL="manipulate_panel"
TABLE_GONGSHANG = 'gongshang'
TABLE_STOCK_LIST = 'stock_list'
TABLE_NETPROFIT = 'netprofit'
TABLE_JIEJIN = 'jiejin'
TABLE_ANNOUNCEMENT = 'announcement'
TABLE_TRANSACTION_STAT = 'transaction_stat'
TABLE_BLACK_LIST = 'black_list'
TABLE_PUNISH = 'punish'
TABLE_PROPAGATE = 'all_source_propagate'
TABLE_WORDCLOUD = 'wordcloud'
TABLE_HOTNEWS = 'hot_news'
TABLE_WEIPAN_SHOW = 'weipan_show'

#esdic
DIC_ANNOUNCEMENT = {'index':'announcement','type':'basic_info'}
DIC_LARGE_TRANS = {'index':'east_money','type':'type1'}
RUMORLIST_INDEX = 'rumor_calculated_list'
WEBOUSER_INDEX = 'weibo_user'

#es
ES_HOST = '219.224.134.214'
ES_PORT = 9202
ES_HOST_WEB0 = '219.224.134.216'
ES_PORT_WEB0 = 9201

#db
SQL_HOST = "219.224.134.214"
SQL_USER = "root"
SQL_PASSWD = ""
DEFAULT_DB = "ruman"
SQL_CHARSET = "utf8"
TEST_DB = ""



#index_name
#操纵模块
RESULT_RESULT = 'result'
RESULT_PROBABILITY = 'probability'
RESULT_ID = 'id'
DAY_STOCK_ID = 'stock_id'
DAY_STOCK_NAME = 'stock_name'
DAY_START_DATE = 'start_date'
DAY_IFEND = 'ifend'
DAY_END_DATE = 'end_date'
DAY_MANIPULATE_TYPE = 'manipulate_type'
DAY_INDUSTRY_NAME = 'industry_name'
DAY_INDUSTRY_CODE = 'industry_code'
DAY_INCREASE_RATIO = 'increase_ratio'
DAY_MARKET_PLATE = 'market_plate'
DAY_ID = 'id'
DAY_MID = 'mid'
DAY_MANIPULATE_LABEL = 'manipulate_label'
DAY_IFPUNISH = 'ifpunish'
WARNING_DATE = 'date'
WARNING_TIMES = 'times'
MARKET_PRICE = 'price'
MARKET_PRICE_FU = 'price_fu'
MARKET_DATE = 'date'
MARKET_INDUSTRY_CODE = 'industry_code'
MARKET_STOCK_ID = 'stock_id'
MARKET_TURNOVER_RATE = 'turnover_rate'
TRADING_DATE = 'date'
TRADING_STOCK_ID = 'stock_id'
TRADING_VOLUME = 'volume'
TRADING_AMT = 'amt'
ES_HOLDERS_SHOW_STOCK_ID = 'stock_id'
ES_HOLDERS_SHOW_DATE = 'date'
ES_HOLDERS_SHOW_HOLDER_NAME = 'holder_name'
ES_HOLDERS_SHOW_ID = 'id'
ES_HOLDERS_SHOW_RANKING = 'ranking'
ES_HOLDERS_PCT_STOCK_ID = 'stock_id'
ES_HOLDERS_PCT_DATE = 'date'
ES_HOLDERS_PCT_ID = 'id'
ES_HOLDERS_PCT_HOLDER_TOP10PCT = 'holder_top10pct'
ES_HOLDERS_PCT_HOLDER_PCTBYINST = 'holder_pctbyinst'
ES_HOLDERS_HOLDER_TOP10BYINST = 'holder_top10byinst'
INFLUENCE_DATE="date"
INFLUENCE_ID="id"
INFLUENCE_FREQUENCY="frequency"
INFLUENCE_1="increasefzero"
INFLUENCE_2="increaseffive"
INFLUENCE_3="increaseften"
INFLUENCE_4="increaseffifteen"
INFLUENCE_5="increaseftwenty"
INFLUENCE_6="increaseftwentyfive"
INFLUENCE_7="increasefthirty"
INFLUENCE_8="increasefthirtyfive"
INFLUENCE_9="increasefforty"
INFLUENCE_10="increaseffortyfive"
INFLUENCE_11="increaseffifty"
INFLUENCE_12="increaseffiftyfive"
INFLUENCE_13="increasefsixty"
INFLUENCE_14="increasefsixtyfive"
INFLUENCE_15="increasefseventy"
INFLUENCE_16="increasezero"
INFLUENCE_17="increasefive"
INFLUENCE_18="increaseten"
INFLUENCE_19="increasefifteen"
INFLUENCE_20="increasetwenty"
INFLUENCE_21="increasetwentyfive"
INFLUENCE_22="increasethirty"
INFLUENCE_23="increasethirtyfive"
INFLUENCE_24="increaseforty"
INFLUENCE_25="increasefortyfive"
INFLUENCE_26="increasefifty"
INFLUENCE_27="increasefiftyfive"
INFLUENCE_28="increasesixty"
INFLUENCE_29="increasesixtyfive"
INFLUENCE_30="increaseseventy"
INFLUENCE_31="increaseseventyfive"
INFLUENCE_32="increaseeighty"
INFLUENCE_33="increaseeightyfive"
INFLUENCE_34="increaseninty"
INFLUENCE_35="increasenintyfive"
INDUSTRY_DATE="date"
INDUSTRY_FREQUENCY="frequency"
INDUSTRY_ID="id"
INDUSTRY_A="industry_A"
INDUSTRY_B="industry_B"
INDUSTRY_C="industry_C"
INDUSTRY_D="industry_D"
INDUSTRY_E="industry_E"
INDUSTRY_F="industry_F"
INDUSTRY_G="industry_G"
INDUSTRY_H="industry_H"
INDUSTRY_I="industry_I"
INDUSTRY_J="industry_J"
INDUSTRY_K="industry_K"
INDUSTRY_L="industry_L"
INDUSTRY_M="industry_M"
INDUSTRY_N="industry_N"
INDUSTRY_O="industry_O"
INDUSTRY_P="industry_P"
INDUSTRY_Q="industry_Q"
INDUSTRY_R="industry_R"
INDUSTRY_S="industry_S"
TYPE_DATE="date"
TYPE_FREQUENCY="frequency"
TYPE_ID="id"
TYPE1="gaosong"
TYPE2="dingxiang"
TYPE3="weishizhi"
TYPE4="sanbumouli"
TYPE5="weipan"
PANEL_DATE="date"
PANEL_FREQUENCY="frequency"
PANEL_STOCK_ID="stock_id"
PANEL_ID="id"
PANEL1="zhuban"
PANEL2="zhongxiaoban"
PANEL3="chuangyeban"
TRAN_DATE="date"
TRAN_STOCK_ID="stock_id"
TRAN_NAME="stock_name"
TRAN_PRICE="transaction_price"
TRAN_NUMBER="transaction_number"
TRAN_AMOUNT="transaction_amount"
TRAN_RATIO="discount_ratio"
TRAN_BUYER="buyer"
TRAN_SELLER="seller"
GONGSHANG_STOCK_ID = "stock_id"
GONGSHANG_ID = "id"
GONGSHANG_STOCK_NAME = "stock_name"
GONGSHANG_PLACE = "place"
GONGSHANG_START_DATE = "start_date"
GONGSHANG_NAME = "name"
GONGSHANG_MONEY = "money"
GONGSHANG_PERSON = "person"
GONGSHANG_KIND = "kind"
GONGSHANG_INDUSTRY = "industry"
GONGSHANG_PLATE = "plate"
NETPROFIT_STOCK_ID = "stock_id"
NETPROFIT_STOCK_NAME = "stock_name"
NETPROFIT_DATE = 'date'
NETPROFIT_ROE = 'roe'
NETPROFIT_NET_PROFIT_RATIO = 'net_profit_ratio'
NETPROFIT_GROSS_PROFIT_RATE = 'gross_profit_rate'
NETPROFIT_NET_PROFITS = 'net_profits'
NETPROFIT_EPS = 'eps'
NETPROFIT_BUSINESS_INCOME = 'business_income'
NETPROFIT_BIPS = 'bips'
JIEJIN_DATE = 'jiejin_date'
JIEJIN_STOCK_ID = 'stock_id'
ANNOUNCEMENT_INVESTMENT = 'Investment_announcement'
ANNOUNCEMENT_PLEDGE = 'Pledge_announcement'
ANNOUNCEMENT_REDUCING = 'Reducing_announcement'
ANNOUNCEMENT_PROFIT = 'Profit_announcement'
#ANNOUNCEMENT_
TRANSACTION_STAT_FREQUENCY = 'frequency'
BLACK_LIST_STOCK_ID = 'stock_id'
BLACK_LIST_REASON = 'reason'
BLACK_LIST_START_TS = 'start_ts'
BLACK_LIST_END_TS = 'end_ts'
BLACK_LIST_INDUSTRY_CODE = 'industry_code'
STOCK_LIST_LISTED = 'listed'
STOCK_LIST_MIDDLE_INDUSTRY_CODE = 'middle_industry_code'
STOCK_LIST_STOCK_ID = 'stock_id'
STOCK_LIST_STOCK_NAME = 'stock_name'
STOCK_LIST_INDUSTRY_NAME = 'industry_name'
STOCK_LIST_INDUSTRY_CODE = 'industry_code'
STOCK_LIST_PLATE = 'plate'
PUNISH_STOCK_ID = 'stock_id'
PUNISH_PUNISH_NAME = 'punish_name'
PUNISH_PUNISH_TIME = 'punish_time'
PUNISH_ABSTRACT = 'abstract'
WEIPAN_SHOW_STOCK_ID = 'stock_id'
WEIPAN_SHOW_TIME = 'time'
WEIPAN_SHOW_DATE = 'date'
WEIPAN_SHOW_PRICE = 'price'
WEIPAN_SHOW_VOLUME = 'volume'
WEIPAN_SHOW_AMT = 'amt'
WEIPAN_SHOW_IFSELF = 'ifself'

#一些其他的常值
SHOW_DATE = '2018-05-15'
table1 = [[TABLE_MARKET_DAILY,MARKET_PRICE_FU],[ES_TABLE_HOLDERS,ES_HOLDERS_HOLDER_TOP10BYINST],[TABLE_ANNOUNCEMENT,ANNOUNCEMENT_INVESTMENT],[TABLE_ANNOUNCEMENT,ANNOUNCEMENT_PLEDGE],[TABLE_ANNOUNCEMENT,ANNOUNCEMENT_REDUCING],[TABLE_TRANSACTION_STAT,TRANSACTION_STAT_FREQUENCY]]#
table2 = [[TABLE_MARKET_DAILY,MARKET_PRICE_FU],[TABLE_MARKET_DAILY,MARKET_TURNOVER_RATE],[TABLE_JIEJIN,JIEJIN_DATE],[TABLE_ANNOUNCEMENT,ANNOUNCEMENT_PLEDGE],[TABLE_ANNOUNCEMENT,ANNOUNCEMENT_REDUCING],[TABLE_ANNOUNCEMENT,ANNOUNCEMENT_PROFIT],[TABLE_TRANSACTION_STAT,TRANSACTION_STAT_FREQUENCY]]

CLUSTER_NUM = 60
CLUSTER_OVER = 200

# 多通道溯源
# TYPE1_DICT = {'bbs':'type1','forum':'type1','webo':'type1','wechat':'type1','zhihu':'type1','news_new':'type1'}
TYPE1_DICT = {'weixin_news':'type1','weibo_news':'type1','bbs_news':'type1','news_new':'type1'}
TOPIC_ABOUT_INDEX = 'topic_about'
# TOPIC_ABOUT_DOCTYPE = ['bbs','forum','webo','wechat','zhihu','news_new']
TOPIC_ABOUT_DOCTYPE = ['weixin_news','weibo_news','bbs_news','news_new']
CLUSTER_INDEX = 'clustering'

#热点新闻
HOT_NEWS_WEB = 'web'
HOT_NEWS_TITLE = 'title'
HOT_NEWS_URL = 'url'
HOT_NEWS_ABSTRACT = 'abstract'
HOT_NEWS_AUTHOR = 'author'
HOT_NEWS_COMMENTS = 'comments'
HOT_NEWS_TEND = 'tend'
HOT_NEWS_CONTENT = 'content'
HOT_NEWS_IN_TIME = 'in_time'
HOT_NEWS_TEXT_ID = 'text_id'
HOT_NEWS_PANEL = 'panel'
HOT_NEWS_KEY_WORD = 'key_word'
HOT_NEWS_DATE = 'date'
HOT_NEWS_ID = 'id'
PROPAGATE_SOURCE = 'source'
PROPAGATE_BEGIN_TS = 'begin_ts'
PROPAGATE_END_TS = 'end_ts'
PROPAGATE_COUNT = 'count'
PROPAGATE_NEWS_ID = 'news_id'
PROPAGATE_ID = 'id'
WORDCLOUD_ID = 'id'
WORDCLOUD_NEWS_ID = 'news_id'
WORDCLOUD_WORDS = 'words'
WORDCLOUD_SOURCE = 'source'