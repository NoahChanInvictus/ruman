#-*-coding: utf-8-*-
from elasticsearch import Elasticsearch

def gonggao_mapping():

    mapping_body = {
        "settings":{
        # just one shard, no replicas for testing
            "number_of_shards": 3,
            "number_of_replicas": 1
        },
        "mappings":{
            "gonggao":{
                "properties":{
                    "stock_id":{"type":"string", "index":"not_analyzed"},                #股票代码
                    "title":{"type":"string", "index":"not_analyzed"},               #公告标题
                    "publish_time":{"type":"string", "index":"not_analyzed"},     #发布时间
                    "url":{"type":"string", "index":"not_analyzed"},           #公告链接
                    "type":{"type":"int", "index":"not_analyzed"},            #公告类型
                    "content":{"type":"string", "index":"not_analyzed"}            #公告内容

                }
            }
        }
    }

def json_mapping():

    mapping_body = {
        "settings":{
        # just one shard, no replicas for testing
            "number_of_shards": 3,
            "number_of_replicas": 1
        },
        "mappings":{
            "dataframe":{
                "properties":{
                    "caonzong_index":{"type":"string", "index":"not_analyzed"},                #股票代码
                    "json":{"type":"string", "index":"not_analyzed"}               #公告标题
                }
            }
        }
    }

def create_index(index_name,mapping_body):

    es = Elasticsearch([{'host':'127.0.0.1','port':9200}])
    es.indices.create(index=index_name,body=mapping_body)


if __name__ == '__main__':
    create_index(index_name='dataframe',mapping_body=json_mapping())