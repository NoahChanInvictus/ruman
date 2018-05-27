# -*- coding:utf-8 -*-
import math

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def aggregation(item_list, item_dict):
    for item in item_list:
        try:
            item_dict[item] += 1
        except:
            item_dict[item] = 1
    return item_dict


def proportion(item_dict):
    results = dict()
    total = sum(item_dict.values())
    for k,v in item_dict.iteritems():
        results[k] = v/(total*1.0)
    return results

def filter_mid(mid_dict): # weibo retweeted detail or comment detail
    mid_list = []
    for k,v in mid_dict.iteritems():
        if int(v) > 0:
            mid_list.append(k)
    return mid_list


def level(item_list): # mean and standard deviation
    mean = 0
    std_var = 0
    if len(item_list):
        n = len(item_list)
        total = sum(item_list)
        mean = total/(n*1.0)
        squre_list = [item**2 for item in item_list]
        std_var = math.sqrt(sum(squre_list)/(n*1.0) - mean**2)

    result = [mean, std_var]
    return result


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

def base62_decode(string, alphabet=ALPHABET):
    base = len(alphabet)
    strlen = len(string)
    num = 0

    idx = 0
    for char in string:
        power = (strlen - (idx + 1))
        num += alphabet.index(char) * (base ** power)
        idx += 1
    return num

def mid2str(mid):
    mid = str(mid)
    s1 = base62_encode(int(mid[:2]))
    s2 = base62_encode(int(mid[2:9]))
    s3 = base62_encode(int(mid[9:16]))

    return s1+s2+s3

def weiboinfo2url(uid, _mid):
    mid_str =  mid2str(_mid)
    return "http://weibo.com/{uid}/{mid}".format(uid=uid, mid=mid_str)



if __name__ == "__main__":
    print proportion({"a": 34, "v": 56, "c":77})
    print level([])
    print weiboinfo2url('1698222553','3618588323310231')
