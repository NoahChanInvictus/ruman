# -*- coding: utf-8 -*-
#from user_portrait.global_config import db,es_user_profile,profile_index_name,profile_index_type
#from user_portrait.info_consume.model import PropagateCount, PropagateWeibos,PropagateTimeWeibos
import re
import math
import json
import datetime
import random
from sqlalchemy import func
from pylab import *
import networkx as nx
from networkx.generators.atlas import *
import matplotlib.pyplot as plt
import sys
from ruman.info_consume.model import TrendMaker, TrendPusher,TopicIdentification
from ruman.global_config import db, es_user_profile
# from ins_network_vis import dict2graph
#sys.path.append('../../../')
from ruman.bulk_insert import read_long_gexf

CONSTANTG=nx.Graph()

Minute = 60
Fifteenminutes = 15 * Minute
Hour = 3600
SixHour = Hour * 6
Day = Hour * 24
MinInterval = Fifteenminutes

def gexf_process(data):
	results = {}
	data = json.loads(data)

	# print "gexf_process"
	# print data
	# 将属性都存为字典
	name_dict={}
	size_dict={}
	uid_dict={}

	comp = re.compile('<node id=\\\"(\d*)\\\"')
	id_list = comp.findall(data)
	comp = re.compile('<attvalue for=\\\"name\\\" value=\\\"(.*)\\\"/>')
	name_list = comp.findall(data)
	comp = re.compile('<viz:size value=\\\"(\d*)\\\"/>\\n')
	size = comp.findall(data)
	comp = re.compile('label=\\\"(\d*)\\\">')
	uid = comp.findall(data)
	comp = re.compile('source=\\\"(\d*)\\\"')
	source = comp.findall(data)
	comp = re.compile('target=\\\"(\d*)\\\"/>\\n')
	target = comp.findall(data)

	nodes_dict = {}
	nodes = []
	for i in range(len(id_list)):
		iter_item = {}
		if name_list[i]=="未知":
			iter_item['name'] = uid[i]
		else:
			iter_item['name'] = name_list[i]

		name_dict[id_list[i]]= iter_item['name']
		iter_item['uid'] = uid[i]
		iter_item['size'] =  size[i]

		nodes_dict[id_list[i]]=iter_item
		# G.add_node(id_list[i])

	links = []
	nx_link_list_input=[]
	nx_node_list_input=[]

	for i in range(len(source)):

		nx_node_list_input.append(source[i])
		nx_node_list_input.append(target[i])

		link_tuple=(source[i],target[i])

		nx_link_list_input.append(link_tuple)

	nx_node_list_input=list(set(nx_node_list_input))


	G=nx.Graph()
	G.add_edges_from(nx_link_list_input)
	G=G.subgraph(nx_node_list_input)

	nx_node_list=[]
	nx_link_list=[]
	# G=nx.k_core(G, k=1) #返回度》=k\
	# G=cutDegree(G, 1) #砍掉度为1的
	# G=pagerank(G,1500) 
	G=save_big_connected_subgraph(G)

	nx_node_list=G.nodes()
	nx_link_list=G.edges()

	dictG=nx.Graph()
	for nx_node_item in nx_node_list:
		iter_item_node = {}
		iter_item_node['name'] = nodes_dict[nx_node_item]['name']
		iter_item_node['label'] = ''
		iter_item_node['symbolSize'] = nodes_dict[nx_node_item]['size']
		iter_item_node['uid'] = nodes_dict[nx_node_item]['uid']
		nodes.append(iter_item_node)
		dictG.add_node(nodes_dict[nx_node_item]['uid'])
		dictG.node[nodes_dict[nx_node_item]['uid']]['label']=nodes_dict[nx_node_item]['name']
		dictG.node[nodes_dict[nx_node_item]['uid']]['symbolSize']=nodes_dict[nx_node_item]['size']
		dictG.node[nodes_dict[nx_node_item]['uid']]['uid']=nodes_dict[nx_node_item]['uid']
		# print dictG.node[nodes_dict[nx_node_item]['uid']]

	for tuple_item in nx_link_list:
		iter_item = {}

		iter_item['source'] = nodes_dict[tuple_item[0]]['name']
		iter_item['target'] = nodes_dict[tuple_item[1]]['name']	

		links.append(iter_item)
		dictG.add_edge(nodes_dict[tuple_item[0]]['uid'],nodes_dict[tuple_item[1]]['uid'],sourceName=nodes_dict[tuple_item[0]]['name'],targetName=nodes_dict[tuple_item[1]]['name'])

	# print len(nodes)
	# print len(links)
	results = {}
	# results=find2jump('1496814565',3,dictG) #华西都市报
	results['nodes'] = nodes
	results['links'] = links
	return results,dictG

def get_gexf(topic, identifyDate, identifyWindow):
	#key = _utf8_unicode(topic) +'_' + str(identifyDate) + '_' + str(identifyWindow) + '_' + 'source_graph'
	#key = str(key)
   
    #gexf2es(key, value)
	result = read_long_gexf(topic, identifyDate, identifyWindow)
	
	# print "get_gexf"
	# print json.loads(result)
	return result

