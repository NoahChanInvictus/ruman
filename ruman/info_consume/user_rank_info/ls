from elasticsearch import Elasticsearch
from global_utils import es_user_portrait as es
def user_rank_task_mapping():
    index_info = {
        "mappings":{
            "user_rank_task":{
                "properties":{
                    "submit_user":{
                        "type": "string",
                        "index": "not_analyzed"
                    },
                    "submit_time":{
                        "type": "string",
                        "index": "not_analyzed"
                    },
                    "keyword":{
                        "type": "string",
                        "index": "not_analyzed"
                    },
                    "start_time":{
                        "type": "string",
                        "index": "not_analyzed"
                    },
                    "end_time":{
                        "type": "string",
                        "index": "not_analyzed"
                    },
                    "search_type":{
                        "type": "string",
                        "index": "not_analyzed"
                    },
                    "status":{
                        "type": "long",
                        "index": "not_analyzed"
                    },
                    "range":{
                        "type": "string",
                        "index": "not_analyzed"
                    },
                    "user_ts":{
                        "type": "string",
                        "index": "not_analyzed"
                    },
                    "pre":{
                        "type": "string",
                        "index": "not_analyzed"
                    },
                    "during":{
                        "type": "string",
                        "index": "not_analyzed"
                    },
                    "sort_norm":{
                        "type": "string",
                        "index": "not_analyzed"
                    },
                    "sort_scope":{
                        "type": "string",
                        "index": "not_analyzed"
                    },
                    "time":{
                        "type": "string",
                        "index": "not_analyzed"
                    },
                    "isall":{
                        "type": "string",
                        "index": "not_analyzed"
                    },
                    "result":{
                        "type": "string",
                        "index": "no"  
                    }
                }
            }
        }
    }
    return es.indices.create(index="user_rank_keyword_task", body=index_info, ignore=400)

if __name__ == "__main__":
    print user_rank_task_mapping()
