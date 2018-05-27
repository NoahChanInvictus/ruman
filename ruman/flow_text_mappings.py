# -*- coding: UTF-8 -*-
'''
use to save text from flow_text --for all people 7day
'''
from elasticsearch import Elasticsearch
from global_utils import es_flow_text as es
#from global_config import weibo_es as es
#from global_utils import es_user_portrait as es

def get_graph_mappings(index_name):
    index_info = {
            'settings':{
                'number_of_shards':5,
                'number_of_replicas':0
            },
            'mappings':{
                'text':{
                    'properties':{
                        'name':{
                            'type': 'string',
                           'index': 'not_analyzed'
                           },
                       
                        'gexf':{
                            'type': 'string',
                            'index': 'no'
                            },
                        'date':{
                            'type':'string',
                            'index': 'not_analyzed'
                            },
                        'window':{
                            'type':'long',
                            'index': 'not_analyzed'
                            }
                        }
                    }
                }
            }
    exist_indice = es.indices.exists(index=index_name)
    print index_name,type(index_name)
    print exist_indice
    if not exist_indice:
        print es.indices.create(index=index_name, body=index_info)


def get_topic_mappings(index_name):
    index_info = {
            'settings':{
                'number_of_shards':5,
                'number_of_replicas':0
            },
            'mappings':{
                'text':{
                    'properties':{
                        'name':{
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'en_name':{
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'submit_user':{
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'start_ts':{
                            'type':'long',
                            },
                        'end_ts':{
                            'type':'long',
                            },
                        'comput_status':{
                            'type':'long'
                            }
                        }
                    }
                }
            }
    exist_indice = es.indices.exists(index=index_name)
    print index_name,type(index_name)
    print exist_indice
    if not exist_indice:
        print es.indices.create(index=index_name, body=index_info)



def get_mappings(index_name):
    index_info = {
            'settings':{
                'analysis':{
                    'analyzer':{
                        'my_analyzer':{
                            'type': 'pattern',
                            'pattern': '&'
                        }
                    }
                }
            },
            'mappings':{
                'text':{
                    'properties':{
                        'text':{
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'mid':{
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'category':{
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'ip':{
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'directed_uid':{
                            'type':'long',
                            },
                        'directed_uname':{
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'sum_retweet':{
                            'type': 'long'
                            },
                        'timestamp':{
                            'type': 'long'
                            },
                        'sentiment': {
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'geo':{
                            'type': 'string',
                            'analyzer': 'my_analyzer'
                            },
                        'keywords_dict':{
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'keywords_string':{
                            'type': 'string',
                            'analyzer': 'my_analyzer'
                            },
                        'sensitive_words_dict':{
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'sensitive_words_string':{
                            'type': 'string',
                            'analyzer': 'my_analyzer'
                            },
                        'message_type':{
                            'type': 'long'
                            },
                        'uid':{
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'root_uid':{
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'root_mid':{
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                         # uncut weibo text
                        'origin_text':{
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'origin_keywords_dict':{
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'origin_keywords_string':{
                            'type': 'string',
                            'analyzer': 'my_analyzer'
                            }
                        }
                    }
                }
            }
    exist_indice = es.indices.exists(index=index_name)
    if not exist_indice:
        es.indices.create(index=index_name, body=index_info, ignore=400)


def get_ads_mappings(index_name):
    index_info = {
            'settings':{
                'analysis':{
                    'analyzer':{
                        'my_analyzer':{
                            'type': 'pattern',
                            'pattern': '&'
                        }
                    }
                }
            },
            'mappings':{
                'text':{
                    'properties':{
                        'text':{
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'mid':{
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'category':{
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'ip':{
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'directed_uid':{
                            'type':'long',
                            },
                        'directed_uname':{
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'sum_retweet':{
                            'type': 'long'
                            },
                        'timestamp':{
                            'type': 'long'
                            },
                        'sentiment': {
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'geo':{
                            'type': 'string',
                            'analyzer': 'my_analyzer'
                            },
                        'keywords_dict':{
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'keywords_string':{
                            'type': 'string',
                            'analyzer': 'my_analyzer'
                            },
                        'sensitive_words_dict':{
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'sensitive_words_string':{
                            'type': 'string',
                            'analyzer': 'my_analyzer'
                            },
                        'message_type':{
                            'type': 'long'
                            },
                        'uid':{
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'root_uid':{
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'root_mid':{
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'ads_keywords':{
                            'type':'string',
                            'analyzer':'my_analyzer'

                            }
                        }
                    }
                }
            }
    exist_indice = es.indices.exists(index=index_name)
    if not exist_indice:
        es.indices.create(index=index_name, body=index_info, ignore=400)

if __name__ == '__main__':
    get_ads_mappings('ads')