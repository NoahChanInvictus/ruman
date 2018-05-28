#-*- coding:utf-8 -*-
'''
use to save parameter
'''
#for test
RUN_TYPE = 0 #0 mark run for test; 1 mark run for operation
#RUN_TEST_TIME = '2016-03-13'
#RUN_TEST_TIME = '2013-09-08'
RUN_TEST_TIME = '2016-11-28'#'2016-11-28'
MYSQL_TOPIC_LEN = 0 #0是20，1是正常
#for all
DAY = 24*3600
Fifteen = 60 * 15
HALF_HOUR = 1800
HOUR = 3600
FOUR_HOUR = 3600*4
MAX_VALUE = 99999999
WEEK = 7
WEEK_TIME = 7*24*3600
MONTH = 30
MONTH_TIME = 35*24*3600
EXPIRE_TIME = 8*24*3600

#new attribute: verified_type
verified_num2ch_dict = {-1: u'普通用户', 0:u'名人', 1: u'政府', 2: u'企业',\
        3:u'媒体', 4:u'校园', 5: u'网站', 6:u'应用', 7:u'团体(机构)',\
        8:u'待审企业', 200:u'初级达人', 220:u'中高级达人', 400:u'已故v用户'}

#attribute: IP
IP_TIME_SEGMENT = 4*3600 # return every 4 hour statistic result for ip information
IP_TOP = 5 # return Top-5 ip for every time segment
IP_CONCLUSION_TOP = 2 # return job/home ip with top2

#attribute: geo
GEO_COUNT_THRESHOLD = 5

#attribute: sentiment
SENTIMENT_DICT = {'1':u'积极', '2':u'悲伤', '3':u'愤怒', '0': u'中性'}
SENTIMENT_DICT_NEW = {'0':u'中性', '1':u'积极', '2':u'生气', '3':'焦虑', \
        '4':u'悲伤', '5':u'厌恶', '6':u'消极其他', '7':u'消极'}
SENTIMENT_FIRST = ['0', '1', '7']
SENTIMENT_SECOND = ['2', '3', '4', '5', '6']

#attribute: online_pattern
PATTERN_THRESHOLD = 3

#activeness threshould 
LOW_INFLUENCE_THRESHOULD = 50

#attribute: domain
domain_en2ch_dict = {'university':u'高校', 'homeadmin':u'境内机构', 'abroadadmin':u'境外机构', \
                     'homemedia':u'媒体', 'abroadmedia':u'境外媒体', 'folkorg':u'民间组织',\
                     'lawyer':u'法律机构及人士', 'politician':u'政府机构及人士', 'mediaworker':u'媒体人士',\
                     'activer':u'活跃人士', 'grassroot':u'草根', 'other':u'其他', 'business':u'商业人士'}

domain_ch2en_dict = {u'高校': 'university', u'境内机构':'homeadmin', u'境外机构':'abroadadmin' ,\
                     u'媒体': 'homemedia', u'境外媒体': 'abroadmedia', u'民间组织': 'folkorg', \
                     u'法律机构及人士': 'lawyer', u'政府机构及人士':'politician', u'媒体人士':'mediaworker',\
                     u'活跃人士': 'activer', u'草根': 'grassroot', u'其他':'other', u'商业人士':'business'}



#attribtue: topic

topic_en2ch_dict = {'art':u'娱乐类','computer':u'科技类','economic':u'经济类', \
                    'education':u'教育类','environment':u'自然类', 'medicine':u'健康类',\
                    'military':u'军事类','politics':u'政治类','sports':u'体育类',\
                    'traffic':u'交通类','social':u'民生类','life':u'生活类'}

topic_ch2en_dict = {u'娱乐类': 'art', u'科技类':'computer', u'经济类':'economic', \
                    u'教育类':'education', u'自然类': 'environment', u'健康类':'medicine',\
                    u'军事类': 'military', u'政治类':'politics', u'体育类':'sports',\
                    u'交通类':'traffic', u'民生类':'social',u'生活类':'life'}
