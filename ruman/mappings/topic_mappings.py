# -*- coding: utf-8 -*-
# 创建索引
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import TransportError
from elasticsearch.helpers import bulk, streaming_bulk
import sys
reload(sys)
sys.path.append('../')
from config import *

def topic_mapping():

    mapping_body = {
        "settings":{
        # just one shard, no replicas for testing
            "number_of_shards": 3,
            "number_of_replicas": 1
        },
        "mappings":{
            "message":{
                "properties":{
                    # "id":{"type":"long", "index":"not_analyzed"},                
                    "content":{"type":"string", "index":"not_analyzed"},               
                    "comment":{"type":"string", "index":"not_analyzed"},    
                    "originnal_id":{"type":"string", "index":"not_analyzed"},
                    "source":{"type":"string", "index":"not_analyzed"},            
                    "topic":{"type":"string", "index":"not_analyzed"},           
                    "period_ts":{"type":"long", "index":"not_analyzed"},#用作统计时间段的ts
                    "publish_time":{"type":"long", "index":"not_analyzed"},           #成立时间
                    # "regist_address":{"type":"string", "index":"not_analyzed"},     #注册地址
                    # "province":{"type":"string", "index":"not_analyzed"},           #省
                    # "city":{"type":"string", "index":"not_analyzed"},               #市
                    # "district":{"type":"string", "index":"not_analyzed"},           #区
                    # "down_level":{"type":"string", "index":"not_analyzed"},         #下一层公司
                    # "up_level":{"type":"string", "index":"not_analyzed"},           #上一层公司
                }
            },


        }
    }



    es = Elasticsearch([{'host':ES_HOST,'port':ES_PORT}])
    if es.indices.exists(index='topic_about'):
        es.indices.delete(index='topic_about')
        print 'an index deleted!'

    try:
        es.indices.create(index='topic_about',body=mapping_body,ignore=400)
    except TransportError as e:
        # ignore already existing index
        if e.error == 'index_already_exists_exception':
            pass
        else:
            raise


if __name__ == '__main__':
    # create_index(index_name='gongshang',mapping_body=gongshang_mapping_v2()) #创建工商数据索引
    topic_mapping()