def find2jump(uid,hops,G):
	# G=CONSTANTG

	print G.number_of_nodes()
	print G.number_of_edges()
	lis=[]
	lis.append(uid)
	local_nodes = set(lis)
	print local_nodes
	for hop in range(0, hops):
		local_nodes = local_nodes | find_friends(local_nodes, G)
		# print "33333"
		# print local_nodes
	local_G = G.subgraph(list(local_nodes))

	links = []
	nodes = []
	nx_node_list=local_G.nodes()
	nx_link_list=local_G.edges()
	# print "1111"
	# print nx_node_list
	for nx_node_item in nx_node_list:
		# print "222222"
		# print G.node[nx_node_item]['label']
		iter_item_node = {}
		iter_item_node['name'] = G.node[nx_node_item]['label']
		iter_item_node['uid'] = G.node[nx_node_item]['uid']
		iter_item_node['label'] = ''
		iter_item_node['symbolSize'] = G.node[nx_node_item]['symbolSize']
		nodes.append(iter_item_node)

	for tuple_item in nx_link_list:
		iter_item = {}

		iter_item['source'] = G[tuple_item[0]][tuple_item[1]]['sourceName']
		iter_item['target'] = G[tuple_item[0]][tuple_item[1]]['targetName']

		links.append(iter_item)

	results = {}
	results['nodes'] = nodes
	results['links'] = links
	# print results
	return results

def add_local_neighbor(center, lis, G):
    G.add_node(center)
    G.add_nodes_from(lis)
    for i in lis:
        G.add_edge(center, i)

    return G

def find_friends(nodes, G):
    result = set()
    for node in nodes:
        result.add(node)
        if node in G:
            for nd in G[node]:
                result.add(nd)

    return result       

def cutDegree(G,k):
	nodes=[]
	nodes_new=[]
	nodes=G.nodes()
	for node in nodes:
		if G.degree(node)>k:
			nodes_new.append(node)
	G=G.subgraph(nodes_new)
	return G

#保留G的topNum位点
def pagerank(G,topNum):
	nodes_new=[]
	pr_dict = nx.pagerank(G, alpha=0.9)
	pr_dict= sorted(pr_dict.iteritems(), key=lambda d:d[1], reverse = True)
	i=1
	for key in pr_dict:
		print key[0]
		nodes_new.append(key[0])
		if i>=topNum:
			break
		i=i+1
	G=G.subgraph(nodes_new)
	return G

#保留前1500个点的连通子图
def save_big_connected_subgraph(G):
	scc_list=sorted(nx.connected_components(G), key = len, reverse=True)
	nodes_new=[]
	set_new=set()
	len_count=0
	for i in xrange(0,len(scc_list)-1):
		if len_count<1500:
			set_new=set_new|scc_list[i]
		else:
			break
		len_count=len_count+len(scc_list[i])
		
	nodes_new = [j for j in set_new]
	G=G.subgraph(nodes_new)
	return G

def get_trend_pusher(topic):
	topic =topic[:20]
	items = db.session.query(TrendPusher).filter(TrendPusher.topic==topic).all()
	#for item in items:
		#print dir(item)
	#return items
	print items
	results = []
	for item in items:
		result = {}
		user_info = json.loads(item.user_info)
		weibo_info = json.loads(item.weibo_info)
		result['timestamp'] = item.timestamp
		result['name'] = user_info['name']
		result['photo'] = user_info['profile_image_url']
		# result['fans'] = user_info['followers_count']
		result['uid'] = item.uid
		result['mid'] = weibo_info[0]['_id']
		result['fans'] = weibo_info[0]['_source']['user_fansnum']
		result['rank'] = item.rank
		results.append(result)
	return results


def get_trend_maker_old(topic, identifyDate, identifyWindow):
	print topic,identifyDate,identifyWindow
	items = db.session.query(TrendMaker).filter(TrendMaker.topic==topic ,\
														TrendMaker.date==identifyDate ,\
														TrendMaker.windowsize==identifyWindow).all()
	
	print items
	results = []
	for item in items:
		result = {}
		#print item.uid
		user_info = json.loads(item.user_info)
		weibo_info = json.loads(item.weibo_info)
		result['timestamp'] = item.timestamp
		result['name'] = user_info['name']
		result['photo'] = user_info['profile_image_url']
		result['fans'] = user_info['followers_count']
		result['uid'] = item.uid
		result['mid'] = weibo_info[0]['_id']
		results.append(result)
	return results
    
def get_trend_maker(topic):
	# print topic,identifyDate,identifyWindow
	items = db.session.query(TrendMaker).filter(TrendMaker.topic==topic).all()
	
	print items
	results = []
	for item in items:
		result = {}
		#print item.uid
		user_info = json.loads(item.user_info)
		weibo_info = json.loads(item.weibo_info)
		# print weibo_info[0]['_source']['user_fansnum']
		result['timestamp'] = item.timestamp
		result['name'] = user_info['name']
		result['photo'] = user_info['profile_image_url']
		result['fans'] = weibo_info[0]['_source']['user_fansnum']
		result['uid'] = item.uid
		result['mid'] = weibo_info[0]['_id']
		result['rank'] = item.rank
		results.append(result)
	return results


