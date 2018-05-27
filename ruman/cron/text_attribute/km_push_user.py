# -*-coding:utf-8-*-

import redis
import json

r = redis.StrictRedis(host="219.224.134.213", port="7381", db=10)

r.lpush("user_portrait_task", json.dumps(["task1", "1483411979", ["1904264611","1657470871"]]))
#k = r.lpop("user_portrait_task")
#print json.loads(k)
