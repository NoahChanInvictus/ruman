# -*- coding: utf-8 -*-

import os
from flask import Flask

REDIS_CLUSTER_HOST_FLOW1 = '219.224.134.213'
REDIS_CLUSTER_HOST_FLOW1_LIST = ["219.224.134.211", "219.224.134.212", "219.224.134.213"]
REDIS_CLUSTER_PORT_FLOW1 = '6379'
REDIS_CLUSTER_PORT_FLOW1_LIST = ["6379", "6380"]
REDIS_CLUSTER_HOST_FLOW2 = '219.224.134.214'
REDIS_CLUSTER_PORT_FLOW2 = '6379'
REDIS_HOST = '219.224.134.212'
REDIS_PORT = '6381'
#uname to uid 
UNAME2UID_HOST = '219.224.134.211'
UNAME2UID_PORT = '7381'
# uname2uid in redis: {'weibo_user': {uname:uid, ...}}
UNAME2UID_HASH = 'weibo_user'
REDIS_TEXT_MID_HOST = '219.224.134.211' # 注意；和redis flow1的host/port相同
REDIS_TEXT_MID_PORT = '7381'
#flow3:retweet/be_retweet redis
RETWEET_REDIS_HOST = '219.224.134.212'
RETWEET_REDIS_PORT = '6381'
#flow3:comment/be_comment redis
COMMENT_REDIS_HOST = '219.224.134.218'
COMMENT_REDIS_PORT = '6379'


#USER_ES_HOST = '219.224.135.97'
ES_CLUSTER_HOST_FLOW1 = ["219.224.134.213", "219.224.134.214"]
ES_COPY_USER_PORTAIT_HOST = ["219.224.134.213", "219.224.134.214"]
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
USER_PROFILE_ES_HOST = ['219.224.134.213:9200']
USER_PROFILE_ES_PORT = 9200
USER_PORTRAIT_ES_HOST = ['219.224.134.213:9200']
USER_PORTRAIT_ES_PORT = 9200
FLOW_TEXT_ES_HOST = ['219.224.134.213:9206', '219.224.134.214:9206']
FLOW_TEXT_ES_PORT = 9206

# use to identify the db number of redis-97
R_BEGIN_TIME = '2013-09-01'

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
