# -*- coding: utf-8 -*-

import csv
import os
import sys
import time

reload(sys)
sys.path.append('./../flow1/')
from csv2json import itemLine2Dict, csv2bin
sys.setdefaultencoding('utf-8')

CSV_FILE_PATH = '/home/ubuntu8/data1309/20130901'
uid_csv_path = './../recommentation_in/'
uid_csv = 'recommentation_list.csv'

count_n = 0
tb = time.time()
uid_set = set()
with open (os.path.join(uid_csv_path, uid_csv), 'rb') as t:
    for line in t:
        uid = line.strip().split(',')[0]
        uid_set.add(uid)
        count_n += 1
        if count_n == 100:
            break
uid_text = file('uid_text.csv', 'wb')
writer = csv.writer(uid_text)
count = 0
count_f = 0

file_list = set(os.listdir(CSV_FILE_PATH))
print "total file is ", len(file_list)

for each in file_list:
    with open(os.path.join(CSV_FILE_PATH, each), 'rb') as f:
        try:
            for line in f:
                count_f += 1
                weibo_item = itemLine2Dict(line)
                if weibo_item:
                    weibo_item_bin = csv2bin(weibo_item)
                    if int(weibo_item_bin['sp_type']) != 1:
                        continue
                    if not str(weibo_item_bin['uid']) in uid_set:
                        continue
                    text = weibo_item_bin['text']
                    if weibo_item_bin['message_type'] == 1:
                        write_text = text
                    elif weibo_item_bin['message_type'] == 2:
                        temp = text.split('//@')[0].split(':')[1:]
                        write_text = ''.join(temp)
                    else:
                        continue
                    item = [str(weibo_item_bin['uid']), write_text]

                    if write_text != "":
                        writer.writerow(item)
                        count += 1

                if count_f % 10000 == 0:
                    ts = time.time()
                    print "%s  per  %s  second" %(count_f, ts-tb)
                    print "have get %s" % count
                    tb = ts
        except SystemError:
            print "system error"

        except Exception, r:
            pass