'''
topic_en2ch_dict = {'art':u'文体类_娱乐','computer':u'科技类','economic':u'经济类', \
                    'education':u'教育类','environment':u'民生类_环保', 'medicine':u'民生类_健康',\
                    'military':u'军事类','politics':u'政治类_外交','sports':u'文体类_体育',\
                    'traffic':u'民生类_交通','life':u'其他类','anti-corruption':u'政治类_反腐',\
                    'employment':u'民生类_就业','fear-of-violence':u'政治类_暴恐',\
                    'house':u'民生类_住房','law':u'民生类_法律','peace':u'政治类_地区和平',\
                    'religion':u'政治类_宗教','social-security':u'民生类_社会保障'}

topic_ch2en_dict = {u'文体类_娱乐': 'art', u'科技类':'computer', u'经济类':'economic', \
                    u'教育类':'education', u'民生类_环保': 'environment', u'民生类_健康':'medicine',\
                    u'军事类': 'military', u'政治类_外交':'politics', u'文体类_体育':'sports',\
                    u'民生类_交通':'traffic', u'其他类':'life', u'政治类_反腐':'anti-corruption',\
                    u'民生类_就业':'employment', u'政治类_暴恐':'fear-of-violence',\
                    u'民生类_住房': 'house', u'民生类_法律':'law', u'政治类_地区和平':'peace',\
                    u'政治类_宗教':'religion', u'民生类_社会保障':'social-security'}
'''
#attribtue:retweet/be_retweet/comment/be_comment/bidirect_interaction
SOCIAL_DEFAULT_COUNT = '20'

#attribute:sentiment trend default time type
SENTIMENT_TREND_DEFAULT_TYPE = 'day'
DEFAULT_SENTIMENT = '1' #happy, angry, sad


#attribute:psy desciption field
PSY_DESCRIPTION_FIELD = ['anger', 'anx', 'sad', 'negemo']
psy_en2ch_dict = {'anger': u'愤怒情绪', 'anx': u'焦虑情绪', 'sad': u'悲伤情绪', 'negemo':u'消极情绪'}
psy_description_dict = {
        '0':u'与个人历史水平持平,但是高于全库平均水平',
        '1':u'高于个人历史水平, 但与全库平均水平持平',
        '2':u'高于个人历史水平及全库平均水平',
        '3':u'心理状态平稳正常'
        }

#recommend in
RECOMMEND_IN_SENSITIVE_TOP = 2000
RECOMMEND_IN_BLACK_USER1 = '/home/ubuntu2/jiangln/jln/user_portrait/user_portrait/cron/recommentation_in/blacklist_2.csv'
RECOMMEND_IN_BLACK_USER2 = '/home/ubuntu2/jiangln/jln/user_portrait/user_portrait/cron/recommentation_in/blacklist_0808.txt'
RECOMMEND_IN_ACTIVITY_THRESHOLD = 50
RECOMMEND_IN_IP_THRESHOLD = 7
RECOMMEND_IN_RETWEET_THRESHOLD = 20
RECOMMEND_IN_MENTION_THRESHOLD = 15
#recommend in
RECOMMEND_IN_AUTO_DATE = 7
RECOMMEND_IN_AUTO_SIZE = 10
RECOMMEND_IN_AUTO_GROUP = 3
RECOMMEND_IN_AUTO_RANDOM_SIZE = 20
RECOMMEND_IN_OUT_SIZE = 50
RECOMMEND_IN_ITER_COUNT = 20
RECOMMEND_IN_MEDIA_PATH = '/home/ubuntu2/jiangln/jln/user_portrait/user_portrait/cron/recommentation_in/media_user.txt'
RECOMMEND_MAX_KEYWORDS = 100
RECOMMEND_IN_WEIBO_MAX = 1000

#recommend out threshould
RECOMMEND_OUT_THRESHOULD = 30


