  # -*- coding: utf-8 -*-

from numpy import *
import numpy as np
import random
import string  
import csv
import re
import jieba
import jieba.posseg as pseg
import jieba.analyse
import math
from collections import defaultdict
from tgrocery import Grocery
STOP_WORDS_FILE = 'stopwords.txt'
USER_DICT_FILE = 'user_dict.txt'

   

def test_grocery():
    grocery = Grocery('model_redian')
    grocery.train('trdata_4.txt')
    grocery.save()
    new_grocery = Grocery('model_redian')
    new_grocery.load()
    test_result = new_grocery.test('tedata_4.txt')
    print test_result.accuracy_labels
    print test_result.recall_labels
    test_result.show_result()

if __name__ == '__main__':
    
    test_grocery()


