使用说明：
from event import event_classfiy

event_classfiy函数输入输出说明：
【输入】 uid_weibo:字典  文本拼成的字符串
示例：{uid1:str(weibo1-weibo2-...)...}

【输出】 user_weight：倾向性字典（取值范围0-3）
示例：
user_weight示例：
{uid1:0.6,uid2:1.2,uid3:0 ...}