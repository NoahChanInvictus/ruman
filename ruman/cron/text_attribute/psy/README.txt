心理状态调用方法：
from new_psy import psychology_classfiy

用户心理状态分类主函数
1、输入数据示例：字典
示例：{uid1:[weibo1,weibo2,weibo3,...]}

2、输出数据示例：字典(每个用户对应两个字典，一个是一层分类器的状态比例，另一个是二层分类器（消极状态）的状态比例)
示例：{uid1:{'first':{'negemo':0.2,'posemo':0.3,'middle':0.5},'second':{'anger':0.2,'anx':0.5,'sad':0.1,'other':0.2}}...}