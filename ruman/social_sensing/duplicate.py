#-*-coding=utf-8-*-

import time
#import Levenshtein

def duplicate(items):
    """
    批量文本去重, 输入的文本可以有部分已经去完重的，以duplicate字段标识
    input:
        items: 一推文本，[{"_id": , "title": , "content": }], 
        文本以utf-8编码
    output:
        更新了duplicate和same_from字段的items， same_from链向相似的新闻的_id
    """

    not_same_items = [item for item in items if 'duplicate' in item and item['duplicate'] == False]
    duplicate_items = [item for item in items if 'duplicate' in item and item['duplicate'] == True]
    candidate_items = [item for item in items if 'duplicate' not in item]

    for item in candidate_items:
        idx, rate, flag = max_same_rate_shingle(not_same_items, item)
        if flag:
            item['duplicate'] = False
            item['same_from'] = item['_id']
            not_same_items.append(item)
        else:
            item['duplicate'] = True
            item['same_from'] = not_same_items[idx]['_id']
            duplicate_items.append(item)

    return not_same_items + duplicate_items


class ShingLing(object):
    def __init__(self, text1, text2, n=3):
        """
        input:
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

        self.jaccard = float(intersection_count) / float(union_count + 1)
        return self.jaccard

    def check_duplicate(self):
        return True if self.jaccard > self.threshold else False 
         

def max_same_rate(items, item):
    #计算item 和 items 的相似度
    reserve = True
    idx = 0
    rate_threshold = 0.8
    max_rate = 0
    for i in items:
        ratio = Levenshtein.ratio(i['text4duplicate'], item['text4duplicate'])
        if ratio >= rate_threshold:
            max_rate = ratio
            reserve = False
            break
        idx += 1

    return idx, max_rate, reserve


def max_same_rate_shingle(items, item, rate_threshold=0.2):
    """
    input:
        items: 已有的不重复数据
        item: 待检测的数据
    output:
        idx: 相似的下标
        max_rate: 相似度
        max_rate: 相似度
    """
    flag = True
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
    items = [{"_id": 1, "title":"", "content":"【台湾是怎样沦为“诈骗之岛”的】1996年，台湾诈骗案为2800起，2008年升至4.1万起，之后逐年下降；而与此同时，2011年以来发生在大陆的诈骗案呈井喷之势，年均增幅达70%，每年损失都在100亿以上。其中，台湾诈骗团伙占20%，诈骗金额占50%。在台湾，每235个人中，就有一个诈骗犯。http://t.cn/RqaSR6P"}, {"_id":2, "title":"", "content":"早啊！新闻来了〔2016.04.17〕】①日本连发地震已致41死 熊本县约9万人疏散避难 ②截至目前全国61条河流发生超警洪水 ③台湾澎湖复兴空难：因台军方航管刁难致49死 ④跨境电商进口新政再松绑：液体奶水果海鲜重返正面清单……更多↓↓↓ http://t.cn/RqS7toK"}, {"_id":3, "title":"", "content":"厄瓜多尔发生7.7级左右地震】中国地震台网自动测定：04月17日07时58分在厄瓜多尔沿岸近海附近（北纬0.46度，西经79.73度）发生7.7级左右地震，最终结果以正式速报为准。据美国地质勘探局地震信息网消息，厄瓜多尔佩德纳莱斯地区发生7.4级地震。 @中国地震台网速报"}, {"_id":4, "title":"", "content":"【日本九州7.3级强震已致32人遇难 尚无中国公民遇险】据日本广播协会等主要日本媒体及相关部门16日最新消息，日本南部九州地区当天凌晨发生的7.3级地震已造成至少32人死亡，伤者超过2000人。截至目前，尚无在日本的中国公民在地震中遇难或受伤的消息。http://t.cn/RqamyTX新华社"}]
    items = [ {"_id":3, "title":"", "content":"人民解放战争"}, {"_id":1, "title":"", "content":"中华人民共和国"}, {"_id":2, "title":"", "content":"中华人民解"}, {"_id":4, "title":"", "content":"中华人民解放"}]
    print duplicate(items)




