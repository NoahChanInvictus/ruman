#-*-coding: utf-8-*-
import pandas as pd
from config import *
from time_utils import *
from sql_utils import *
from elasticsearch import Elasticsearch
from deal import *
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split

def get_training_data():
    print 'Ready to prepare training...'
    dfx = deal_data()
    dfy = pd.DataFrame([[0]]*len(dfx),columns=['y'])
    black_list = get_black_list()
    indexs = []
    for blackcode in black_list:   #对于在黑名单中的公司的时间进行匹配，在对应的位置标签改为1
        blackframe = dfx[dfx['code'] == blackcode['stock_id']]
        blackframe = blackframe[blackframe['date'] <= ts2datetime(blackcode['end_ts'])]
        index = blackframe[blackframe['date'] >= ts2datetime(blackcode['start_ts'])].index.tolist()
        indexs.extend(index)
    indexs = set(indexs)
    dfy.loc[indexs] = 1
    #print dfx,dfy
    #
    #dfy.to_csv(r'/home/lfz/python/dfy.csv',encoding='utf_8_sig')
    dfx['label'] = dfy['y']
    dfx.to_csv(r'/home/lfz/python/yaoyan/modelcode/csv/dfx20155.csv',encoding='utf_8_sig')
    print 'Finish getting training DataFrame!'
    return dfx

def training(inputuple):
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
    model.save_model('./model/xgb20155.model')    # 用于存储训练出的模型
    print "best best_ntree_limit",model.best_ntree_limit

def predict(inputuple):
    conn = default_db()
    cur = conn.cursor()
    sql = "SELECT * FROM stock_list"
    cur.execute(sql)
    results = cur.fetchall()
    stock_dict = {}
    for result in results:
        stock_dict[result['stock_id']] = [result['stock_name'],result['industry_name'],result['industry_code']]
    
    df = pd.DataFrame()
    df['date'] = inputuple['date']
    df['code'] = inputuple['code']
    tests = inputuple.drop(['date','code'],axis=1)
    #print tests
    model = xgb.Booster(model_file='./model/xgb.model')
    xgb_test = xgb.DMatrix(tests)
    preds = model.predict(xgb_test)#,ntree_limit=model.best_ntree_limit
    df['probability'] = preds

    for num in range(len(df)):
        print num
        stock_id = df.iloc[num]['code']
        date = df.iloc[num]['date']
        stock_name = stock_dict[stock_id][0]
        manipulate_type = 1
        industry_name = stock_dict[stock_id][1]
        industry_code = stock_dict[stock_id][2]
        probability = float(df.iloc[num]['probability'])
        if probability >= 0.5:
            result = 1
        else:
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
    #get_training_data()
    #training(get_training_data())
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
    f.close()
