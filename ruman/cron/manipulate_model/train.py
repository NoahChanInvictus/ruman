#-*-coding: utf-8-*-
import sys
reload(sys)
sys.path.append("../../")
import pandas as pd
from config import *
from time_utils import *
from sql_utils import *
from elasticsearch import Elasticsearch
from create import get_frame_theday
from calculate import *
from deal import *
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn import metrics

def get_training_data(reason,year1,month1,day1,year2,month2,day2):
    print 'Ready to prepare training...'
    if reason == 1:
        dfx = deal_data(1,year1,month1,day1,year2,month2,day2)
        dfy = pd.DataFrame([[0]]*len(dfx),columns=['y'])
        black_list = get_black_list(1)
    elif reason == 2:
        dfx = deal_data(2,year1,month1,day1,year2,month2,day2)
        dfy = pd.DataFrame([[0]]*len(dfx),columns=['y'])
        black_list = get_black_list(2)
    indexs = []
    for blackcode in black_list:   #对于在黑名单中的公司的时间进行匹配，在对应的位置标签改为1
        blackframe = dfx[dfx['code'] == blackcode[BLACK_LIST_STOCK_ID]]
        blackframe = blackframe[blackframe['date'] <= ts2datetime(blackcode[BLACK_LIST_END_TS])]
        index = blackframe[blackframe['date'] >= ts2datetime(blackcode[BLACK_LIST_START_TS])].index.tolist()
        indexs.extend(index)
    indexs = set(indexs)
    dfy.loc[indexs] = 1
    #print dfx,dfy
    #
    #dfy.to_csv(r'/home/lfz/python/dfy.csv',encoding='utf_8_sig')
    dfx['label'] = dfy['y']
    dfx.to_csv('dfx%d.csv' % (reason),encoding='utf_8_sig')
    print 'Finish getting training DataFrame!'
    return dfx

def training(inputuple,reason):
    print 'Start training...'
    train = inputuple.drop(['date','code'],axis=1)    #读入数据
    train_xy,val = train_test_split(train, test_size = 0.2,random_state=1)  #用sklearn.cross_validation进行训练数据集划分，这里训练集和交叉验证集比例为7：3，可以自己根据需要设置
    
    y = train_xy.label
    X = train_xy.drop(['label'],axis=1)
    val_y = val.label
    val_X = val.drop(['label'],axis=1)

    xgb_val = xgb.DMatrix(val_X,label=val_y)   #xgb矩阵赋值
    xgb_train = xgb.DMatrix(X, label=y)

    params={
        'booster':'gbtree',
        'objective': 'binary:logistic',    #两分类的问题：logistic回归
        #'num_class':10,    # 类别数，与 multisoftmax 并用
        'gamma':0,     # 用于控制是否后剪枝的参数,越大越保守，一般0.1、0.2这样子。
        'max_depth':6,    # 构建树的深度，越大越容易过拟合
        #'lambda':2,     # 控制模型复杂度的权重值的L2正则化项参数，参数越大，模型越不容易过拟合。
        'subsample':1,   # 随机采样训练样本
        'colsample_bytree':1,   # 生成树时进行的列采样
        'min_child_weight':1, 
        # 这个参数默认是 1，是每个叶子里面 h 的和至少是多少，对正负样本不均衡时的 0-1 分类而言
        #，假设 h 在 0.01 附近，min_child_weight 为 1 意味着叶子节点中最少需要包含 100 个样本。
        #这个参数非常影响结果，控制叶子节点中二阶导的和的最小值，该参数值越小，越容易 overfitting。 
        'silent':0 ,  #设置成1则没有运行信息输出，最好是设置为0.
        'eta': 0.3,    # 学习率
        #'seed':1000,
        #'nthread':7,   # cpu 线程数
        'eval_metric': 'auc'   #评价标准：auc
        }
    plst = list(params.items())
    num_rounds = 15    # 迭代次数
    watchlist = [(xgb_train, 'train'),(xgb_val, 'val')]

    #训练模型并保存
    # early_stopping_rounds 当设置的迭代次数较大时，early_stopping_rounds 可在一定的迭代次数内准确率没有提升就停止训练
    model = xgb.train(plst, xgb_train, num_rounds, watchlist,early_stopping_rounds=100)
    '''
    predicted = model.predict(xgb.DMatrix(val_X)) 

    print "预测完毕!!!"  

    print '精度:{0:.3f}'.format(metrics.precision_score(xgb_val['label'], predicted,average='weighted'))  
    print '召回:{0:0.3f}'.format(metrics.recall_score(xgb_val['label'], predicted,average='weighted'))  
    print 'f1-score:{0:.3f}'.format(metrics.f1_score(xgb_val['label'], predicted,average='weighted')) '''

    if reason == 1:
        model.save_model('./model/xgbwsz.model')    # 用于存储训练出的模型
    elif reason == 2:
        model.save_model('./model/xgbgsz.model')
    print "best best_ntree_limit",model.best_ntree_limit

