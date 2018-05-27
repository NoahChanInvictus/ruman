# -*- coding: UTF-8 -*-
import sys
import time
import urllib
import json
reload(sys)
sys.path.append('../../')
from time_utils import ts2datetime, datetime2ts

ORIGIN_KEYS = ['user', 'retweeted_uid', '_id', 'retweeted_mid', 'timestamp',
               'input_time', 'geo', 'province', 'city', 'message_type', 'user_fansnum',
               'user_friendsnum', 'comments_count', 'reposts_count',
               'retweeted_comments_count', 'retweeted_reposts_count', 'text', 'is_long',
               'bmiddle_pic', 'pic_content', 'audio_url', 'audio_content', 'video_url',
               'video_content', 'sp_type']
RESP_ITER_KEYS = ['_id', 'user', 'retweeted_uid', 'retweeted_mid', 'text',
                  'timestamp', 'reposts_count', 'source', 'bmiddle_pic',
                  'geo', 'attitudes_count', 'comments_count', 'message_type']
CONVERT_TO_INT_KEYS = ['_id', 'user', 'retweeted_uid', 'retweeted_mid',
                       'reposts_count', 'comments_count', 'timestamp', 'message_type']
ABSENT_KEYS = ['attitudes_count', 'source']
IP_TO_GEO_KEY = 'geo'
MID_STARTS_WITH_C = '_id'  # weibo mid starts with 'c_'
SP_TYPE_KEYS = '1'  # 1代表新浪微博

CSV2BIN_DICT = {'uid':'user', 'root_uid':'retweeted_uid', 'mid':'_id', \
                'root_mid':'retweeted_mid', 'text':'text', 'user_fansnum':0 ,\
                'mid_commentnum':0, 'text_length':0, 'audit_status':0 ,\
                'mid_retweetnum':0, 'video_url_length':0, 'send_ip':'geo' ,\
                'send_port':0, 'client_type':0, 'mobile_type':0, 'timestamp':'timestamp' ,\
                'sp_type': 1, 'video_content_length':0, 'pic_content_length':0 ,\
                'client_remark_len':0, 'rootid_retweetnum':0, 'pic_url_length':0 ,\
                'rootid_commentnum':0, 'audio_content_length':0, 'net_type':0 ,\
                'audio_url_length':0, 'user_friendsum':0, 'message_type':'message_type'}

# IP address manipulation functions
def numToDottedQuad(n):
    "convert long int to dotted quad string"

    d = 256 * 256 * 256
    q = []
    while d > 0:
        m, n = divmod(n, d)
        q.append(str(m))
        d = d / 256

    return '.'.join(q)

def ip2geo(ip_addr):
    # ip_addr: '236112240'
    DottedIpAddr = numToDottedQuad(int(ip_addr))
    return DottedIpAddr


def WeiboItem(itemList):
    weibo = dict()

    for key in RESP_ITER_KEYS:

        value = None

        if key not in ABSENT_KEYS:
            value = itemList[ORIGIN_KEYS.index(key)]

            if key == IP_TO_GEO_KEY:
                value = ip2geo(value)

            elif key == MID_STARTS_WITH_C:
                if value[:2] == 'c_':
                    value = int(value[2:])
                else:
                    value = int(value)

            elif key in CONVERT_TO_INT_KEYS:
                value = int(value) if value != '' else 0

        if value is not None:
            weibo[key] = value

    return weibo


class UnkownParseError(Exception):
    pass


def itemLine2Dict(line):
    line = line.decode("utf8", "ignore")
    itemlist = line.strip().split(',')
    if itemlist[-1] == SP_TYPE_KEYS:
        if len(itemlist) != 25:
            try:
                tp = line.strip().split('"')
                if len(tp) != 3:
                    raise UnkownParseError()
                field_0_15, field_16, field_17_24 = tp
                field_0_15 = field_0_15[:-1].split(',')
                field_17_24 = field_17_24[1:].split(',')
                field_0_15.extend([field_16])
                field_0_15.extend([field_17_24])
                itemlist = field_0_15
                if len(itemlist) != 25:
                    raise UnkownParseError()
            except UnkownParseError:
                return None
    else:
        return None

    try:
        itemdict = WeiboItem(itemlist)
    except:
        itemdict = None

    return itemdict


def csv2bin(weibo_item):
    weibo_item_bin = dict()
    for field in CSV2BIN_DICT:
        field_value = CSV2BIN_DICT[field]
        if isinstance(field_value, str):
            weibo_item_bin[field] = weibo_item[field_value]
        else:
            if field == 'sp_type':
                weibo_item_bin[field] = '1'
            else:
                weibo_item_bin[field] = CSV2BIN_DICT[field]
    
    return weibo_item_bin

