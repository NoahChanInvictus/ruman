# -*- coding:utf-8 -*-
import pandas as pd


def read_data(path):
    df = pd.read_csv(path)
    # print df.head(5)
    return df
def read_data_xlsx(path):
    df = pd.read_excel(path, sheetname='sample_data')
    return df

def get_traceback(sampleid,data):
    sample_data = pd.DataFrame(data)
    selected = sample_data.loc[sample_data['id']==sampleid]
    selected_dict = selected.to_dict(orient= 'records')
    selected_dict = sorted(selected_dict,key = lambda x:x['publish_time'])
    return selected_dict

def weibo_fix(weibo_data):
    # print weibo_data['id']
    real_mids = []
    with open('./ruman/cron/sample_data/Wechatreal_id-wb.txt') as f:
        for row in f.readlines():
            nrow = row.strip('\n').strip('\r').strip('\xef\xbb\xbf')
            real_mids.append(nrow)
    # print real_mid
    for index in weibo_data.index:
        raw_id = weibo_data.ix[index]['id']
        for real_mid in real_mids:
            if real_mid[:-1] == str(raw_id)[:-1]:
                # print raw_id,real_mid
                weibo_data['id'][index] = int(real_mid)
                break
    # print weibo_data['id']
    return weibo_data

news_data = read_data_xlsx('./ruman/cron/sample_data/Wechatall_data-xw.xlsx')
yaoyan_data = read_data_xlsx('./ruman/cron/sample_data/Wechatall_data-yy.xlsx')
weibo_data = read_data_xlsx('./ruman/cron/sample_data/Wechatall_data-wb.xlsx')
weibo_data = weibo_fix(weibo_data)
def sample_data_main(sampleid,mode):
    
    if mode == 'news':
        data = news_data
    elif mode == 'yaoyan':
        data = yaoyan_data
    elif mode == 'weibo':
        data = weibo_data
    result = get_traceback(sampleid,data)
    return result


if __name__=="__main__":
    # global data
    # # data = read_data('./sample_data.csv')
    # data = read_data_xlsx('./Wechatall_data-xw.xlsx')
    # print get_traceback('AWNN6Tcwvel9p8sC_YIY')
    print sample_data_main('AWNN6Tcwvel9p8sC_YIY','news')[0]
    print sample_data_main('AWNN6Tcwvel9p8sC_YIY','news')[0]
# print get_traceback(4045473440545681)
