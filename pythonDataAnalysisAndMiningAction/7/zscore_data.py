#coding=utf-8
'''
Created on 2017年8月4日

@author: cuiyufei

@description: 将数据标准化
'''
import pandas as pd
def zscore_data():
    datafile = '../data/7/zscoredata.xls'
    zscoredfile = '../data/tmp/zscoreddata.xls'
    
    data = pd.read_excel(datafile)
    #标准化处理
    data = (data - data.mean(axis = 0))/(data.std(axis=0))
    
    data.columns = ['Z'+i for i in data.columns]
    
    data.to_excel(zscoredfile, index=False)
    print u'数据标准化完成！'
if __name__ == '__main__':
    zscore_data()
