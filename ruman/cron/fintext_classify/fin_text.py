# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.path.append('../../')
from config import *

from tgrocery import Grocery
STOP_WORDS_FILE = 'stopwords.txt'
USER_DICT_FILE = 'user_dict.txt'

model_fintext = Grocery('model_fintext')
model_fintext.load()
sys.path.append('../')
from get_es import *
es = Elasticsearch([{'host':ES_HOST,'port':ES_PORT}])

def search(index_name):
    es_search_options = set_search_optional()
    es_result = get_search_result(es_search_options,index=index_name)
    # final_result = get_result_list(es_result)
    # return final_result
    return es_result


def get_result_list(es_result):
    final_result = []
    for item in es_result:
        final_result.append(item['_source'])
    return final_result


def get_search_result(es_search_options, index,scroll='25m', doc_type='type1', timeout="500m"):
# def get_search_result(es_search_options, scroll='5m', index=INDEX_GONGSHANG, timeout="1m"):
    # elasticsearch.helpers.scan(client, query=None, scroll='5m', preserve_order=False, **kwargs)
    es_result = helpers.scan(
        client=es,
        query=es_search_options,
        scroll=scroll,
        index=index,
        doc_type=doc_type,
        # timeout=timeout
    )
    return es_result


def set_search_optional():
    # 检索选项
    # es_search_options = {
        
    #         "match_all": {}
        
    # }
    es_search_options = {"match": {"comments": 0}}
    # es_search_options = {"query":{ "bool": {
    #     # "must":{"term":{"ad01":1}},
    #     ##########
    #     # 改动版本，用于更新之前错分的
    #     # "should":[{"term":{"ad01":1}},{"term":{"ad01":0}}],
    #     # "minimum_should_match":1,
    #     ##########
    #     "filter":{"range":{"publish_time":{"gte": start_time,"lte": end_time}}}
    # }}}
    return es_search_options

def main_relabel():     #用于把之前的结果重新标注
    global start_time,end_time
    start_day = '2015-11-30'
    end_day = '2018-03-29'

    start_time = time.mktime(time.strptime(str(start_day)+' 00:00:00', '%Y-%m-%d %H:%M:%S'))
    end_time = time.mktime(time.strptime(str(end_day)+' 23:59:59', '%Y-%m-%d %H:%M:%S'))



    
    for index in TOPIC_ABOUT_DOCTYPE:
        ACTIONS = []
        count = 0
        ad_result = search(index)
        for item in ad_result:
            doc_id = item['_id']
            # ad_content = item['_source']['content'].encode('utf-8')
            # entity_name = item['_source']['query_name'].replace('\n','').encode('utf-8')
            # ad01 = item['_source']['ad01'] if item['_source'].has_key('ad01') else 0
            fintext = int(model_fintext.predict(item['_source']['content']).predicted_y)
            
            action = { 
                    "_op_type":"update" ,
                    "_index":index,  
                    "_type":'type1',
                    "_id":doc_id,  
                    "doc":{"fintext":fintext,
                           
                    }
                }
            ACTIONS.append(action)
            
            count += 1
            if count % 1000 == 0:
                # success, _ = bulk(es, ACTIONS, raise_on_error=True, request_timeout=400)
                ACTIONS = []
                print 'in',index,count,'has been updated!'
        # 最后把余下的也bulk进去
        if ACTIONS != []:
            # success, _ = bulk(es, ACTIONS, raise_on_error=True, request_timeout=400)
            ACTIONS = []

def fin_classify(content):
    # model_fintext = Grocery('model_fintext')
    # model_fintext.load()
    ad01 = int(model_fintext.predict(content).predicted_y)
    return ad01

if __name__ == '__main__':
    print fin_classify(u'今天天气真好呀')
    print fin_classify(u'老师留了好多作业') 
    # main_relabel()



