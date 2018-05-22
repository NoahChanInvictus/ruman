#-*-coding=utf-8-*-
# User: linhaobuaa
# Date: 2014-12-28 17:00:00
# Version: 0.3.0
# Modified by Noah

import time

def duplicate(items):
    """批量文本去重, 输入的文本可以有部分已经去完重的，以duplicate字段标识
       input:
           items: 一推文本，[{"_id": , "title": , "content": }], 
           文本以utf-8编码
       output:
           更新了duplicate和same_from字段的items， same_from链向相似的新闻的_id
    """
    not_same_items = [item for item in items if 'duplicate' in item and item['duplicate'] == False]
    duplicate_items = [item for item in items if 'duplicate' in item and item['duplicate'] == True]
    candidate_items = [item for item in items if 'duplicate' not in item]
    # dup_id = 0
    for item in candidate_items:
        # item['_id'] = dup_id
        # dup_id += 1
        if not item.has_key('title'):
            item['title'] = 'empty'.encode('utf-8')
        else:
            item['title'] = item['title'].encode('utf-8')
        item['content'] = item['content'].encode('utf-8')
        idx, rate, flag = max_same_rate_shingle(not_same_items, item)
        if flag:
            item['duplicate'] = False
            # item['same_from'] = item['_id']
            item['same_count'] = 0
            not_same_items.append(item)
        else:
            item['duplicate'] = True
            # item['same_from'] = not_same_items[idx]['_id']
            not_same_items[idx]['same_count'] += 1
            duplicate_items.append(item)

    # return not_same_items + duplicate_items
    return not_same_items

class ShingLing(object):
    """shingle算法
    """
    def __init__(self, text1, text2, n=3):
        """input
               text1: 输入文本1, unicode编码
               text2: 输入文本2, unicode编码
               n: 切片长度
        """
        if not isinstance(text1, unicode):
            raise ValueError("text1 must be unicode")

        if not isinstance(text2, unicode):
            raise ValueError("text2 must be unicode")

        self.n = n
        self.threshold = 0.2
        self.text1 = text1
        self.text2 = text2
        self.set1 = set()
        self.set2 = set()
        self._split(self.text1, self.set1)
        self._split(self.text2, self.set2)
        self.jaccard = 0

    def _split(self, text, s):
        if len(self.text1) < self.n:
            self.n = 1

        for i in range(len(text) - self.n + 1):
            piece = text[i: i + self.n]
            s.add(piece)

    def cal_jaccard(self):
        intersection_count = len(self.set1 & self.set2)
        union_count = len(self.set1 | self.set2)

        self.jaccard = float(intersection_count) / float(union_count)
        return self.jaccard

    def check_duplicate(self):
        return True if self.jaccard > self.threshold else False

def max_same_rate_shingle(items, item, rate_threshold=0.3):
    """input:
           items: 已有的不重复数据
           item: 待检测的数据
       output:
           idx: 相似的下标
           max_rate: 相似度
           flag: True表示不相似
    """
    flag = True
    idx = 0
    max_rate = 0
    # for i in items:
    #     # print (i['title']).decode('utf-8'),'\n',(item['title']).decode('utf-8')
    #     # sl = ShingLing((i['title']).decode('utf-8'), (item['title']).decode('utf-8'), n=3)
    #     # sl.cal_jaccard()
    #     # if sl.jaccard >= rate_threshold:
    #     #     max_rate = sl.jaccard
    #     #     flag = False            #False表示相似
    #     #     break

    #     idx += 1

    if flag == True:                #如果上一步没有找到相似的
        idx = 0
        max_rate = 0
        for i in items:
            sl = ShingLing((i['title'] + i['content']).decode('utf-8'), (item['title'] + item['content']).decode('utf-8'), n=3)
            sl.cal_jaccard()
            if sl.jaccard >= rate_threshold:
                max_rate = sl.jaccard
                flag = False
                break
            idx += 1

    return idx, max_rate, flag


if __name__ == '__main__':
    text1 = u"中国中央电视台"
    text2 = u"中央电视台广播"
    s = ShingLing(text1, text2, 3)
    print s.cal_jaccard()
    print s.check_duplicate()