#attribute: influence index and conclusion
INFLUENCE_RETWEETED_THRESHOLD = 500
INFLUENCE_COMMENT_THRESHOLD = 500
INFLUENCE_TAG = {
         "0": "昨日无影响", # 无数据
         "1": "热门信息发布者", # 原创微博的被转发量和评论量高
         "2": "热门信息传播者", # 转发微博的被转发量和评论量高
         "3": "热门信息发布者和传播者", # 同时高
         "4": "影响力低"
    }

#attribtue: influence trend conclusion
INFLUENCE_TREND_SPAN_THRESHOLD = 400
INFLUENCE_TREND_AVE_MIN_THRESHOLD = 500
INFLUENCE_TREND_AVE_MAX_THRESHOLD = 900
INFLUENCE_TREND_DESCRIPTION_TEXT = {
        '0': u'影响力较高,且保持平稳',
        '1': u'影响力较高,且波动性较大',
        '2': u'影响力一般,且保持平稳',
        '3': u'影响力一般,且波动性较大',
        '4': u'影响力较低,且保持平稳',
        '5': u'影响力较低,且波动性较大'
    }

#attribute: activeness trend conclusion
ACTIVENESS_TREND_SPAN_THRESHOLD = 30
ACTIVENESS_TREND_AVE_MIN_THRESHOLD = 40
ACTIVENESS_TREND_AVE_MAX_THRESHOLD = 70
ACTIVENESS_TREND_DESCRIPTION_TEXT = {
        '0': u'活跃度较高, 且保持平稳',
        '1': u'活跃度较高, 且波动性较大',
        '2': u'活跃度一般, 且保持平稳', 
        '3': u'活跃度一般, 且波动性较大',
        '4': u'活跃度较低, 且保持平稳',
        '5': '活跃度较低, 且波动性较大'
    }

ACTIVENESS_TREND_TAG_VECTOR = {
         '0': u'活跃度高且平稳',
         '1': u'活跃度高且波动性大',
         '2': u'活跃度一般且平稳',
         '3': u'活跃度一般且波动性大',
         '4': u'活跃度低且平稳',
         '5': '活跃度低且波动性大'
    }

#cron/text_attribute/weibo_api
# weibo_api.py read_flow_text_sentiment/read_flow_text 
WEIBO_API_INPUT_TYPE = 0 # 1 mark: need compute sentiment
                         # 0 mark: not need compute sentiment
#cron/text_attribute/topic
TOPIC_ABS_PATH = '/home/ubuntu2/jiangln/jln/user_portrait/user_portrait/cron/model_file/topic'

#cron/text_attribute/domain
DOMAIN_ABS_PATH = '/home/ubuntu2/jiangln/jln/user_portrait/user_portrait/cron/model_file/domain'

#cron/text_attribute/psy
PSY_ABS_PATH = '/home/ubuntu2/jiangln/jln/user_portrait/user_portrait/cron/model_file/psy'

#cron/text_attribute/event
EVENT_ABS_PATH = '/home/ubuntu2/jiangln/jln/user_portrait/user_portrait/cron/model_file/event'

#cron/text_attribute/character
CH_ABS_PATH = '/home/ubuntu2/jiangln/jln/user_portrait/user_portrait/cron/model_file/character'
CHARACTER_TIME_GAP = 7


try:
    from . import zxy_params
    UID_TXT_PATH = zxy_params.BASE_DIR + '/user_portrait/user_portrait/info_consume/weibo_hashtag'
except:
    #jln
    UID_TXT_PATH = '/home/ubuntu2/jiangln/info_consume/user_portrait/user_portrait/info_consume/weibo_hashtag'

# pre-influence index
pre_influence_index = "bci_"
influence_doctype = "bci"

