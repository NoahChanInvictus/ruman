# -*-coding:utf-8-*-

import time
import sys
import json
from elasticsearch import Elasticsearch
reload(sys)
sys.path.append('../')
from time_utils import datetime2ts,ts2datetime
from global_utils import es_flow_text


def main():
    uid_list = []
    count = 0
    with open('uid_list_0520.txt', 'rb') as f:
        for item in f:
            uid_list.append(item.strip())
    print "uid_list: ", len(uid_list)
    print uid_list[:3]

    query_body = {
        "query":{
            "filtered":{
                "filter":{
                    "terms":{"uid":uid_list}
                }
            }
        },
        "size":100000
    }


    with open('uid_text_0523.txt', 'wb') as f_txt:
        #ts = datetime2ts(ts2datetime(time.time()-24*3600))
        ts = datetime2ts(ts2datetime(time.time())) #today
        while 1:
            date = ts2datetime(ts)
            index_name = "flow_text_"+str(date)
            print index_name
            exist_bool = es_flow_text.indices.exists(index=index_name)
            if not exist_bool:
                break
            search_results = es_flow_text.search(index=index_name, doc_type="text", body=query_body)["hits"]["hits"]
            print len(search_results)
            if search_results:
                for item in search_results:
                    f_txt.write(json.dumps(item['_source'])+"\n")
                    count += 1
            ts = ts-24*3600
            break
    print count


if __name__ == "__main__":
    main()
