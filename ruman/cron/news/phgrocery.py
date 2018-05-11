  # -*- coding: utf-8 -*-


from tgrocery import Grocery
import os
import csv

def phgrocery(text):
    # result_text = []
    model_grocery = Grocery('model_redian')
    model_grocery.load()

    result = int(model_grocery.predict(text).predicted_y)
    # print result
    # if result == 1:
    #     result_text.append(text)
    return result
if __name__ == "__main__":
    text = '美国财长说漏一句话世界都惊了,美元对人民币狂跌'
    print phgrocery(text)



##    model_fintext = Grocery('model_fintext')
##    model_fintext.load()
##
##    filelist = []
##    files = os.listdir('/home/ubuntu8/jy/python/非法集资/results/')
##    fout = open('/home/ubuntu8/jy/python/非法集资/fiterfi.txt','w+')
##    for f in files:    
##        filelist.append(f)
##    for filename in filelist:
##        read = csv.reader(open('/home/ubuntu8/jy/python/实体感知文本数据20171206/data2_7/fiterfi.txt'filename))
##        for line in read:
##            content = line
##            result = int(model_fintext.predict(content).predicted_y)
##            print result
##            if result == 1:
##                fout.write(content)
##    fout.close()
    
    # model_grocery = Grocery('model_redian')
    # model_grocery.load()

    # fout = open('/home/jy/python/非法集资/data2_7/new_data_ph.txt','w+')
    # f= open('/home/jy/python/非法集资/third/wechat.txt','r+')
    # for line in f.readlines():
    #     content =''.join(line)
    #     print content
    #     result = int(model_grocery.predict(content).predicted_y)
    #     print result
    #     if result == 1:
    #         fout.write(content)
    # fout.close()



                
                                  
