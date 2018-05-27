# -*- coding: UTF-8 -*-

#topic en2ch dict
# topic_en2ch_dict = {'art':u'文体类_娱乐','computer':u'科技类','economic':u'经济类', \
#            'education':u'教育类','environment':u'民生类_环保', 'medicine':u'民生类_健康',\
#            'military':u'军事类','politics':u'政治类_外交','sports':u'文体类_体育',\
#            'traffic':u'民生类_交通','life':u'其他类','anti-corruption':u'政治类_反腐',\
#            'employment':u'民生类_就业','fear-of-violence':u'政治类_暴恐',\
#            'house':u'民生类_住房','law':u'民生类_法律','peace':u'政治类_地区和平',\
#            'religion':u'政治类_宗教','social-security':u'民生类_社会保障'}

topic_en2ch_dict = {'art':u'娱乐类','computer':u'科技类','economic':u'经济类', \
                    'education':u'教育类','environment':u'自然类', 'medicine':u'健康类',\
                    'military':u'军事类','politics':u'政治类','sports':u'体育类',\
                    'traffic':u'交通类','social':u'民生类','life':u'生活类'}

topic_ch2en_dict = {u'娱乐类': 'art', u'科技类':'computer', u'经济类':'economic', \
                    u'教育类':'education', u'自然类': 'environment', u'健康类':'medicine',\
                    u'军事类': 'military', u'政治类':'politics', u'体育类':'sports',\
                    u'交通类':'traffic', u'民生类':'social',u'生活类':'life'}

#activeness weight dict used by evaluate_index.py
activeness_weight_dict = {'activity_time':0.3, 'activity_geo':0.2, 'statusnum':0.5}
#importance weight dict
importance_weight_dict = {'fansnum':0.2, 'domain':0.5, 'topic':0.3}
#topic weight dict
'''
topic_weight_dict = {'政治':0.3, '军事':0.15, '社会':0.15, '环境':0.05, \
                      '医药':0.05, '经济':0.05, '交通':0.05, '教育':0.05, \
                      '计算机':0.05, '艺术':0.05, '体育':0.05}
'''

topic_weight_dict = {'娱乐类':0.8,'科技类':0.5,'经济类':0.5,'教育类':0.4, \
                     '自然类':0.3, '健康类':0.7,'军事类':0.4,\
                     '政治类':0.5,'体育类':0.6,'交通类':0.3,\
                     '民生类':0.8,'生活类':0.3}


#domain en2ch dict
domain_en2ch_dict = {'university':u'高校', 'homeadmin':u'境内机构', 'abroadadmin':u'境外机构', \
                     'homemedia':u'媒体', 'abroadmedia':u'境外媒体', 'folkorg':u'民间组织',\
                     'lawyer':u'法律机构及人士', 'politician':u'政府机构及人士', 'mediaworker':u'媒体人士',\
                     'activer':u'活跃人士', 'grassroot':u'草根', 'other':u'其他', 'business':u'商业人士'}

#domain weight dict
domain_weight_dict = {'高校':0.8, '境内机构':0.6, '境外机构':1, '媒体':1, \
                      '境外媒体':1, '民间组织':0.8,'法律机构及人士':1, '政府机构及人士':0.8,\
                      '媒体人士':0.8, '活跃人士':0.6, '草根':0.6, '其他':0.5, '商业人士':0.6}
