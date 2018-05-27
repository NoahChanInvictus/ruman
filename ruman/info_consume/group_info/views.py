#-*- coding:utf-8 -*-

import os
import time
import json
from werkzeug import secure_filename
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect, send_from_directory
from utils import submit_tasks, search_task, get_group_list,\
       delete_group_results, get_social_inter_content, search_group_sentiment_weibo,\
       get_group_user_track, search_group_results, get_influence_content
from utils import get_group_member_name, get_activity_weibo,\
        group_user_weibo, edit_state, show_vary_detail,search_group_member

from ruman.global_config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from ruman.search_user_profile import es_get_source
from ruman.time_utils import ts2datetime

mod = Blueprint('info_group', __name__, url_prefix='/info_group')

# use to upload file
@mod.route('/upload_file/', methods=['GET', 'POST'])
def upload_file():
    upload_data = request.form['upload_data']
    task_name = request.form['task_name']
    state = request.form['state']
    now_ts = time.time()
    now_date = ts2datetime(now_ts)
    line_list = upload_data.split('\n')
    input_data = {}
    input_data['submit_date'] = now_date
    input_data['task_name'] = task_name
    input_data['state'] = state
    uid_list = []
    for line in line_list:
        uid = line[:10]
        if len(uid)==10:
            uid_list.append(uid)
    input_data['uid_list'] = uid_list
    status = submit_tasks(input_data)
    return json.dumps(status)


# submit group analysis task and save to redis as lists
# submit group task: task name should be unique
# input_data is dict ---two types
# one type: {'submit_date':x, 'state': x, 'uid_list':[],'task_name':x, 'submit_user':submit_user}
# two type: {'submit_date':x, 'state': x, 'task_name':x, 'uid_file':filename, 'submit_user':submit_user}
@mod.route('/submit_task/',methods=['GET', 'POST'])
def ajax_submit_task():
    input_data = dict()
    input_data = request.get_json()
    try:
        submit_user = input_data['submit_user']
    except:
        return 'no submit_user information'
    now_ts = int(time.time())
    input_data['submit_date'] = now_ts
    #print '###################'
    status = submit_tasks(input_data)
    return json.dumps(status)

# show the group task table
@mod.route('/show_task/')
def ajax_show_task():
    results = {}
    task_name = request.args.get('task_name', '')
    submit_date = request.args.get('submit_date', '')
    state = request.args.get('state', '')
    status = request.args.get('status', '')
    submit_user = request.args.get('submit_user', 'admin')
    results = search_task(task_name, submit_date, state, status, submit_user)
    return json.dumps(results)


# show the group analysis result---different module
# input: task_name, module
#        module: overview/basic/activity/preference/influence/social/think
# output: module result
@mod.route('/show_group_result/')
def ajax_show_group_result_basic():
    results = {}
    task_name = request.args.get('task_name', '')
    submit_user = request.args.get('submit_user', 'admin')
    module = request.args.get('module', 'basic')
    results = search_group_results(task_name, module, submit_user)
    return json.dumps(results)

#jln 2016/09/28
@mod.route('/show_group_member/')
def show_group_member():
    results = {}
    task_name = request.args.get('task_name', '')
    submit_user = request.args.get('submit_user', 'admin')
    results = search_group_member(task_name,submit_user)
    return results


# show the group weibo result
# version: write in 16-03-26
# input: task_name, submit_user, sort_type
# ouput: weibo result
@mod.route('/group_user_weibo/')
def ajax_group_user_weibo():
    results = {}
    task_name = request.args.get('task_name', '')
    submit_user = request.args.get('submit_user', 'admin')
    sort_type = request.args.get('sort_type', '')
    results = group_user_weibo(task_name, submit_user, sort_type)
    if not results:
        results = {}
    return json.dumps(results)

#show group members geo track
#input: uid
#output: geo track
@mod.route('/show_group_member_track/')
def ajax_show_group_menber_track():
    results = {}
    uid = request.args.get('uid', '')
    results = get_group_user_track(uid)
    return json.dumps(results)

