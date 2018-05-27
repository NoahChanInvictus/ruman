# -*- coding:utf-8 -*-

import sys
import json
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
reload(sys)
sys.path.append("./../")
from global_utils import es_user_portrait as es

def mappings_sensing_task(task_name):
    index_info = {
        "mappings":{
            task_name:{
                "properties":{
                    "origin_weibo_number":{
                        "type": "long",
                        "index": "no"
                    },
                    "retweeted_weibo_number":{
                        "type": "long",
                        "index": "no"
                    },
                    "comment_weibo_number":{
                        "type": "long",
                        "index": "no"
                    },
                    "weibo_total_number":{
                        "type": "long",
                        "index": "no"
                    },
                    "sensitive_origin_weibo_number":{
                        "type": "long",
                        "index": "no"
                    },
                    "sensitive_retweeted_weibo_number":{
                        "type": "long",
                        "index": "no"
                    },
                    "sensitive_comment_weibo_number":{
                        "type": "long",
                        "index": "no"
                    },
                    "sensitive_weibo_total_number":{
                        "type": "long",
                        "index": "no"
                    },
                    "sentiment_distribution":{
                        "type": "string",
                        "index": "no"
                    },
                    "important_users":{
                        "type": "string",
                        "index": "no"
                    },
                    "timestamp":{
                        "type": "long",
                    },
                    "burst_reason":{
                        "type": "string",
                        "index": "not_analyzed"
                    },
                    "geo":{
                        "type": "string",
                        "index": "no"
                    },
                    "clustering_topic":{
                        "type": "string",
                        "index": "no"
                    },
                    "user":{
                        "type": "string",
                        "index": "not_analyzed"
                    }
                }
            }
        }
    }

    es.indices.create(index="social_sensing_task", body=index_info, ignore=400)

    return "1"

def manage_sensing_task():
    index_info = {
        "mappings":{
            "task":{
                "properties":{
                    "task_name":{
                        "type": "string",
                        "index": "not_analyzed"
                    },
                    "task_type":{
                        "type": "string",
                        "index": "not_analyzed"
                    },
                    "create_by":{
                        "type": "string",
                        "index": "not_analyzed"
                    }, # 任务创建者
                    "new":{
                        "type": "long"
                    },
                    "last_time":{
                        "type": "string",
                        "index": "not_analyzed"
                    },
                    "processing_status":{
                        "type": "string",
                        "index": "not_analyzed"
                    },
                    "stop_time":{
                        "type": "string",
                        "index": "not_analyzed"
                    },
                    "remark":{
                        "type": "string",
                        "index": "not_analyzed"
                    },
                    "social_sensors":{
                        "type": "string",
                        "index": "not_analyzed"
                    },
                    "keywords":{
                        "type": "string",
                        "index": "not_analyzed"
                    },
                    "sensitive_words":{
                        "type": "string",
                        "index": "not_analyzed"
                    },
                    "history_status":{
                        "type": "string",
                        "index": "not_analyzed"
                    },
                    "create_at":{
                        "type": "string",
                        "index": "not_analyzed"
                    },
                    "warning_status":{
                        "type": "string",
                        "index": "not_analyzed"
                    },
                    "finish":{
                        "type": "string",
                        "index": "not_analyzed"
                    },
                    "burst_reason":{
                        "type": "string",
                        "index": "not_analyzed"
                    },
                    "user":{
                        "type": "string",
                        "index": "not_analyzed"
                    }
                }
            }
        }
    }

    es.indices.create(index="manage_sensing_task", body=index_info, ignore=400)

if __name__ == "__main__":
    manage_sensing_task()
    #es.indices.create(index="social_sensing_task", ignore=400)


