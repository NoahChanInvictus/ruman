# -*- coding:utf-8 -*-

import os
import sys
import zmq
import time
import json
import struct
from datetime import datetime
from bin2json import bin2json

reload(sys)
sys.path.append('../../')
from global_config import ZMQ_VENT_PORT_FLOW5, ZMQ_CTRL_VENT_PORT_FLOW5, ZMQ_VENT_HOST_FLOW1, ZMQ_CTRL_HOST_FLOW1, BIN_FILE_PATH, WRITTEN_TXT_PATH
from global_config import REPLICA_BIN_FILE_PATH

BIN_FILE_PATH = REPLICA_BIN_FILE_PATH

def load_items_from_bin(bin_path):
    return open(bin_path, 'rb')

#def ordered_file_list(file_list):
    

def send_all(f, sender):
    count = 0
    tb = time.time()
    ts = tb

    while 1:
        hdr = f.read(8)
        if len(hdr) != 8 or '' == hdr:
            f.close()
            break

        d1, sp_type, d3, d4, total_len = struct.unpack("!ccccI", hdr)

        data = f.read(total_len - 8)
        if len(data) != total_len - 8 or '' == data:
            f.close()
            break

        weibo_item = bin2json(data, total_len, sp_type)

        if weibo_item and int(weibo_item.get("sp_type", 0)) == 1:
            message_type = int(weibo_item['message_type'])
            if message_type == 2:
                weibo_item['mid'] = str(weibo_item['mid'][2:])
            sender.send_json(weibo_item)
            count += 1

        if count % 10000 == 0:
            te = time.time()
            print '[%s] deliver speed: %s sec/per %s' % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), te - ts, 10000)
            time.sleep(0.5)
        if count % 100000 == 0:
            print '[%s] total deliver %s, cost %s sec [avg %s per/sec]' % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), count, te - tb, count / (te - tb))
            ts = te

    total_cost = time.time() - tb
    return count, total_cost


def send_weibo(sender, poller, controller, total_count=0, total_cost=0):
    """
    send weibo data to zmq_work
    """

    file_list = set(os.listdir(BIN_FILE_PATH))
    txt_list = set(os.listdir(WRITTEN_TXT_PATH))
    print "total file is ", len(file_list)
    for each in file_list:
        event = poller.poll(0)
        if event:
            socks = dict(poller.poll(0))
        else:
            socks = None
        if socks and socks.get(controller) == zmq.POLLIN:
            item = controller.recv()
            if str(item) == "PAUSE":
                print item
                break
        else:
            pass
        if 'data' in each:
            filename = each.split('.')[0]
            print filename
            if '%s_yes5.txt' % filename not in txt_list and "20160307" in filename:
                bin_input = load_items_from_bin(os.path.join(BIN_FILE_PATH, each))
                load_origin_data_func = bin_input
                tmp_count, tmp_cost = send_all(load_origin_data_func, sender)
                total_count += tmp_count
                total_cost += tmp_cost

                fw = open(os.path.join(WRITTEN_TXT_PATH, '%s_yes5.txt' % filename), 'w')
                fw.write('finish reading' + '\n')
                fw.close()

        print 'this scan total deliver %s, cost %s sec' % (total_count, total_cost)

    return total_count, total_cost