# get group member uid_uname dict
# input: task_name
# output: uid_uname dict
@mod.route('/group_member/')
def ajax_group_member():
    results = {}
    task_name = request.args.get('task_name', '')
    submit_user = request.args.get('submit_user', 'admin')
    results = get_group_member_name(task_name, submit_user)
    return json.dumps(results)


# show group members weibo for activity module--week
# input: task_name, start_ts
# output: weibo_list
@mod.route('/activity_weibo/')
def ajax_activity_weibo():
    results = []
    task_name = request.args.get('task_name', '')
    start_ts = int(request.args.get('start_ts', ''))
    submit_user = request.args.get('submit_user', 'admin')
    results = get_activity_weibo(task_name, start_ts, submit_user)
    return json.dumps(results)


# show group members weibo for influence content
# input: uid, timestamp_range
# output: weibo_list
@mod.route('/influence_content/')
def ajax_get_influence_content():
    results= {}
    uid = request.args.get('uid', '')
    timestamp_from = request.args.get('timestamp_from', '')
    timestamp_to = request.args.get('timestamp_to', '')
    if timestamp_from == '' or timestamp_to == '':
        return 'timestamp range invalid'
    if int(timestamp_from) >= int(timestamp_to):
        return 'timestamp range invalid'
    else:
        results = get_influence_content(uid, int(timestamp_from), int(timestamp_to))

    return json.dumps(results)

# show group members interaction weibo content
# input: uid1, uid2
# output: weibo_list
@mod.route('/social_inter_content/')
def ajax_get_social_inter_content():
    results = {}
    uid1 = request.args.get('uid1', '')
    uid2 = request.args.get('uid2', '')
    results = get_social_inter_content(uid1, uid2, 'in')
    return json.dumps(results)

#show group members out-interaction weibo content
#input: uid1, uid2
#output: webo_list
@mod.route('/social_out_content/')
def ajax_get_social_out_content():
    results = {}
    uid1 = request.args.get('uid1', '')
    uid2 = request.args.get('uid2', '')
    results = get_social_inter_content(uid1, uid2, 'out')
    return json.dumps(results)

#show group members sentiment weibo content
#input: task_name, start_time, sentiment_type
#output: weibo_list
@mod.route('/group_sentiment_weibo/')
def ajax_group_sentiment_weibo():
    task_name = request.args.get('task_name', '')
    submit_user = request.args.get('submit_user', 'admin')
    start_ts = request.args.get('start_ts', '')
    start_ts = int(start_ts)
    sentiment_type = request.args.get('sentiment', '')
    results = search_group_sentiment_weibo(task_name, start_ts, sentiment_type, submit_user)
    if not results:
        results = []
    return json.dumps(results)
    
#show the group member list
@mod.route('/show_group_list/')
def sjax_show_group_list():
    results = []
    task_name = request.args.get('task_name', '')
    submit_user = request.args.get('submit_user', 'admin')
    results = get_group_list(task_name, submit_user)
    return json.dumps(results)

# delete the group task
@mod.route('/delete_group_task/')
def ajax_delete_group_task():
    results = {}
    task_name = request.args.get('task_name', '')
    submit_user = request.args.get('submit_user', 'admin')
    results = delete_group_results(task_name, submit_user)
    return json.dumps(results)

#edit state for group task
@mod.route('/edit_state/')
def ajax_edit_state():
    task_name = request.args.get('task_name', '')
    submit_user = request.args.get('submit_user', 'admin')
    new_state = request.args.get('new_state', '')
    results = edit_state(task_name, submit_user, new_state)
    return json.dumps(results)

#show vary detail geo
@mod.route('/show_vary_detail/')
def ajax_show_vary_detail():
    task_name = request.args.get('task_name', '')
    submit_user = request.args.get('submit_user', 'admin')
    vary_pattern = request.args.get('city_pattern', '') #city1-city2
    results = show_vary_detail(task_name, submit_user, vary_pattern)
    return json.dumps(results)
