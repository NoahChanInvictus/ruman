# -*- coding:utf-8 -*-

import redis
import json
import sys
from global_utils import R_RECOMMENTATION_OUT as r_out

def all_delete_uid():
    temp = r_out.hgetall('decide_delete_list')
    keys = r_out.hkeys('decide_delete_list')

    uid_list = []
    if temp:
        for v in temp.values():
            uid_list.extend(json.loads(v))

    return set(uid_list)

if __name__ == "__main__":
    print all_delete_uid()
