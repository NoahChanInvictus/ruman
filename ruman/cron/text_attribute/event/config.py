# -*- coding: utf-8 -*-

import os
import os
import re
import csv
import sys
sys.path.append('../../../')
from parameter import EVENT_ABS_PATH as abs_path

def load_word(name):

    word_weight = dict()
    total_weight = 0
    reader = csv.reader(file(abs_path + '/word/%s_word.csv' % name, 'rb'))
    for word,weight in reader:
        word_weight[word] = int(weight)
        total_weight = total_weight + int(weight)

    return word_weight,total_weight

RANK_AVARAGE = 0.05
RANK_WEIGHT = 2.7
WORD_NAME = 'political'

WORD_WEIGHT,TOTAL_WEIGHT = load_word(WORD_NAME)