# conclusion of history influence
INFLUENCE_LENTH = 30
INFLUENCE_LEVEL = [200, 500, 700, 900, 1100]
ACTIVENESS_LEVEL = [0.5, 1, 1.5, 2]
PRE_ACTIVENESS = "activeness_"
INFLUENCE_CONCLUSION = {
    "0": "该用户近期无影响力",
    "1": "该用户近期影响力很小",
    "2": "该用户近期影响力一般",
    "3": "该用户近期影响力持续较高",
    "4": "该用户近期影响力较高，波动较大",
    "5": "该用户近期影响力持续很高",
    "6": "该用户近期影响力很高，波动性大",
    "7": "该用户影响力接近意见领袖",
    "8": "该用户影响力巨大"
    }

CURRNET_INFLUENCE_THRESHOULD = [200,500,700,900,1100]
CURRENT_INFLUENCE_CONCLUSION = {
    "0": "无影响力",
    "1": "影响力较低",
    "2": "影响力一般",
    "3": "影响力较高",
    "4": "影响力高",
    "5": "影响力极高"
    }

ACTIVENESS_CONCLUSION = {
    "0": "该用户近期没有活跃",
    "1": "该用户近期不太活跃",
    "2": "该用户近期活跃程度一般",
    "3": "该用户近期较为活跃",
    "4": "该用户近期非常活跃",
    "5": "该用户近期极其活跃"
    }

BCI_LIST = ["origin_weibo_number", "origin_weibo_number", "retweeted_weibo_number", "retweeted_weibo_retweeted_brust_average", "origin_weibo_retweeted_average_number", "origin_weibo_comment_top_number", \
           "origin_weibo_comment_brust_average", "retweeted_weibo_top_retweeted_id", "retweeted_weibo_comment_top_number", "origin_weibo_top_comment_id", "retweeted_weibo_retweeted_total_number", "retweeted_weibo_retweeted_average_number", \
           "origin_weibo_retweeted_total_number", "retweeted_weibo_top_comment_id", "origin_weibo_top_retweeted_id", "origin_weibo_comment_average_number", "origin_weibo_retweeted_brust_average", "origin_weibo_retweeted_top_number", \
           "retweeted_weibo_retweeted_top_number","user_index", "retweeted_weibo_comment_total_number", "retweeted_weibo_comment_brust_average", "origin_weibo_comment_total_number", "retweeted_weibo_comment_average_number"]


INFLUENCE_TOTAL_THRESHOULD = [1000, 1000, 1000, 1000]
INFLUENCE_TOTAL_LIST = ['origin_weibo_retweeted_total_number','origin_weibo_comment_total_number','retweeted_weibo_retweeted_total_number','retweeted_weibo_comment_total_number']
INFLUENCE_TOTAL_CONCLUSION = ['原创微博被转发量高', '原创微博被评论量高', '转发微博被转发量高', '转发微博被评论量高']
UNDERLINE_CONCLUSION = ['热门信息发布者', '发布的热门信息容易引发公众热议', '热门信息传播者', '传播的热门信息容易引发公众热议']
INFLUENCE_BRUST_THRESHOULD = [100, 100,100, 100]
INFLUENCE_BRUST_LIST = ['origin_weibo_retweeted_brust_average','origin_weibo_comment_brust_average','retweeted_weibo_retweeted_brust_average','retweeted_weibo_comment_brust_average']
INFLUENCE_BRUST_CONCLUSION = ['传播速度快', '评论速度快', '传播速度快', '评论速度快']


