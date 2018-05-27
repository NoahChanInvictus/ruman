# -*- coding:utf-8 -*-

import json
import sys
reload(sys)
sys.path.append('./../')
from global_utils import R_SOCIAL_SENSING as r

sensing_words = ["民主", "法治", "宪政", "维权", "上访", "强拆", "政府", "歹徒", "腐败", "暴恐", "爆炸", "袭击", "地震", "坠亡","不雅", "火灾", "车祸", "中毒", "抢劫", "强奸", "死亡", "雾霾", "污染"]
r.hset("sensing_words", "sensing_words", json.dumps(sensing_words))

sensitive_words = ["宪政", "暴恐", "维权", "强拆"]
r.hset("sensitive_words", "sensitive_words", json.dumps(sensitive_words))

