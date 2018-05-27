# -*- coding: UTF-8 -*-
'''
use to scan the user_portrait uid, activeness_history and influence_history to redis
for 
'''
import sys
import time
import json
from elasticsearch.helpers import scan

reload(sys)
sys.path.append('../../')
from global_utils import es_user_portrait, portrait_index_name, portrait_index_type
from global_utils import update_day_redis, UPDATE_DAY_REDIS_KEY
from global_utils import update_week_redis, UPDATE_WEEK_REDIS_KEY, UPDATE_MONTH_REDIS_KEY
from global_utils import update_month_redis, UPDATE_MONTH_REDIS_KEY

#scan es to redis as a queue for update day
#write in version: 15-12-08
#order time task for every day
#data in redis: [{'uid':uid, 'activity_geo_dict':json.dumps([activity_geo_dict])}, {'uid':uid, 'activity_geo_dict':...}]
def scan_es2redis():
    count = 0
    s_re = scan(es_user_portrait, query={'query':{'match_all':{}}, 'size':1000}, index=portrait_index_name, doc_type=portrait_index_type)
    start_ts = time.time()
    user_list = []
    user_info = {}
    while True:
        try:
            scan_re = s_re.next()['_source']
            count += 1
            uid = scan_re['uid']
            user_info[uid] = {'activity_geo_dict':scan_re['activity_geo_dict']}
            update_day_redis.lpush(UPDATE_DAY_REDIS_KEY, json.dumps(user_info))
            user_info = {}
            if count % 1000==0 and count!=0:
                end_ts = time.time()
                print '%s sec count 1000' % (end_ts - start_ts)
                start_ts = end_ts
        except StopIteration:
            print 'all done'
            if user_info:
                update_day_redis.lpush(UPDATE_DAY_REDIS_KEY, json.dumps(user_info))
                user_info = {}
            break
        except Exception, r:
            raise r
            break
    
    if user_info:
        update_day_redis.lpush(UPDATE_DAY_REDIS_KEY, json.dumps(user_info))

    print 'count:', count


#scan es to redis as a queue for update_week
#write in version: 15-12-08
#order time task for every week
def scan_es2redis_week():
    count = 0
    s_re = scan(es_user_portrait, query={'query':{'match_all': {}}, 'size':1000}, index=portrait_index_name, doc_type=portrait_index_type)
    user_info = {}
    start_ts = time.time()
    while True:
        try:
            scan_re = s_re.next()['_source']
            count += 1
            uid = scan_re['uid']
            user_info[uid] = {'fansnum':scan_re['fansnum'], 'domain':scan_re['domain']}
            update_week_redis.lpush(UPDATE_WEEK_REDIS_KEY, json.dumps(user_info))
            user_info = {}
            if count % 1000 == 0 and count != 0:
                end_ts = time.time()
                print '%s sec count 1000' % (end_ts - start_ts)
                start_ts = end_ts
        except StopIteration:
            print 'all done'
            if user_info:
                update_week_redis.lpush(UPDATE_WEEK_REDIS_KEY, json.dumps(user_info))
                user_info = {}
            break
        except Exception, r:
            raise r
            break

    if user_info:
        update_week_redis.lpush(UPDATE_WEEK_REDIS_KEY, json.dumps(user_info))
    print 'count:', count

#scan es to redis as queue for update month
#write in version: 16-02-27
#order time task for every month
def scan_es2redis_month():
    count = 0
    s_re = scan(es_user_portrait, query={'query':{'match_all': {}}, 'size':1000}, index=portrait_index_name, doc_type=portrait_index_type)
    start_ts = time.time()
    user_info = {}
    while True:
        try:
            scan_re = s_re.next()['_source']
            count += 1
            uid = scan_re['uid']
            user_info[uid] = {'fansnum':scan_re['fansnum'], 'topic_string':scan_re['topic_string']}
            update_month_redis.lpush(UPDATE_MONTH_REDIS_KEY, json.dumps(user_info))
            user_info = {}
            if count % 1000 == 0 and count != 0:
                end_ts = time.time()
                print '%s sec count 1000' % (end_ts - start_ts)
                start_ts = end_ts
        except StopIteration:
            print 'all done'
            if user_info:
                update_month_redis.lpush(UPDATE_MONTH_REDIS_KEY, json.dumps(user_info))
                user_info = {}
            break
        except Exception, r:
            raise r
            break
    if user_info:
        update_month_redis.lpush(UPDATE_MONTH_REDIS_KEY, json.dumps(user_info))
    print 'count:', count

if __name__=='__main__':
    scan_es2redis()
