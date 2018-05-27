# -*- coding: utf-8 -*-

import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from elasticsearch import Elasticsearch

GRAPH_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../graph/')

REDIS_CLUSTER_HOST_FLOW1 = '219.224.134.212'
REDIS_CLUSTER_HOST_FLOW1_LIST = ["219.224.134.211", "219.224.134.212", "219.224.134.213"]
REDIS_CLUSTER_PORT_FLOW1 = '6669'#'6379'
REDIS_CLUSTER_PORT_FLOW1_LIST = ["6379", "6380"]

#yuanhuiru
'''
REDIS_CLUSTER_HOST_FLOW2 = '219.224.134.212'
REDIS_CLUSTER_PORT_FLOW2 = '6666'
'''
REDIS_CLUSTER_HOST_FLOW2 = '219.224.134.213'
REDIS_CLUSTER_PORT_FLOW2 = '6666'

#JLN for keyword find user
REDIS_KEYWORD_HOST = '219.224.134.212'
REDIS_KEYWORD_PORT = '6381'
#flow2用了

REDIS_HOST = '219.224.134.212'#'219.224.134.212'
REDIS_PORT = '6670'#'6381'

#uname to uid 
UNAME2UID_HOST = '219.224.134.211'
UNAME2UID_PORT = '7381'
# uname2uid in redis: {'weibo_user': {uname:uid, ...}}
UNAME2UID_HASH = 'weibo_user'
REDIS_TEXT_MID_HOST = '219.224.134.211' # 注意；和redis flow1的host/port相同
REDIS_TEXT_MID_PORT = '7381'
#flow3:retweet/be_retweet redis
RETWEET_REDIS_HOST = '219.224.134.215'#'219.224.134.212'
RETWEET_REDIS_PORT = '6667'#'6381'
#flow3:comment/be_comment redis
COMMENT_REDIS_HOST = '219.224.134.215'#'219.224.134.212'
COMMENT_REDIS_PORT = '6668'


#USER_ES_HOST = '219.224.135.97'
#ES_CLUSTER_HOST_FLOW1 = ["219.224.134.213", "219.224.134.211"]
#ES_COPY_USER_PORTAIT_HOST = ["219.224.134.213", "219.224.134.211"]
#USER_ES_HOST = '219.224.135.97'
ES_CLUSTER_HOST_FLOW1 = ["219.224.134.216:9201"]#, "219.224.134.217:9201","219.224.134.218:9201"
#ES_CLUSTER_HOST_FLOW1 = ["219.224.134.216", "219.224.134.217","219.224.134.218"]
ES_COPY_USER_PORTAIT_HOST = ["219.224.134.216:9201"]#, "219.224.134.217:9201","219.224.134.218:9201"

ZMQ_VENT_PORT_FLOW1 = '6387'
ZMQ_CTRL_VENT_PORT_FLOW1 = '5585'
ZMQ_VENT_HOST_FLOW1 = '219.224.134.213'
ZMQ_CTRL_HOST_FLOW1 = '219.224.134.213'

ZMQ_VENT_PORT_FLOW2 = '6388'
ZMQ_CTRL_VENT_PORT_FLOW2 = '5586'

ZMQ_VENT_PORT_FLOW3 = '6389'
ZMQ_CTRL_VENT_PORT_FLOW3 = '5587'

ZMQ_VENT_PORT_FLOW4 = '6390'
ZMQ_CTRL_VENT_PORT_FLOW4 = '5588'

ZMQ_VENT_PORT_FLOW5 = '6391'
ZMQ_CTRL_VENT_PORT_FLOW5 = '5589'

#use to save txt file
WRITTEN_TXT_PATH = '/home/ubuntu2/txt'
REPLICA_BIN_FILE_PATH = '/home/ubuntu2/txt'

# csv file path
'''
BIN_FILE_PATH = '/home/ubuntu8/yuankun/data' # '219.224.135.93:/home/ubuntu8/yuankun'
'''
BIN_FILE_PATH = '/home/ubuntu2/txt'

# first part of csv file1

FIRST_FILE_PART = 'MB_QL_9_7_NODE'

# sensitive words path
SENSITIVE_WORDS_PATH = '/home/ubuntu2/jiangln/jln/user_portrait/user_portrait/cron/flow4/sensitive_words.txt'