# social sensoring time interval
SOCIAL_SENSOR_TIME_INTERVAL = 3600
SOCIAL_SENSOR_FORWARD_RANGE = 12*3600
INDEX_MANAGE_SOCIAL_SENSING = "manage_sensing_task"
DOC_TYPE_MANAGE_SOCIAL_SENSING = "sensing_task"
DETAIL_SOCIAL_SENSING = "social_sensing_task"
FORWARD_N = 24
INITIAL_EXIST_COUNT = 12 #从任务开始到经历多少个时间片段开始计数
IMPORTANT_USER_NUMBER = 100 # 每个时间间隔内es查询时设置重要的人的个数
IMPORTANT_USER_THRESHOULD = 70 # 重要的人其重要度的阈值，不低于
signal_nothing = "0" # 无事件
signal_brust = "1" # 事件爆发
signal_track = "2" # 事件跟踪
signal_count_varition = "1"
signal_sentiment_varition = "2"
signal_sensitive_variation = '3'
signal_nothing_variation = ""
finish_signal = "1"
unfinish_signal = "0"
SOCIAL_SENSOR_INFO = ['uid', 'uname', "photo_url", "domain", "topic_string", "importance", "influence", "activeness"]
AGGRAGATION_KEYWORDS_NUMBER = 20
PRE_AGGREGATION_NUMBER = 50
WARNING_SENSITIVE_COUNT = 1000

# 预警提示句
CURRENT_WARNING_DICT = {
    "0": "目前没有感知到事件爆发",
    "1": "预警：与事件相关的微博的数量发生异常，可能发生相关事件，请及时查看",
    "2": "预警：与事件相关的微博的负面情绪发生异常，可能发生相关事件，请及时查看",
    "3": "预警：与事件相关的微博的数量和负面情绪均发生异常，可能发生相关事件，请及时查看"
    }


#group detect: query information---single/multi
DETECT_QUERY_ATTRIBUTE = ['location', 'domain', 'topic_string', 'keywords_string', 'hashtag', \
                          'activity_geo', 'tag', 'remark']
DETECT_QUERY_ATTRIBUTE_MULTI = ['topic_string', 'keywords_string', 'hashtag', 'activity_geo']
DETECT_QUERY_STRUCTURE = ['retweet', 'comment', 'bidirect','hop']
DETECT_QUERY_FILTER = ['count', 'influence', 'importance']
DETECT_DEFAULT_WEIGHT = 0.5
DETECT_DEFAULT_MARK = '0'
DETECT_DEFAULT_COUNT = 100
DETECT_FILTER_VALUE_FROM = 0
DETECT_FILTER_VALUE_TO = 100
DETECT_ITER_COUNT = 100
DETECT_TEXT_FUZZ_ITEM = ['text']
DETECT_TEXT_RANGE_ITEM = ['timestamp']
MAX_DETECT_COUNT = 900
DETECT_COUNT_EXPAND = 3
MAX_PROCESS = 100
#group detect: attribute detect
DETECT_ATTRIBUTE_FUZZ_ITEM = ['location', 'activity_geo', 'keywords_string','hashtag', 'remark']
DETECT_ATTRIBUTE_MULTI_ITEM = ['topic_string', 'domain']
DETECT_ATTRIBUTE_SELECT_ITEM = ['tendency', 'tag']
DETECT_PATTERN_FUZZ_ITEM = ['geo', 'ip']
DETECT_PATTERN_SELECT_ITEM = ['message_type', 'sentiment']
DETECT_PATTERN_RANGE_ITEM = ['timestamp']
#group detect: event detect
DETECT_EVENT_ATTRIBUTE = ['topic_string', 'domain']
DETECT_EVENT_TEXT_FUZZ_ITEM = ['text']
DETECT_EVENT_TEXT_RANGE_ITEM = ['timestamp']
#identify user attribute list
IDENTIFY_ATTRIBUTE_LIST = ['domain', 'uid', 'hashtag_dict', 'importance', 'influence', 'domain_v3', \
        'online_pattern', 'keywords_string', 'topic', 'activity_geo', 'uname', 'hashtag', 'keywords', 'fansnum', \
        'psycho_status', 'tendency', 'photo_url', 'verified', 'statusnum', 'gender', 'topic_string',\
        'activeness', 'location', 'activity_geo_dict', 'friendsnum', 'group', 'remark', 'character_text',\
        'character_sentiment', 'activity_geo_aggs', 'online_pattern_aggs']

