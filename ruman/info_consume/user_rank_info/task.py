#-*- coding:utf-8 -*-

from elasticsearch import Elasticsearch
import sys
import json
import datetime
from time_utils import ts2datetime, datetime2ts
from parameter import DAY, LOW_INFLUENCE_THRESHOULD
from in_filter import in_sort_filter
from all_filter import all_sort_filter
from Makeup_info import make_up_user_info
from global_utils import es_user_portrait
from global_utils import es_flow_text
from global_utils import R_CLUSTER_FLOW3 as redis_task


USER_INDEX_NAME = 'user_portrait_1222'
USER_INDEX_TYPE = 'user'

USER_RANK_KEYWORD_TASK_INDEX = 'user_rank_keyword_task'
USER_RANK_KEYWORD_TASK_TYPE = 'user_rank_task'



