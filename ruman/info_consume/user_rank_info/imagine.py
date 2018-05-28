# -*- coding:utf-8 -*-

import sys
import json
import math
from elasticsearch import Elasticsearch
from user_portrait.global_utils import es_user_portrait as es
from user_portrait.global_utils import portrait_index_name, portrait_index_type
from user_portrait.filter_uid import all_delete_uid
from user_portrait.global_utils import R_ADMIN

#use to get evaluate max
def get_evaluate_max():
    max_result = {}
    evaluate_index = ['influence', 'activeness', 'importance']
    for evaluate in evaluate_index:
        query_body = {
            'query':{
                'match_all':{}
                    },
                'size':1,
                'sort':[{evaluate: {'order': 'desc'}}]
                }
        try:
            result = es.search(index=portrait_index_name, doc_type=portrait_index_type, body=query_body)['hits']['hits']
        except Exception, e:
            raise e
        max_evaluate = result[0]['_source'][evaluate]
        max_result[evaluate] = max_evaluate
    return max_result


def imagine(submit_user, uid, query_fields_dict,index_name=portrait_index_name, doctype=portrait_index_type):
    default_setting_dict = query_fields_dict
    print es,portrait_index_name,portrait_index_type,uid
    try :
        personal_info = es.get(index=portrait_index_name, doc_type=portrait_index_type, id=uid, _source=True)['_source']
    except:
        return None
    user_tag = submit_user + "-tag"
    user_tag_string = personal_info.get(user_tag, "")
    if user_tag_string:
        tag_pairs_list = user_tag_string.split('&')
    else:
        tag_pairs_list = []
    tag_dict = dict()
    if tag_pairs_list:
        for item in tag_pairs_list:
            iter_pair = item.split('-')
            tag_dict[iter_pair[0]] = iter_pair[1]

    keys_list = []
    for k, v in query_fields_dict.iteritems():
        if v:
            keys_list.append(k) #需要进行关联的键
    keys_list.remove('size')

    search_dict = {}
    iter_list = []
    tag_attri_vaule = []

    # 对搜索的键值进行过滤，去掉无用的键
    for iter_key in keys_list:
        if iter_key in personal_info:
            if not personal_info[iter_key] or not query_fields_dict[iter_key]:
                query_fields_dict.pop(iter_key)
                continue
            else:
                iter_list.append(iter_key)
                temp = personal_info[iter_key]
                search_dict[iter_key] = temp.split('&')

        else:
            query_fields_dict.pop(iter_key)
            if tag_dict.get(iter_key,''):
                tag_attri_vaule.append(iter_key+"-"+tag_dict[iter_key])
                

    if len(iter_list) == 0 and len(tag_attri_vaule) == 0:
        return []
    query_body = {
        'query':{
            'function_score':{
                'query':{
                    'bool':{
                        'must':[
                            
                        ]
                    }
                }
            }
        }
    }
    number = es.count(index=index_name, doc_type=doctype, body=query_body)['count']

    query_body['size'] = 150 # default number
    query_number = query_fields_dict['size'] #  required number
    query_fields_dict.pop('size')

    if tag_attri_vaule:
        query_body['query']['function_score']['query']['bool']['must'].append({"terms":{user_tag:tag_attri_vaule}})

    for (k,v) in query_fields_dict.items():

        temp = {}
        temp_list = []
        if k in personal_info and v != 0:
            for iter_key in search_dict[k]:
                temp_list.append({'wildcard':{k:{'wildcard':'*'+iter_key+'*', 'boost': v}}})

            query_body['query']['function_score']['query']['bool']['must'].append({'bool':{'should':temp_list}})

    filter_uid = all_delete_uid()
    result = es.search(index=index_name, doc_type=doctype, body=query_body)['hits']['hits']
    field_list = ['uid','uname', 'activeness','importance', 'influence']
    evaluate_index_list = ['activeness', 'importance', 'influence']
    result_list = []

    count = 0

    if len(result) > 1 and result:
        if result[0]['_id'] != uid:
            top_score = result[0]['_score']
        else:
            top_score = result[1]['_score']

    #get evaluate max to normal
    evaluate_max_dict = get_evaluate_max()
    for item in result:
        return_dict = {}
        if uid == item['_id'] or uid in filter_uid:
            score = item['_score']
            continue
        for field in field_list:
            if field == 'uid':
                uid = item['_source'][field]
                normal_value = uid
                return_dict['uid'] = uid
            elif field in evaluate_index_list:
                value = item['_source'][field]
                normal_value = math.log(value / float(evaluate_max_dict[field] )* 9 + 1, 10) * 100
                return_dict[field] = normal_value
            else:
                normal_value = item['_source'][field]
                return_dict[field] = normal_value
                return_dict['similiar'] = item['_score']/float(top_score)*100
        result_list.append(return_dict)
        count += 1

        if count == query_number:
            break

    #return result_list
    temp_list = []
    for field in field_list:
        if field in evaluate_index_list:
            value = personal_info[field]
            normal_value = math.log(value / float(evaluate_max_dict[field]) * 9 + 1, 10) * 100
        else:
            normal_value = personal_info[field]
        temp_list.append(normal_value)

    results = []
    results.append(temp_list)
    results.extend(result_list)
    return results

if __name__ == '__main__':
    print imagine(2010832710, {'topic':1, 'keywords':2,'field':'default','size':11}, index_name='test_user_portrait', doctype='user')