#cron_group
TOPIC_MODEL_COUNT = 5
TOPIC_MODEL_WORD_COUNT = 10
ACTIVITY_GEO_TOP = 3
HIS_BINS_COUNT = 5
GROUP_ACTIVITY_TIME_THRESHOLD = [0.3, 0.5]
GROUP_ACTIVITY_TIME_DESCRIPTION_DICT = {
        '0': u'群体用户活跃时间较分散',
        '1': u'群体用户活跃时间较集中',
        '2': u'群体用户活跃时间非常集中'
        }
GROUP_ITER_COUNT = 100
GROUP_INFLUENCE_FILTER_LOW_THRESHOLD = 500
GROUP_INFLUENCE_FILTER_RANK_RATIO = 0.05
GROUP_SOCIAL_OUT_COUNT = 100
GROUP_SENTIMENT_LIST = ['0', '1', '2'] # need to modify
GROUP_NEGATIVE_SENTIMENT = ['2','3','4','5','6'] # need to modify
GROUP_AVE_ACTIVENESS_RANK_THRESHOLD = [0.3, 0.7]
GROUP_AVE_INFLUENCE_RANK_THRESHOLD = [0.3, 0.7]
GROUP_AVE_IMPORTANCE_RANK_THRESHOLD = [0.3, 0.7]
GROUP_AVE_ACTIVENESS_RANK_DESCRIPTION = {
        '0': u'群体用户整体活跃度较高',
        '1': u'群体用户整体活跃度一般',
        '2': u'群体用户整体活跃度较低'
        }
GROUP_AVE_INFLUENCE_RANK_DESCRIPTION = {
        '0': u'群体用户整体影响力较高',
        '1': u'群体用户整体影响力一般',
        '2': u'群体用户整体活跃度较低'
        }
GROUP_AVE_IMPORTANCE_RANK_DESCRIPTION = {
        '0': u'群体用户整体重要度较高',
        '1': u'群体用户整体重要度一般',
        '2': u'群体用户整体重要度较低'
        }
GROUP_DENSITY_THRESHOLD = [0.1, 0.3]
GROUP_DENSITY_DESCRIPTION = {
        '0': u'群体内交互紧密度较低',
        '1': u'群体内交互进密度一般',
        '2': u'群体内交互进密度较高'
        }
GROUP_KEYWORD_COUNT = 50
GROUP_HASHTAG_COUNT = 50
GROUP_SENTIMENT_WORD_COUNT = 50

# 敏感词等级评分, string类型
sensitive_score_dict = {
    "1": 1,
    "2": 5,
    "3": 10
}

#SENTIMENT ANALYSIS
SENTIMENT_MAX_TEXT = 100
SENTIMENT_MAX_USER = 10
SENTIMENT_TEXT_SORT = 'timestamp'
SENTIMENT_MAX_KEYWORDS = 100
SENTIMENT_ITER_USER_COUNT = 1000
SENTIMENT_ITER_TEXT_COUNT = 5000
SENTIMENT_SORT_EVALUATE_MAX = 999999999999
SENTIMENT_TYPE_COUNT = 7
str2segment = {'fifteen': 900, 'hour': 3600, 'day':3600*24}
sentiment_type_list = ['0', '1', '7']

topic_value_dict = {"art": 1, "computer":2, "economic":7, "education":7.5, "environment":8.7, "medicine":7.8,"military":7.4, "politics":10, "sports":4, "traffic":6.9, "life":1.8, "anti-corruption":9.5, "employment":6, "fear-of-violence":9.3, "house":6.4, "law":8.6, "peace":5.5, "religion":7.6, "social-security":8.6}



# micro prediction
minimal_time_interval = 3600
pre_flow_text = "flow_text_"
type_flow_text = "text"
data_order = ["total_fans_number", "origin_weibo_number", "retweeted_weibo_number", "comment_weibo_number",\
"origin_important_user_number", "retweet_important_user_count",\
"average_origin_imp_hour", "average_retweet_imp_hour", "total_count", "uid_number",\
"average_origin_ts", "average_retweet_ts"]
K = 6
