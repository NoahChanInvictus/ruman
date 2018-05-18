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

def clustering_mapping():

    mapping_body = {
        "settings":{
        # just one shard, no replicas for testing
            "number_of_shards": 3,
            "number_of_replicas": 1
        },
        "mappings":{
            
            "type1":{
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
                    "news_id":{"type":"long"},
                    "source":{"type":"string", "index":"not_analyzed"},
                    "cluster_id":{"type":"long"},
                    "text_id":{"type":"string", "index":"not_analyzed"},


                }
            },
          
        }
    }
    



    
    print ES_HOST,ES_PORT
    if es.indices.exists(index='clustering'):
        es.indices.delete(index='clustering')
        print 'an index deleted!'

    es.indices.create(index='clustering',body=mapping_body,ignore=400)
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
    clustering_mapping()
