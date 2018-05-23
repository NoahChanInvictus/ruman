# -*- coding: utf-8 -*-
# 创建索引
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import TransportError
from elasticsearch.helpers import bulk, streaming_bulk
import sys
reload(sys)
sys.path.append('../')
from config import *
es = Elasticsearch([{'host':ES_HOST,'port':ES_PORT}])

def topic_mapping():

    mapping_body = {
        "settings":{
        # just one shard, no replicas for testing
            "number_of_shards": 3,
            "number_of_replicas": 1
        },
        "mappings":{
            # "bbs":{
            #     "properties":{
            #         # "id":{"type":"long", "index":"not_analyzed"},                
            #         "content":{"type":"string", "index":"not_analyzed"},               
            #         "comment":{"type":"string", "index":"not_analyzed"},    
            #         "originnal_id":{"type":"string", "index":"not_analyzed"},
            #         "source":{"type":"string", "index":"not_analyzed"},            
            #         "topic":{"type":"string", "index":"not_analyzed"},           
            #         "period_ts":{"type":"long", "index":"not_analyzed"},#用作统计时间段的ts
            #         "publish_time":{"type":"long", "index":"not_analyzed"},           #成立时间
            #         # "regist_address":{"type":"string", "index":"not_analyzed"},     #注册地址
            #         # "province":{"type":"string", "index":"not_analyzed"},           #省
            #         # "city":{"type":"string", "index":"not_analyzed"},               #市
            #         # "district":{"type":"string", "index":"not_analyzed"},           #区
            #         # "down_level":{"type":"string", "index":"not_analyzed"},         #下一层公司
            #         # "up_level":{"type":"string", "index":"not_analyzed"},           #上一层公司
            #     }
            # },
            # "forum":{
            "forum_news":{
                "properties":{
                    "fid":{"type":"string","index":"not_analyzed"},
                    "it":{"type":"long","index":"not_analyzed"},
                    "fin_text":{"type":"long","index":"not_analyzed"},
                    "kv":{"type":"string","index":"not_analyzed"},
                    "em0":{"type":"long","index":"not_analyzed"},
                    "em1":{"type":"long","index":"not_analyzed"},
                    "pid":{"type":"string","index":"not_analyzed"},
                    "ad01":{"type":"long","index":"not_analyzed"},
                    "site_name":{"type":"string","index":"not_analyzed"},
                    "k":{"type":"string","index":"not_analyzed"},
                    "url":{"type":"string","index":"not_analyzed"},
                    "board_name":{"type":"string","index":"not_analyzed"},
                    "emotion":{"type":"long","index":"not_analyzed"},
                    # "content":{"type":"string","index":"not_analyzed"},
                    "content":{"type":"string",},
                    "sentiment":{"type":"float","index":"not_analyzed"},
                    "u":{"type":"string","index":"not_analyzed"},
                    "title":{"type":"string","index":"not_analyzed"},
                    "sent":{"type":"long","index":"not_analyzed"},
                    "ad123":{"type":"long","index":"not_analyzed"},
                    "publish_time":{"type":"integer","index":"not_analyzed"},
                    "last_modify":{"type":"double","index":"not_analyzed"},
                    "comments":{"type":"integer","index":"not_analyzed"},
                    "query_name":{"type":"string","index":"not_analyzed"},
                    # 以下是新增字段
                    "originnal_id":{"type":"string", "index":"not_analyzed"},
                    "source":{"type":"string", "index":"not_analyzed"},
                    # "topic":{"type":"string", "index":"not_analyzed"},
                    "news_id":{"type":"long"}

                }
            },
            
            # "wechat":{
            "weixin_news":{
                "properties":{
                    "abstract":{"type":"string"},
                    "author":{"type":"string", "index":"not_analyzed"},
                    "content":{"type":"string"},
                    "it":{"type":"long", "index":"not_analyzed"},
                    "k":{"type":"string", "index":"not_analyzed"},
                    "publish_time":{"type":"integer", "index":"not_analyzed"},
                    "comment":{"type":"string", "index":"not_analyzed"},
                    "sentiment":{"type":"float", "index":"not_analyzed"},
                    "title":{"type":"string"},
                    "url":{"type":"string", "index":"not_analyzed"},
                    "wxh":{"type":"string", "index":"not_analyzed"},

                    # 以下是新增字段
                    "originnal_id":{"type":"string", "index":"not_analyzed"},
                    "source":{"type":"string", "index":"not_analyzed"},
                    # "topic":{"type":"string", "index":"not_analyzed"},
                    "news_id":{"type":"long"}

                }
            },
            # "bbs":{
            "bbs_news":{
                "properties":{
                    "author":{"type":"string", "index":"not_analyzed"},
                    "board_name":{"type":"string", "index":"not_analyzed"},
                    "comments":{"type":"integer", "index":"not_analyzed"},
                    "content":{"type":"string"},
                    "it":{"type":"long", "index":"not_analyzed"},
                    "k":{"type":"string", "index":"not_analyzed","ignore_above":256},
                    "kv":{"type":"string", "index":"not_analyzed","ignore_above":256},
                    "pid":{"type":"string", "index":"not_analyzed"},
                    "publish_time":{"type":"integer", "index":"not_analyzed"},
                    "sentiment":{"type":"float", "index":"not_analyzed"},
                    "site_name":{"type":"string", "index":"not_analyzed"},
                    "title":{"type":"string"},
                    "u":{"type":"string", "index":"not_analyzed"},

                    # 以下是新增字段
                    "originnal_id":{"type":"string", "index":"not_analyzed"},
                    "source":{"type":"string", "index":"not_analyzed"},
                    # "topic":{"type":"string", "index":"not_analyzed"},
                    "news_id":{"type":"long"}

                }
            },
            # "zhihu":{
            "zhihu_news":{
                "properties":{
                    "zid":{"type":"string", "index":"not_analyzed"},
                    "author":{"type":"string", "index":"not_analyzed"},
                    "board_name":{"type":"string", "index":"not_analyzed"},
                    "comments":{"type":"integer", "index":"not_analyzed"},
                    "content":{"type":"string"},
                    "k":{"type":"string", "index":"not_analyzed"},
                    "publish_time":{"type":"integer", "index":"not_analyzed"},
                    "sentiment":{"type":"float", "index":"not_analyzed"},
                    "site_name":{"type":"string", "index":"not_analyzed"},
                    "title":{"type":"string"},
                    "url":{"type":"string", "index":"not_analyzed"},

                    # 以下是新增字段
                    "originnal_id":{"type":"string", "index":"not_analyzed"},
                    "source":{"type":"string", "index":"not_analyzed"},
                    # "topic":{"type":"string", "index":"not_analyzed"},
                    "news_id":{"type":"long"}
                }
            },
            # "webo":{
            "weibo_news":{
                "properties":{
                    "wid":{"type":"string", "index":"not_analyzed"},
                    "url":{"type":"string", "index":"not_analyzed"},
                    "bp":{"type":"string", "index":"not_analyzed"},
                    "comments":{"type":"integer", "index":"not_analyzed"},
                    "k":{"type":"string", "index":"not_analyzed"},
                    "pics":{"type":"string", "index":"not_analyzed"},
                    "publish_time":{"type":"integer", "index":"not_analyzed"},
                    "sentiment":{"type":"float", "index":"not_analyzed"},
                    "tp":{"type":"string", "index":"not_analyzed"},
                    "user_id":{"type":"string", "index":"not_analyzed"},
                    "usn":{"type":"string", "index":"not_analyzed"},
                    "content":{"type":"string"},
                    "rwid":{"type":"string", "index":"not_analyzed"},
                    "rwpt":{"type":"integer", "index":"not_analyzed"},
                    "rwuid":{"type":"string", "index":"not_analyzed"},
                    "rwwc":{"type":"string", "index":"not_analyzed"},

                    # 以下是新增字段
                    "originnal_id":{"type":"string", "index":"not_analyzed"},
                    "source":{"type":"string", "index":"not_analyzed"},
                    # "topic":{"type":"string", "index":"not_analyzed"},
                    "news_id":{"type":"long"}

                }
            },
        }
    }
    



    
    print ES_HOST,ES_PORT
    if es.indices.exists(index='topic_about'):
        es.indices.delete(index='topic_about')
        print 'an index deleted!'

    es.indices.create(index='topic_about',body=mapping_body,ignore=400)
    print 'new index created!'
    # try:
    #     es.indices.create(index='topic_about',body=mapping_body,ignore=400)
    #     print 'new index created!'
    # except TransportError as e:
    #     # ignore already existing index
    #     if e.error == 'index_already_exists_exception':
    #         pass
    #     else:
    #         raise


if __name__ == '__main__':
    # create_index(index_name='gongshang',mapping_body=gongshang_mapping_v2()) #创建工商数据索引
    topic_mapping()
