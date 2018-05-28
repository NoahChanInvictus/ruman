# -*- coding:utf-8 -*-
import pandas as pd

data = [{'title':'贾跃亭又要动刀子，谁将是乐视移动最大的变数？冯幸？','publish_time':'2016-11-25 00:00:00',\
            'id':4045473440545680},{'title':'贾跃亭又要动刀子，谁将是乐视移动最大的变数？冯幸？','publish_time':'2016-11-25 00:00:00',\
            'id':4045473440545680}]
sample_data = pd.DataFrame(data)
selected = sample_data.loc[sample_data['id']==4045473440545680]
for item in selected:
    print item