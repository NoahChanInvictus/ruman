# -*- coding: utf-8 -*-
from datetime import *
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import TransportError
from elasticsearch.helpers import bulk  #, streaming_bulk



# ES
ES_HOST = '219.224.134.214'
ES_PORT = 9202  

INDEX_BBS = 'bbs'
INDEX_FORUM = 'forum'
INDEX_WEBO = 'webo'
INDEX_ZHIHU = 'zhihu'
INDEX_WECHAT = 'wechat'
INDEX_NEWS = 'news'
INDEX_WDZJ = 'wdzj1'
INDEX_GONGSHANG = 'gongshang'

TYPE1 = 'type1'
TYPE2 = 'type2'

# 模型参数
## 画像部分
AD_SOURCE = {'bbs':'bbs','forum':'forum','webo':'webo','wechat':'wechat','zhihu':'zhihu'}
COMMENT_SOURCE = {'bbs':'bbs','forum':'forum','webo':'webo','wechat':'wechat','zhihu':'zhihu'}
TYPE1_DICT = {'bbs':'type1','forum':'type1','webo':'type1','wechat':'type1','zhihu':'type2'}
TYPE2_DICT = {'bbs':'type2','forum':'type2','webo':'type2','wechat':'type2','zhihu':'type1'}
TYPE_LIST = [TYPE1_DICT] # ,TYPE2_DICT
STATISTIC_WINDOW = 90

# 数据库配置项
SQL_HOST = '219.224.134.214'
SQL_USER = 'root'
SQL_PASSWD = ''
DEFAULT_DB = 'ruman'
SQL_CHARSET = 'utf8'

# 数据库表
TABLE_MARKET_DAILY = 'market_daily'
TABLE_LARGE_TRANS = 'large_trans'
TABLE_HOLDERS = 'holders'
TABLE_ANNOUNCE = 'announce'
TABLE_FREQUENCY = 'transaction_stat'
TABLE_TRANS_STAT = 'transaction_stat'
TABLE_STOCK_LIST = 'stock_list'

   