def train(reason):
    if reason == 1:
        training(get_training_data(1,2013,5,1,2015,6,30),reason)
    elif reason == 2:
        training(get_training_data(2,2014,12,1,2015,1,31),reason)

def predict(theday):
    #get_frame_theday(theday)
    print 'Finish update json...'
    if theday in get_tradelist_all():
        conn = default_db()
        cur = conn.cursor()
        reasonlist = [1]
        sql = "SELECT * FROM %s WHERE %s = '%d'" % (TABLE_STOCK_LIST,STOCK_LIST_LISTED,1)
        cur.execute(sql)
        results = cur.fetchall()
        stock_dict = {}
        for result in results:
            stock_dict[result[STOCK_LIST_STOCK_ID]] = [result[STOCK_LIST_STOCK_NAME],result[STOCK_LIST_INDUSTRY_NAME],result[STOCK_LIST_INDUSTRY_CODE]]
        
        #print tests
        df = pd.DataFrame()
        preds = []
        types = []
        datelist = []
        codelist = []
        for reason in reasonlist:
            inputuple = deal_data_theday(reason,theday)
            tests = inputuple.drop(['date','code'],axis=1)
            if reason == 1:
                model = xgb.Booster(model_file='./model/xgbwsz.model')
            elif reason == 2:
                model = xgb.Booster(model_file='./model/xgbgsz.model')
            xgb_test = xgb.DMatrix(tests)
            pred = model.predict(xgb_test)
            datelist.extend(list(inputuple['date']))
            codelist.extend(list(inputuple['code']))
            preds.extend(pred)#,ntree_limit=model.best_ntree_limit
            types.extend([reason]*len(pred))

        df['date'] = datelist
        df['code'] = codelist
        df['probability'] = preds
        df['type'] = types
        #inputuple.to_csv('2.csv')
        #df.to_csv('22.csv')
        print inputuple

        for code in sorted(list(set(df['code']))):
            stock_id = code
            stock_name = stock_dict[stock_id][0]
            industry_name = stock_dict[stock_id][1]
            industry_code = stock_dict[stock_id][2]
            codedf = df[df['code'] == code]
            if len(codedf) == 1:
                date = codedf.iloc[0]['date']
                probability = float(codedf.iloc[0]['probability'])
                if probability >= 0.5:
                    manipulate_type = codedf.iloc[0]['type']
                    result = 1
                else:
                    manipulate_type = 0
                    result = 0
            else:
                date = codedf.iloc[0]['date']
                probability = max(codedf['probability'])
                if probability >= 0.5:
                    manipulate_type = codedf[codedf['probability'] == probability].iloc[0]['type']
                    result = 1
                else:
                    manipulate_type = 0
                    result = 0
            
            order = 'insert into manipulate_result_test ( stock_id,date,stock_name,manipulate_type,industry_name,industry_code,probability,result)values("%s", "%s","%s","%d","%s","%s","%f","%d")' % (stock_id,date,stock_name,manipulate_type,industry_name,industry_code,probability,result)
            try:
                cur.execute(order)
                conn.commit()
            except Exception, e:
                print e
        #return result
        #result.to_csv('/home/lfz/python/yaoyan/modelcode/csv/result.csv',encoding='utf_8_sig')
        #print preds,type(preds)
        #np.savetxt('./csv/xgb_submission.csv',np.c_[range(1,len(tests)+1),preds],delimiter=',',header='ImageId,Label',comments='',fmt='%d')

if __name__=="__main__":
    #get_training_data(1,2013,5,1,2015,6,30)
    #predict('2016-01-04')
    #for day in get_datelist(2016,1,5,2016,12,31):
    #    predict(day)
    train(1)
    #training(get_training_data())
    '''
    frame = pd.DataFrame()
    f = open(r'/home/lfz/python/yaoyan/modelcode/wrong201412.txt','w')
    for day in get_tradelist(2015,7,1,2015,7,1):
        print day
        try:
            df = predict(deal_data_theday(day))
        except Exception, e:
            print e
            pass
    #frame.to_csv('/home/lfz/python/yaoyan/modelcode/csv/result20157-12.csv',encoding='utf_8_sig')
    f.close()'''


'''
伪市值案例时间区间：2013-05-09~2015-06-09
高送转案例时间区间：2014-12-24~2015-01-30
'''