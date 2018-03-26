#!/usr/bin/env python
# coding:utf-8
from db import *
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#table
TABLE_HOLDERS = 'holders'
TABLE_DAY = 'manipulate_day'
TABLE_WARNING = 'manipulate_warning'
TABLE_MARKET_DAILY = 'market_daily_new'
TABLE_HOLDERS_SHOW = 'holders_show'
TABLE_HOLDERS_PCT = 'holders_pct'
TABLE_INFLUENCE="manipulate_influence"
TABLE_INDUSTRY="manipulate_industry"
TABLE_TYPE="manipulate_type"
TABLE_PANEL="manipulate_panel"
TABLE_TRANCE="large_trans"
TABLE_GONGSHANG = 'gongshang'

#es
ES_HOST = '219.224.134.214'
ES_PORT = 9202

#db
HOST = "219.224.134.214"
USER = "root"
PASSWORD = ""
DEFAULT_DB = "ruman"
CHARSET = "utf8"
TEST_DB = ""



#index_name
DAY_STOCK_ID = 'stock_id'
DAY_STOCK_NAME = 'stock_name'
DAY_START_DATE = 'start_date'
DAY_IFEND = 'ifend'
DAY_END_DATE = 'end_date'
DAY_MANIPULATE_TYPE = 'manipulate_type'
DAY_INDUSTRY_NAME = 'industry_name'
DAY_INDUSTRY_CODE = 'industry_code'
DAY_INCREASE_RATIO = 'increase_ratio'
DAY_ID = 'id'
WARNING_DATE = 'date'
WARNING_TIMES = 'times'
MARKET_PRICE = 'price'
MARKET_DATE = 'date'
MARKET_INDUSTRY_CODE = 'industry_code'
MARKET_STOCK_ID = 'stock_id'
HOLDERS_SHOW_STOCK_ID = 'stock_id'
HOLDERS_SHOW_DATE = 'date'
HOLDERS_SHOW_HOLDER_NAME = 'holder_name'
HOLDERS_SHOW_ID = 'id'
HOLDERS_SHOW_RANKING = 'ranking'
HOLDERS_PCT_STOCK_ID = 'stock_id'
HOLDERS_PCT_DATE = 'date'
HOLDERS_PCT_ID = 'id'
HOLDERS_PCT_HOLDER_TOP10PCT = 'holder_top10pct'
HOLDERS_PCT_HOLDER_PCTBYINST = 'holder_pctbyinst'
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
TYPE5="others"
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