# need three ES identification 
USER_PROFILE_ES_HOST = ['219.224.134.216:9201']#,'219.224.134.217:9201','219.224.134.218:9201'
USER_PROFILE_ES_PORT = 9206
USER_PORTRAIT_ES_HOST = ['219.224.134.216:9201']#,'219.224.134.217:9201','219.224.134.218:9201'
USER_PORTRAIT_ES_PORT = 9206
FLOW_TEXT_ES_HOST = ['219.224.134.216:9201']#, '219.224.134.217:9201','219.224.134.218:9201'
FLOW_TEXT_ES_PORT = 9206

# use to identify the db number of redis-97
R_BEGIN_TIME = '2016-11-21'

# use to recommentation
RECOMMENTATION_FILE_PATH = '/home/ubuntu2/jiangln/jln/user_portrait/recommentaion_file'
RECOMMENTATION_TOPK = 10000

# use to config leveldb
DEFAULT_LEVELDBPATH = '/home/ubuntu2'

# use to upload the user list for group task
UPLOAD_FOLDER = '/home/ubuntu2/jiangln/jln/user_portrait/cron/group/upload/'
ALLOWED_EXTENSIONS = set(['txt'])

# use to save user_portrait weibo 7day
XAPIAN_DB_PATH = 'user_portrait_weibo'
XAPIAN_DATA_DIR = '/home/ubuntu2/jiangln/jln/user_portrait_weibo_xapian/data/'
XAPIAN_STUB_FILE_DIR = '/home/ubuntu2/jiangln/jln/user_portrait_weibo_xapian/stub/'

XAPIAN_INDEX_SCHEMA_VERSION = 5
XAPIAN_INDEX_LOCK_FILE = '/tmp/user_portrait_weibo_xapian'

XAPIAN_SEARCH_DEFAULT_SCHEMA_VERSION = 5

XAPIAN_ZMQ_POLL_TIMEOUT = 100000


# all weibo database
WEIBO_API_HOST = ''
WEIBO_API_PORT = ''


# redis/elasticsearch path
redis_path = '/home/redis-3.0.1'
es_path = '/home/elasticsearch-1.6.0'




#jln info_consume
mtype_kv = {'origin':1, 'comment': 2, 'forward':3}
emotions_kv = {'happy': 1, 'angry': 2, 'sad': 3, 'news': 4}
emotions_zh_kv = {'happy': '高兴', 'angry': '愤怒', 'sad': '悲伤', 'news': '新闻'}

#jln
SENTIMENT_TYPE_COUNT = 7
SENTIMENT_FIRST = ['0', '1', '7']
SENTIMENT_SECOND = ['2', '3', '4', '5', '6']
MAX_REPOST_SEARCH_SIZE = '100'
MAX_FREQUENT_WORDS = 100
MAX_LANGUAGE_WEIBO = 200
NEWS_LIMIT = 100

#lcr223
MYSQL_HOST = '219.224.134.222' #47
MYSQL_USER = 'root'
MYSQL_DB = 'weibocase'
MONGODB_HOST = '219.224.134.222' #47
MONGODB_PORT = 27019
SSDB_PORT = 8888
SSDB_HOST = '219.224.134.222' # SSDB服务器在47

#lcr223
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@219.224.134.220/weibocase?charset=utf8'
# Create application
app = Flask('xxx')
# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
# Create database
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_ECHO'] = False
db = SQLAlchemy(app)

#jln:for getTopicByNameStEt
TOPIC_ES_HOST = '219.224.134.216:9204'
topic_es = Elasticsearch(TOPIC_ES_HOST,timeout=1000)
topic_index_name = 'topics'
topic_index_type ='text'

WEIBO_ES_HOST = '219.224.134.211:9201'
weibo_es = Elasticsearch(WEIBO_ES_HOST,timeout=1000)
weibo_index_name = 'weibo'
weibo_index_type ='text'
topics_river_index_name='topics_river'
topics_river_index_type='text'
subopinion_index_type='text'
subopinion_index_name='subopinion'

es_user_profile = Elasticsearch(USER_PORTRAIT_ES_HOST, timeout = 1000)
es_retweet = Elasticsearch(USER_PORTRAIT_ES_HOST, timeout = 1000)
retweet_index_name_pre = '1225_retweet_' # retweet: 'retweet_1' or 'retweet_2'
retweet_index_type = 'user'
profile_index_name = 'weibo_user'  # user profile es
profile_index_type = 'user'


#yangshi video data
VIDEO_PATH='/home/ubuntu2/jiangln/info_consume/user_portrait/user_portrait/info_consume/weibo_hashtag/'
video_file = '2015-04-30---fixed.json'
