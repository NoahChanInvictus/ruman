# -*- coding: UTF-8 -*-
import os


ALPHABET = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

def base62_encode(num, alphabet=ALPHABET):
    if (num == 0):
        return alphabet[0]
    arr = []
    base = len(alphabet)
    while num:
        rem = num % base
        num = num // base
        arr.append(alphabet[rem])
    arr.reverse()
    return ''.join(arr)


def mid2str(mid):
    mid = str(mid)
    s1 = base62_encode(int(mid[:2]))
    s2 = base62_encode(int(mid[2:9]))
    try:
        s3 = base62_encode(int(mid[9:16]))
    except:
        s3 = ''
    return s1+s2+s3


def weiboinfo2url(uid, _mid):
    mid_str = mid2str(_mid)
    return 'http://weibo.com/{uid}/{mid}'.format(uid=uid, mid=mid_str)
