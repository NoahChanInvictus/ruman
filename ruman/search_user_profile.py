# -*- coding: UTF-8 -*-
'''
the common function of searching user profile
'''
from elasticsearch.exceptions import NotFoundError
from global_utils import es_user_profile as es


INDEX_NAME = 'weibo_user'
DOC_TYPE = 'user'

# search uname by uid
def search_uid2uname(uid):
    try:
        source = es.get_source(index=INDEX_NAME, doc_type=DOC_TYPE, id=uid)
    except Exception as e:
        # TODO handle exception
        raise e
    uname = source['nick_name']
    # print uname.encode('utf-8')
    return uname

# 自定义查询
def es_get_source(id):
    # return {"name":name, "email":email...}
    try:
        source = es.get_source(index=INDEX_NAME, doc_type=DOC_TYPE, id=id)
    except NotFoundError as e:
        source = {}
    except Exception as e:
        # TODO handle exception
        raise e
    return source

def es_mget_source(ids):
    try:
        source = es.mget(index=INDEX_NAME, doc_type=DOC_TYPE, body={'ids': ids})
    except Exception as e:
        raise e
    source = [item['_source'] for item in source['docs'] if item['found'] is True]
    return source

if __name__ == '__main__':
    uid = '1770831781'
    # search_uid2uname(uid)
    source = es_get_source(uid)
    print source
