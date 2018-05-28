# -*- coding:utf-8 -*-

import os
import sys
import zmq
import time
import json
import struct
from datetime import datetime
from bin2json import bin2json
from zmq_utils import load_items_from_bin, send_all, send_weibo
#from zmq_csv_utils import send_weibo

reload(sys)
sys.path.append('../../')
from global_config import ZMQ_VENT_PORT_FLOW5, ZMQ_CTRL_VENT_PORT_FLOW5,\
                          ZMQ_VENT_HOST_FLOW1, ZMQ_CTRL_HOST_FLOW1, BIN_FILE_PATH



if __name__=="__main__":
    """
    push data to every work

    """
    

    context = zmq.Context()

    # used for send weibo
    sender = context.socket(zmq.PUSH)
    sender.bind('tcp://%s:%s' %(ZMQ_VENT_HOST_FLOW1, ZMQ_VENT_PORT_FLOW5))  
    
    # used for controlled by controllor
    controller = context.socket(zmq.SUB)
    controller.connect('tcp://%s:%s' % (ZMQ_CTRL_HOST_FLOW1, ZMQ_CTRL_VENT_PORT_FLOW5))
    controller.setsockopt(zmq.SUBSCRIBE, "")

    poller = zmq.Poller()
    poller.register(controller, zmq.POLLIN)
    
    total_count = 0
    total_cost = 0
    message = "PAUSE" # default start

    while 1:
        event = poller.poll(0)
        if event:
            socks = dict(poller.poll(0))
        else:
            socks = None

        if socks and socks.get(controller) == zmq.POLLIN: # receive data from zmq pollor
            item = controller.recv()
            if item == "PAUSE": # pause the vent work
                message = "PAUSE"
                time.sleep(1)
                continue
            elif item == "RESTART": # restart the vent work
                message = "RESTART"
                total_count, total_cost = send_weibo(sender, poller, controller, total_count, total_cost)
        else:
            if message == "PAUSE":
                time.sleep(1)
                print message
                continue
            else:
                total_count, total_cost = send_weibo(sender, poller, controller, total_count, total_cost)





