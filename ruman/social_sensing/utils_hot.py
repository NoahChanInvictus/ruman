# -*-coding:utf-8-*-

import json
import redis
from elasticsearch import Elasticsearch

r = redis.StrictRedis(host='219.224.134.212', port='6670', db=14)
es = Elasticsearch("219.224.134.216:9201", timeout=600)

index_list = ["flow_text_2016-11-26", "flow_text_2016-11-25", "flow_text_2016-11-24", "flow_text_2016-11-23"]

def get_recommend(uid):
    sensing_text = es.get(index="social_sensing_task", doc_type="-media",id=1480176000)["_source"]
    sensing_retweet_dict = dict()
    sensing_comment_dict = dict()
    origin_weibo_detail = json.loads(sensing_text["origin_weibo_detail"])
    retweeted_weibo_detail = json.loads(sensing_text["retweeted_weibo_detail"])
    for k,v in origin_weibo_detail.iteritems():
        sensing_retweet_dict[k] = v["retweeted"]
        sensing_comment_dict[k] = v["comment"]
    for k,v in retweeted_weibo_detail.iteritems():
        sensing_retweet_dict[k] = v["retweeted"]
        sensing_comment_dict[k] = v["comment"]



    # popularity recommend
    popular_dict = r.hgetall("event_prediction")
    sorted_popular_dict = sorted(popular_dict.iteritems(), key=lambda x:x[1], reverse=True)
    popular_mid_list = []
    popular_text_list = []
    for k,v in sorted_popular_dict[:5]:
        popular_mid_list.append(k)
    popular_results = es.search(index=index_list, doc_type="text", body={"query":{"terms":{"mid":popular_mid_list}}})["hits"]["hits"]
    for item in popular_results:
        tmp = dict()
        mid = item["_source"]["mid"]
        tmp["mid"] = mid
        tmp["text"] = item["_source"]["text"]
        tmp["timestamp"] = item["_source"]["timestamp"]
        uuid = item["_source"]["uid"]
        try:
            person_detail = es.get(index="weibo_user", doc_type="user", id=uuid)["_source"]
            uname = person_detail["nick_name"]
            if uname:
                tmp["uname"] = uname
            else:
                tmp["uname"] = uuid
            tmp["photo_url"] = person_detail["photo_url"]
        except:
            tmp["uname"] = uuid
            tmp["photo_url"] = ""
        tmp["retweeted"] = sensing_retweet_dict.get(mid, 0)
        tmp["comment"] = sensing_comment_dict.get(mid, 0)
        tmp["popular"] = popular_dict[mid]
        popular_text_list.append(tmp)
    popular_text_list = sorted(popular_text_list, key=lambda x:x["popular"], reverse=True)



    # fans recommend
    fans_dict = r.hgetall("recommend_fans_"+str(uid))
    fans_join_dict = dict()
    total_join_dict = dict()
    for k,v in fans_dict.iteritems():
        v_list = v.split("_")
        fans_join_dict[k] = v_list[0]
        total_join_dict[k] = v_list[1]
    fans_dict  = fans_join_dict
    sorted_fans_dict = sorted(fans_dict.iteritems(), key=lambda x:x[1], reverse=True)
    fans_mid_list = []
    fans_text_list = []
    for k,v in sorted_fans_dict[:5]:
        fans_mid_list.append(k)
    fans_results = es.search(index=index_list, doc_type="text", body={"query":{"terms":{"mid":fans_mid_list}}})["hits"]["hits"]
    for item in fans_results:
        tmp = dict()
        mid = item["_source"]["mid"]
        tmp["mid"] = mid
        tmp["text"] = item["_source"]["text"]
        tmp["timestamp"] = item["_source"]["timestamp"]
        uuid = item["_source"]["uid"]
        try:
            person_detail = es.get(index="weibo_user", doc_type="user", id=uuid)["_source"]
            uname = person_detail["nick_name"]
            if uname:
                tmp["uname"] = uname
            else:
                tmp["uname"] = uuid
            tmp["photo_url"] = person_detail["photo_url"]
        except:
            tmp["uname"] = uuid
            tmp["photo_url"] = ""
        tmp["retweeted"] = sensing_retweet_dict.get(mid, 0)
        tmp["comment"] = sensing_comment_dict.get(mid, 0)
        tmp["fans"] = fans_dict[mid]
        tmp["total_user"] = total_join_dict[mid]
        fans_text_list.append(tmp)
    fans_text_list = sorted(fans_text_list, key=lambda x:x["fans"], reverse=True)

    # text similarity
    text_recommend_dict = r.hgetall(uid)
    keys_list = text_recommend_dict.keys()
    text_mid_dict = dict()
    for item in keys_list:
        item_list = item.split("_")
        text_mid_dict[item_list[0]] = float(item_list[1])
    sorted_text_dict = sorted(text_mid_dict.iteritems(), key=lambda x:x[1], reverse=True)
    text_mid_list = []
    text_recommend_list = []
    for k,v in sorted_text_dict[:5]:
        text_mid_list.append(k)

    text_results = es.search(index=index_list, doc_type="text", body={"query":{"terms":{"mid":text_mid_list}}})["hits"]["hits"]
    for item in text_results:
        tmp = dict()
        mid = item["_source"]["mid"]
        tmp["mid"] = mid
        tmp["text"] = item["_source"]["text"]
        tmp["timestamp"] = item["_source"]["timestamp"]
        uid = item["_source"]["uid"]
        try:
            person_detail = es.get(index="weibo_user", doc_type="user", id=uid)["_source"]
            uname = person_detail["nick_name"]
            if uname:
                tmp["uname"] = uname
            else:
                tmp["uname"] = uid
            tmp["photo_url"] = person_detail["photo_url"]
            
        except:
            tmp["uname"] = uid
            tmp["photo_url"] = ""
        tmp["retweeted"] = sensing_retweet_dict.get(mid, 0)
        tmp["comment"] = sensing_comment_dict.get(mid, 0)
        for kk, vv in text_recommend_dict.iteritems():
            if mid in kk:
                ttmp = json.loads(vv)
                tmp["self_keywords"] = ttmp[0]
                tmp["keywords"] = ttmp[1]
        tmp["similarity"] = text_mid_dict[mid]
        text_recommend_list.append(tmp)
    text_recommend_list = sorted(text_recommend_list, key=lambda x:x["similarity"], reverse=True)

    return json.dumps([text_recommend_list, fans_text_list, popular_text_list])


if __name__ == "__main__":
    print get_recommend("3069348215")


