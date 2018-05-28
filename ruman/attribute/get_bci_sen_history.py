# -*-coding:utf-8-*-

import time
import json
import sys

reload(sys)
sys.path.append('./../')
from global_utils import es_user_profile, es_user_portrait

def main():
    uid_list = []
    with open("uid_list_0520.txt", 'rb') as f:
        for item in f:
            uid_list.append(item.strip())

    bci_results = es_user_profile.mget(index="bci_history", doc_type="bci", body={"ids":uid_list})["docs"]
    sen_results = es_user_profile.mget(index="sensitive_history", doc_type="sensitive", body={"ids":uid_list})["docs"]

    with open("bci_history.txt", 'wb') as f_bci:
        for item in bci_results:
            if item['found']:
                f_bci.write(json.dumps(item['_source'])+"\n")

    with open("sen_history.txt", "wb") as f_sen:
        for item in sen_results:
            if item['found']:
                f_sen.write(json.dumps(item['_source'])+"\n")

def get_bci_detail():
    uid_list = []
    with open("uid_list_0520.txt", 'rb') as f:
        for item in f:
            uid_list.append(item.strip())
    
    print uid_list
    index_name = "bci_20160522"
    bci_results = es_user_portrait.mget(index=index_name, doc_type="bci", body={"ids":uid_list})["docs"]
    with open("bci_detail_0522.txt", "wb") as f:
       for item in bci_results:
           if item["found"]:
               f.write(json.dumps(item["_source"])+"\n")

if __name__ == "__main__":
    #main()
    get_bci_detail()
 
