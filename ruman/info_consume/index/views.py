#-*- coding:utf-8: -*-
from flask import Blueprint,render_template,request,url_for,redirect,Flask
from flask.ext.security import login_required
from ruman.info_consume.topic_language_analyze.utils import get_topics
mod = Blueprint('index', __name__, url_prefix='/index')
import urllib2

@mod.route('/home/')
@login_required
def home():
	return render_template('/info_consume/index.html')

@mod.route('/date_index/')
@login_required
def date_index():
    keyword = request.args.get('topic_name','')
    return render_template('/info_consume/date_index.html',topic_name=keyword)

@mod.route('/index/')
@login_required
def content():
    return render_template('/info_consume/index.html')

@mod.route('/my_friend/')
@login_required
def my_friend():
	return render_template('/info_consume/my_friend.html')

@mod.route('/weiborecommand/')
@login_required
def weiborecommand():
	return render_template('/info_consume/weiborecommand.html')

@mod.route('/viewinformation/')
@login_required
def viewinformation():
	uid = request.args.get('uid','')
	return render_template('/info_consume/viewinformation.html',uid=uid)

@mod.route('/daohang_public/')
@login_required
def daohang_public():
	return render_template('/info_consume/daohang_public.html')

@mod.route('/boot_test/')
@login_required
def boot_test():
	username='admin@qq.com'
	return render_template('/info_consume/boot_test.html',username=username)

@mod.route('/circle_test/')
@login_required
def circle_test():
	username = 'admin@qq.com'
	return render_template('/info_consume/circle_test.html',username=username)


@mod.route('/myzone/')
@login_required
def myzone():
    return render_template('/info_consume/myzone.html')

@mod.route('/test_api/')
def test_api():
    app =  Flask('jln_try')
    #return redirect(url_for('topic_language_analyze.topics'))
    with app.test_request_context():
        print  url_for('topic_language_analyze.topics')
    return '1'
    
@mod.route('/personalizedRec/')
@login_required
def personalizedRec():
    return render_template('/info_consume/personalizedRec.html')


@mod.route('/admin_management/')
def admin():
    return render_template('/info_consume/admin.html')