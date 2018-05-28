#-*- coding: utf-8 -*-

import time
import sys
import json
from elasticsearch import Elasticsearch
reload(sys)
sys.path.append('../')
from time_utils import datetime2ts,ts2datetime
from global_utils import es_user_profile, profile_index_name, profile_index_type


def main():
    uid_list = []
    f = open("uid_list_0520.txt")
    for line in f:
        uid_list.append(line.strip())
    f.close()

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

    fw = open("uidlist_20160521.txt", "w")
    with open('user_profile_0521.txt', 'w') as f_txt:
        for uid in uid_list:
            print uid
            try:
                search_results = es_user_profile.get(profile_index_name, uid, doc_type=profile_index_type, params=None)
                if search_results['found']:
                    f_txt.write(json.dumps(search_results['_source'])+"\n")
                else:
                    fw.write("%s\n" % uid)
            except:
                fw.write("%s\n" % uid)


if __name__=="__main__":
    main()
