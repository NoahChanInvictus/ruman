文件说明：
global_utils.py  配置文件
test_code.py 测试文件（仅供测试用）
protou.py 根据种子用户及其粉丝列表形成种子用户群（训练的时候需要）
find_users.py 根据uid查询用户的背景信息和粉丝结构
domain_by_text.py 根据用户微博文本进行身份分类
test_domain_v2.py 用户领域分类主函数

使用说明：
from test_domain_v2 import domain_classfiy

domain_classfiy函数输入输出说明：
【输入】 
uid_list:uid列表 [uid1,uid2,uid3,...]
uid_weibo:分词之后的词频字典  {uid1:{'key1':f1,'key2':f2...}...}

【输出】 domain：标签字典，re_label：推荐标签字典
示例：
domain示例：
{uid1:[label1,label2,label3],uid2:[label1,label2,label3]...}
注：label1是根据粉丝结构分类的结果，label2是根据认证类型分类的结果，label3是根据用户文本分类的结果

re_label示例：
{uid1:label,uid2:label2...}