def get_pusher_weibos_byts(topic, identifyDate, identifyWindow):
	items = db.session.query(TrendPusher).filter(TrendPusher.topic==topic ,\
														TrendPusher.date==identifyDate ,\
													TrendPusher.windowsize==identifyWindow).all()
	weibos = []
	for item in items:
		#print len(json.loads(item.weibo_info))
		user_info = json.loads(item.user_info)
		#print user_info
		weibos_info = json.loads(item.weibo_info)[:]
		for weibo_info in weibos_info:
			weibo_info['_source']['uname'] = user_info['name']
			weibo_info['_source']['photo_url'] = user_info['profile_image_url']
			#print weibo_info
			if weibo_info in weibos:
				continue
			else:
				weibos.append(weibo_info)
	sorted_weibos = sorted(weibos, key = lambda x:x['_source']['timestamp'])
	#for weibo in sorted_weibos:
		#print weibo['_source']['timestamp']
	return sorted_weibos
def get_pusher_weibos_byhot(topic, identifyDate, identifyWindow):
	items = db.session.query(TrendPusher).filter(TrendPusher.topic==topic ,\
														TrendPusher.date==identifyDate ,\
													TrendPusher.windowsize==identifyWindow).all()
	weibos = []
	for item in items:
		#print len(json.loads(item.weibo_info))
		user_info = json.loads(item.user_info)
		#print user_info
		weibos_info = json.loads(item.weibo_info)[:]
		for weibo_info in weibos_info:
			weibo_info['_source']['uname'] = user_info['name']
			weibo_info['_source']['photo_url'] = user_info['profile_image_url']
			#print weibo_info
			if weibo_info in weibos:
				continue
			else:
				weibos.append(weibo_info)
	sorted_weibos = sorted(weibos, key = lambda x:x['_source']['retweeted'], reverse=True)
	#for weibo in sorted_weibos:
		#print weibo['_source']['retweeted']
	return sorted_weibos

def get_maker_weibos_byts(topic, identifyDate, identifyWindow):
	items = db.session.query(TrendMaker).filter(TrendMaker.topic==topic ,\
														TrendMaker.date==identifyDate ,\
														TrendMaker.windowsize==identifyWindow).all()

	weibos = []
	for item in items:
		#print len(json.loads(item.weibo_info))
		user_info = json.loads(item.user_info)
		#print user_info
		weibos_info = json.loads(item.weibo_info)[:]
		for weibo_info in weibos_info:
			weibo_info['_source']['uname'] = user_info['name']
			weibo_info['_source']['photo_url'] = user_info['profile_image_url']
			#print weibo_info
			if weibo_info in weibos:
				continue
			else:
				weibos.append(weibo_info)
	sorted_weibos = sorted(weibos, key = lambda x:x['_source']['timestamp'])
	#for weibo in sorted_weibos:
		#print weibo['_source']['timestamp']
	return sorted_weibos

def get_maker_weibos_byhot(topic, identifyDate, identifyWindow):
	items = db.session.query(TrendMaker).filter(TrendMaker.topic==topic ,\
														TrendMaker.date==identifyDate ,\
														TrendMaker.windowsize==identifyWindow).all()
	weibos = []
	for item in items:
		#print len(json.loads(item.weibo_info))
		user_info = json.loads(item.user_info)
		#print user_info
		weibos_info = json.loads(item.weibo_info)[:]
		for weibo_info in weibos_info:
			weibo_info['_source']['uname'] = user_info['name']
			weibo_info['_source']['photo_url'] = user_info['profile_image_url']
			#print weibo_info
			if weibo_info in weibos:
				continue
			else:
				weibos.append(weibo_info)
	sorted_weibos = sorted(weibos, key = lambda x:x['_source']['retweeted'], reverse=True)
	#for weibo in sorted_weibos:
		#print weibo['_source']['retweeted']
	return sorted_weibos


def get_top_pagerank(topic, identifyDate, identifyWindow):
	items = db.session.query(TopicIdentification).filter(TopicIdentification.topic==topic ,\
														TopicIdentification.identifyDate==identifyDate ,\
														TopicIdentification.identifyWindow==identifyWindow).limit(50)
	uid_list = [(item.userId,item.pr) for item in items]
	

	return uid_list


if __name__ == '__main__':
	#get_gexf('aoyunhui', "2016-08-11", 37 )
	#get_trend_maker('aoyunhui', "2016-08-11", 37 )
	#get_trend_pusher('aoyunhui', "2016-08-11", 37 )
	#get_pusher_weibos_byts('aoyunhui', "2016-08-11", 37 )
	#get_maker_weibos_byts('aoyunhui', "2016-08-11", 37 )
	#get_pusher_weibos_byhot('aoyunhui', "2016-08-11", 37 )
	get_maker_weibos_byhot('aoyunhui', "2016-08-11", 37 )
